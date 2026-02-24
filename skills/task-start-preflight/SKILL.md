---
name: task-start-preflight
description: Prepare to work on a task. Use when user says "start task", "begin task", "pick up task", or similar.
---

# Task Start Preflight

Run these checks before starting work on any task to ensure proper context and setup.

## When to Use

Before beginning work on a task, run this preflight. Ensures you understand the task, have a clean environment, and follow project conventions.

## Execution Contract (Required)

- You MUST run steps 1-9 in order for new task starts (unless an explicit skip condition applies).
- Step 9 output is mandatory and MUST use the preflight summary template with all sections present.
- If data is missing, show `N/A` instead of omitting a section.
- Do not start implementation before showing Step 9 and receiving user confirmation.
- Do not replace the template with a free-form summary.

## Autonomy Thresholds (Required)

Default behavior for this preflight is **act without prompting** for deterministic, reversible checks.

**Auto-continue (no prompt):**
- Missing optional local setup (for example, no `Makefile`/`dev-status` target)
- Dev environment is stopped
- Runtime is non-stable (warn and continue)
- Informational PR states (awaiting review / changes requested)

**Prompt required (human decision gate):**
- Intent is ambiguous (for example, unclear whether uncommitted files belong to this task)
- Irreversible/destructive actions would be taken
- Policy gates require explicit approval (for example, merging an approved PR before starting new work)

Do not ask yes/no questions for routine reporting steps.

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
- List the files.
- If relation to the task is obvious, proceed with the obvious path and report it.
- If relation is unclear, ask: "These uncommitted changes may conflict with this task. Should I stash them, commit them, or continue as-is?"

**If project requires PRs and on main:**
- Suggest creating a feature branch
- Propose branch name: `feature/<task-id>-<short-description>`

### 5. Check Open PRs

Check for unmerged PRs before starting new work. First, detect the git host:

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if echo "$REMOTE_URL" | grep -q "github.com"; then
  HOST="github"
else
  HOST="forgejo"
fi
```

**GitHub:**
```bash
gh pr list --state open --json number,title,reviewDecision,headRefName
```

**Forgejo:**
```bash
zsh -ic "fj pr list --state open"
```

**If approved PRs exist (not merged):**
- Warn: "⚠️ PR #X (title) is approved but not merged"
- Ask: "Merge it before starting new task? [yes / no / skip]"
- If yes: merge the PR with `gh pr merge <num> --squash --delete-branch` (or `zsh -ic "fj pr merge <num>"` for Forgejo), then pull main
- If no/skip: proceed but note the risk of confusion

**If PRs awaiting review or with changes requested:**
- Info only: "ℹ️ PR #X is awaiting review" or "ℹ️ PR #X has changes requested"
- No blocking, just awareness

**Why this matters:**
- Approved PRs left unmerged cause confusion when features appear missing
- Starting new work on top of unmerged changes can create conflicts
- Keep the PR queue clean before starting fresh work

### 6. Check Dev Environment

If project has a Makefile with `dev-status` target:

```bash
if [ -f Makefile ] && grep -q "dev-status:" Makefile; then
  STATUS=$(make -s dev-status 2>/dev/null)
  echo "Dev environment: $STATUS"
fi
```

**If stopped:**
- Do not prompt.
- Default action: continue preflight without starting the dev environment.
- Note in preflight summary: "Dev environment stopped (not required for preflight)."

**If running:**
- Note: "Dev environment is running ✓"

**If no Makefile or no dev-status target:**
- Skip this check silently

**Skip for docs-only tasks:**
- If task title/labels indicate documentation-only work, skip this check

### 7. Check Runtime Versions

Check that runtime environments are using stable versions (not canary/beta/alpha/rc):

```bash
# Check common runtimes
node --version 2>/dev/null | grep -qE '(-canary|-beta|-alpha|-rc)' && echo "⚠️ Node: non-stable version"
bun --version 2>/dev/null | grep -qE '(-canary|-beta|-alpha|-rc)' && echo "⚠️ Bun: non-stable version"
```

**If non-stable version detected:**
- Warn: "⚠️ Runtime uses non-stable version: <version>"
- Note potential issues: "Canary/beta versions may have bugs or missing features"
- Default action: continue and record risk in the preflight summary.
- Prompt only if project policy explicitly requires stable runtime for this task.

**Why this matters:**
- Canary builds can have breaking bugs (e.g., bun:sqlite failures)
- Beta/RC versions may have incomplete features
- Stable versions are tested and reliable

### 8. Understand Context

**Check for related files mentioned in task:**
- If task references specific files, verify they exist
- If task references PRs or issues, note their status

**Check linked source:**
```bash
# If task has external source URL (GitHub issue, etc.)
todu task show <task-id> | grep "Source URL"
```

### 9. Establish the Plan (Mandatory Output)

Before any implementation work, output the following template with **all sections present**.

Rules:
- Keep section headings exactly as shown.
- Fill every line (use `N/A` if unavailable).
- Do not omit Open PRs, Project Requirements, Acceptance Criteria, Testing, or Plan.
- End with `Ready to proceed? [yes / modify plan]` and wait for user response.

```text
=== Task Start Preflight: Task #<id> ===

Task: <title>

Open PRs: ✅ None | ⚠️ #X approved (not merged) | ℹ️ #X awaiting review | N/A
Dependencies: ✅ None | ⚠️ Depends on #X (incomplete) | N/A
Git Status: ✅ Clean | ⚠️ <n> uncommitted files | N/A
Branch: <current-branch> | 💡 Suggest: feature/<id>-<name> | N/A
Dev Environment: ✅ Running | ⚠️ Stopped | ⏭️ N/A

Project Requirements:
- <relevant guideline 1> | N/A
- <relevant guideline 2> | N/A

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- ...

🧪 Testing: Each acceptance criterion should have a corresponding automated test.
   (Use "N/A - docs-only task" when appropriate)

Plan:
1. <Step 1>
2. <Step 2>
...

Ready to proceed? [yes / modify plan]
```

**Testing Reminder:** For non-documentation tasks, each acceptance criterion should be verified by an automated test, not just manual checking. Plan tests explicitly in the Plan section.

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

Some checks can be skipped, but Step 9 output is still required:

- **Continuation of prior work**: If resuming work in same session, abbreviated preflight is okay
- **Trivial tasks**: Abbreviated preflight is okay
- **No project docs**: If project has no CONTRIBUTING.md/CODE_STANDARDS.md, mark requirements as `N/A`

Even for abbreviated preflights, you MUST output the Step 9 template and wait for confirmation.

## Notes

- Always run preflight when starting a new task
- Default to autonomous progress for reversible, deterministic checks
- Ask only at ambiguity, irreversible actions, or explicit policy gates
- If dependencies are incomplete, get explicit approval to proceed
- Feature branches keep main clean and enable proper PR review
