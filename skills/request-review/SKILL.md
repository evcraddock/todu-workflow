---
name: request-review
description: Request a PR review from a separate agent session. Use immediately after creating a PR, or when user says "request review", "get this reviewed", etc.
---

# Request Review

Run an independent PR review in a separate tmux-backed agent session, then report the result and stop at the human merge-approval gate.

## Position in Mandatory PR Pipeline

This is **step 4**:
1. `./scripts/pre-pr.sh`
2. Push branch
3. Resolve CI gate
4. Run `request-review` (this skill)
5. Report review result
6. Wait for explicit human merge approval

Do not skip or reorder.

## Invariants (Hard Rules)

- Do not run before CI gate is resolved.
- Do not merge in this skill.
- **No simulated waiting:** do not say "waiting" unless a real blocking wait command is already running.
- Do not report completion until all required proof is present:
  1) PR review comment posted
  2) task comment posted (if task ID exists)
  3) tmux wait executed and returned success
  4) tmux cleanup executed and session absence verified

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

## Configuration Precedence

Use this precedence for model, visibility, and CI-unavailable behavior:

`user request > project AGENTS.md preference > default`

Defaults:
- model: omit `--model` (agent default)
- visibility: `--visible`
- ci-unavailable behavior: ask human (unless a standing policy is documented in AGENTS.md)

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
- If failed: show failures, fix, rerun `./scripts/pre-pr.sh`, push, re-wait.

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

Set:
```bash
PROJECT_PATH=$(pwd)
SOCKET="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}/claude.sock"
SESSION_BASE="pr-review-<number>"
CHANNEL="review-done-<number>"
```

### 4) Spawn Reviewer Session

- Use `$CODING_AGENT_CMD` if set; otherwise use the current agent CLI.
- Build reviewer prompt instructing reviewer to:
  - run `pr-review`
  - post PR comment
  - post task comment when task ID exists
  - signal completion: `tmux -S $SOCKET wait-for -S $CHANNEL`

Start session (respect effective visibility):
```bash
# VISIBILITY_FLAG is --visible or --detached from config precedence
OUTPUT=$(./scripts/start-session.sh -s "$SESSION_BASE" -c "$REVIEW_CMD" $VISIBILITY_FLAG)
SESSION=$(echo "$OUTPUT" | grep "Created session" | sed "s/Created session '\([^']*\)'.*/\1/")
```

### 5) Start Real Blocking Wait (Required)

Run the wait command first:
```bash
timeout 600 tmux -S "$SOCKET" wait-for "$CHANNEL"
WAIT_EXIT=$?
```

Only after this command starts may you report "Waiting for review to complete...".

Exit handling:
- `WAIT_EXIT=0`: reviewer signaled completion
- `WAIT_EXIT=124`: timeout
- otherwise: wait error/interruption

### 6) Mandatory Cleanup (Always)

Run cleanup regardless of wait outcome:
```bash
tmux -S "$SOCKET" kill-session -t "$SESSION"
KILL_EXIT=$?
LIST_OUTPUT=$(tmux -S "$SOCKET" list-sessions 2>&1)
```

Verification rules:
- Fail if session still appears in `LIST_OUTPUT`.
- If `kill-session` fails and server is still running, fail.

### 7) Verify Review Artifacts

After successful wait + cleanup verification:
- Verify PR review comment exists (fetch latest PR comments).
- If task ID exists, verify task contains review comment entry (for example `PR Review for #<number>` in `todu task show <task-id>` output).
- If `WAIT_EXIT != 0`, treat run as failed even if comments exist.

### 8) Report Outcome and Stop at Merge Gate

Outcomes:
- `approved`: report approval, wait for explicit human merge approval
- `warnings`: list warnings; fix by default; only skip fixes if human explicitly waives
- `changes-requested`: fix and restart pipeline from local checks

Never merge inside this skill.

## ACTION_PROOF (Required)

Do not claim completion without evidence for all applicable items:

1. **review_wait**
   - wait command executed (exact command)
   - channel name
   - exit code
2. **pr_review_comment**
   - command used to fetch comments
   - evidence latest review comment was posted
3. **task_review_comment** (when task ID exists)
   - command used to check task
   - evidence review comment exists on task
4. **tmux_cleanup**
   - `kill-session` executed
   - absence verified with `list-sessions`

If any required proof is missing or fails, status is not complete.

## Agent Output Contract (Required)

```text
PR Pipeline Status
- local_checks: pass|fail
- push: done|pending
- ci: pass|fail|unavailable-needs-human-decision
- review: pending|approved|warnings|changes-requested
- review_wait: pending|pass|fail
- review_session_cleanup: pending|pass|fail
- merge_approval: waiting-human|approved
```

Rules:
- Do not skip fields.
- Do not phrase required next steps as optional.
- If `ci=unavailable-needs-human-decision`, either apply a documented standing policy or obtain explicit per-PR human decision before review starts.
- Do not report completion while `review_wait` or `review_session_cleanup` is `pending|fail`.
- Never merge without explicit human approval.

## Notes

- Reviewer runs in a separate tmux-backed process for isolation.
- Use `tmux wait-for` signaling for synchronization (not output polling).
- Timeout is required to avoid indefinite hangs.
- Cleanup is a hard gate, not best-effort.
