#!/usr/bin/env bash
# Stop a running Electron test instance.
#
# Usage: ./stop.sh [port]
#   port    CDP port to clean up (default: 9222)

PORT="${1:-9222}"

if [[ -f /tmp/electron-testing.pid ]]; then
  PID=$(cat /tmp/electron-testing.pid)
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Stopped Electron (PID $PID)"
  else
    echo "PID $PID not running"
  fi
  rm -f /tmp/electron-testing.pid
else
  # Fallback: kill by port
  PIDS=$(lsof -ti :"$PORT" 2>/dev/null || true)
  if [[ -n "$PIDS" ]]; then
    echo "$PIDS" | xargs kill 2>/dev/null
    echo "Stopped processes on port $PORT"
  else
    echo "No Electron test instance found"
  fi
fi
