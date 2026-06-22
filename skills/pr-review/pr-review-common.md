# PR Review Common Logic

Shared review logic for all hosts.

## Required Inputs

- task ID (required)
- PR title/body
- PR diff

## Bounded Checklist

1. Load task details once with `task-show` using the provided task ID.
2. Extract task objective and acceptance criteria from the task description.
3. Compare the PR diff against each acceptance criterion.
4. Check only review-relevant quality concerns.
5. Decide exactly one outcome.
6. Prepare required artifact content.

Stop once the outcome and artifact content are ready. Do not reread broad context, revisit settled criteria, or continue exploratory checks after choosing the verdict.

## Procedure

1. Load task details via `task-show` using the provided task ID.
2. Extract task objective and acceptance criteria from the task description.
3. Review PR changes against each acceptance criterion.
   - mark each criterion as: `met` | `partial` | `not-evident`
4. Run quality checks during review:
   - scope alignment
   - code quality and maintainability
   - tests for logic changes
   - security concerns
   - documentation impact
5. Decide exactly one outcome:
   - `approved`
   - `warnings`
   - `changes-requested`

## Decision Rules

- Any acceptance criterion marked `not-evident` => `changes-requested`
- Missing tests for logic changes => `changes-requested`
- Potential bugs/correctness issues => `changes-requested`
- Policy violations => `changes-requested`
- `warnings` only for non-blocking concerns

## Required Review Content

Use `task-comment-authoring` when drafting the task-facing review summary. Review comment content must include:
- summary
- acceptance criteria checklist with per-criterion status
- blocking issues (if any)
- warnings (if any)
- final verdict

## Common Result Fields

```text
- review: approved|warnings|changes-requested
- blocking_issues: <count>
- warnings: <count>
- criteria_total: <count>
- criteria_met: <count>
- criteria_missing: <count>
```
