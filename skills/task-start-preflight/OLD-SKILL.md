
---
name: task-start-preflight
description: Build and confirm a task execution plan before any work starts. Use when user says "start task", "begin task", "pick up task", or similar.
---

# Task Start Preflight

Run these checks before starting work on any task to ensure proper context and setup.

## When to Use

Before beginning work on a task, run this preflight to establish an execution plan, surface constraints, and give the user a chance to approve or modify the plan before any work begins.

## Execution Contract (Required)

- Run steps 1-4 in order for new task starts (unless an explicit skip condition applies).
- Always output the Step 4 preflight summary template with all sections present (`N/A` when data is missing).
- Do not start implementation or take side-effecting actions in this skill. After user confirmation, hand off to the `todu-work` skill.

## Autonomy Thresholds (Required)

- Default: run deterministic, reversible preflight checks without prompting.
- Ask the user only when:
  - intent is ambiguous,
  - an action is destructive/irreversible,
  - a policy gate requires explicit human approval (for example, merge decisions).
- Non-blocking issues should be reported in the summary unless project policy explicitly makes them blocking.

## Preflight Steps

### 1. Load Task Details and Comments

```bash
todu task show <task-id> --format json
```

Use a single task payload to gather both task metadata and comment history.

**Display:**
- Task title and description
- Acceptance criteria (checklist of what "done" looks like)
- Dependencies on other tasks
- Any blocking status or warnings
- Relevant comments from prior sessions (`comments` in JSON)

**If task has dependencies:**
- Check if dependent tasks are complete
- If not, warn: "This task depends on #X which is not complete. Proceed anyway?"

**Look for in comments:**
- Prior work or decisions made
- Context from previous sessions
- Blockers that were identified
- Questions that were answered

### 2. Check Project Documentation

Read `CONTRIBUTING.md` only and extract what is needed for this task.

**Lookup order (required):**
1. `CONTRIBUTING.md`
2. `docs/CONTRIBUTING.md`

Use the first file that exists. If neither exists, record `N/A`.

**Extraction scope (required):**
- Branching strategy
- PR/review/CI requirements
- Testing requirements
- Code style/quality requirements
- Workflow/task conventions relevant to this task

**Context-control rules (required):**
- Do **not** dump full document contents into the preflight output.
- Extract concise requirements only.
- Include source path for each extracted requirement (for example: `CONTRIBUTING.md`).

**Step 4 output requirement:**
Populate `Workflow Requirements` with concise, source-tagged bullets from `CONTRIBUTING.md` (or `N/A` when unavailable).

### 3. Check Git Status

```bash
git status
```

**Check for:**
- Current branch (are we on main?)
- Uncommitted changes
- Untracked files

**If issues found:**
- List the files.
- If relation to the task is obvious, record the recommended handling in the plan.
- If relation is unclear, ask for a decision and record it in the plan.
- Do not stash/commit/clean in preflight.

**If project requires PRs and on main:**
- Recommend creating a feature branch in `todu-work`.
- Propose branch name: `feature/<task-id>-<short-description>`

### 4. Establish the Plan (Mandatory Output)

Before any implementation work, output the following template with **all sections present**.

Rules:
- Keep section headings exactly as shown.
- Fill every line (use `N/A` if unavailable).
- Do not omit Workflow Requirements, Acceptance Criteria, Testing, or Plan.
- End with `Ready to proceed to todu-work? [yes / modify plan]` and wait for user response.

```text
=== Task Start Preflight: Task #<id> ===

Task: <title>

Dependencies: ✅ None | ⚠️ Depends on #X (incomplete) | N/A
Git Status: ✅ Clean | ⚠️ <n> uncommitted files | N/A
Branch: <current-branch> | 💡 Suggest: feature/<id>-<name> | N/A

Workflow Requirements:
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

Ready to proceed to todu-work? [yes / modify plan]
```

## After Approval (Handoff Only)

Once user confirms, hand off to `todu-work`.

`task-start-preflight` must not perform execution actions (status updates, branch creation, implementation, or environment/runtime execution checks).

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

=== Git Status ===
⚠️ On branch: main
⚠️ 3 modified files (unrelated to task)

💡 Recommend: Create feature branch for this work

=== Acceptance Criteria ===
- [ ] Skill file created at ~/.local/dotfiles/common/ai-assistant/skills/task-start-preflight/SKILL.md
- [ ] ~/Private/code/.pi/skills/ directory created
- [ ] Symlink created: ~/Private/code/.claude/skills/task-start-preflight
- [ ] Symlink created: ~/Private/code/.pi/skills/task-start-preflight
- [ ] Covers all preflight steps
- [ ] Checks for CONTRIBUTING.md
- [ ] Follows same pattern as task-close-preflight
- [ ] Includes example flow
- [ ] Documents when to skip checks

=== Plan ===
1. Create feature branch in todu-work: feature/1230-task-start-preflight
2. Create skill file following task-close-preflight pattern
3. Create symlinks for .claude and .pi
4. Commit and prepare for merge

Ready to proceed to todu-work? [yes / modify plan]
```

## When to Skip

Some checks can be skipped, but Step 4 output is still required:

- **Continuation of prior work**: If resuming work in same session, abbreviated preflight is okay
- **Trivial tasks**: Abbreviated preflight is okay
- **No project docs**: If project has no `CONTRIBUTING.md` (or `docs/CONTRIBUTING.md`), mark requirements as `N/A`

Even for abbreviated preflights, you MUST output the Step 4 template and wait for confirmation.

## Notes

- Always run preflight when starting a new task
- Default to autonomous progress for reversible, deterministic checks
- Ask only at ambiguity, irreversible actions, or explicit policy gates
- If dependencies are incomplete, get explicit approval to proceed
- Feature branches keep main clean and enable proper PR review
