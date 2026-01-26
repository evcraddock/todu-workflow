---
name: dev-environment
description: Set up local development environment with process management (overmind) and optional services (postgres, redis). Use when asked to "set up dev environment", "add docker services", "create Makefile", or similar.
---

# Dev Environment

Set up local development environment with process management and optional Docker services.

## When to Use

- After project scaffolding and quality tooling to add dev environment
- On existing projects to add Makefile, Procfile, or Docker services
- When asked to set up overmind, add postgres, add redis, etc.

## Required Inputs

- `name` - Project name (for DB name, etc.)
- `stack` - typescript, go, python, or rust
- `framework` - (optional) hono, express, gin, echo, fastapi, flask, axum
- `database` - none, postgres, or sqlite
- `services` - none, redis, or s3
- `localPath` - Where to write files

## Files to Generate

| File | When | Template |
|------|------|----------|
| Procfile.dev | Always | Based on services selected |
| Makefile | Always | `templates/Makefile` |
| compose.yaml | If postgres or redis | Compose from service snippets |
| .env.example | Always | Based on services selected |

## Process

1. **Determine run command**
   - Read from `templates/run-commands/{stack}-{framework}.txt`
   - If no framework, use `templates/run-commands/{stack}-none.txt`

2. **Generate Procfile.dev**
   - Base: `app: {run_command}`
   - If postgres: add `db: docker compose up postgres`
   - If redis: add `redis: docker compose up redis`

3. **Generate Makefile**
   - Use `templates/Makefile`
   - Replace `{check_command}` with stack-appropriate command:
     - typescript: `npm run lint && npm test`
     - go: `golangci-lint run && go test ./...`
     - python: `ruff check . && pytest`
     - rust: `cargo clippy && cargo test`

4. **Generate compose.yaml** (if services selected)
   ```yaml
   services:
   {postgres_service}
   {redis_service}

   volumes:
     postgres_data:
   ```
   - Include service snippets from `templates/compose/`
   - Only include volumes section if postgres selected

5. **Generate .env.example**
   - Select appropriate template based on services

6. **Check for overmind**
   ```bash
   which overmind
   ```
   If not installed, notify user:
   > overmind not found. Install with:
   > - Arch: `paru -S overmind`
   > - Mac: `brew install overmind`
   > - Other: https://github.com/DarthSim/overmind

## Run Commands

| Stack | Framework | Command |
|-------|-----------|---------|
| typescript | hono | `bun run --hot src/index.ts` |
| typescript | express | `npx tsx watch src/index.ts` |
| typescript | none | `npx tsx watch src/index.ts` |
| go | gin | `go run .` |
| go | echo | `go run .` |
| go | none | `go run .` |
| python | fastapi | `uvicorn app.main:app --reload` |
| python | flask | `flask run --reload` |
| python | none | `python -m {name}` |
| rust | axum | `cargo watch -x run` |
| rust | none | `cargo watch -x run` |

## Check Commands

| Stack | Command |
|-------|---------|
| typescript | `npm run lint && npm test` |
| go | `golangci-lint run && go test ./...` |
| python | `ruff check . && pytest` |
| rust | `cargo clippy && cargo test` |

## Verification

After generating files:

```bash
ls -la {localPath}/Procfile.dev
ls -la {localPath}/Makefile
ls -la {localPath}/compose.yaml  # if services
ls -la {localPath}/.env.example
```

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

- This skill is optional in project-init flow (Phase 6)
- compose.yaml only generated if postgres or redis selected
- sqlite doesn't need Docker - just creates local file
- s3 (object storage) support not yet implemented
- Detect existing Makefile/compose.yaml and offer to merge
