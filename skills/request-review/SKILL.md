---
name: request-review
description: Request a PR review from a separate agent session. Use immediately after creating a PR, or when user says "request review", "get this reviewed", etc.
---

# Request Review

Spawn a separate agent session in a new tmux window to review a PR. This ensures the reviewer has fresh context and no implementation bias.

## When to Use

After creating a PR and confirming CI passes, use this to request an independent review.

## Prerequisites

- tmux installed (uses the tmux skill for session management)
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

## Configuration

### Model

Determine the review model in this order:

1. **User request** — If user says "review with claude-sonnet", "use opus for review", etc., use that
2. **Project config** — Check AGENTS.md for a `review-model` preference
3. **Default** — Omit `--model` flag (uses pi's default)

### Visibility

The review session can be **visible** (user can watch) or **detached** (runs in background).

Determine visibility in this order:

1. **User request** — If user says "review visibly", "review in background", "watch the review", etc., use that
2. **Project config** — Check AGENTS.md for a `review-visibility` preference (visible/detached)
3. **Default** — If neither specified, use **visible**

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

### 5. Spawn Review Session

Use the **tmux skill** to create a session for the review agent.

The command to run:

```
cd $PROJECT_PATH && pi $MODEL_FLAG -p "Review PR #<number> (Task #<task-id>) using the pr-review skill. Post review to PR and task, then exit."
```

Use the tmux skill's **run and capture** pattern:
1. Determine visibility (see Configuration above)
2. Start session with `--visible` or `--detached`
3. Wait for completion (session ends when pi exits)
4. If visible, window closes automatically

### 6. Check Review Results

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

Spawning review session (using tmux skill)...
Opened visible session 'pr-review-17-a3f9'

Waiting for review to complete...
```

*[Review agent runs in visible tmux window. User can watch.]*

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
