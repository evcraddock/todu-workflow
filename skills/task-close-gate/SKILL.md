---
name: task-close-gate
description: Assess task completion without task mutations when verification-only or a close-gate assessment is explicitly requested or required by task/project instructions. Not a mandatory task-perform completion step. Close/complete requests belong to task-perform. Do not start or implement work.
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

Stop after the assessment: verification does not authorize closure. If an execution workflow explicitly requested this assessment, return to that existing caller without restarting it. This skill is not an automatic completion step. Explicit close/complete/verify-and-close requests belong to [task-perform's close-only path](../task-perform/SKILL.md#close-only-requests), which checks the result directly unless task/project instructions require this assessment. This verifier never posts comments or changes status.
