# GitHub PR Review

Use only after the [PR Review skill](SKILL.md) resolves the target as GitHub. Bind every command to the verified repository with `--repo <host/owner/repo>`; do not let an ambient checkout select a different PR.

1. Confirm the PR exists and is open, and capture its identity and base/head revisions:
   - `gh pr view <number> --repo <host/owner/repo> --json number,url,title,body,state,baseRefOid,headRefOid`
   - Require `state=OPEN`. A missing, inaccessible, closed, or merged PR cannot complete this workflow; report the actual result.
   - `gh pr diff <number> --repo <host/owner/repo>`
2. Apply [shared assessment](pr-review-common.md) with the required fresh-context independence. Relevant surrounding code or targeted checks are permitted; use the PR's reviewed revision rather than assuming the working tree matches it. A completed fresh assessment for that revision can be reused without another review.
3. Before posting, confirm the PR remains open at the assessed base/head revisions. If it changed, report the assessment as stale and obtain review of the changed revision through the caller; do not approve the new head using old evidence.
4. Draft the PR review and linked-task summary inline. Post once through the designated poster:
   - `gh pr comment <number> --repo <host/owner/repo> --body-file <review-file>`
   - Native `task_comment_create` with the resolved `taskId` and factual `content`, including the PR reference.
5. Confirm each artifact independently. A successful command result with its comment URL is confirmation; if ambiguous, use a focused read-back such as `gh pr view <number> --repo <host/owner/repo> --comments` to reconcile before any retry. Preserve a successful post when the other fails; mark an unreconciled timeout `unknown`, not `posted` or safely absent.
6. Return the [single review result](SKILL.md#result-and-boundaries), including reviewed revision, evidence, independence, and separate artifact statuses. A supported assessment plus one failed/uncertain post is an incomplete workflow, not a successful review delivery. If a subsequent head change is known, report that limitation and leave the current-revision review gate unsatisfied. Stop before merge or remediation.
