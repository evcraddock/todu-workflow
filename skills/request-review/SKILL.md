---
name: request-review
description: Request a PR review from a separate agent session. Use when PR is ready and you say "request review", "get this reviewed", "need a review on PR #*", or similar.
---

# Request Review

Spawn a separate agent session in a new tmux window to review a PR. This ensures the reviewer has fresh context and no implementation bias.

## When to Use

After creating a PR and confirming CI passes, use this to request an independent review.

## Prerequisites

- Must be in a tmux session (or will create one)
- PR must exist and CI should be passing
- Current directory should be the project root

## Host Detection

Detect the git host from the remote URL:

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if echo "$REMOTE_URL" | grep -q "github.com"; then
  HOST="github"
else
  HOST="forgejo"
fi
```

## CLI Commands by Host

| Operation | GitHub | Forgejo |
|-----------|--------|---------|
| View PR | `gh pr view <num>` | `zsh -ic "fj pr view <num>"` |
| View PR JSON | `gh pr view <num> --json ...` | `zsh -ic "fj pr view <num> --json ..."` |
| Comment on PR | `gh pr comment <num> --body "..."` | `zsh -ic "fj pr comment <num> --body '...'"` |
| Comment from file | `gh pr comment <num> --body-file <file>` | `zsh -ic "fj pr comment <num> --body-file <file>"` |

**Note:** Forgejo CLI (`fj`) requires `zsh -ic` wrapper for keyring access.

## Model Configuration

The review agent model is configurable:

1. Check `$PI_REVIEW_MODEL` environment variable
2. If not set, omit `--model` flag (uses pi's default)

```bash
if [ -n "$PI_REVIEW_MODEL" ]; then
  MODEL_FLAG="--model $PI_REVIEW_MODEL"
else
  MODEL_FLAG=""
fi
```

## Steps

### 1. Detect Host and Set CLI

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if echo "$REMOTE_URL" | grep -q "github.com"; then
  HOST="github"
  PR_VIEW="gh pr view"
  PR_COMMENT="gh pr comment"
else
  HOST="forgejo"
  PR_VIEW='zsh -ic "fj pr view'
  PR_COMMENT='zsh -ic "fj pr comment'
fi
```

### 2. Confirm PR Details

**GitHub:**
```bash
gh pr view <number> --json number,title,state,statusCheckRollup,body
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number>"
```

Verify:
- PR exists
- CI has passed (or is passing)

### 3. Extract Task ID

Parse the task ID from the PR body:

**GitHub:**
```bash
gh pr view <number> --json body --jq '.body' | grep -oP 'Task:?\s*#?\K\d+' | head -1
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number>" | grep -oP 'Task:?\s*#?\K\d+' | head -1
```

### 4. Get Project Path

```bash
PROJECT_PATH=$(pwd)
```

### 5. Set Up tmux Session

Use the tmux skill patterns. Set up socket and session:

```bash
SOCKET_DIR=${TMPDIR:-/tmp}/claude-tmux-sockets
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/claude.sock"
SESSION="pr-review-<number>"
```

### 6. Spawn Review Session

Create a new tmux window with the review agent:

```bash
# Build model flag
if [ -n "$PI_REVIEW_MODEL" ]; then
  MODEL_FLAG="--model $PI_REVIEW_MODEL"
else
  MODEL_FLAG=""
fi

# Spawn review session
tmux -S "$SOCKET" new-window -n "$SESSION" \
  "cd $PROJECT_PATH && pi $MODEL_FLAG -p \"Review PR #<number> (Task #<task-id>) using the pr-review skill. Post review to PR and task, then exit.\""
```

**Tell the user how to monitor:**
```
To monitor the review session:
  tmux -S $SOCKET attach -t $SESSION

Or capture output:
  tmux -S $SOCKET capture-pane -p -J -t $SESSION:0.0 -S -200
```

### 7. Wait for Review to Complete

Poll until the tmux window closes:

```bash
echo "Waiting for review to complete..."
while tmux -S "$SOCKET" list-windows -F '#{window_name}' 2>/dev/null | grep -q "$SESSION"; do
  sleep 3
done
echo "Review complete."
```

### 8. Check Review Results

After the window closes, fetch the review comment:

**GitHub:**
```bash
gh pr view <number> --json comments --jq '.comments[-1].body'
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number> --comments" | tail -50
```

Report the review findings to the user and ask how to proceed:
- If approved: offer to merge
- If changes requested: show what needs fixing

## Example Flow

**User:** "Request a review for PR 17"

**Agent:**
```
Detecting host... GitHub (github.com)
Checking PR #17...
✓ PR exists: "docs: add README with project overview"
✓ CI passed
✓ Task ID: #1232

Spawning review session...

To monitor the review session:
  tmux -S /tmp/claude-tmux-sockets/claude.sock attach -t pr-review-17

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

## Notes

- Reviewer agent starts fresh with no context from this session
- Reviewer uses `pr-review` skill which has its own checklist
- Review is posted as both a PR comment and a task comment
- Window closing signals review completion
- After review, check the comment and decide whether to merge
- Set `PI_REVIEW_MODEL` env var to use a specific model for reviews
