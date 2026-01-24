---
name: task-close-preflight
description: Verify work is complete before closing a task. Use before "close task", "complete task", "mark task as done", or similar.
---

# Task Close Preflight

Run these checks before closing any task to ensure work is complete.

## When to Use

Before closing a task, run this preflight. Do not close until all checks pass or issues are acknowledged.

## Preflight Steps

### 1. Check Git Status

```bash
git status
```

**Check for:**
- Uncommitted changes (modified files)
- Untracked files that should be committed
- Staged but uncommitted changes

**If issues found:**
- List the files
- Ask user: "These files are uncommitted. Should I commit them, or are they unrelated to this task?"
- Commit related files before proceeding
- Note unrelated changes in closing comment

### 2. Verify Acceptance Criteria

```bash
todu task show <task-id>
```

**For each acceptance criterion in the task:**
1. State the criterion
2. Verify it was completed
3. Note the evidence (file created, test passing, etc.)

**Format:**
```
Checking acceptance criteria for Task #<id>:

- [ ] Criterion 1: <text>
  └─ Status: ✅ Complete | ⚠️ Partial | ❌ Incomplete | 🚫 Blocked
  └─ Evidence: <file, commit, or explanation>

- [ ] Criterion 2: <text>
  └─ Status: ...
```

**If incomplete items found:**
- Ask user: "This criterion is not complete. Should we complete it first, mark as blocked, or close anyway?"
- Do not close with incomplete criteria unless explicitly approved

### 3. Check Related Artifacts

**If code was changed:**
- Were tests added or updated?
- Do tests pass? (`npm test` or equivalent)

**If behavior changed:**
- Was documentation updated?
- Were CHANGELOG entries added (if project uses one)?

**If project requires PRs:**
- Is there a merged PR for this work?
- Or is this preparatory work before a PR?

### 4. Prepare Closing Comment

Generate a summary comment that includes:

```markdown
## Summary
<Brief description of what was accomplished>

## Changes Made
- <Change 1>
- <Change 2>

## Decisions
- <Any decisions made during implementation>

## Follow-up
- <Any related work identified but not done>
- <Any blockers or dependencies noted>
```

### 5. Final Confirmation

Present summary to user:

```
=== Task Close Preflight: Task #<id> ===

Git Status: ✅ Clean | ⚠️ <n> uncommitted files
Acceptance Criteria: ✅ <n>/<n> complete | ⚠️ <n> incomplete
Artifacts: ✅ All present | ⚠️ Missing <x>

Proposed closing comment:
---
<comment>
---

Proceed with close? [yes / no / edit comment]
```

## After Approval

Once user confirms:

```bash
todu task close <id>
todu task comment <id> -m "<closing comment>" --format json
```

## Example Flow

**User:** "Close task 1223"

**Agent:**
```
Running preflight for Task #1223...

=== Git Status ===
✅ Working tree clean

=== Acceptance Criteria ===
✅ CONTRIBUTING.md created - docs/CONTRIBUTING.md exists
✅ CODE_STANDARDS.md created - docs/CODE_STANDARDS.md exists  
✅ PR template created - .github/PULL_REQUEST_TEMPLATE.md exists
🚫 Test with first task - blocked until #1214 complete

=== Artifacts ===
✅ Documentation updated
ℹ️ No code changes requiring tests

=== Proposed Comment ===
## Summary
Created AI-first development process documentation.

## Changes Made
- docs/CONTRIBUTING.md - process rules for agents
- docs/CODE_STANDARDS.md - code quality standards
- .github/PULL_REQUEST_TEMPLATE.md - PR checklist

## Decisions
- CI pipeline moved to separate task #1224
- Agent review skill moved to task #1225

## Follow-up
- Task #1214 must complete to validate process
- Blocked criterion will be verified when process is tested

---

Proceed with close? [yes / no / edit]
```

## Notes

- Always run preflight, even for small tasks
- Err on the side of asking rather than assuming
- Blocked criteria are okay if noted in comment
- The goal is quality, not bureaucracy
