#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: start-session.sh -s session-name [options]

Create a tmux session on an isolated socket.

Options:
  -s, --session      session name (required)
  -S, --socket-path  tmux socket path (default: $TMUX_SKILL_SOCKET_DIR/tmux-skill.sock)
  -n, --window-name  initial window name (default: shell)
  -c, --command      command to run in the session
  -v, --visible      open a window in current tmux to show session
  -d, --detached     run detached, print attach command (default)
  -h, --help         show this help
USAGE
}

session=""
socket_path=""
window_name="shell"
command=""
visible=false
socket_dir="${TMUX_SKILL_SOCKET_DIR:-${TMPDIR:-/tmp}/tmux-skill-sockets}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--session)     session="${2-}"; shift 2 ;;
    -S|--socket-path) socket_path="${2-}"; shift 2 ;;
    -n|--window-name) window_name="${2-}"; shift 2 ;;
    -c|--command)     command="${2-}"; shift 2 ;;
    -v|--visible)     visible=true; shift ;;
    -d|--detached)    visible=false; shift ;;
    -h|--help)        usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$session" ]]; then
  echo "Error: session name is required (-s)" >&2
  usage
  exit 1
fi

# Validate session name (no spaces, reasonable chars)
if [[ ! "$session" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: session name must be alphanumeric with dashes/underscores only" >&2
  exit 1
fi

# Generate unique suffix
suffix=$(printf '%04x' $RANDOM)
session="${session}-${suffix}"

# Set default socket path
if [[ -z "$socket_path" ]]; then
  mkdir -p "$socket_dir"
  socket_path="$socket_dir/tmux-skill.sock"
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "Error: tmux not found in PATH" >&2
  exit 1
fi

# Check if session already exists
if tmux -S "$socket_path" has-session -t "$session" 2>/dev/null; then
  echo "Error: session '$session' already exists on socket '$socket_path'" >&2
  echo "To attach: tmux -S '$socket_path' attach -t $session" >&2
  echo "To kill:   tmux -S '$socket_path' kill-session -t $session" >&2
  exit 1
fi

# Create the session (always detached initially)
if [[ -n "$command" ]]; then
  tmux -S "$socket_path" new -d -s "$session" -n "$window_name" "$command"
else
  tmux -S "$socket_path" new -d -s "$session" -n "$window_name"
fi

echo "Created session '$session' on socket '$socket_path'"

# Handle visibility
if [[ "$visible" == true ]]; then
  if [[ -n "$TMUX" ]]; then
    tmux new-window -n "$session" "tmux -S '$socket_path' attach -t $session"
    echo "Opened window '$session' in current tmux"
  else
    echo "Warning: not inside tmux, cannot open visible window" >&2
    echo "To attach: tmux -S '$socket_path' attach -t $session"
  fi
else
  echo "To attach: tmux -S '$socket_path' attach -t $session"
fi
