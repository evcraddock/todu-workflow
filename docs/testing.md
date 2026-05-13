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

## Automated Testing

TODO: Add automated tests for skills.
