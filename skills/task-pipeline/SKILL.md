---
name: task-pipeline
description: Run the development delivery pipeline when the user asks to "pick up" or "pickup" a task.
---

# Task Pipeline — Development Delivery

Use this pipeline when the user asks to "pick up" or "pickup" a task, when the user/task requests the pipeline, or when project instructions explicitly select it. Repository changes or individual PR/merge requirements alone do not select the whole pipeline. Plain task execution uses ordinary agent handling and native task tools, not a dedicated execution skill.

## Planning and lifecycle boundary

Read the applicable project instructions and agree on a plan for substantial or ambiguous development work. Honor explicit project preview/approval requirements before implementation. Follow `docs/CONTRIBUTING.md` when present, otherwise [DEFAULT_CONTRIBUTING.md](DEFAULT_CONTRIBUTING.md). These development rules belong here, not in every task execution.

When the work is associated with a todu task, before starting work, set its status to `inprogress` using its explicit task ID and verify the update succeeded. If it is already `inprogress`, leave its status unchanged.

Continue the requested development stages without restarting task execution. Close an associated todu task only after the completion requirements below are satisfied.

## Choose the delivery path before editing

- Use the agreed deliverable and explicit applicable project policy, not request wording, file type, or a judgment that a change is too small for review.
- For planned tracked repository changes, default to a task branch (with a task worktree when used), PR, independent review, and explicit human-approved merge unless project policy explicitly permits a different delivery path. Small fixes and documentation-only changes do not bypass applicable gates.
- If policy is conflicting or unclear, return the specific decision needed to the caller for resolution during planning, before editing. An absent alternative policy uses the default repository path; it is not itself a conflict.
- Non-repository deliverables do not automatically need branch/worktree setup, PR, review, or merge stages. Brainstorming may stay in chat, Todu, or an untracked local document, or become committed repository documentation as agreed. There is no fixed storage destination; planned tracked documentation uses the repository delivery path.

## Applicable repository delivery stages

For the default PR path, follow these stages under project instructions. For an explicitly permitted alternative, follow that policy while retaining any applicable approval and verification requirements.

1. **Implement on the task branch or in a task worktree.** Make scoped changes for the agreed outcome, using existing project conventions and proportional tests/checks.
2. **Verify and publish.** Run required local checks, address failures, push the task branch associated with the working checkout or task worktree, and open/update the PR. When CI exists, resolve failures and wait for required checks to pass. If CI is unavailable, follow an explicit fallback policy or obtain the needed decision; do not silently count absence as success.
3. **Obtain review.** Use [pr-review](../pr-review/SKILL.md) for the assessment. Fix requested changes and non-waived warnings, recheck, and obtain review of the updated changes.
4. **Merge and normalize.** After satisfied gates, merge the reviewed changes, update the local target branch in its checkout or worktree, and clean up the task branch locally/remotely and any task worktree according to project policy. The default is branch and worktree cleanup after merge; ask if cleanup policy is uncertain. Do not force updates or discard unrelated work.

Applicable project review gates still apply.

## Return the delivery result

Check the requested development outcome and applicable gates against concrete evidence. Return what changed, relevant check results, PR/review artifacts, approval and merge state, branch/worktree normalization and cleanup, and any unresolved issue. Do not claim a gate passed without evidence or treat waiting for approval as completion.

Follow the applicable contributing document (`docs/CONTRIBUTING.md` or the default fallback) to determine whether to automatically start a preflight handoff. Return the result to the caller or user.

## Close the task

When the work is associated with a todu task, close it only after all task instructions and applicable project checks, reviews, approvals, and delivery requirements are satisfied. Add a comment summarizing the completed work and verification results, then set the task's status to `done`. Use the explicit task ID for both actions and verify they succeeded. An existing result comment containing this summary can satisfy the comment requirement; do not duplicate it.

If any instructions or requirements remain incomplete, do not mark the task `done`; inform the user what remains incomplete and ask for guidance. Waiting for approval is not completion.
