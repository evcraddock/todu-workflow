#!/usr/bin/env bash
# Launch an Electron app with CDP (Chrome DevTools Protocol) debugging enabled.
#
# Usage: ./launch.sh [options]
#   --app-path <path>     Path to the Electron app's main JS entry (required)
#   --electron <path>     Path to electron binary (default: auto-detect from node_modules)
#   --port <port>         CDP debugging port (default: 9222)
#   --build-cmd <cmd>     Build command to run before launch (optional)
#   --env KEY=VALUE       Set environment variable for Electron process (repeatable)
#   --no-sandbox          Pass --no-sandbox to Chromium (disabled by default)
#   --help                Show this help
#
# Environment variables are passed through to the Electron process. Use --env to set
# additional ones (e.g., --env TODU_DATA_DIR=/tmp/test-data for isolated test runs).
#
# Examples:
#   ./launch.sh --app-path ./packages/electron/dist/main/index.js
#   ./launch.sh --app-path ./dist/main.js --env TODU_DATA_DIR=/tmp/test-data
#   ./launch.sh --app-path ./dist/main.js --port 9333 --build-cmd "npm run build"
#   ./launch.sh --app-path ./dist/main.js --electron ./node_modules/electron/dist/electron

set -euo pipefail

APP_PATH=""
ELECTRON_BIN=""
PORT=9222
BUILD_CMD=""
NO_SANDBOX=""
EXTRA_ENV=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --app-path)   APP_PATH="$2"; shift 2 ;;
    --electron)   ELECTRON_BIN="$2"; shift 2 ;;
    --port)       PORT="$2"; shift 2 ;;
    --build-cmd)  BUILD_CMD="$2"; shift 2 ;;
    --env)        EXTRA_ENV+=("$2"); shift 2 ;;
    --no-sandbox) NO_SANDBOX="--no-sandbox"; shift ;;
    --help)
      sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$APP_PATH" ]]; then
  echo "Error: --app-path is required" >&2
  exit 1
fi

# Auto-detect electron binary
if [[ -z "$ELECTRON_BIN" ]]; then
  # Walk up from app-path looking for node_modules/electron
  SEARCH_DIR="$(cd "$(dirname "$APP_PATH")" && pwd)"
  while [[ "$SEARCH_DIR" != "/" ]]; do
    CANDIDATE="$SEARCH_DIR/node_modules/electron/dist/electron"
    if [[ -x "$CANDIDATE" ]]; then
      ELECTRON_BIN="$CANDIDATE"
      break
    fi
    SEARCH_DIR="$(dirname "$SEARCH_DIR")"
  done

  if [[ -z "$ELECTRON_BIN" ]]; then
    echo "Error: Could not find electron binary. Use --electron to specify." >&2
    exit 1
  fi
fi

# Run build command if provided
if [[ -n "$BUILD_CMD" ]]; then
  echo "Building: $BUILD_CMD"
  eval "$BUILD_CMD"
fi

# Kill any existing electron on this port
if lsof -ti :"$PORT" >/dev/null 2>&1; then
  echo "Warning: Port $PORT in use, killing existing process"
  lsof -ti :"$PORT" | xargs kill 2>/dev/null || true
  sleep 1
fi

# Export extra environment variables
for env_pair in "${EXTRA_ENV[@]}"; do
  export "$env_pair"
  echo "  Env: $env_pair"
done

# Launch electron with CDP
echo "Launching Electron with CDP on port $PORT"
echo "  Binary: $ELECTRON_BIN"
echo "  App: $APP_PATH"
"$ELECTRON_BIN" $NO_SANDBOX --remote-debugging-port="$PORT" "$APP_PATH" >/tmp/electron-testing-stdout.log 2>/tmp/electron-testing-stderr.log &
PID=$!
echo "  PID: $PID"

# Wait for CDP to be ready
echo -n "Waiting for CDP endpoint..."
for i in $(seq 1 30); do
  if curl -s "http://127.0.0.1:$PORT/json/version" >/dev/null 2>&1; then
    echo " ready!"
    curl -s "http://127.0.0.1:$PORT/json/version" | grep -oP '"Browser":\s*"\K[^"]*'
    echo "CDP endpoint: http://127.0.0.1:$PORT"
    echo "$PID" > /tmp/electron-testing.pid
    exit 0
  fi
  sleep 1
  echo -n "."
done

echo " timeout!"
echo "Electron may have crashed. Check /tmp/electron-testing-stderr.log"
kill "$PID" 2>/dev/null
exit 1
