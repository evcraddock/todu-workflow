---
name: task-start-preflight
description: Read-only check of explicit task prerequisites, only when requested or required by task/project instructions.
---

# Task Start Preflight

Use the task details and context already supplied by the caller. Do not call `task_show`, repeat task lookups, or reassess the task's status or intent.

- Check only explicit prerequisites. Related work, examples, and suggestions are not dependencies.
- Use existing evidence of prerequisite completion. Known unfinished prerequisites block; cancelled prerequisites need a decision. Missing or uncertain evidence remains unresolved, not satisfied; report the gap without fetching it.
Do not query task lists or run unrelated checks.

Report **prerequisites satisfied**, **blocked**, **unresolved**, or **no explicit prerequisites**, with a brief reason and relevant dependency IDs/statuses. No fixed template or default approval prompt.

Never edit tasks, post comments, plan implementation, or create branches. Project planning/approval stays in the execution workflow.
