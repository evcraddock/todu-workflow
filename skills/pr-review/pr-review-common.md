# PR Review — Shared Assessment

Use this logic for either supported host. The [PR Review skill](SKILL.md) owns the single result format, independence requirement, artifact confirmation, and merge boundary; host guides supply commands rather than another review contract.

## Scope and evidence

Load the linked task with native `task_show`, or reuse its fresh successful result. Establish the task's intent, agreed outcome, explicit constraints, and any acceptance criteria. A formal criteria section is not required: assess the actual agreed outcome without inventing obligations or mandatory counts.

Review the PR title/body, diff, base/head revision, and applicable project instructions against that outcome. Consider correctness, security, maintainability, scope, documentation impact, and relevant tests in proportion to the change. Assess formal criteria individually when present; otherwise explain how the outcome is or is not supported.

Permit relevant surrounding code, callers, configuration, and targeted non-destructive checks when needed to resolve a concrete review question. Existing task-linked check results may be reused when they support the reviewed revision. Distinguish tests actually run, supplied results, unrun checks, and unavailable verification; never invent passing checks. Missing tests matter when an agreed requirement or a concrete verification gap warrants them, not as an automatic rejection of every logic change.

Stop when sufficient evidence supports a verdict or a specific unresolved gap prevents it. Do not continue unrelated exploration, rerun broad suites without a reason, or enforce a diff-only evidence limit. Do not implement fixes during review.

## Findings and verdict

For each actionable finding, identify the relevant file/line or other concrete evidence and explain its impact. For correctness/security blockers, describe the input or conditions that produce the failure and why they contradict the agreed outcome or applicable policy. Distinguish:

- **Supported blockers:** demonstrated defects, unmet agreed requirements, or established policy violations. These support `changes-requested`, with a scoped correction described rather than implemented.
- **Uncertainty:** evidence is missing or inconclusive. State what is known and the focused check/context needed. A speculative potential bug alone is not a demonstrated blocker. If the uncertainty prevents a credible assessment of the agreed outcome, use `pending`; do not approve without evidence or falsely label the uncertainty a proven defect.
- **Non-blocking suggestions:** optional clarity/maintainability improvements or other concerns that do not prevent the agreed outcome. Use `warnings` when these are the only findings. Do not require their implementation or treat them as permission to expand scope; the execution caller handles any separate project policy.

Use `approved` only when the evidence adequately supports the outcome and policy and there are no findings. Where a supported blocker and an evidence gap coexist, report both; do not hide a demonstrated failure behind uncertainty. Approval never authorizes merge.

## Artifact content

Draft a factual review containing the reviewed revision and review kind, outcome/criteria assessment, actionable findings and evidence, checks and limitations, and verdict. An empty section or generic checklist is unnecessary. The linked-task summary may be shorter, but must preserve blockers, unresolved questions, material suggestions, and the review's limitations. Include a PR reference so the task can be traced to the detailed assessment.

Use the same assessment for both artifacts; do not fabricate posting success, independent review, test results, human approval, or completion. Draft-only work does not post. Authorized review posts directly through the host command and native `task_comment_create`; the [skill result](SKILL.md#result-and-boundaries) separately reports confirmed/failed/uncertain artifacts. No standalone task/comment skill or authoring handoff is required.
