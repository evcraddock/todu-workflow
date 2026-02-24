---
name: request-review
description: Request a PR review from a separate agent session. Use immediately after creating a PR, or when user says "request review", "get this reviewed", etc.
---

# Request Review

Spawn a separate agent session in a new tmux window to review a PR. This ensures the reviewer has fresh context and no implementation bias.

## Position in Mandatory PR Pipeline

This skill is **step 4** in the required post-PR sequence:

1. Run `./scripts/pre-pr.sh`
2. Push branch
3. Resolve CI gate (green, or explicit human decision when CI cannot be verified)
4. Run `request-review` (this skill)
5. Report review result
6. Stop and wait for explicit human merge approval

Do not skip or reorder these steps.

## Hard Rules

- Do **not** run this skill before step 3 (CI gate) is resolved.
- Do **not** phrase mandatory next steps as optional (no "want me to...?").
- Do **not** merge a PR in this skill. Stop after reporting review status and wait for explicit human approval.
- Do **not** report review completion until reviewer tmux session cleanup is verified (`kill-session` executed and session absence confirmed).

## Prerequisites

- tmux installed (uses the tmux skill for session management)
- PR exists
- Current directory is the project root
- CI gate must be resolved before spawning review:
  - checks available: green required
  - checks unavailable: explicit human decision required
  - this skill enforces that gate in Step 3

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
| View PR body | `gh pr view <num> --json body` | `zsh -ic "fj pr view <num> body"` |
| View PR comments | `gh pr view <num> --json comments` | `zsh -ic "fj pr view <num> comments"` |
| Comment on PR | `gh pr comment <num> --body "..."` | `zsh -ic "fj pr comment <num> '...'"` |
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
- PR is open

### 3. Enforce CI Gate (Required Before Review)

#### 3a) If check runs are available (GitHub)

Wait for completion and require green:

```bash
gh pr checks <number> --watch
```

Expected result:
- Success path: all checks report pass/success
- Failure path: at least one check reports fail/error/cancelled

If checks fail, run the required failure loop:

```bash
# 1) Show failing checks
gh pr checks <number> --json name,state,link \
  --jq '.[] | select(.state == "FAILURE" or .state == "ERROR" or .state == "CANCELLED") | "\(.name): \(.state) -> \(.link)"'

# 2) Fix code locally, then rerun local gate
./scripts/pre-pr.sh

# 3) Push fix
git push

# 4) Re-wait CI
gh pr checks <number> --watch
```

Expected status progression:
- `ci=fail` with failing check names/links
- `local_checks=pass` after fixes
- `ci=pass` after re-push

#### 3b) If CI cannot be verified automatically (example: Forgejo without CI integration)

Do **not** assume pass/skip. Ask the human and wait for explicit choice:

- Continue without CI signal
- Wait for human CI verification
- Stop

Only proceed when the human explicitly selects one.

### 4. Extract Task ID

Parse the task ID from the PR body:

**GitHub:**
```bash
gh pr view <number> --json body --jq '.body' | grep -oP 'Task:?\s*#?\K\d+' | head -1
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number>" | grep -oP 'Task:?\s*#?\K\d+' | head -1
```

### 5. Get Project Path

```bash
PROJECT_PATH=$(pwd)
```

### 6. Spawn Review Session

Use the **tmux skill** to create a session for the review agent.

#### Determine Agent CLI

1. If `$CODING_AGENT_CMD` is set, use it
2. Otherwise, use your own CLI (you know what agent you're running in from your system prompt — e.g., `pi`, `claude`, etc.)

#### Start the session with the review command

Generate the channel name and start the session:

```bash
SOCKET="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}/claude.sock"

# Use PR number for channel (simple, predictable)
SESSION_BASE="pr-review-<number>"
CHANNEL="review-done-<number>"

# Build prompt with signal command included
SIGNAL_CMD="tmux -S $SOCKET wait-for -S $CHANNEL"
REVIEW_PROMPT="Review PR #<number> (Task #<task-id>) using the pr-review skill. Post review to PR and task. When completely done, run this bash command to signal completion: $SIGNAL_CMD"

REVIEW_CMD="cd $PROJECT_PATH && $AGENT_CMD $MODEL_FLAG \"$REVIEW_PROMPT\""

# Start session - script adds its own suffix to session name
OUTPUT=$(./scripts/start-session.sh -s "$SESSION_BASE" -c "$REVIEW_CMD" --visible)

# Parse actual session name from output for cleanup later
SESSION=$(echo "$OUTPUT" | grep "Created session" | sed "s/Created session '\([^']*\)'.*/\1/")
```

The reviewing agent runs the signal command when it finishes, notifying the calling agent.

### 7. Wait for Review Completion

Block until the review agent finishes:

```bash
# Wait up to 10 minutes for review to complete
timeout 600 tmux -S "$SOCKET" wait-for "$CHANNEL"
WAIT_EXIT=$?

if [ $WAIT_EXIT -eq 124 ]; then
  echo "Review timed out after 10 minutes"
elif [ $WAIT_EXIT -ne 0 ]; then
  echo "Review session ended unexpectedly"
fi

# Cleanup is mandatory. Do not report completion until verified.
tmux -S "$SOCKET" kill-session -t "$SESSION"
KILL_EXIT=$?

LIST_OUTPUT=$(tmux -S "$SOCKET" list-sessions 2>&1)
if [ $KILL_EXIT -ne 0 ] && ! echo "$LIST_OUTPUT" | grep -q "no server running"; then
  echo "Failed to close review session: $SESSION"
  exit 1
fi

if echo "$LIST_OUTPUT" | grep -Fq "$SESSION:"; then
  echo "Cleanup verification failed: session still open ($SESSION)"
  exit 1
fi

if [ $WAIT_EXIT -ne 0 ]; then
  echo "Review did not complete successfully"
  exit 1
fi
```

**Important:** The `$SESSION` variable must be the actual session name parsed from `start-session.sh` output, not a pre-computed name. The script always adds its own random suffix.

**Completion gate:** Review is only complete after all three are true: PR comment posted, task comment posted (if task exists), and tmux review session cleanup verified.

Tell the user you're waiting:
```
Waiting for review to complete...
```

### 8. Check Review Results and Stop at Merge Gate

After wait and cleanup verification complete, fetch the review comment:

**GitHub:**
```bash
gh pr view <number> --json comments --jq '.comments[-1].body'
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number> comments" | tail -50
```

Report the review findings and handle by outcome:
- If approved: report approval and wait for explicit human merge approval
- If warnings: list warnings clearly and **fix them by default**, then re-run the mandatory pipeline from local checks
  - If the human explicitly says to ignore/waive warnings, skip fixes and proceed to merge approval gate
- If changes requested: report blocking issues, fix them, then re-run the mandatory pipeline from local checks

## Agent Output Contract (Required)

Use this status block when reporting progress:

```text
PR Pipeline Status
- local_checks: pass|fail
- push: done|pending
- ci: pass|fail|unavailable-needs-human-decision
- review: pending|approved|warnings|changes-requested
- review_session_cleanup: pending|pass|fail
- merge_approval: waiting-human|approved
```

Rules:
- Do not skip fields
- Do not phrase required next steps as optional
- If `review=warnings`, fix warnings by default; proceed without fixes only after explicit human waiver ("ignore warnings")
- Do not report completion while `review_session_cleanup` is `pending` or `fail`
- Never merge without explicit human approval

## Example Flow

**User:** "Request a review for PR 17"

**Agent (GitHub):**
```
Detecting host... GitHub
Checking PR #17...
✓ PR exists: "docs: add README with project overview"

CI gate: waiting for checks...
✓ CI passed
✓ Task ID: #1232

Spawning review session (using tmux skill)...
Opened visible session 'pr-review-17-a3f9'

Waiting for review to complete...
```

*[Review agent runs in visible tmux window. User can watch.]*

**Agent (Forgejo without CI checks):**
```
Detecting host... Forgejo
Checking PR #17...
✓ PR exists: "docs: add README with project overview"

CI status cannot be verified automatically on this host.
Choose how to proceed:
1) Continue without CI signal
2) Wait for your manual CI verification
3) Stop
```

After user chooses 1:
```
Proceeding without CI signal (explicit human decision).
✓ Task ID: #1232

Spawning review session (using tmux skill)...
Opened visible session 'pr-review-17-a3f9'

Waiting for review to complete...
```

After review (approved):
```
Review complete.

## Code Review: Approved ✅

PR Pipeline Status
- local_checks: pass
- push: done
- ci: unavailable-needs-human-decision (human chose continue)
- review: approved
- review_session_cleanup: pass
- merge_approval: waiting-human

Waiting for your explicit merge approval.
```

After review (warnings):
```
Review complete.

## Code Review: Warnings ⚠️

Warnings:
1. docs/WORKFLOW.md:120 - Wording is ambiguous around CI gate fallback.
2. skills/request-review/SKILL.md:260 - Add explicit retry limit guidance.

PR Pipeline Status
- local_checks: pass
- push: done
- ci: pass
- review: warnings
- review_session_cleanup: pass
- merge_approval: waiting-human

Default action is to fix warnings before merge. I will proceed with fixes now.
If you want to waive warnings and merge anyway, explicitly say "ignore warnings".
```

## Notes

- Reviewer agent starts fresh with no context from this session
- Reviewer uses `pr-review` skill which has its own checklist
- Review is posted as both a PR comment and a task comment
- Uses `tmux wait-for` signaling to know when review completes (no polling)
- Requires tmux session cleanup verification (`kill-session` + absence check) before completion
- 10 minute timeout prevents hanging if session crashes
- Set `CODING_AGENT_CMD` env var to override the agent CLI (e.g., `export CODING_AGENT_CMD=claude`)
