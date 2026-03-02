#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
channel="tmux-smoke-${RANDOM}"
session_base="tmux-smoke"

out="$($script_dir/run-agent-command.sh \
  --session-base "$session_base" \
  --channel "$channel" \
  --command "echo '<<<TMUX_RESULT_START>>>'; echo 'smoke-ok'; echo '<<<TMUX_RESULT_END>>>'" \
  --hold-open \
  --wait \
  --wait-timeout 30 \
  --print-result \
  --cleanup)"

printf '%s\n' "$out"

get_kv() {
  local key="$1"
  printf '%s\n' "$out" | awk -F= -v k="$key" '$1==k {print substr($0, index($0,"=")+1)}' | tail -n1
}

session="$(get_kv SESSION)"
socket="$(get_kv SOCKET)"
wait_exit="$(get_kv WAIT_EXIT)"
result_found="$(get_kv RESULT_FOUND)"
cleanup_ok="$(get_kv CLEANUP_OK)"

if [[ -z "$session" || -z "$socket" ]]; then
  echo "SMOKE_OK=0" >&2
  echo "Missing SESSION or SOCKET output" >&2
  exit 1
fi

if [[ "$wait_exit" != "0" ]]; then
  echo "SMOKE_OK=0" >&2
  echo "WAIT_EXIT expected 0, got: ${wait_exit:-<empty>}" >&2
  exit 1
fi

if [[ "$result_found" != "1" ]]; then
  echo "SMOKE_OK=0" >&2
  echo "RESULT_FOUND expected 1, got: ${result_found:-<empty>}" >&2
  exit 1
fi

if [[ "$cleanup_ok" != "1" ]]; then
  echo "SMOKE_OK=0" >&2
  echo "CLEANUP_OK expected 1, got: ${cleanup_ok:-<empty>}" >&2
  exit 1
fi

if tmux -S "$socket" list-sessions 2>/dev/null | grep -q "^${session}:"; then
  echo "SMOKE_OK=0" >&2
  echo "Session still present after cleanup: $session" >&2
  exit 1
fi

echo "SMOKE_OK=1"
