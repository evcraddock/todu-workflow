#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: run-agent-command.sh -s session-base --channel name [options]

Start an isolated tmux session, run an agent command, and signal completion.

Required:
  -s, --session-base  session name base
      --channel       tmux wait-for channel to signal when command exits

Command source (choose exactly one):
  -p, --prompt        prompt text (runs: <agent-cmd> "<prompt>")
  -c, --command       raw command string to run

Options:
  -a, --agent-cmd     agent CLI command prefix (default: $CODING_AGENT_CMD or pi)
  -S, --socket-path   tmux socket path (default: $TMUX_SKILL_SOCKET_DIR/tmux-skill.sock)
  -n, --window-name   initial tmux window name (default: agent)
      --cwd           working directory for command (default: current directory)
      --hold-open     keep session alive after signaling until caller kills it
      --exit-on-complete
                      exit session immediately after signaling (default)
  -v, --visible       open observer view in current tmux
  -d, --detached      do not open observer view (default)
      --display-mode  observer mode when visible: window|pane (default: window)
      --split         pane split direction when display-mode=pane: h|v (default: h)

  --wait              block until channel is signaled
  --wait-timeout      timeout seconds for --wait (default: 600)
  --print-result      after wait, print marker-delimited result from pane
  --capture-lines     lines to capture when extracting result (default: 1200)
  --result-fallback-tail
                      lines of pane tail to print if markers are missing (default: 120)
  --result-grace-timeout
                      seconds to keep polling for markers after signal (default: 20)
  --cleanup           kill session after wait/result handling and report CLEANUP_OK

  --result-start      start marker for result extraction (default: <<<TMUX_RESULT_START>>>)
  --result-end        end marker for result extraction (default: <<<TMUX_RESULT_END>>>)

  -h, --help          show this help

Outputs machine-readable metadata on stdout:
  SESSION=<session>
  SOCKET=<socket-path>
  CHANNEL=<channel>
  WAIT_CMD=timeout 600 tmux -S '<socket-path>' wait-for '<channel>'
Human-oriented progress/result text is written to stderr.
USAGE
}

session_base=""
channel=""
prompt=""
command=""
agent_cmd="${CODING_AGENT_CMD:-pi}"
socket_path=""
window_name="agent"
working_dir="$(pwd)"
visible=false
display_mode="window"
split_direction="h"
hold_open=false

wait_for_signal=false
wait_timeout=600
print_result=false
capture_lines=1200
result_fallback_tail=120
result_grace_timeout=20
cleanup=false
result_start="<<<TMUX_RESULT_START>>>"
result_end="<<<TMUX_RESULT_END>>>"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--session-base) session_base="${2-}"; shift 2 ;;
    --channel)         channel="${2-}"; shift 2 ;;
    -p|--prompt)       prompt="${2-}"; shift 2 ;;
    -c|--command)      command="${2-}"; shift 2 ;;
    -a|--agent-cmd)    agent_cmd="${2-}"; shift 2 ;;
    -S|--socket-path)  socket_path="${2-}"; shift 2 ;;
    -n|--window-name)  window_name="${2-}"; shift 2 ;;
    --cwd)             working_dir="${2-}"; shift 2 ;;
    --hold-open)       hold_open=true; shift ;;
    --exit-on-complete) hold_open=false; shift ;;
    -v|--visible)      visible=true; shift ;;
    -d|--detached)     visible=false; shift ;;
    --display-mode)    display_mode="${2-}"; shift 2 ;;
    --split)           split_direction="${2-}"; shift 2 ;;
    --wait)            wait_for_signal=true; shift ;;
    --wait-timeout)    wait_timeout="${2-}"; shift 2 ;;
    --print-result)    print_result=true; shift ;;
    --capture-lines)   capture_lines="${2-}"; shift 2 ;;
    --result-fallback-tail) result_fallback_tail="${2-}"; shift 2 ;;
    --result-grace-timeout) result_grace_timeout="${2-}"; shift 2 ;;
    --cleanup)         cleanup=true; shift ;;
    --result-start)    result_start="${2-}"; shift 2 ;;
    --result-end)      result_end="${2-}"; shift 2 ;;
    -h|--help)         usage; exit 0 ;;
    *)                 echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$session_base" ]]; then
  echo "Error: --session-base is required" >&2
  usage
  exit 1
fi

if [[ -z "$channel" ]]; then
  echo "Error: --channel is required" >&2
  usage
  exit 1
fi

if [[ -n "$prompt" && -n "$command" ]]; then
  echo "Error: provide either --prompt or --command, not both" >&2
  exit 1
fi

if [[ -z "$prompt" && -z "$command" ]]; then
  echo "Error: one of --prompt or --command is required" >&2
  exit 1
fi

if [[ "$display_mode" != "window" && "$display_mode" != "pane" ]]; then
  echo "Error: --display-mode must be 'window' or 'pane'" >&2
  exit 1
fi

if [[ "$split_direction" != "h" && "$split_direction" != "v" ]]; then
  echo "Error: --split must be 'h' or 'v'" >&2
  exit 1
fi

if ! [[ "$wait_timeout" =~ ^[0-9]+$ ]]; then
  echo "Error: --wait-timeout must be an integer" >&2
  exit 1
fi

if ! [[ "$capture_lines" =~ ^[0-9]+$ ]]; then
  echo "Error: --capture-lines must be an integer" >&2
  exit 1
fi

if ! [[ "$result_fallback_tail" =~ ^[0-9]+$ ]]; then
  echo "Error: --result-fallback-tail must be an integer" >&2
  exit 1
fi

if ! [[ "$result_grace_timeout" =~ ^[0-9]+$ ]]; then
  echo "Error: --result-grace-timeout must be an integer" >&2
  exit 1
fi

if [[ "$print_result" == true && "$wait_for_signal" == false ]]; then
  echo "Error: --print-result requires --wait" >&2
  exit 1
fi

if [[ "$cleanup" == true && "$wait_for_signal" == false ]]; then
  echo "Error: --cleanup requires --wait" >&2
  exit 1
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "Error: tmux not found in PATH" >&2
  exit 1
fi

if [[ -z "$socket_path" ]]; then
  socket_dir="${TMUX_SKILL_SOCKET_DIR:-${TMPDIR:-/tmp}/tmux-skill-sockets}"
  mkdir -p "$socket_dir"
  socket_path="$socket_dir/tmux-skill.sock"
fi

if [[ -n "$command" ]]; then
  user_command="$command"
else
  result_instruction=$'\n\nWhen finished, you MUST print your final output between these exact marker lines:\n'
  result_instruction+="$result_start"
  result_instruction+=$'\n<final output>\n'
  result_instruction+="$result_end"
  result_instruction+=$'\n\nThen run this exact command via the bash tool to signal completion:\n'
  result_instruction+="tmux -S '$socket_path' wait-for -S '$channel'"
  full_prompt="$prompt$result_instruction"
  user_command="$agent_cmd $(printf '%q' "$full_prompt")"
fi

quoted_cwd=$(printf '%q' "$working_dir")
quoted_socket=$(printf '%q' "$socket_path")
quoted_channel=$(printf '%q' "$channel")

wrapped_command="set +e; cd $quoted_cwd; __tmux_skill_status=\$?; if [[ \$__tmux_skill_status -eq 0 ]]; then $user_command; __tmux_skill_status=\$?; fi; tmux -S $quoted_socket wait-for -S $quoted_channel; if [[ $hold_open == true ]]; then while true; do sleep 3600; done; fi; exit \$__tmux_skill_status"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
start_output="$($script_dir/start-session.sh -s "$session_base" -S "$socket_path" -n "$window_name" -c "$wrapped_command" -d)"

session="$(printf '%s\n' "$start_output" | sed -n "s/Created session '\([^']*\)' on socket .*/\1/p" | head -1)"
if [[ -z "$session" ]]; then
  echo "Error: could not parse created session name" >&2
  echo "$start_output" >&2
  exit 1
fi

if [[ "$visible" == true ]]; then
  if [[ -n "${TMUX:-}" ]]; then
    attach_cmd="tmux -S '$socket_path' attach -t '$session'"
    if [[ "$display_mode" == "pane" ]]; then
      tmux split-window "-$split_direction" "$attach_cmd"
      echo "Opened pane attached to '$session'" >&2
    else
      tmux new-window -n "$session" "$attach_cmd"
      echo "Opened window '$session'" >&2
    fi
  else
    echo "Warning: not inside tmux, cannot open visible observer" >&2
    echo "To attach: tmux -S '$socket_path' attach -t '$session'" >&2
  fi
fi

printf 'SESSION=%s\n' "$session"
printf 'SOCKET=%s\n' "$socket_path"
printf 'CHANNEL=%s\n' "$channel"
printf "WAIT_CMD=timeout %s tmux -S '%s' wait-for '%s'\n" "$wait_timeout" "$socket_path" "$channel"
printf 'RESULT_START=%s\n' "$result_start"
printf 'RESULT_END=%s\n' "$result_end"

wait_exit=0
if [[ "$wait_for_signal" == true ]]; then
  set +e
  timeout "$wait_timeout" tmux -S "$socket_path" wait-for "$channel"
  wait_exit=$?
  set -e
  printf 'WAIT_EXIT=%s\n' "$wait_exit"
fi

if [[ "$print_result" == true ]]; then
  attempts=$(( result_grace_timeout * 2 ))
  if (( attempts < 1 )); then
    attempts=1
  fi

  pane_text=""
  result_text=""
  for ((i=0; i<attempts; i++)); do
    pane_text="$(tmux -S "$socket_path" capture-pane -p -J -t "$session" -S "-$capture_lines" 2>/dev/null || true)"
    result_text="$(printf '%s\n' "$pane_text" | awk -v start="$result_start" -v end="$result_end" '
      $0 == start {in_block=1; next}
      $0 == end {in_block=0; next}
      in_block {print}
    ')"

    if [[ -n "$result_text" ]]; then
      break
    fi

    if (( i + 1 < attempts )); then
      sleep 0.5
    fi
  done

  if [[ -n "$result_text" ]]; then
    printf 'RESULT_FOUND=1\n'
    echo '--- RESULT START ---' >&2
    printf '%s\n' "$result_text" >&2
    echo '--- RESULT END ---' >&2
  else
    fallback_text="$(printf '%s\n' "$pane_text" | tail -n "$result_fallback_tail")"
    printf 'RESULT_FOUND=0\n'
    printf 'RESULT_GRACE_TIMEOUT=%s\n' "$result_grace_timeout"
    printf 'RESULT_FALLBACK_TAIL=%s\n' "$result_fallback_tail"
    echo '--- RESULT START ---' >&2
    echo '(No marker-delimited result found; showing pane tail fallback.)' >&2
    printf '%s\n' "$fallback_text" >&2
    echo '--- RESULT END ---' >&2
  fi
fi

cleanup_ok=1
if [[ "$cleanup" == true ]]; then
  kill_exit=0
  tmux -S "$socket_path" kill-session -t "$session" >/dev/null 2>&1 || kill_exit=$?

  list_output="$(tmux -S "$socket_path" list-sessions 2>&1 || true)"
  if printf '%s\n' "$list_output" | grep -q "^$session:"; then
    cleanup_ok=0
  fi

  printf 'KILL_EXIT=%s\n' "$kill_exit"
  printf 'CLEANUP_OK=%s\n' "$cleanup_ok"
fi

if [[ "$wait_for_signal" == true && "$wait_exit" -ne 0 ]]; then
  exit "$wait_exit"
fi

if [[ "$cleanup" == true && "$cleanup_ok" -ne 1 ]]; then
  exit 1
fi
