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
| `dev` | Start dev environment (idempotent - checks if already running) |
| `dev-stop` | Stop dev environment |
| `dev-status` | Check if running (outputs "running" or "stopped") |
| `dev-logs` | Connect to overmind logs |
| `check` | Run linting and tests |
| `pre-pr` | Run pre-PR checks |

## Accessing Overmind Logs

When services are running via `make dev` (overmind), access logs using tmux commands.

### Find the overmind socket

```bash
OVERMIND_SOCKET=$(ls /tmp/overmind-*/overmind.sock 2>/dev/null | head -1)
```

### Capture logs from a service

Pane names match Procfile.dev entries (`app`, `db`, `redis`, etc.):

```bash
# Last 200 lines from app
tmux -S "$OVERMIND_SOCKET" capture-pane -p -t app -S -200

# Last 500 lines from db
tmux -S "$OVERMIND_SOCKET" capture-pane -p -t db -S -500
```

### Search logs

```bash
# Find errors
tmux -S "$OVERMIND_SOCKET" capture-pane -p -t app -S -500 | grep -i error

# Find a specific pattern (e.g., magic link)
tmux -S "$OVERMIND_SOCKET" capture-pane -p -t app -S -500 | grep -i "magic\|token\|link"

# Tail-like view (last 50 lines)
tmux -S "$OVERMIND_SOCKET" capture-pane -p -t app -S -50
```

### List available panes

```bash
tmux -S "$OVERMIND_SOCKET" list-panes -a
```

## Notes

- This skill creates scaffolding, not full configuration
- The created task allows user/agent to discuss actual needs
- Procfile.dev is NOT created - that's part of the setup task
- compose.yaml is NOT created - that's part of the setup task if needed
- `make dev` will fail until Procfile.dev exists (prompts setup)
