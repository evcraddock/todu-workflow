---
name: task-pipeline
description: Use when user says "pickup task <task-id|task-name>", "get started on task <task-id|task-name>", or "work on task <task-id|task-name>".
---

# task-pipeline

Single gated flow for picking up and finishing one coding task.

## Steps

1. Check task readiness with `task-start-preflight`.
   - `READY` → continue
   - `BLOCKED` → stop

2. Load contributing instructions and follow them.
   - Use `docs/CONTRIBUTING.md` if it exists.
   - Otherwise use `DEFAULT_CONTRIBUTING.md` in this skill directory.
   - If neither can be loaded, return `BLOCKED`.

3. Follow the instructions in the task description.
   - Implement exactly what the task asks for.
   - If instructions are ambiguous/conflicting, return `BLOCKED`.

4. Ensure the task is closed correctly.
   - Run `task-close-preflight` for the task.
   - Complete closure only if close preflight passes.

## Rules

- Do not move to the next step until the current step is `READY`.
- All task comments must be created with the `task-comment-create` skill.
- Do not add manual line breaks in markdown paragraphs.
