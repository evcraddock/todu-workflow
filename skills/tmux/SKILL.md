---
name: tmux
description: Orchestrate isolated tmux sessions for interactive agent work and command execution. Use when user asks to run something in tmux or says "use a sub-agent".
---

# tmux Skill

Use this skill when you want to run work in a separate tmux session (optionally in a visible pane/window), wait for completion, capture final output, and clean up reliably.

## Defaults

```bash
SOCKET="${TMUX_SKILL_SOCKET_DIR:-${TMPDIR:-/tmp}/tmux-skill-sockets}/tmux-skill.sock"
```

All helper scripts default to this private socket path so automation sessions stay separate from personal tmux sessions.

## Sub-agent shorthand (default behavior)

When the user says **"use a sub-agent to <task>"**, treat it as this detached orchestration profile:

```bash
./scripts/run-agent-command.sh \
  --session-base subagent \
  --channel subagent-done-<id> \
  --prompt "<task>" \
  --detached \
  --hold-open \
  --wait \
  --wait-timeout 1200 \
  --print-result \
  --cleanup
```

This is the default sub-agent mode unless the user explicitly asks for visible pane/window behavior.

## Canonical workflows

### 1) Run prompt in a pane, wait, print result, cleanup

```bash
./scripts/run-agent-command.sh \
  --session-base preflight-2033 \
  --channel preflight-done-2033 \
  --prompt "start preflight for task 2033" \
  --socket-path "$SOCKET" \
  --visible \
  --display-mode pane \
  --split v \
  --hold-open \
  --wait \
  --wait-timeout 900 \
  --print-result \
  --cleanup
```

### 2) Run detached prompt, wait, print result, cleanup

```bash
./scripts/run-agent-command.sh \
  --session-base subagent \
  --channel subagent-done-001 \
  --prompt "research popular llm agent harnesses" \
  --detached \
  --hold-open \
  --wait \
  --wait-timeout 1200 \
  --print-result \
  --cleanup
```

### 3) Start session only (manual tmux control)

```bash
./scripts/start-session.sh -s debug-shell --visible
```

Use this only when you explicitly want manual tmux control.

## Script responsibilities

- `scripts/run-agent-command.sh`
  - high-level orchestrator (start session, optional visible pane/window, wait, result extraction, cleanup)
  - recommended default for automation
- `scripts/start-session.sh`
  - create a named session on isolated socket
- `scripts/wait-for-text.sh`
  - poll pane text for regex/fixed-string prompt synchronization
- `scripts/find-sessions.sh`
  - list sessions on a specific/all sockets
- `scripts/smoke.sh`
  - quick integration check for wait/result/cleanup behavior

## `run-agent-command.sh` output contract

`run-agent-command.sh` writes machine-readable `KEY=VALUE` fields to stdout.
Human progress and extracted result blocks are written to stderr.

Common fields:
- `SESSION`
- `SOCKET`
- `CHANNEL`
- `WAIT_CMD`
- `WAIT_EXIT` (when `--wait` used)
- `RESULT_FOUND` (when `--print-result` used)
- `CLEANUP_OK` (when `--cleanup` used)

## Result markers

In `--prompt` mode, the script injects instructions for the spawned agent to print final output between:

- `<<<TMUX_RESULT_START>>>`
- `<<<TMUX_RESULT_END>>>`

If markers are missing, `--print-result` falls back to printing pane tail (`--result-fallback-tail`).

## Validation

Run smoke test after changing tmux scripts:

```bash
./scripts/smoke.sh
```

## Advanced tmux usage

For raw tmux techniques, pane targeting details, REPL recipes, and manual command patterns, see:

- `./ADVANCED.md`
