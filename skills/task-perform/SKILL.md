---
name: task-perform
description: Own the Todu task lifecycle for do/work-on/start/pickup requests, or close/complete/verify-and-close requests in closure-only mode without starting work. Do not use for habits, task lookup, readiness-only, or verification-only requests. (plugin:todu)
---

# Perform Task

Own the task lifecycle. Wording such as "do", "work on", or "pickup" must not select different approval rules. Use native `task_show`, `task_update`, and `task_comment_create` tools, not CLI commands or task/comment wrapper skills. If required tools are unavailable, report the limitation; do not pretend a status change or comment succeeded.

## Closure-only requests

For an explicit close/complete/verify-and-close request, load the task and applicable project instructions, then enter section 4 directly. Do not run start preflight, set inprogress, post a starting/resuming comment, or implement missing work. Reuse a fresh successful task load from the caller when available; do not restart an existing invocation.

For already-done tasks, report that state without duplicate closure writes. Do not silently reopen cancelled tasks; report the status decision needed. Active, inprogress, or waiting tasks may proceed to completion assessment, but any unresolved blocker and applicable project gate still prevent closure. If verification is not ready, explain/record the actual gap and leave the status unchanged rather than starting work to fill it.

Verification-only requests belong to [task-close-gate](../task-close-gate/SKILL.md) and end with its assessment, without lifecycle writes. This closure-only path shares the section 4 completion ordering and failure handling; it is not a second lifecycle implementation or permission to bypass approval gates.

## 1. Understand and check readiness

- Load the task with `task_show` and read applicable repository/project instructions. Follow `docs/CONTRIBUTING.md` when present, otherwise the [default contributing instructions](../task-pipeline/DEFAULT_CONTRIBUTING.md). Resolve conflicting instructions before editing.
- For `active` tasks or resuming `inprogress` tasks, use [task-start-preflight](../task-start-preflight/SKILL.md) as a read-only shared readiness check. Do not reset a resumed task to `active` merely to run preflight.
- Do not silently reopen `done` or `cancelled` tasks. For a `waiting` task, establish whether the blocker is resolved and whether starting is authorized before transitioning. If status or requirements prevent work, explain the issue and ask only for the decision or clarification needed.
- Agree on a plan for substantial or ambiguous work and honor explicit project preview/approval requirements. Readiness checks and plan discussion may precede the start transition; implementation may not.

## 2. Confirm the start and record intent

- If the task is not already `inprogress`, call `task_update` with only `taskId` and `status: "inprogress"`. Require a confirmed successful result before performing work. If the task was already `inprogress`, leave its status unchanged.
- A failed or uncertain update is not confirmation. Re-read the task when necessary to reconcile an uncertain result; stop if `inprogress` cannot be confirmed. Do not blindly retry writes or alter assignees/other metadata.
- Post a concise starting (or resuming) comment with `task_comment_create`, describing the intended work and relevant boundaries. If posting fails or is uncertain, report/reconcile it before proceeding; do not claim the update was recorded.

## 3. Perform the agreed work

- Follow the task's agreed outcome and project constraints. Keep comments factual and proportional: record meaningful progress, decisions, blockers, or agreed scope changes, not every command or file edit.
- Select delivery stages from the agreed deliverable and explicit project policy, not from request wording or a judgment that a change is too small for review.
- For planned tracked repository changes, default to branch, PR, independent review, and explicit human-approved merge unless explicit project policy permits another delivery path. Load [task-pipeline](../task-pipeline/SKILL.md) as development-workflow guidance, not as another lifecycle executor. Resolve unclear delivery policy before editing.
- Non-repository deliverables do not automatically require a branch, PR, or merge. Brainstorming may result in chat conclusions, backend records, local documents, or committed documentation; there is no fixed storage destination. Tracked documentation changes still count as repository changes.
- Do not mandate tmux delegation for execution or completion verification. Preserve any independent-review requirement; self-review is not independent review. If the required review mechanism is unavailable, report the blocker rather than silently bypassing it. This skill does not change `pr-review`'s own mechanism.

## 4. Verify, summarize, and close

- Use [task-close-gate](../task-close-gate/SKILL.md) in the current session. It is always assessment-only and returns completion evidence and a verdict without posting comments or changing status.
- Verify the requested outcome and any acceptance criteria with concrete, proportional evidence. When there is no formal criteria section, assess the agreed outcome instead. Do not invent requirements or substitute an unsupported "done" claim for evidence. Reuse applicable existing checks/review artifacts; gather targeted evidence when needed.
- All applicable project gates must be satisfied before closure, including explicit merge approval and completed merge when required. Automatic completion never bypasses an approval gate. Waiting for approval is not completion.
- If work is blocked, verification fails, or evidence is inconclusive, post a concise comment explaining what was done, what remains, and any decision needed. Keep the task open; do not mark it `done` or change it to another status merely to signal a blocker. Report a failed comment write as well as the underlying issue.
- When verification and applicable gates pass, post a completion comment describing what changed and the verification evidence. Only after confirmed comment success call `task_update` with only `taskId` and `status: "done"`. Do not ask for an additional default completion approval.
- If a write fails or its outcome is uncertain, report partial completion and reconcile current task/comment state before retrying. A successful comment followed by a failed status update must not produce a false closure claim or a blind duplicate comment.
- Report the actual final status and any unresolved issue concisely. Task lookup, readiness-only, verification-only, and habit requests must not start this lifecycle. Explicit close requests use the closure-only path, never execution sections 1–3.
