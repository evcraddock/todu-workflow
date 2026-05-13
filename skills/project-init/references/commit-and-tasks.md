# Commit and Tasks

Use this reference after scaffold, quality tooling, and dev environment setup.

## README Dev Task Link

If `dev_task_url` is available, replace `{dev_task_url}` in `README.md`:

```bash
sed -i "s|{dev_task_url}|$dev_task_url|g" README.md
```

Use the platform-appropriate `sed` form when needed.

## Initial Commit and Push

Ask before committing or pushing. These are persistent Git side effects.

From `{localPath}`:

```bash
git add -A
git commit -m "Initial project setup

- Project scaffolding (README, LICENSE, AGENTS.md, docs/)
- Quality tooling (linting, formatting, testing)
- Dev environment (Procfile, Makefile, Docker)

Generated with project-init skill"
git push -u origin main
```

If push fails, show the error and ask whether to retry or leave the commit local.

## Design Task Lookup

Check for an existing design task:

```bash
todu task list --project "{name}" --label design --format json
```

If a design task exists, update its description with the current project context.

If no design task exists, create a new design/backlog task. Prefer `task-authoring` when the draft needs improvement, but ensure the final task record keeps the required structure.

Task creation or update is non-critical for project initialization. If it fails, warn and continue.

## Design Task Draft

Use this title:

```text
Design {name} architecture and backlog
```

Use this description shape:

```md
Create the initial architecture/design for {name} and turn it into an actionable implementation backlog.

## Context

- Stack: {stack}
- Framework: {framework}
- Database: {database}
- Description: {description}

## Goal

Produce an architecture/design deliverable for {name} and create the initial implementation backlog in the task backend so future agents can execute the work without guessing.

## Requirements

- Document the proposed architecture/design for the current project context.
- Distinguish clearly between architecture/design content, execution instructions for this design task, and implementation work that must become follow-on tasks.
- Create follow-on implementation tasks in the task backend. Do not leave the backlog only in repo docs, markdown notes, or loose checklists.
- Each follow-on task must include title, `## Goal`, `## Requirements`, `## Acceptance criteria`, and `## Dependencies`.
- Use real task IDs in each follow-on task's `## Dependencies` section to express sequencing.
- If a follow-on task has no blockers, state that explicitly in `## Dependencies`.
- Do not use task status changes such as moving untouched tasks to `waiting` just to communicate order. Represent order through dependencies instead.
- Keep this task focused on architecture/design output plus backlog creation. Do not fold follow-on implementation work into this task.

## Acceptance criteria

- [ ] Architecture/design output exists and is specific enough to guide implementation.
- [ ] The initial implementation backlog exists as real backend task records.
- [ ] Every follow-on task includes title, `## Goal`, `## Requirements`, `## Acceptance criteria`, and `## Dependencies`.
- [ ] Sequencing and blockers are represented with real task IDs rather than status-only conventions.
- [ ] This task is considered done only after both the architecture/design deliverable and the initial implementation backlog are complete.
```

## Final Summary

After all phases complete, report:

```text
Project initialized successfully.

Repository: {repoUrl}
Local path: {localPath}
Stack: {stack} + {framework}

Tasks:
- Design task: {design_task_url}
- Dev environment setup: {dev_task_url}
```

Also include next steps:

```text
Install dependencies: {install_command}
Start dev environment: make dev
View logs: make dev-logs or make dev-tail
Run checks: make check
Before PR: make pre-pr
Stop dev environment: make dev-stop
All commands: make help
```

Install command by stack:

| Stack | Command |
| ----- | ------- |
| typescript | `bun install` or `npm install` |
| go | `go mod download` |
| python | `pip install -r requirements.txt` |
| rust | `cargo build` |
