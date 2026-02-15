---
name: project-init
description: Initialize a new project end-to-end. Creates repo, scaffolds files, sets up quality tooling and dev environment. Use when asked to "create a new project", "init project", "start a new app", or similar.
---

# Project Init

Initialize a new project from scratch. This skill orchestrates the full setup flow.

## Prerequisites

Verify required CLI tools are available:

```bash
# Check for GitHub CLI (if using GitHub)
command -v gh &>/dev/null && echo "OK: gh" || echo "MISSING: gh (install from https://cli.github.com/)"

# Check for Forgejo CLI (if using Forgejo)
command -v fj &>/dev/null && echo "OK: fj" || echo "MISSING: fj (cargo install forgejo-cli)"

# Check for todu
command -v todu &>/dev/null && echo "OK: todu" || echo "MISSING: todu"
```

## Overview

0. **Detect Existing Project** - Check if re-running on existing project
1. **Gather Info** - Use questionnaire to collect project details (skip if existing)
2. **Determine Location** - Check/set env vars for project directory (skip if existing)
3. **Create Repo** - Create remote repo, clone locally, register with todu (skip if existing)
4. **Scaffold** - Generate README, LICENSE, .gitignore, AGENTS.md, docs/
5. **Quality Tooling** - Set up linting, formatting, testing
6. **Dev Environment** - Set up Procfile, Makefile, Docker services
7. **Commit & Push** - Initial commit with all generated files
8. **Create Task** - Create initial design task (skip if existing)

---

## Phase 0: Detect Existing Project

Apply the `project-check` skill to determine if we're re-running on an existing project.

**If "Not Registered"**: This is a new project → proceed to Phase 1a.

**If "Registered"**: This is an existing project. Set variables:

- `name` - from project-check result
- `host` - from project-check result (github or forgejo)
- `localPath` - current working directory

Detect stack from files:

```bash
if [ -f package.json ]; then detected_stack="typescript"
elif [ -f go.mod ]; then detected_stack="go"
elif [ -f pyproject.toml ]; then detected_stack="python"
elif [ -f Cargo.toml ]; then detected_stack="rust"
fi
```

Ask user to confirm or change:

```
Detected existing project: {name}
Stack detected: {detected_stack}

Use this stack or choose different?
Options: {detected_stack} (detected), typescript, go, python, rust
```

→ Store as `stack`

Then **skip to Phase 4** (Scaffold).

---

## Phase 1a: Gather Project Info (New Projects Only)

Ask the user these questions sequentially. Use your agent's native prompting capability (e.g., ask a question and wait for response before proceeding to the next).

### Question 1: Project Name
```
What is the project name?
```
→ Store as `name`

### Question 2: Host
```
Where will this project be hosted?
Options: forgejo, github
```
→ Store as `host`

### Question 3: Tech Stack
```
What tech stack will you use?
Options: typescript, go, python, rust
```
→ Store as `stack`

### Question 4: Framework
```
What framework? (optional)

For TypeScript: none, hono, express
For Go: none, gin, echo
For Python: none, fastapi, flask
For Rust: none, axum

(Use "none" for CLI tools or libraries)
```
→ Store as `framework`

### Question 5: Description
```
Brief project description:
```
→ Store as `description`

### Question 6: Database
```
Database needed?
Options: none, postgres, sqlite
```
→ Store as `database`

### Question 7: Additional Services
```
Additional services?
Options: none, redis, s3
```
→ Store as `services`

### Collected Variables

After gathering, you should have:
- `name` - project name
- `host` - forgejo or github
- `stack` - typescript, go, python, or rust
- `framework` - none, hono, express, gin, echo, fastapi, flask, or axum
- `description` - brief description
- `database` - none, postgres, or sqlite
- `services` - none, redis, or s3

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

1. **Ask for shell config preference**

   If `$PROJECT_INIT_SHELL_CONFIG` is not set, ask the user:
   
   ```
   Which shell config should I update to save your project directory preference?
   Options: ~/.zshrc, ~/.bashrc, ~/.profile, or specify another
   ```
   
2. **Ask for projects directory**

   ```
   Where do you keep your {host} projects?
   Common options: ~/Private/code/{host}, ~/Projects/{host}, ~/code/{host}
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
# Check if directory already exists
test -d {localPath} && echo "EXISTS" || echo "OK"
```

If exists, use the existing directory (this allows re-running project-init on existing projects).

---

## Phase 2-3: Create Repository

Apply the `repo-create` skill with:
- `name` - from Phase 1a
- `host` - from Phase 1a
- `description` - from Phase 1a
- `localPath` - from Phase 1b

### Error Handling

| Error | Action |
|-------|--------|
| CLI not installed | Show install instructions, abort |
| Not authenticated | Show auth instructions, abort |
| Repo already exists | Use existing repo (skip creation) |
| Directory exists | Use existing directory (skip clone) |

On success, proceed to Phase 4.

---

## Phase 4: Project Scaffold

Change to project directory:

```bash
cd {localPath}
```

Apply the `project-scaffold` skill with:
- `name` - from Phase 1a
- `description` - from Phase 1a
- `stack` - from Phase 1a
- `framework` - from Phase 1a
- `host` - from Phase 1a (for PR template location)
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
- `name` - from Phase 1a
- `stack` - from Phase 1a
- `localPath` - from Phase 2-3

This generates:
- Linter config (eslint, golangci-lint, ruff, clippy)
- Formatter config (prettier, rustfmt)
- Test config (vitest, pytest)
- tsconfig.json (TypeScript only)
- scripts/pre-pr.sh
- Example test file

---

## Phase 6: Dev Environment

Apply the `dev-environment` skill with:
- `name` - from Phase 1a
- `stack` - from Phase 1a
- `framework` - from Phase 1a
- `database` - from Phase 1a
- `services` - from Phase 1a
- `localPath` - from Phase 2-3

This generates:
- `.env.example`
- `Makefile`

It also creates a follow-up task "Set up dev environment" for project-specific configuration (Procfile.dev, compose.yaml, etc.).

Store the task URL as `dev_task_url` for use in the README and summary.

### Update README with Task Link

After the dev task is created, update the README to replace `{dev_task_url}` with the actual task URL:

```bash
sed -i "s|{dev_task_url}|$dev_task_url|g" README.md
```

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

## Phase 8: Create or Update Design Task

First, check if a design task already exists for this project:

```bash
todu task search --project {name} --label design --format json
```

**If a design task exists**: Update its description with current context:

```bash
todu task update {task_id} --description "..."
```

**If no design task exists**: Use the `task-create` skill to create a new task.

### Task Description

```
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

### New Task Properties

```
Title: Design {name} architecture
Project: {name}
Priority: high
Labels: design, architecture
```

### Error Handling

If task creation/update fails, show warning but continue (non-critical).

---

## Summary

After all phases complete, show summary:

```
✓ Project initialized successfully!

  Repository: {repoUrl}
  Local path: {localPath}
  Stack: {stack} + {framework}

  Tasks:
  - Design task: {design_task_url}
  - Dev environment setup: {dev_task_url}
```

### Next Steps

```
## How to Work on This Project

### 1. Install Dependencies

{install_command based on stack}

### 2. Start the Dev Environment

make dev

This starts all services defined in Procfile.dev. The command returns immediately (daemonized).

If make dev fails, configure the dev environment first. See: {dev_task_url}

### 3. View Logs

make dev-logs    # Stream all logs (Ctrl+C to stop)
make dev-tail    # Quick peek at recent logs

### 4. Run Tests and Linting

make check

### 5. Before Opening a PR

make pre-pr

### 6. Stop the Dev Environment

make dev-stop

### All Available Commands

make help
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
- All phases use skills and shell scripts - works with any coding agent
