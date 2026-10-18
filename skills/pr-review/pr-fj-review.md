# Forgejo PR Review

Use only after the [PR Review skill](SKILL.md) positively identifies the target as Forgejo. Verify that `origin` resolves to that repository and bind commands with `fj --host <verified-host> pr --remote origin ...`. If the supplied target uses another remote, resolve and explicitly select that verified remote instead; do not silently use a different repository. Confirm installed CLI support with `fj pr --help` when necessary; do not invent unsupported flags or assume every self-hosted server is Forgejo.

1. Confirm the PR exists and is open, and capture its identity and base/head revisions:
   - `fj --host <verified-host> pr --remote origin view <number>`
   - `fj --host <verified-host> pr --remote origin view <number> diff`
   - Require confirmed open state and identify the assessed base/head from supported CLI output or an authorized read-only Forgejo API request. If the available output cannot establish state or revision, report the missing evidence rather than assuming it.
2. Apply [shared assessment](pr-review-common.md) with the required fresh-context independence. Relevant surrounding code or targeted checks are permitted; use the PR's reviewed revision rather than assuming the working tree matches it. A completed fresh assessment for that revision can be reused without another review.
3. Before posting, confirm the PR remains open at the assessed base/head revisions using the supported metadata source. A changed revision makes the old assessment stale; return to the caller for review of the changed revision, not approval from old evidence.
4. Draft the PR review and linked-task summary inline. Post once through the designated poster:
   - `fj --host <verified-host> pr --remote origin comment <number> --body-file <review-file>`
   - Native `task_comment_create` with the resolved `taskId` and factual `content`, including the PR reference.
5. Confirm each artifact independently from the command/tool result. When the PR post is ambiguous, use a focused read-back such as `fj --host <verified-host> pr --remote origin view <number> comments` before any retry. Preserve a successful post when the other fails; mark an unreconciled timeout `unknown`, not `posted` or safely absent.
6. Return the [single review result](SKILL.md#result-and-boundaries), including reviewed revision, evidence, independence, and separate artifact statuses. A supported assessment plus one failed/uncertain post is an incomplete workflow, not a successful review delivery. If a subsequent head change is known, report that limitation and leave the current-revision review gate unsatisfied. Stop before merge or remediation.
