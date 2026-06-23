# Testing todu-workflow Skills

This document describes how to test the skills in this repository.

## Manual Testing

### Skill Routing Evals

Use [skill-evals.md](skill-evals.md) after changing skill descriptions, trigger wording, or routing-sensitive skill bodies.

Run the prompt matrix manually in a fresh agent context when practical. Record whether the expected skill or fallback was selected, whether the expected outcome happened, and whether any nearby skill over-triggered. Repeat high-risk prompts a few times because routing can vary between runs.

When an eval fails, fix the relevant skill description first. Change the skill body only when the description is already clear and the loaded instructions are the problem.

### tmux wait-for Signaling

Test the wait-for pattern used for inter-agent communication:

```bash
cd ~/.pi/agent/skills/todu-workflow/tmux

SOCKET="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}/claude.sock"

# Start a test session
OUTPUT=$(./scripts/start-session.sh -s test-waitfor --detached)
SESSION=$(echo "$OUTPUT" | grep "Created session" | sed "s/Created session '\([^']*\)'.*/\1/")
CHANNEL="test-done-$SESSION"

# Send command with signal
tmux -S "$SOCKET" send-keys -t "$SESSION" \
  "echo 'Working...'; sleep 2; echo 'Done!'; tmux -S $SOCKET wait-for -S $CHANNEL" Enter

# Wait for signal (blocks until complete)
timeout 10 tmux -S "$SOCKET" wait-for "$CHANNEL"
echo "Exit code: $?"

# Cleanup
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

### pr-review Skill

To test the full review flow:

1. Create a PR in any project
2. Run: `review PR #<number> for task #<task-id>`
3. Verify:
   - Review comment is posted to the PR
   - Review comment is posted to the task via `task-comment-create`
   - Agent reports review outcome and waits for explicit merge approval

When testing through the tmux sub-agent wrapper, use a small PR and the wrapper's 120-second timeout. Verify that the review follows the bounded checklist, uses `task-comment-authoring` only for concise artifact drafting, posts both required comments, emits the marker-delimited `PR Review Status`, signals completion immediately, and does not continue with extra exploration after the verdict.

### task-close-gate Skill

To test close-gate behavior:

1. Use a task with clear acceptance criteria and existing completion evidence in task comments or a referenced merged PR.
2. Run: `verify and close task #<task-id>`.
3. Verify:
   - Each acceptance criterion is marked `met`, `partial`, or `missing` with explicit evidence
   - The task is marked done only when all criteria are met
   - A closing task comment is posted via `task-comment-create`

When testing through the tmux sub-agent wrapper, use the wrapper's 120-second timeout. Verify that the close gate follows the bounded checklist, uses only bounded evidence sources, emits the marker-delimited close-gate result, signals completion immediately after the closing update or `BLOCKED` decision, and does not invoke unrelated skills or continue exploratory checks.

## Automated Testing

TODO: Add automated tests for skills.
