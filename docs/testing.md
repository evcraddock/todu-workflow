# Testing todu-workflow Skills

This document describes how to test the skills in this repository.

## Manual Testing

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

### request-review Skill

To test the full review flow:

1. Create a PR in any project
2. Run: `request review for PR #<number>`
3. Verify:
   - Review session spawns in tmux
   - Calling agent blocks until review completes
   - Review comment is fetched and displayed

## Automated Testing

TODO: Add automated tests for skills.
