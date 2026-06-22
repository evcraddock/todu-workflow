---
name: pr-review
description: Run PR review, verify artifacts, report outcome, and stop at the human merge gate. Use for "request review", "review PR", or "get this reviewed". Do not merge.
---

# PR Review

Review a PR and stop before merge.

## Inputs

- PR number
- task ID (required)

## Bounded Execution Contract

Complete the review with this short checklist only:

1. Validate required inputs.
2. Detect the PR host.
3. Run the matching host worker.
4. Validate required worker result fields and artifacts.
5. Report the outcome and stop at the merge gate.

Do not broaden the review after the worker returns a verdict. Do not reread unrelated project context, rerun checks, or continue exploratory reasoning after required artifacts are posted.

## Steps

1. Validate task ID is provided.
   - if missing, stop as `BLOCKED`
2. Detect host from `origin` remote.
   - GitHub => follow `./pr-gh-review.md`
   - otherwise => follow `./pr-fj-review.md`
3. Use worker output as source of truth.
   - required: `pr=open`
   - required: `pr_comment=posted`
   - required: `task_comment=posted`
   - required: criteria fields reported (`criteria_total`, `criteria_met`, `criteria_missing`)
   - if required artifacts are missing: status is not complete
4. Report outcome and stop at merge gate.
   - `approved` => wait for explicit human merge approval
   - `warnings` => fix by default unless human waives
   - `changes-requested` => fix and rerun review

## Rules

- Never merge in this skill.
- Never claim completion while required artifacts are missing.
- Do not phrase required next steps as optional.
- Avoid sub-skill calls except the explicitly required task/comment tooling used to post artifacts and `task-comment-authoring` when drafting structured review/task comments.
- After the verdict is determined and required artifacts are posted, do not run additional checks or broad rereads.

## Tmux Completion Rule

When this skill runs inside the tmux sub-agent wrapper, emit the final `PR Review Status` output between the wrapper's result markers and signal completion immediately after posting required artifacts. No additional commentary, verification, or exploration may follow the marker-delimited result.

## Output Contract

```text
PR Review Status
- review: pending|approved|warnings|changes-requested
- merge_approval: waiting-human|approved
```

## Worker Output Contract (Required)

```text
PR Review Worker Result
- pr: open|invalid|closed
- review: approved|warnings|changes-requested
- pr_comment: posted|failed
- task_comment: posted|failed
- blocking_issues: <count>
- warnings: <count>
- criteria_total: <count>
- criteria_met: <count>
- criteria_missing: <count>
```
