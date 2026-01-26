---
name: project-init
description: Initialize a new project end-to-end. Creates repo, scaffolds files, sets up quality tooling and dev environment. Use when asked to "create a new project", "init project", "start a new app", or similar.
---

# Project Init

Initialize a new project from scratch. This skill orchestrates the full setup flow.

## Prerequisites

Before starting, verify required extensions are installed:

```bash
# Check for questionnaire extension
ls ~/.pi/agent/extensions/questionnaire.ts 2>/dev/null || echo "MISSING: questionnaire.ts"

# Check for repo-create extension (in todu-workflow)
ls ~/todu-workflow/extensions/repo-create.ts 2>/dev/null || echo "MISSING: repo-create.ts"
```

If missing, install from todu-workflow:
```bash
# Questionnaire (from pi examples)
PI_PATH=$(dirname $(which pi))/../lib/node_modules/@mariozechner/pi-coding-agent
cp $PI_PATH/examples/extensions/questionnaire.ts ~/.pi/agent/extensions/

# Repo-create should be available if todu-workflow is installed
```

**Do not proceed if extensions are missing.**

## Overview

1. **Gather Info** - Use questionnaire to collect project details
2. **Determine Location** - Check/set env vars for project directory
3. **Create Repo** - Create remote repo, clone locally, register with todu
4. **Scaffold** - Generate README, LICENSE, .gitignore, AGENTS.md, docs/
5. **Quality Tooling** - Set up linting, formatting, testing
6. **Dev Environment** - Set up Procfile, Makefile, Docker services (optional)
7. **Commit & Push** - Initial commit with all generated files
8. **Create Task** - Create initial design task

---

## Phase 1a: Gather Project Info

Call the `questionnaire` tool with these questions:

```json
{
  "questions": [
    {
      "id": "name",
      "label": "Name",
      "prompt": "What is the project name?",
      "options": [],
      "allowOther": true
    },
    {
      "id": "host",
      "label": "Host",
      "prompt": "Where will this project be hosted?",
      "options": [
        { "value": "forgejo", "label": "Forgejo" },
        { "value": "github", "label": "GitHub" }
      ]
    },
    {
      "id": "stack",
      "label": "Stack",
      "prompt": "What tech stack will you use?",
      "options": [
        { "value": "typescript", "label": "TypeScript" },
        { "value": "go", "label": "Go" },
        { "value": "python", "label": "Python" },
        { "value": "rust", "label": "Rust" }
      ],
      "allowOther": true
    },
    {
      "id": "framework",
      "label": "Framework",
      "prompt": "What framework? (optional)",
      "options": [
        { "value": "none", "label": "None / CLI tool" },
        { "value": "hono", "label": "Hono (TS)" },
        { "value": "express", "label": "Express (TS)" },
        { "value": "gin", "label": "Gin (Go)" },
        { "value": "echo", "label": "Echo (Go)" },
        { "value": "fastapi", "label": "FastAPI (Python)" },
        { "value": "flask", "label": "Flask (Python)" },
        { "value": "axum", "label": "Axum (Rust)" }
      ],
      "allowOther": true
    },
    {
      "id": "description",
      "label": "Description",
      "prompt": "Brief project description:",
      "options": [],
      "allowOther": true
    },
    {
      "id": "database",
      "label": "Database",
      "prompt": "Database needed?",
      "options": [
        { "value": "none", "label": "None" },
        { "value": "postgres", "label": "PostgreSQL" },
        { "value": "sqlite", "label": "SQLite" }
      ],
      "allowOther": true
    },
    {
      "id": "services",
      "label": "Services",
      "prompt": "Additional services?",
      "options": [
        { "value": "none", "label": "None" },
        { "value": "redis", "label": "Redis" },
        { "value": "s3", "label": "Object Storage (S3-compatible)" }
      ],
      "allowOther": true
    }
  ]
}
```

Store the answers for use in subsequent phases.

---

## Phase 1b: Determine Project Location

### Check Environment Variables

```bash
# Check for existing project directory config
echo $FORGEJO_PROJECTS_DIR
echo $GITHUB_PROJECTS_DIR
echo $PROJECT_INIT_SHELL_CONFIG
```

### If env var NOT set for selected host:

1. **Check shell config preference**

   If `$PROJECT_INIT_SHELL_CONFIG` is not set, ask using the `question` tool:
   
   ```
   Which shell config should I update?
   Options: ~/.zshrc, ~/.bashrc, ~/.profile, Other
   ```
   
2. **Ask for projects directory**

   Use `question` tool:
   ```
   Where do you keep your {host} projects?
   Options: ~/Private/code/{host}, ~/Projects/{host}, ~/code/{host}, Other
   ```

3. **Save to shell config**

   Append to the shell config file:
   ```bash
   # Project Init settings
   export PROJECT_INIT_SHELL_CONFIG="{shell_config_path}"
   export FORGEJO_PROJECTS_DIR="{projects_dir}"  # or GITHUB_PROJECTS_DIR
   ```
   
   Notify user: "Added {VAR_NAME} to {shell_config}"

### If env var IS set:

Use it as the default `baseDir`.

### Compute localPath

```
localPath = {baseDir}/{name}
```

### Validate

```bash
# Check directory doesn't already exist
test -d {localPath} && echo "EXISTS" || echo "OK"
```

If exists, ask user whether to abort or use existing directory.

---

## Phase 2-3: Create Repository

Call the `repo_create` tool:

```json
{
  "name": "{name}",
  "host": "{host}",
  "description": "{description}",
  "localPath": "{localPath}"
}
```

### Error Handling

| Error | Action |
|-------|--------|
| CLI not installed | Show install instructions, abort |
| Not authenticated | Show auth instructions, abort |
| Repo already exists | Ask: clone existing, or abort? |
| Directory exists | Ask: use existing, or abort? |

Store the returned `repoUrl` and `localPath` for later phases.

---

## Phase 4: Project Scaffold

Change to project directory:

```bash
cd {localPath}
```

Apply the `project-scaffold` skill with:
- `name` - from questionnaire
- `description` - from questionnaire
- `stack` - from questionnaire
- `framework` - from questionnaire
- `host` - from questionnaire (for PR template location)
- `localPath` - from Phase 2-3

This generates:
- LICENSE
- .gitignore
- README.md
- AGENTS.md
- docs/CONTRIBUTING.md
- docs/CODE_STANDARDS.md
- .github/ or .forgejo/ PR template

---

## Phase 5: Quality Tooling

Apply the `quality-tooling` skill with:
- `name` - from questionnaire
- `stack` - from questionnaire
- `localPath` - from Phase 2-3

This generates:
- Linter config (eslint, golangci-lint, ruff, clippy)
- Formatter config (prettier, rustfmt)
- Test config (vitest, pytest)
- tsconfig.json (TypeScript only)
- scripts/pre-pr.sh
- Example test file

---

## Phase 6: Dev Environment (Optional)

**Skip if**: database = "none" AND services = "none" AND user confirms skipping.

Ask user:
```
Set up dev environment (Procfile, Makefile, Docker services)?
Options: Yes, No (skip)
```

If yes, apply the `dev-environment` skill with:
- `name` - from questionnaire
- `stack` - from questionnaire
- `framework` - from questionnaire
- `database` - from questionnaire
- `services` - from questionnaire
- `localPath` - from Phase 2-3

This generates:
- Procfile.dev
- Makefile
- compose.yaml (if postgres or redis)
- .env.example

---

## Phase 7: Commit & Push

```bash
cd {localPath}

# Stage all files
git add -A

# Commit
git commit -m "Initial project setup

- Project scaffolding (README, LICENSE, AGENTS.md, docs/)
- Quality tooling (linting, formatting, testing)
- Dev environment (Procfile, Makefile, Docker)

Generated with project-init skill"

# Push
git push -u origin main
```

### Error Handling

If push fails:
- Show the error
- Ask: Retry, or skip (commit is local)?

---

## Phase 8: Create Design Task

Use the `task-create` skill to create an initial task:

```
Title: Design {name} architecture
Project: {name}
Priority: high
Labels: design, architecture

Description:
Create the initial architecture design for {name}.

## Context
- Stack: {stack}
- Framework: {framework}
- Database: {database}
- Description: {description}

## Deliverables
- [ ] Define core data models
- [ ] Design API endpoints / CLI commands
- [ ] Document key architectural decisions
- [ ] Create initial implementation tasks
```

### Error Handling

If task creation fails, show warning but continue (non-critical).

---

## Summary

After all phases complete, show summary:

```
✓ Project created successfully!

  Repository: {repoUrl}
  Local path: {localPath}
  Stack: {stack} + {framework}

  Files created:
  - README.md
  - LICENSE
  - .gitignore
  - AGENTS.md
  - docs/CONTRIBUTING.md
  - docs/CODE_STANDARDS.md
  - {.github or .forgejo}/pull_request_template.md
  - {quality tooling files based on stack}
  - {dev environment files if generated}

  Task created: #{task_id} - Design {name} architecture

  Next steps:
  1. cd {localPath}
  2. {install_command based on stack}
  3. make dev
```

### Install Commands by Stack

| Stack | Command |
|-------|---------|
| typescript | `bun install` or `npm install` |
| go | `go mod download` |
| python | `pip install -r requirements.txt` |
| rust | `cargo build` |

---

## Notes

- If any phase fails, stop and report the error
- User can re-run the skill after fixing issues
- The questionnaire extension must be installed for Phase 1a
- The repo_create extension must be installed for Phase 2-3
