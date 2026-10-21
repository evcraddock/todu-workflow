---
name: task-pipeline
description: Run the development delivery pipeline when explicitly requested by the user/task or explicitly selected by project instructions. Covers planning, implementation, checks, PR, independent review, and human-approved merge. Does not own task status or comments.
---

# Task Pipeline — Development Delivery

Use this pipeline only when the user/task requests it or project instructions explicitly select it. Repository changes or individual PR/merge requirements alone do not select the whole pipeline. Plain task execution uses ordinary agent handling and native task tools, not a dedicated execution skill.

## Planning and lifecycle boundary

Read the applicable project instructions and agree on a plan for substantial or ambiguous development work. Honor explicit project preview/approval requirements before implementation. Follow `docs/CONTRIBUTING.md` when present, otherwise [DEFAULT_CONTRIBUTING.md](DEFAULT_CONTRIBUTING.md). These development rules belong here, not in every task execution.

This pipeline handles development delivery, not task status or comments. Continue the requested development stages without restarting task execution.

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
