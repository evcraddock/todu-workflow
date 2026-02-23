# Contributing

This project uses an AI-first development process. Agents do the work, automation enforces quality, humans approve.

## Workflow

### 1. Pick Up a Task

Get assigned a task or pick from available tasks. Understand requirements before starting.

### 2. Create a Branch

```bash
git checkout main && git pull
git checkout -b feat/{task-id}-short-description
```

Branch prefixes:
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `chore/` - Maintenance

### 3. Implement

- Follow [CODE_STANDARDS.md](CODE_STANDARDS.md)
- Write tests as you go
- Commit frequently with clear messages

Commit format:
```
<type>: <short description>

Task: #<task-id>
```

### 4. Verify Quality

Before opening a PR:

```bash
./scripts/pre-pr.sh
```

Do not open a PR if this fails.

### 5. Push and Open PR

Push branch and create a PR with a clear description linking to the task.

### 6. Resolve CI Gate (Required)

- If CI checks are available, wait for completion and green status before requesting review.
- If CI fails: fetch failing checks/logs, fix, rerun `./scripts/pre-pr.sh`, push, and wait again.
- If CI status cannot be verified automatically (for example, Forgejo without CI integration): stop and ask the human whether to continue without a CI signal.

### 7. Request Independent Review (Required)

After the CI gate is resolved, run the `request-review` workflow so another agent performs review.

### 8. Report Review Result and Handle Warnings (Required)

Report pipeline state explicitly:

```text
PR Pipeline Status
- local_checks: pass|fail
- push: done|pending
- ci: pass|fail|unavailable-needs-human-decision
- review: pending|approved|warnings|changes-requested
- merge_approval: waiting-human|approved
```

Warning policy:
- If `review=warnings`, list warnings clearly and fix them by default before merge.
- Human can explicitly waive warnings (e.g., "ignore warnings") and proceed.

Do not phrase required next steps as optional (no "want me to...?").

### 9. Merge and Close Task

- Merge only after explicit human approval.
- Never auto-merge.
- Close the task after merge is complete.

## When Stuck

After 3 failed attempts at the same problem:

1. Stop - Don't keep trying the same approach
2. Document - What was tried and why it failed
3. Ask - Request guidance or suggest alternatives
