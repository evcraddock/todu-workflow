---
name: task-close-gate
description: Verify a task is ready to close. Use when user says "close task", "complete task", "finish task", or "verify and close".
---

# Task Close Gate

Minimal closure gate for one task.

## Input

- task ID (required)

## Steps

1. Load task details via `task-show`.
2. Extract acceptance criteria from the task description.
3. Evaluate each acceptance criterion with explicit evidence.
   - status per criterion: `met` | `partial` | `missing`
   - do not assume evidence
4. Determine readiness.
   - all criteria `met` => `READY`
   - any `partial`/`missing` => `BLOCKED`
5. Prepare a closing summary comment.
6. If status is `READY`:
   - close task
   - add closing summary comment via `task-comment-create`
   If status is `BLOCKED`, stop and report issues.

## Rules

- Do not close a task with incomplete criteria.
- Keep checks focused on acceptance criteria and closure readiness.
- Do not run stack-specific verification commands here (tests/log scraping/CI checks).

## Output Template

```text
=== Task Close Gate: Task #<id> ===

Task: <title>
Acceptance Criteria:
- [ ] <criterion 1> — met|partial|missing — <evidence>
- [ ] <criterion 2> — met|partial|missing — <evidence>

Readiness: READY | BLOCKED

Proposed Closing Comment:
<comment>

Next Action: close-task | needs-work
```
