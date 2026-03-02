# tmux Skill — Advanced Notes

Use this file for raw tmux operations and lower-level control patterns.

## Socket and targeting conventions

```bash
SOCKET="${TMUX_SKILL_SOCKET_DIR:-${TMPDIR:-/tmp}/tmux-skill-sockets}/tmux-skill.sock"
```

- Pane target format: `{session}:{window}.{pane}`
- Defaults if omitted: `:0.0`
- Inspect sessions/panes:
  - `tmux -S "$SOCKET" list-sessions`
  - `tmux -S "$SOCKET" list-panes -a`

## Creating windows and panes

### New window

```bash
tmux -S "$SOCKET" new-window -t tmux-dev -n debug
tmux -S "$SOCKET" new-window -t tmux-dev -n debug 'lldb ./myapp'
```

### Split pane

```bash
# Horizontal (left/right)
tmux -S "$SOCKET" split-window -h -t tmux-dev:0

# Vertical (top/bottom)
tmux -S "$SOCKET" split-window -v -t tmux-dev:0

# Split + command
tmux -S "$SOCKET" split-window -h -t tmux-dev:0 'tail -f app.log'
```

## Sending input safely

- Literal send:
  - `tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`
- Inline command:
  - `tmux ... send-keys -t target -- $'python3 -m http.server 8000'`
- Control keys:
  - `tmux ... send-keys -t target C-c`
  - `tmux ... send-keys -t target C-d`

## Output capture

```bash
tmux -S "$SOCKET" capture-pane -p -J -t target -S -200
```

`-J` joins wrapped lines to reduce display artifacts.

## Session discovery

```bash
./scripts/find-sessions.sh -S "$SOCKET"
./scripts/find-sessions.sh --all
./scripts/find-sessions.sh -S "$SOCKET" -q py
```

## Waiting patterns

### A) Wait for prompt text

```bash
./scripts/wait-for-text.sh -S "$SOCKET" -t "$SESSION":0.0 -p '^>>>' -T 15 -l 4000
```

### B) Wait-for channel signaling

```bash
CHANNEL="done-$SESSION"

tmux -S "$SOCKET" send-keys -t "$SESSION" "run-your-command; tmux -S $SOCKET wait-for -S $CHANNEL" Enter
timeout 600 tmux -S "$SOCKET" wait-for "$CHANNEL"
```

## Interactive tool notes

- Debugging default: `lldb`
- Python REPL: always set `PYTHON_BASIC_REPL=1`

Examples:

```bash
# Python REPL
tmux -S "$SOCKET" send-keys -t "$SESSION" -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter

# lldb
tmux -S "$SOCKET" send-keys -t "$SESSION" -- 'lldb ./a.out' Enter

# gdb
tmux -S "$SOCKET" send-keys -t "$SESSION" -- 'gdb --quiet ./a.out' Enter
tmux -S "$SOCKET" send-keys -t "$SESSION" -- 'set pagination off' Enter
```

## Cleanup

```bash
# one session
tmux -S "$SOCKET" kill-session -t "$SESSION"

# all sessions on socket
tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t

# entire server on socket
tmux -S "$SOCKET" kill-server
```
