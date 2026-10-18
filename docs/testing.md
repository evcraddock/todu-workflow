# Testing todu-workflow Skills

This document describes how to test the skills in this repository.

## Manual Testing

### Skill Routing Evals

Use [skill-evals.md](skill-evals.md) after changing skill descriptions, trigger wording, or routing-sensitive skill bodies.

Run the prompt matrix manually in a fresh agent context when practical. Record whether the expected skill or fallback was selected, whether the expected outcome happened, and whether any nearby skill over-triggered. Repeat high-risk prompts a few times because routing can vary between runs.

When an eval fails, fix the relevant skill description first. Change the skill body only when the description is already clear and the loaded instructions are the problem.

### Task Authoring

Use the fixtures and inspection criteria in [Task Authoring Evaluation](evals/task-authoring.md) to test faithful intent capture, preservation of explicit constraints, unapproved suggestions, short tasks, incomplete bug reports, and draft/create/pickup boundaries. Repeat in three fresh contexts with no live writes. Inspect actual drafts; do not treat static checks or the calendar CLI tests as evidence of model compliance.

### Task Lifecycle

Recorded dry-run fixtures, invocation details, results, and limitations are in [Task Lifecycle Evaluation](evals/task-lifecycle.md).

Use E06-E09 and E30-E41 in [skill-evals.md](skill-evals.md) to evaluate the shared task-perform lifecycle. Supply controlled task/project state and mocked tool outcomes in a fresh context; require a proposed tool/action trace only, with no real task, Git, or external writes. Include active and resumed tasks, terminal status, failed/uncertain writes, incomplete verification, non-repository deliverables, and explicit merge/review gates. Repeat high-risk cases at least three times. Record the model, loaded skill versions, verdict, and observed ordering; static document checks alone do not establish model compliance.

Expected write ordering is confirmed inprogress, starting/resuming comment, meaningful work updates, assessment-only completion verification, confirmed completion comment, then done. Existing inprogress status does not require a redundant update. A failed start/comment or an unsatisfied project gate must prevent the corresponding later work/closure. Report limitations honestly if fresh-context behavioral evaluations cannot be run.

### Task Pipeline Development Reference

Use [Task Pipeline Evaluation](evals/task-pipeline.md) to evaluate the complete development reference together with the lifecycle/readiness/completion skills. Cover do/work-on/pickup equivalence, tiny tracked changes, explicit alternative policy, policy conflicts, planning requirements, chat/backend/untracked versus committed results, failed gates, independent review, human merge approval, and current-session completion handoff. Use controlled no-write proposals in three fresh contexts, not real task or repository writes; distinguish author verification from independent review and report simulation limits.

### Task Comments

Use [Task Comment Evaluation](evals/task-comments.md) for direct drafting versus authorized posting, factual/proportional content, evidence limitations, missing identity, lifecycle ordering, both review hosts, and partial posting failures. Repeat in three fresh no-write contexts with the active repository skill catalog and native schemas. Verify simple updates need neither a generic template nor an authoring-skill handoff, drafts do not write, authorized workflow posts do not acquire a new default approval gate, and comment-only requests do not start or close tasks.

### Task Start Preflight

Use [Task Start Preflight Evaluation](evals/task-start-preflight.md) for the shared read-only readiness contract. Cover active/resumed/terminal/waiting tasks, genuinely missing intent versus pickup details, direct cross-project lookups, incomplete/cancelled/missing/failed dependencies, unresolved references, and standalone-versus-execution ownership. Repeat controlled no-write simulations in three fresh contexts. Inspect proposed calls and actual concise responses; no-tool simulations do not validate live tool behavior or automatic discovery.

### Next Actions

Use [Next Actions Evaluation](evals/nextactions.md) for the four native selections, duplicate IDs, due-date/nulls-last ordering, scheduled-only context, intentionally excluded backlog, successful emptiness versus partial/all failures, portable sequential fallback, project/timezone consistency, unavailable detail fields, and read-only behavior. Repeat in three fresh no-write contexts with supplied schemas and mocked results. Inspect actual output and proposed calls; simulations do not validate live native return shapes, automatic discovery, or measured batching latency. Keep the optional codemode pilot separate.

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

Use [PR Review Evaluation](evals/pr-review.md) for controlled no-write scenarios covering plain outcomes and formal criteria, relevant context/targeted checks, supported blockers versus uncertainty and suggestions, explicit GitHub/Forgejo routing, independent review availability, self-review labeling, partial posting failures, stale revisions, and the prohibition on remediation/merge. Supply all four review documents in three fresh contexts; inspect proposed actions and actual reports, not just static wording. Report simulation limits and distinguish author checks from independent PR review.

For an authorized live review, use `review PR #<number> for task <task-id>` on a known open PR. Verify that the fresh reviewer assesses the correct revision, the matching host command posts the PR artifact, native `task_comment_create` posts the linked-task summary, and both are confirmed with accurate references/statuses. The report must preserve evidence and limitations, stop before remediation/merge, and leave human merge approval outstanding. No tmux wrapper, marker-delimited output, mandatory criteria counts, or separate comment-authoring handoff is required. Test write failures with mocks rather than deliberately creating duplicate or broken live artifacts.

### Task Close Gate and Closure-only Requests

Use [Task Close Gate Evaluation](evals/task-close-gate.md) with complete verifier/caller skills, explicit mock evidence, native input schemas, and no live writes. Repeat in three fresh contexts. Cover outcomes without formal sections, supported versus unsupported/stale evidence, missing/partial completion, artifact reuse, targeted permitted checks and failures, outstanding project gates, and verification-only versus explicit/automatic closure.

The verifier returns only a concise assessment and evidence; it never posts comments, changes status, launches tmux, implements missing work, or initiates another PR review. For authorized closure, task-perform uses its closure-only path or existing execution completion path, confirms the completion comment via native task_comment_create before task_update(done), and accurately handles failures. Explicit close requests must not start preflight, set inprogress, or post starting comments. Verification-only requests must not write or imply actual closure. Check these ownership/order boundaries rather than requiring a rigid report or redundant tests.

## Automated Testing

TODO: Add automated tests for skills.
