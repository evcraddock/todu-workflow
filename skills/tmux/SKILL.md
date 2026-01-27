---
name: tmux
description: Remote control tmux sessions for interactive CLIs (python, gdb, etc.) by sending keystrokes and scraping pane output.
---

# tmux Skill

> Based on the [tmux skill](https://github.com/mitsuhiko/agent-stuff/tree/main/skills/tmux) from [mitsuhiko/agent-stuff](https://github.com/mitsuhiko/agent-stuff).

Use tmux as a programmable terminal multiplexer for interactive work. Works on Linux and macOS with stock tmux; avoid custom config by using a private socket.

## Quickstart

```bash
# Start a session (detached by default)
./scripts/start-session.sh -s claude-python
# Output: Created session 'claude-python-4b5a' on socket '/tmp/claude-tmux-sockets/claude.sock'

# Or start visible (opens window in current tmux)
./scripts/start-session.sh -s claude-python --visible

# Start with a command
./scripts/start-session.sh -s claude-python -c 'PYTHON_BASIC_REPL=1 python3 -q' --visible
```

The script outputs the actual session name (with unique suffix) and socket path. Use these for subsequent commands:

```bash
SOCKET="/tmp/claude-tmux-sockets/claude.sock"
SESSION="claude-python-4b5a"  # from script output
tmux -S "$SOCKET" send-keys -t "$SESSION" 'print("hello")' Enter
tmux -S "$SOCKET" capture-pane -p -t "$SESSION" -S -50
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## Socket convention

Sessions use an isolated socket at `$CLAUDE_TMUX_SOCKET_DIR/claude.sock` (defaults to `${TMPDIR:-/tmp}/claude-tmux-sockets/claude.sock`). This keeps agent sessions separate from your personal tmux.

The `start-session.sh` script handles socket setup automatically. For manual commands, always use `-S "$SOCKET"`.

## Targeting panes and naming

- Target format: `{session}:{window}.{pane}`, defaults to `:0.0` if omitted. Keep names short (e.g., `claude-py`, `claude-gdb`).
- Use `-S "$SOCKET"` consistently to stay on the private socket path. If you need user config, drop `-f /dev/null`; otherwise `-f /dev/null` gives a clean config.
- Inspect: `tmux -S "$SOCKET" list-sessions`, `tmux -S "$SOCKET" list-panes -a`.

## Creating windows and panes

### New window in existing session

```bash
# Create a new window named "debug" in session claude-dev
tmux -S "$SOCKET" new-window -t claude-dev -n debug

# Create and run a command in it
tmux -S "$SOCKET" new-window -t claude-dev -n debug 'lldb ./myapp'
```

### New pane (split existing window)

```bash
# Horizontal split (side by side)
tmux -S "$SOCKET" split-window -h -t claude-dev:0

# Vertical split (stacked)
tmux -S "$SOCKET" split-window -v -t claude-dev:0

# Split and run a command
tmux -S "$SOCKET" split-window -h -t claude-dev:0 'tail -f app.log'
```

### Targeting after creation

After creating a new window or pane, update your target:
- New window: `claude-dev:1.0` (window index increments)
- New pane: `claude-dev:0.1` (pane index increments)

List panes to confirm: `tmux -S "$SOCKET" list-panes -t claude-dev -a`

## Finding sessions

- List sessions on your active socket with metadata: `./scripts/find-sessions.sh -S "$SOCKET"`; add `-q partial-name` to filter.
- Scan all sockets under the shared directory: `./scripts/find-sessions.sh --all` (uses `CLAUDE_TMUX_SOCKET_DIR` or `${TMPDIR:-/tmp}/claude-tmux-sockets`).

## Sending input safely

- Prefer literal sends to avoid shell splitting: `tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`
- When composing inline commands, use single quotes or ANSI C quoting to avoid expansion: `tmux ... send-keys -t target -- $'python3 -m http.server 8000'`.
- To send control keys: `tmux ... send-keys -t target C-c`, `C-d`, `C-z`, `Escape`, etc.

## Watching output

- Capture recent history (joined lines to avoid wrapping artifacts): `tmux -S "$SOCKET" capture-pane -p -J -t target -S -200`.
- For continuous monitoring, poll with the helper script (below) instead of `tmux wait-for` (which does not watch pane output).
- You can also temporarily attach to observe: `tmux -S "$SOCKET" attach -t "$SESSION"`; detach with `Ctrl+b d`.
- When giving instructions to a user, **explicitly print a copy/paste monitor command** alongside the action—don't assume they remembered the command.

## Spawning Processes

Some special rules for processes:

- When asked to debug, use lldb by default
- When starting a python interactive shell, always set the `PYTHON_BASIC_REPL=1` environment variable. This is very important as the non-basic console interferes with your send-keys.

## Synchronizing / waiting for prompts

- Use timed polling to avoid races with interactive tools. Example: wait for a Python prompt before sending code:
  ```bash
  ./scripts/wait-for-text.sh -S "$SOCKET" -t "$SESSION":0.0 -p '^>>>' -T 15 -l 4000
  ```
- For long-running commands, poll for completion text (`"Type quit to exit"`, `"Program exited"`, etc.) before proceeding.

## Interactive tool recipes

- **Python REPL**: `tmux ... send-keys -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter`; wait for `^>>>`; send code with `-l`; interrupt with `C-c`.
- **lldb**: `tmux ... send-keys -- 'lldb ./a.out' Enter`; wait for `(lldb)`; issue commands; exit via `quit` then confirm `y`.
- **gdb**: `tmux ... send-keys -- 'gdb --quiet ./a.out' Enter`; disable paging `tmux ... send-keys -- 'set pagination off' Enter`; break with `C-c`; issue `bt`, `info locals`, etc.; exit via `quit` then confirm `y`.
- **Other TTY apps** (ipdb, psql, mysql, node, bash): same pattern—start the program, poll for its prompt, then send literal text and Enter.

## Run and capture

For one-shot commands where you need to know when they complete, use `tmux wait-for` channel signaling:

```bash
SOCKET="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}/claude.sock"

# 1. Start session with command that signals when done
OUTPUT=$(./scripts/start-session.sh -s my-task --visible)
SESSION=$(echo "$OUTPUT" | grep "Created session" | sed "s/Created session '\([^']*\)'.*/\1/")
CHANNEL="done-$SESSION"

# 2. Send command with completion signal
tmux -S "$SOCKET" send-keys -t "$SESSION" "pi \"do something\"; tmux -S $SOCKET wait-for -S $CHANNEL" Enter

# 3. Wait for signal (blocks until command completes)
# Use timeout to avoid hanging forever if session crashes
timeout 600 tmux -S "$SOCKET" wait-for "$CHANNEL"

# 4. Capture output (if needed)
OUTPUT=$(tmux -S "$SOCKET" capture-pane -p -t "$SESSION" -S -500)
echo "$OUTPUT"

# 5. Kill session
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

### How wait-for signaling works

1. The command ends with `; tmux -S $SOCKET wait-for -S $CHANNEL`
2. When the main command exits, it signals the channel with `-S` (signal)
3. The calling process blocks on `wait-for $CHANNEL` (no flag = wait)
4. When signaled, the caller unblocks and continues

**Benefits over pattern matching:**
- No polling or regex matching on terminal output
- Clean synchronization primitive built into tmux
- No race conditions with partial output

**Timeout:** Always wrap `wait-for` with `timeout` to avoid hanging if the session crashes:
```bash
timeout 600 tmux -S "$SOCKET" wait-for "$CHANNEL" || echo "Timed out or session died"
```

## Cleanup

- Kill a session when done: `tmux -S "$SOCKET" kill-session -t "$SESSION"`.
- Kill all sessions on a socket: `tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t`.
- Remove everything on the private socket: `tmux -S "$SOCKET" kill-server`.

## Helper: start-session.sh

`./scripts/start-session.sh` creates a tmux session on an isolated socket.

```bash
./scripts/start-session.sh -s session-name [options]
```

- `-s`/`--session` session name base (required, alphanumeric with dashes/underscores)
- `-S`/`--socket-path` tmux socket path (default: `$CLAUDE_TMUX_SOCKET_DIR/claude.sock`)
- `-n`/`--window-name` initial window name (default: shell)
- `-c`/`--command` command to run in the session
- `-v`/`--visible` open a window in current tmux to show session
- `-d`/`--detached` run detached, print attach command (default)

Session names are auto-suffixed with a random ID (e.g., `claude-python` becomes `claude-python-4b5a`) to avoid collisions. The actual session name is printed in the output.

If `--visible` and inside tmux, opens a new window attached to the session. Window closes automatically when session is killed.

## Helper: wait-for-text.sh

`./scripts/wait-for-text.sh` polls a pane for a regex (or fixed string) with a timeout. Works on Linux/macOS with bash + tmux + grep.

```bash
./scripts/wait-for-text.sh -S "$SOCKET" -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-S`/`--socket-path` tmux socket path (optional, uses default socket if omitted)
- `-t`/`--target` pane target (required)
- `-p`/`--pattern` regex to match (required); add `-F` for fixed string
- `-T` timeout seconds (integer, default 15)
- `-i` poll interval seconds (default 0.5)
- `-l` history lines to search from the pane (integer, default 1000)
- Exits 0 on first match, 1 on timeout. On failure prints the last captured text to stderr to aid debugging.

## Helper: find-sessions.sh

`./scripts/find-sessions.sh` lists tmux sessions on a socket.

```bash
./scripts/find-sessions.sh -S "$SOCKET"           # list sessions on specific socket
./scripts/find-sessions.sh --all                  # scan all sockets in CLAUDE_TMUX_SOCKET_DIR
./scripts/find-sessions.sh -S "$SOCKET" -q py     # filter by name
```
