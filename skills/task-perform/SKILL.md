---
name: task-perform
description: Execute a Todu task as written, record the result, and mark it done when finished. Use for do/work-on/start/pickup requests, or close/complete/verify-and-close requests without starting work. Not for habits, lookups, readiness-only, or verification-only requests. (plugin:todu)
---

# Perform Task

Use native `task_show`, `task_update`, and `task_comment_create`. Report unavailable tools or failed writes honestly; reconcile uncertain results before retrying, without duplicating comments or claiming success.

## 1. Start

- Load the task (or reuse a fresh successful load) and read applicable project instructions. If the task is missing, intent is unclear, or an actual blocker prevents work, explain it and ask only for what is needed.
- Do not silently reopen `done` or `cancelled` tasks. For `waiting`, establish whether its blocker is resolved before starting.
- Confirm `inprogress` with `task_update` using only `taskId` and `status` before doing work. If already `inprogress`, resume without a redundant status update. A starting comment is optional, not a prerequisite.

## 2. Do what the task says

- Execute the requested work within its scope and project rules. Record meaningful progress or blockers when useful, not every action.
- Do not impose a preflight skill, implementation-plan approval, close-gate handoff, or fallback contributing policy. Use `task-pipeline` only when the user/task requests that pipeline or project instructions explicitly select it. Repository changes or individual PR/merge requirements alone do not select the whole pipeline.
- Honor explicit planning, review, and approval requirements wherever they apply. Check the actual result with proportional evidence; normal verification does not require another skill.

## 3. Finish

- If the requested outcome is complete and applicable project requirements are satisfied, post a concise completion comment with the result and verification evidence. After confirmed comment success, mark `done` using only `taskId` and `status`. No extra default completion approval is needed.
- If blocked, incomplete, or unverified, comment with the actual gap and leave the task open without changing status merely to signal a blocker.
- If a comment or status write fails, report the partial result and reconcile before retrying. Report the actual final status.

## Close-only requests

For close/complete/verify-and-close requests, load the task and applicable instructions, check the existing result, and use step 3. Do not start implementation, set `inprogress`, or post a starting comment. Already-done tasks need no duplicate writes; cancelled tasks need a reopening decision. If evidence is insufficient, leave status unchanged and explain the gap. Verification-only, readiness-only, lookup, comment-only, and habit requests do not start this workflow.
