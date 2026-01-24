---
name: request-review
description: Request a PR review from a separate agent session. Use when PR is ready and you say "request review", "get this reviewed", "need a review on PR #*", or similar.
---

# Request Review

Spawn a separate agent session in a new tmux pane to review a PR. This ensures the reviewer has fresh context and no implementation bias.

## When to Use

After creating a PR and confirming CI passes, use this to request an independent review.

## Prerequisites

- Must be in a tmux session
- PR must exist and CI should be passing
- Current directory should be the project root

## Steps

### 1. Confirm PR Details

```bash
gh pr view <number> --json number,title,state,statusCheckRollup,body
```

Verify:
- PR exists
- CI has passed (or is passing)

### 2. Extract Task ID

Parse the task ID from the PR body:

```bash
gh pr view <number> --json body --jq '.body' | grep -oP 'Task:?\s*#?\K\d+' | head -1
```

### 3. Get Project Path

```bash
pwd
```

### 4. Spawn Review Session

Include both PR number and task ID in the prompt:

**With task ID:**
```bash
tmux new-window -n "pr-review-<number>" "cd <project-path> && pi --model gpt-5.2-codex \"Review PR #<number> (Task #<task-id>) using the pr-review skill. After reviewing:
1. Post review to PR: gh pr comment <number> --body-file /tmp/review-<number>.md
2. Post review to task: todu task comment <task-id> -m '<review-content>'
3. Close this window: tmux kill-window\""
```

**Without task ID:**
```bash
tmux new-window -n "pr-review-<number>" "cd <project-path> && pi --model gpt-5.2-codex \"Review PR #<number> using the pr-review skill. After reviewing:
1. Post review to PR: gh pr comment <number> --body-file /tmp/review-<number>.md
2. Close this window: tmux kill-window\""
```

### 5. Wait for Review to Complete

Poll until the tmux window closes:

```bash
echo "Waiting for review to complete..."
while tmux list-windows -F '#{window_name}' 2>/dev/null | grep -q "pr-review-<number>"; do
  sleep 3
done
echo "Review complete."
```

### 6. Check Review Results

After the window closes, fetch the review comment:

```bash
gh pr view <number> --json comments --jq '.comments[-1].body'
```

Report the review findings to the user and ask how to proceed:
- If approved: offer to merge
- If changes requested: show what needs fixing

## Example Flow

**User:** "Request a review for PR 17"

**Agent:**
```
Checking PR #17...
✓ PR exists: "docs: add README with project overview"
✓ CI passed
✓ Task ID: #1232

Spawning review session in tmux window 'pr-review-17'...
Waiting for review to complete...
```

*[Agent waits while reviewer works in other window]*

```
Review complete.

Fetching review comment...

## Code Review: Approved ✅

### Checklist
- [x] PR description clear
- [x] Code follows standards
- [x] No security concerns

LGTM 🚀

---

Review passed. Merge the PR? [yes/no]
```

## Non-Interactive Mode

For fully automated reviews:

```bash
tmux new-window -n "pr-review-<number>" "cd <project-path> && pi --model gpt-5.2-codex -p \"Review PR #<number> using the pr-review skill. Add comment to PR with gh pr comment and to task #<task-id> with todu task comment.\""
```

The `-p` flag makes pi exit after completing, which will close the window automatically.

## Notes

- Reviewer agent starts fresh with no context from this session
- Reviewer uses `pr-review` skill which has its own checklist
- Review is posted as both a PR comment and a task comment
- Window closing signals review completion
- After review, check the comment and decide whether to merge
