---
name: task-pipeline
description: Development-delivery reference loaded by task-perform for applicable repository changes. Not a standalone execution workflow; route do, work-on, start, and pickup requests to task-perform.
---

# Task Pipeline — Development Reference

Use this reference for the development stages of work owned by [task-perform](../task-perform/SKILL.md), not as another task executor.

## Lifecycle boundary

`task-perform` owns task/instruction loading, the shared [readiness check](../task-start-preflight/SKILL.md), plan agreement, confirmed start/resume, task comments, completion assessment, and closure. Direct execution requests enter through that skill regardless of wording. If it has already loaded this reference, continue the applicable development stages without recursively invoking it or repeating its lifecycle actions.

The caller obtains plan agreement for substantial or ambiguous work and honors additional explicit project preview/approval requirements before implementation. Do not add a second default planning gate here. Project contributing instructions apply; when none exist, the caller uses [DEFAULT_CONTRIBUTING.md](DEFAULT_CONTRIBUTING.md).

## Choose the delivery path before editing

- Use the agreed deliverable and explicit applicable project policy, not request wording, file type, or a judgment that a change is too small for review.
- For planned tracked repository changes, default to a branch, PR, independent review, and explicit human-approved merge unless project policy explicitly permits a different delivery path. Small fixes and documentation-only changes do not bypass applicable gates.
- If policy is conflicting or unclear, return the specific decision needed to the caller for resolution during planning, before editing. An absent alternative policy uses the default repository path; it is not itself a conflict.
- Non-repository deliverables do not automatically need branch/PR/review/merge stages. Brainstorming may stay in chat, Todu, or an untracked local document, or become committed repository documentation as agreed. There is no fixed storage destination; planned tracked documentation uses the repository delivery path.

## Applicable repository delivery stages

For the default PR path, follow these stages under project instructions. For an explicitly permitted alternative, follow that policy while retaining any applicable approval and verification requirements.

1. **Implement on the task branch.** Make scoped changes for the agreed outcome, using existing project conventions and proportional tests/checks.
2. **Verify and publish.** Run required local checks, address failures, push the branch, and open/update the PR. When CI exists, resolve failures and wait for required checks to pass. If CI is unavailable, follow an explicit fallback policy or obtain the needed decision; do not silently count absence as success.
3. **Obtain independent review.** Use [pr-review](../pr-review/SKILL.md) and its existing mechanism. Fix requested changes and non-waived warnings, recheck, and obtain review of the updated changes. Current-session author verification is not independent review. If required review is unavailable, report the blocker rather than substitute self-review or skip it.
4. **Wait for human merge approval.** Report the review result and stop until explicit approval is given. Review approval is not human merge approval; do not merge automatically or treat waiting as completed delivery.
5. **Merge and normalize.** After approval and satisfied gates, merge the reviewed changes, update the local target branch, and clean up the task branch locally/remotely according to project policy. The default is branch cleanup after merge; ask if cleanup policy is uncertain. Do not force updates or discard unrelated work.

No tmux delegation is required for development execution or completion verification. This does not redefine the PR-review skill's independent-review mechanism or waive explicit project gates.

## Return evidence to the lifecycle owner

Return concise development evidence to `task-perform`: what changed, relevant check results, PR/review artifacts, approval and merge state, branch normalization/cleanup, and any unresolved issue. Do not claim a required gate passed without evidence or continue past a blocker as though delivery succeeded.

The caller uses [task-close-gate](../task-close-gate/SKILL.md) in assessment-only mode in the current session to verify the agreed outcome and applicable gates with concrete evidence. This reference does not launch a hidden verifier, require another default permission prompt, or own task closure. After successful verification and applicable gates, `task-perform` posts its completion comment through native `task_comment_create` and then marks done through native `task_update`. If blocked or evidence is inconclusive, it records what remains and keeps the task open. Do not duplicate those lifecycle writes here.
