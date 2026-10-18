---
name: pr-review
description: Run PR review, verify artifacts, report outcome, and stop at the human merge gate. Use for "request review", "review PR", or "get this reviewed". Do not merge.
---

# PR Review

Assess a PR, post evidence-based findings to the PR and linked task, and stop before merge. Keep review separate from remediation and task closure.

## Establish the target

- Require a PR number/URL and a resolved task ID. Load task intent with native `task_show` (`taskId`); reuse a fresh successful load when available. Missing identity or failed context loading blocks review; do not guess.
- Resolve the repository and host from `origin` and any supplied PR URL or explicit target. Handle SSH and HTTPS remotes; do not infer provider from URL syntax alone. Resolve conflicting or ambiguous targets before reviewing or posting.
- Route GitHub (`github.com` or a positively identified GitHub Enterprise host) to [GitHub review](pr-gh-review.md). Route a positively identified Forgejo host to [Forgejo review](pr-fj-review.md). Establish custom-host identity from authoritative project configuration or verified server metadata. A non-GitHub URL, successful authentication, or a familiar API shape alone does not establish Forgejo. Report unsupported/unknown providers rather than defaulting to Forgejo.
- The host guide validates the open PR and reviewed revision; both hosts use [shared review logic](pr-review-common.md).

## Preserve independent review

Use a supported fresh reviewer context for independent assessment, without requiring tmux or a new orchestration platform. An already-running fresh reviewer can perform the review directly; do not recursively delegate. Give the reviewer the task's agreed outcome/constraints, PR identity and base/head revision, applicable instructions, diff, and relevant evidence; permit scoped context gathering and targeted checks. The author's conclusions are not a substitute for the reviewer's own assessment.

If the caller authored the changes and no fresh context is available, report independent review as unavailable and keep that gate unsatisfied. Do not silently substitute current-session review. Explicitly requested same-session self-review must be labeled **self-review**, including in artifacts; it cannot satisfy a required independent-review gate. Do not launch a second review when a fresh assessment already exists for the same revision and scope; validate and reuse its evidence.

## Assess, post, and stop

1. Apply shared review logic in the reviewer context. Inspect enough relevant evidence to support the verdict, then stop; do not restrict review to the diff or broaden it into unrelated exploration.
2. Follow the selected host guide to post the findings and a matching factual summary via native `task_comment_create` (`taskId`, `content`). The reviewer or caller may post; use one designated poster to avoid duplicates. This authorized review workflow needs no separate authoring handoff or extra default posting approval. Draft-only requests do not authorize writes.
3. Confirm each post independently from the command/tool result or a targeted read-back. Record returned PR comment URL and task note ID when available. A failure or uncertain write is not success: reconcile before retrying, retain successful artifacts, and report partial results without blind duplicate posts.
4. Return one concise result as described below. Do not run broad checks or revisit settled findings after sufficient assessment and posting. If new relevant evidence or a changed revision invalidates the assessment, report that gap rather than claiming completion.

## Result and boundaries

Report the reviewed PR/revision, **independent review** or **self-review**, a verdict (`approved`, `warnings`, `changes-requested`, or `pending`), actionable findings with evidence, relevant checks/limitations, and separate PR/task artifact statuses (`posted`, `failed`, `unknown`, or `not-attempted`) with references when available. Reuse this result across the caller and host guides; no worker-specific result template or mandatory criteria counts are needed.

- `approved`: sufficient evidence supports the agreed outcome and applicable policy, with no supported blockers or non-blocking findings.
- `warnings`: only non-blocking findings; report them as suggestions, not automatic fixes.
- `changes-requested`: supported blocking findings; explain the failure scenario and required correction without implementing it.
- `pending`: evidence, context, or required independence is insufficient; explain the actual gap, not a fabricated defect.

A review workflow is complete only for an open PR at the assessed revision, with an adequately supported assessment, required independence, and both artifacts confirmed posted. Posting failures do not change a supported code verdict, but make the workflow incomplete. An explicit self-review can finish its requested report/posts while leaving the independent-review gate unsatisfied; do not present it as completed required independent review.

Never edit the implementation, automatically fix warnings, expand approved task scope, merge, or close the task in this skill. Return findings to the execution workflow for scoped remediation and any applicable warning-waiver policy; material changes need review of the updated revision. An approved review is not human merge approval. Report the outstanding gate and stop; even an explicit merge request belongs outside this skill.
