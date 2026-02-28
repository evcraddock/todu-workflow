---
name: request-review
description: Request a PR review from a separate review pass. Use when user says "request review", "get this reviewed", or similar.
---

# Request Review

Run a PR review pass, report the result, and stop at the human merge-approval gate.

## Invariants (Hard Rules)

- Do not merge in this skill.
- Do not report completion until required review artifacts are present:
  1) PR review comment posted
  2) task comment posted via `task-comment-create` skill (if task ID exists)
- Never claim an in-progress state as complete.

## Host Detection

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if echo "$REMOTE_URL" | grep -q "github.com"; then
  HOST="github"
else
  HOST="forgejo"
fi
```

## Command Map by Host

| Operation | GitHub | Forgejo |
|---|---|---|
| View PR | `gh pr view <num>` | `zsh -ic "fj pr view <num>"` |
| View PR body | `gh pr view <num> --json body --jq '.body'` | `zsh -ic "fj pr view <num>"` |
| View PR comments | `gh pr view <num> --json comments` | `zsh -ic "fj pr view <num> comments"` |
| Comment on PR | `gh pr comment <num> --body-file <file>` | `zsh -ic "fj pr comment <num> --body-file <file>"` |

> Forgejo CLI requires `zsh -ic` for keyring access.

## Required Procedure

### 1) Validate PR

- Confirm PR exists and is open.

GitHub:
```bash
gh pr view <number> --json number,title,state,statusCheckRollup,body
```

Forgejo:
```bash
zsh -ic "fj pr view <number>"
```

### 2) Enforce CI Gate (before review)

GitHub (checks available):
```bash
gh pr checks <number> --watch
```
- Require green before proceeding.
- If failed: report failures and either fix/re-run checks or stop for user decision.

If CI cannot be verified automatically, resolve using this order:
1. Current user instruction for this PR (continue / wait / stop)
2. Standing policy from AGENTS.md
3. Ask human (only if neither 1 nor 2 exists)

Accepted actions:
- **continue**: proceed without CI signal and report `ci: unavailable-needs-human-decision` with note that standing/explicit human policy was applied.
- **wait**: pause until human confirms manual CI verification.
- **stop**: stop the workflow.

### 3) Gather Context

Extract task ID from PR body:
```bash
gh pr view <number> --json body --jq '.body' | grep -oP 'Task:?\s*#?\K\d+' | head -1
```
(Use Forgejo equivalent if needed.)

### 4) Run Review Pass

- Execute the `pr-review` process.
- Ensure it posts:
  - PR review comment
  - task comment via `task-comment-create` skill when task ID exists

### 5) Verify Review Artifacts

- Verify PR review comment exists (fetch latest PR comments).
- If task ID exists, verify task contains review comment entry created via `task-comment-create` skill (for example `PR Review for #<number>` in `todu task show <task-id>` output).

If required artifacts are missing, status is not complete.

### 6) Report Outcome and Stop at Merge Gate

Outcomes:
- `approved`: report approval, wait for explicit human merge approval
- `warnings`: list warnings; fix by default; only skip fixes if human explicitly waives
- `changes-requested`: fix and re-run review after updates

Never merge inside this skill.

## ACTION_PROOF (Required)

Do not claim completion without evidence for all applicable items:

1. **ci_gate**
   - command used to verify CI or explicit policy decision if unavailable
2. **pr_review_comment**
   - command used to fetch comments
   - evidence latest review comment was posted
3. **task_review_comment** (when task ID exists)
   - evidence `task-comment-create` skill was used
   - command used to check task
   - evidence review comment exists on task

If any required proof is missing or fails, status is not complete.

## Agent Output Contract (Required)

```text
Request Review Status
- ci: pass|fail|unavailable-needs-human-decision
- review: pending|approved|warnings|changes-requested
- merge_approval: waiting-human|approved
```

Rules:
- Do not skip fields.
- Do not phrase required next steps as optional.
- If `ci=unavailable-needs-human-decision`, either apply a documented standing policy or obtain explicit per-PR human decision before review starts.
- Never merge without explicit human approval.
