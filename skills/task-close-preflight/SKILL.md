---
name: task-close-preflight
description: Verify work is complete before closing a task. Use when user says "close task", "complete task", "finish task", "verify and close", or similar.
---

# Task Close Preflight

Run these checks before closing any task to ensure work is complete.

## When to Use

Before closing a task, run this preflight. Do not close until all checks pass or issues are acknowledged.

## Autonomy Thresholds (Required)

Default behavior for this preflight is **act without prompting** for deterministic, reversible checks.

**Auto-continue (no prompt):**
- Documentation-only/config-only skip paths
- Missing optional local setup needed for log checks (for example, no `Makefile`/`dev-status`)
- Dev server not running (skip log inspection and record it)

**Prompt required (human decision gate):**
- Closing with incomplete acceptance criteria
- Overriding failing quality gates (for example, missing tests or unresolved runtime errors)
- Irreversible/destructive actions

Do not ask yes/no questions for routine status reporting.

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
- List the files.
- If relation to the task is obvious, proceed with the obvious path and report it.
- If relation is unclear, ask: "These uncommitted changes may conflict with closing this task. Should I commit them now, or treat them as unrelated?"
- Commit related files before proceeding.
- Note unrelated changes in closing comment.

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

### 3. Check Tests

**Skip this step if:**
- Task is documentation-only (no code with logic)
- Task is configuration-only (no testable behavior)

**Check for new/modified test files:**
```bash
# Check for test files in staged or recent commits
git diff --name-only HEAD~5 | grep -E '\.(test|spec)\.(ts|js|py|go)$' || echo "No test files changed"
```

**If code was changed but no tests added:**
- Warn: "⚠️ Code changes detected but no test files added/modified"
- Default action: stop preflight and require one of the following before closing:
  1. Add tests, or
  2. Provide explicit human-approved rationale for why tests are not needed (for example, "refactor only, existing tests cover this").

**If tests exist, verify they pass:**
```bash
npm test  # or equivalent for project
```

**Acceptable reasons to skip tests:**
- Pure refactoring with existing test coverage
- Configuration changes (env vars, build settings)
- Documentation-only changes
- Skill/template files (no runtime code)

### 4. Check Other Artifacts

**If behavior changed:**
- Was documentation updated?
- Were CHANGELOG entries added (if project uses one)?

**If project requires PRs:**
- Is there a merged PR for this work?
- Or is this preparatory work before a PR?

### 5. Check Application Logs

Check dev server logs for runtime errors that tests might miss.

**Skip this step if:**
- Task is documentation-only (no code changes)
- Project has no dev server / Makefile

**Check if dev server is running:**
```bash
if [ -f Makefile ] && grep -q "dev-status:" Makefile; then
  STATUS=$(make -s dev-status 2>/dev/null)
  if [ "$STATUS" != "running" ]; then
    echo "Dev server not running"
  fi
fi
```

**If dev server not running:**
- Warn: "⚠️ Dev server not running - skipping log check"
- Default action: continue without starting dev server.
- Note in closing comment that logs were not checked.

**Check for errors in logs:**
```bash
make dev-tail 2>&1 | grep -iE "(error|warn|exception)" | head -20
```

**If errors found:**
- Warn: "⚠️ Found errors in application logs:"
- Show the matching log lines (up to 20).
- Default action: stop preflight and fix issues before close.
- Prompt only for explicit override. If user wants to proceed anyway, require explanation to include in PR/task notes.

**If no errors:**
- Show: "✅ No errors in logs"
- Proceed to next step

### 6. Prepare Closing Comment

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

### 7. Final Confirmation

Present summary to user:

```
=== Task Close Preflight: Task #<id> ===

Git Status: ✅ Clean | ⚠️ <n> uncommitted files
Acceptance Criteria: ✅ <n>/<n> complete | ⚠️ <n> incomplete
Tests: ✅ All passing | ⚠️ <n> failing | ⏭️ N/A
Logs: ✅ No errors | ⚠️ <n> errors found | ⏭️ Skipped
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

Then immediately suggest next work using `todu`.

### Next Task Suggestions (Required)

1. Get the task's project ID from `todu task show <id>`.
2. Query remaining **active** tasks in this project by priority:

```bash
todu task list --project <project-id> --status active --priority high
todu task list --project <project-id> --status active --priority medium
todu task list --project <project-id> --status active --priority low
```

3. Build a combined shortlist in this strict order:
   - High priority first
   - Then medium
   - Then low
4. Show at most 5 tasks.
5. If at least one task is listed, ask whether to pick up the first task now.

**Output format:**

```text
Next up (top 5):
1. #<id> <title> [high|medium|low]
2. ...

Pick up #<first-id> now? [yes / no]
```

If user says yes, run `task-start-preflight` for that task.

If no active tasks remain in the project, send:

```text
🎉 Congratulations — no active tasks left in this project. You're a badass.
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

=== Application Logs ===
⏭️ Skipped - documentation-only task

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

**User:** "yes"

**Agent:**
```text
Task #1223 closed.

Next up (top 5):
1. #1301 Add CI pipeline status gate to pr-review [high]
2. #1298 Add integration tests for task-start-preflight [high]
3. #1277 Improve PR review severity docs [medium]
4. #1264 Add examples for project-init questionnaire [medium]
5. #1214 End-to-end workflow validation task [low]

Pick up #1301 now? [yes / no]
```

If none remain:

```text
🎉 Congratulations — no active tasks left in this project. You're a badass.
```

### Example: Errors Found in Logs

**Agent:**
```
=== Application Logs ===
⚠️ Found errors in application logs:

  [ERROR] 2026-01-27 10:23:45 - Failed to connect to database
  [WARN]  2026-01-27 10:23:46 - Retrying connection (attempt 2/3)
  [ERROR] 2026-01-27 10:23:47 - Database connection timeout

Default action: stop preflight and fix these before close.
If you want to override and proceed anyway, provide explicit rationale to include in PR/task notes.
```

**User:** "override - these are from my local db being down, not related to code changes"

**Agent:**
```
Recorded override rationale and including it in PR/task notes:
> Logs showed database connection errors - confirmed unrelated to code changes (local db was down)

Continuing preflight with human-approved override.
```

## Notes

- Always run preflight, even for small tasks
- Default to autonomous progress for reversible, deterministic checks
- Ask only at ambiguity, irreversible actions, or explicit policy override gates
- Blocked criteria are okay if noted in comment
- The goal is quality, not bureaucracy
