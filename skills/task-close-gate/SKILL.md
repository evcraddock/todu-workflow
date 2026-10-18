---
name: task-close-gate
description: Assess task completion against the agreed outcome and evidence without task mutations. Use for verification-only requests and task-perform completion checks. Explicit close/complete/verify-and-close requests use task-perform's closure-only path. Do not start or implement work.
---

# Task Close Gate — Completion Assessment

One shared verifier for completion, always assessment-only. Return evidence and a readiness verdict; never post task comments or change task status. [task-perform](../task-perform/SKILL.md) owns lifecycle writes for automatic completion and explicit close requests.

## Assess the agreed outcome

1. Load the task with native `task_show` (`taskId`), or reuse the caller's fresh successful result. Use the task, relevant agreed context, and explicit project gates to identify what completion means. Assess supplied acceptance criteria when present, or the agreed outcome when no formal section exists. Do not invent requirements or demand a template. Missing/failed task retrieval or unresolved scope prevents a ready verdict; explain the specific issue.
2. Prefer relevant existing evidence: delivered results, task-linked check reports, review artifacts, merge/approval state when required, and directly relevant files. Check that evidence actually supports the agreed outcome and delivered version. A prior comment merely saying "done" is not proof; neither is an irrelevant test result or an unmerged PR when merge is required.
3. If evidence is insufficient and a focused check can resolve it, use available native task/note tools, ordinary file reads, or targeted, proportionate non-destructive verification commands. Do not require another test run when existing evidence is sufficient. Respect explicit approvals and safety constraints for any particular action; do not add a default permission prompt merely to verify.
4. Assess the outcome/criteria as met, partial, or missing, with source references or observed results. A failed/unavailable check or unconfirmed result is not proof. Stop once evidence is sufficient or an actual blocker is established; do not search indefinitely for a passing result.

Verification is not implementation or another PR review. Do not fill in missing work, change the agreed deliverable, start a review/merge flow, or broaden into unrelated files, checks, or environment setup. Report what remains to the caller instead.

## Return readiness, not closure

- Ready only when the agreed outcome and any acceptance criteria are supported and applicable project gates are satisfied. Explicit merge/approval requirements remain effective; waiting for approval or missing gate evidence is not completion.
- Otherwise return not ready, distinguishing partial/missing outcomes, insufficient evidence, lookup/check failures, and pending decisions or gates. Explain only the actual gap and any focused next decision needed.
- Keep the result concise: task identity, verdict, supporting evidence, and unresolved items when relevant. No rigid output template, empty sections, mandatory criteria count, or claim that a closing comment/status change occurred.

Run in the current session; no tmux wrapper, detached verifier, or separate verification approval is required. A successful assessment is not independent PR review and does not replace one when project policy requires it.

## Handoff boundary

When invoked by task-perform, return the assessment to that existing caller without recursively invoking it. For a verification-only request, stop after the verdict: verification does not authorize closure. For an explicit close/complete/verify-and-close request, [task-perform's closure-only path](../task-perform/SKILL.md#closure-only-requests) owns the request and calls this verifier; it must not start implementation just to close already-delivered work. After successful verification and applicable gates, that owner records completion and changes status without an extra default approval prompt. This verifier performs neither write.
