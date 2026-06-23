---
name: task-close-gate
description: Verify a Todu task is ready to close against acceptance criteria. Use for "close task", "complete task", or "verify and close". Do not use to start work.
---

# Task Close Gate

Minimal closure gate for one task.

## Input

- task ID (required)

## Bounded Execution Contract

Complete the close gate with this short checklist only:

1. Load task details once.
2. Extract acceptance criteria.
3. Gather concise evidence from already-available artifacts.
4. Decide `READY` or `BLOCKED`.
5. If `READY`, post the closing comment and mark the task done.
6. Emit the close-gate result and stop.

If evidence is not found after the bounded checks below, return `BLOCKED` instead of broadening the search.

## Steps

1. Load task details via `task-show`.
2. Extract acceptance criteria from the task description.
3. Gather concise evidence from bounded sources only:
   - recent task comments,
   - referenced PR or merge status already present in task comments,
   - current branch/commit status when the user explicitly asked to verify a merged branch,
   - files directly named by the task, PR, or comments.
4. Evaluate each acceptance criterion with explicit evidence.
   - status per criterion: `met` | `partial` | `missing`
   - do not assume evidence
5. Determine readiness.
   - all criteria `met` => `READY`
   - any `partial`/`missing` => `BLOCKED`
6. Prepare a closing summary comment.
7. If status is `READY`:
   - add closing summary comment via `task-comment-create`
   - close task
   If status is `BLOCKED`, stop and report issues.
8. Emit the required output and stop immediately.

## Rules

- Do not close a task with incomplete criteria.
- Keep checks focused on acceptance criteria and closure readiness.
- Do not run stack-specific verification commands here (tests/log scraping/CI checks).
- Do not invoke unrelated skills such as `pr-review`; use existing review artifacts as evidence instead.
- Do not reread broad repository context, inspect unrelated files, or continue exploratory checks after each criterion has evidence.
- Do not add commentary after the required output.

## Tmux Completion Rule

When this skill runs inside the tmux sub-agent wrapper, emit the final close-gate output between the wrapper's result markers and signal completion immediately after the closing comment/status update or `BLOCKED` decision. No additional commentary, verification, or exploration may follow the marker-delimited result.

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
