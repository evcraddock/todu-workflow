---
name: task-start-preflight
description: Prepare to work on a task. Use when user says "start task", "begin task", "pick up task", or similar.
---

# Task Start Preflight

Run these checks before starting work on any task to ensure proper context and setup.

## When to Use

Before beginning work on a task, run this preflight. Ensures you understand the task, have a clean environment, and follow project conventions.

## Preflight Steps

### 1. Load Task Details

```bash
todu task show <task-id>
```

**Display:**
- Task title and description
- Acceptance criteria (checklist of what "done" looks like)
- Dependencies on other tasks
- Any blocking status or warnings

**If task has dependencies:**
- Check if dependent tasks are complete
- If not, warn: "This task depends on #X which is not complete. Proceed anyway?"

### 2. Check Task Comments

```bash
todu task comments <task-id>
```

**Look for:**
- Prior work or decisions made
- Context from previous sessions
- Blockers that were identified
- Questions that were answered

### 3. Check Project Documentation

Look for project-specific guidelines that apply to this work:

```bash
# Check for AGENTS.md (primary project guidelines)
cat AGENTS.md 2>/dev/null || cat docs/AGENTS.md 2>/dev/null

# Check for contributing guidelines
cat CONTRIBUTING.md 2>/dev/null || cat docs/CONTRIBUTING.md 2>/dev/null

# Check for code standards
cat CODE_STANDARDS.md 2>/dev/null || cat docs/CODE_STANDARDS.md 2>/dev/null
```

**IMPORTANT:** Read and internalize these documents. You MUST follow these guidelines throughout your work on this task.

**Extract and surface:**
- Branching strategy (e.g., create feature branch for PRs)
- PR requirements (reviews, CI checks)
- Testing requirements
- Code style requirements
- Workflow requirements (e.g., how to request reviews)
- Any task-specific conventions

**If branching is required:**
- Note that a feature branch should be created
- Suggest branch name based on task (e.g., `feature/1230-task-start-preflight`)

### 4. Check Git Status

```bash
git status
```

**Check for:**
- Current branch (are we on main?)
- Uncommitted changes
- Untracked files

**If issues found:**
- List the files
- Ask: "There are uncommitted changes. Should I stash them, commit them, or are they related to this task?"

**If project requires PRs and on main:**
- Suggest creating a feature branch
- Propose branch name: `feature/<task-id>-<short-description>`

### 5. Check Dev Environment

If project has a Makefile with `dev-status` target:

```bash
if [ -f Makefile ] && grep -q "dev-status:" Makefile; then
  STATUS=$(make -s dev-status 2>/dev/null)
  echo "Dev environment: $STATUS"
fi
```

**If stopped:**
- Ask: "Dev environment is stopped. Start it? [yes / no / skip]"
- If yes, run `make dev`
- If no or skip, note it and proceed

**If running:**
- Note: "Dev environment is running ✓"

**If no Makefile or no dev-status target:**
- Skip this check silently

**Skip for docs-only tasks:**
- If task title/labels indicate documentation-only work, skip this check

### 6. Understand Context

**Check for related files mentioned in task:**
- If task references specific files, verify they exist
- If task references PRs or issues, note their status

**Check linked source:**
```bash
# If task has external source URL (GitHub issue, etc.)
todu task show <task-id> | grep "Source URL"
```

### 7. Establish the Plan

Summarize for the user:

```
=== Task Start Preflight: Task #<id> ===

Task: <title>

Dependencies: ✅ None | ⚠️ Depends on #X (incomplete)
Git Status: ✅ Clean | ⚠️ <n> uncommitted files
Branch: <current-branch> | 💡 Suggest: feature/<id>-<name>
Dev Environment: ✅ Running | ⚠️ Stopped | ⏭️ N/A

Project Requirements:
- <relevant guidelines from CONTRIBUTING.md>
- <relevant standards from CODE_STANDARDS.md>

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- ...

🧪 Testing: Each acceptance criterion should have a corresponding test.
   (Skip for docs-only tasks)

Plan:
1. <Step 1>
2. <Step 2>
...

Ready to proceed? [yes / modify plan]
```

**Testing Reminder:** For non-documentation tasks, each acceptance criterion should be verified by an automated test, not just manual checking. Plan to write tests as you implement each criterion.

## After Approval

Once user confirms, **do all of these before starting work**:

### 1. Update Task Status

**REQUIRED:** Mark the task as in progress:

```bash
todu task update <task-id> --status inprogress
```

### 2. Create Feature Branch

If project requires PRs:

```bash
git checkout -b feature/<task-id>-<short-description>
```

### 3. Begin Work

Start on first acceptance criterion.

## Example Flow

**User:** "Start task 1230"

**Agent:**
```
Running preflight for Task #1230...

=== Task Details ===
Task #1230: Create task-start-preflight skill
Priority: medium
Project: dotfiles

Dependencies: None

=== Task Comments ===
No prior comments.

=== Project Documentation ===
No CONTRIBUTING.md found.
No CODE_STANDARDS.md found.

=== Git Status ===
⚠️ On branch: main
⚠️ 3 modified files (unrelated to task)

💡 Recommend: Create feature branch for this work

=== Dev Environment ===
✅ Running (overmind)

=== Acceptance Criteria ===
- [ ] Skill file created at ~/.local/dotfiles/common/ai-assistant/skills/task-start-preflight/SKILL.md
- [ ] ~/Private/code/.pi/skills/ directory created
- [ ] Symlink created: ~/Private/code/.claude/skills/task-start-preflight
- [ ] Symlink created: ~/Private/code/.pi/skills/task-start-preflight
- [ ] Covers all preflight steps
- [ ] Checks for CONTRIBUTING.md and CODE_STANDARDS.md
- [ ] Follows same pattern as task-close-preflight
- [ ] Includes example flow
- [ ] Documents when to skip checks

=== Plan ===
1. Create feature branch: feature/1230-task-start-preflight
2. Create skill file following task-close-preflight pattern
3. Create symlinks for .claude and .pi
4. Commit and prepare for merge

Ready to proceed? [yes / modify plan]
```

## When to Skip

Some checks can be skipped:

- **Continuation of prior work**: If resuming work in same session, skip full preflight
- **Trivial tasks**: For very small tasks, abbreviated preflight is okay
- **No project docs**: If project has no CONTRIBUTING.md, just note it and proceed

## Notes

- Always run preflight when starting a new task
- The goal is context and clarity, not bureaucracy
- If dependencies are incomplete, get explicit approval to proceed
- Feature branches keep main clean and enable proper PR review
