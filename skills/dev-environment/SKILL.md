---
name: dev-environment
description: Set up local development environment with process management (overmind). Use when asked to "set up dev environment", "create Makefile", or as part of project-init.
---

# Dev Environment

Set up local development environment scaffolding and create a task for detailed configuration.

## When to Use

- During project-init (Phase 6)
- When asked to set up dev environment on existing project
- When asked to add Makefile or overmind support

## Required Inputs

- `name` - Project name
- `stack` - typescript, go, python, or rust
- `framework` - (optional) hono, express, gin, echo, fastapi, flask, axum
- `database` - none, postgres, or sqlite
- `services` - none, redis, or s3
- `localPath` - Where to write files

## Files to Generate

| File | Template |
|------|----------|
| `.env.example` | `templates/env.example` |
| `Makefile` | `templates/Makefile` |

## Process

### 1. Generate .env.example

Copy from `templates/env.example`. This provides a minimal starting point.

### 2. Generate Makefile

Copy from `templates/Makefile`, replacing `{check_command}` with stack-appropriate command:

| Stack | Check Command |
|-------|---------------|
| typescript | `npm run lint && npm test` |
| go | `golangci-lint run && go test ./...` |
| python | `ruff check . && pytest` |
| rust | `cargo clippy && cargo test` |

### 3. Check for overmind

```bash
which overmind
```

If not installed, notify user:
> overmind not found. Install with:
> - Arch: `paru -S overmind`
> - Mac: `brew install overmind`
> - Other: https://github.com/DarthSim/overmind

### 4. Create Dev Environment Setup Task

Create a task in the project for configuring the dev environment:

```
Title: Set up dev environment
Project: {name}
Priority: medium
Labels: setup, dev-environment

Description:
Configure the local development environment for {name}.

## Context (from project-init)
- Stack: {stack}
- Framework: {framework}
- Database: {database}
- Services: {services}

## To Configure
- [ ] Create Procfile.dev with appropriate services
- [ ] Create compose.yaml if database/services need Docker
- [ ] Update .env.example with required variables
- [ ] Verify `make dev` starts everything correctly
- [ ] Document any manual setup steps in README

## Makefile Targets Available
- `make help` - Show available commands
- `make dev` - Start dev environment (needs Procfile.dev)
- `make dev-stop` - Stop dev environment
- `make dev-status` - Check if running
- `make dev-logs` - View logs
- `make check` - Run linting and tests
- `make pre-pr` - Run pre-PR checks
```

## Makefile Targets

The generated Makefile includes:

| Target | Description |
|--------|-------------|
| `help` | Show available commands (auto-generated from comments) |
| `dev` | Start dev environment (daemonized, returns immediately) |
| `dev-stop` | Stop dev environment (cleans up socket and stale tmux sessions) |
| `dev-status` | Check if running (outputs "running" or "stopped") |
| `dev-logs` | Stream all logs (foreground, Ctrl+C to stop) |
| `dev-tail` | Show last 100 lines of logs (non-blocking) |
| `check` | Run linting and tests |
| `pre-pr` | Run pre-PR checks |

### Key Design Decisions

1. **Daemonized startup**: `overmind start -D` so `make dev` returns immediately
2. **Reliable status**: Uses `overmind ps -s $(SOCKET)` instead of unreliable `pgrep`
3. **Socket management**: Explicit `SOCKET` variable, cleaned up on stop
4. **Stale session cleanup**: `dev-stop` kills orphaned tmux sessions
5. **Non-blocking logs**: `dev-tail` uses tmux capture-pane for quick inspection
6. **Streaming logs**: `dev-logs` uses `overmind echo` for continuous output

### Connect to Specific Service

To connect to a specific service's terminal (for debugging, REPL access, etc.):

```bash
overmind connect -s ./.overmind.sock <service-name>
```

Where `<service-name>` matches the entry in Procfile.dev. Detach with `Ctrl+b d`.

You can add convenience targets to the Makefile:

```makefile
connect-app: ## Connect to app terminal
	overmind connect -s $(SOCKET) app

connect-db: ## Connect to db terminal
	overmind connect -s $(SOCKET) db
```

## Accessing Overmind Logs Programmatically

When services are running via `make dev` (overmind), access logs using tmux commands. The socket is at `./.overmind.sock` in the project directory.

### Quick Access

```bash
# Use make targets
make dev-tail    # Last 100 lines, non-blocking
make dev-logs    # Stream all logs (Ctrl+C to stop)
```

### Direct tmux Access

```bash
SOCKET="./.overmind.sock"

# Capture logs from a specific service (pane names match Procfile.dev entries)
tmux -S "$SOCKET" capture-pane -p -t app -S -200    # Last 200 lines from app
tmux -S "$SOCKET" capture-pane -p -t db -S -500     # Last 500 lines from db

# Search logs
tmux -S "$SOCKET" capture-pane -p -t app -S -500 | grep -i error
tmux -S "$SOCKET" capture-pane -p -t app -S -500 | grep -i "magic\|token\|link"

# List available panes
tmux -S "$SOCKET" list-panes -a
```

### For Agent Log Access

When an agent needs to check logs programmatically:

```bash
# Check if dev environment is running
if [ "$(make -s dev-status)" = "running" ]; then
  # Capture recent logs
  make dev-tail | grep -i error
fi
```

## Notes

- This skill creates scaffolding, not full configuration
- The created task allows user/agent to discuss actual needs
- Procfile.dev is NOT created - that's part of the setup task
- compose.yaml is NOT created - that's part of the setup task if needed
- `make dev` will fail until Procfile.dev exists (prompts setup)
