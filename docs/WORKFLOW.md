# Development Workflow

How to use todu-workflow skills for AI-first development.

## Project Creation

### New Project

Use `project-init` to create a project from scratch:

```
"Create a new project"
→ Triggers project-init skill
→ Questionnaire gathers: name, host, stack, framework, database, services
→ Creates repo, scaffolds files, sets up tooling
→ Creates initial design task
```

### Add to Existing Project

Use individual skills to add specific capabilities:

| Need | Skill |
|------|-------|
| README, LICENSE, AGENTS.md, docs/ | `project-scaffold` |
| Linting, formatting, testing | `quality-tooling` |
| Makefile, Procfile, Docker | `dev-environment` |

## Task Workflow

### 1. Start a Task

```
"Start task #1234"
→ Triggers task-start-preflight skill
→ Shows task details, acceptance criteria
→ Checks git status, suggests feature branch
→ Marks task as in-progress
```

### 2. Do the Work

- Create feature branch: `feat/{task-id}-{description}`
- Implement changes
- Write tests
- Commit incrementally

### 3. Verify Before Closing

```
"Close task #1234"
→ Triggers task-close-preflight skill
→ Verifies acceptance criteria are met
→ Checks tests pass
→ Confirms ready to close
```

### 4. Mandatory Post-PR Pipeline (Required Sequence)

After implementation is complete, agents MUST execute these steps in order.
Do not treat these as optional, and do not ask "want me to...?" when the next step is required.

1. **Run local gate**

   ```bash
   ./scripts/pre-pr.sh
   ```

2. **Push branch and open/update PR**

   ```bash
   git push -u origin feat/1234-description
   gh pr create --title "feat: description" --body "Task: #1234"
   ```

3. **Enforce CI gate before review request**
   - If CI check runs are available: wait until checks complete and are green.
   - If CI fails: follow the required failure path (below), then re-push and re-check.
   - If CI status is not available on the host (for example, local Forgejo without CI integration): **stop and ask the human how to proceed**.

4. **Request independent review**

   ```
   "Request review for this PR"
   → Triggers request-review skill
   → Spawns separate agent session to review
   → Reviewer uses pr-review skill
   ```

5. **Report review result to human**
   - Summarize whether review is approved, warnings, or changes requested.
   - If warnings are present, list them explicitly and fix them by default, then return to step 1.
   - Human may explicitly waive warnings ("ignore warnings") and proceed without fixing.
   - If changes are requested, fix and return to step 1.

6. **Stop and wait for explicit human merge approval**
   - Never merge automatically.
   - Merge only after explicit human approval ("merge", "approved", "LGTM", etc.).

### 5. CI Failure Path (Required)

When CI is available and a check fails, run this failure loop:

1. Fetch failing checks/logs.
2. Explain what failed.
3. Fix the issue.
4. Re-run `./scripts/pre-pr.sh`.
5. Push fixes.
6. Wait for CI to finish green.

Expected status progression:

- `local_checks=pass`
- `ci=failed` (with failure details)
- `local_checks=pass` (after fix)
- `ci=pass`

### 6. Agent Output Contract (Required)

At each gate, report state explicitly in this format:

```text
PR Pipeline Status
- local_checks: pass|fail
- push: done|pending
- ci: pass|fail|unavailable-needs-human-decision
- review: pending|approved|warnings|changes-requested
- merge_approval: waiting-human|approved
```

Rules:
- Do not skip fields.
- Do not present required next steps as optional questions.
- If `ci=unavailable-needs-human-decision`, stop and ask the human before review request.

### 7. Close Task

```
"Close task #1234"
→ Adds completion comment
→ Marks task as done
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     PROJECT CREATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  project-init ─────┬──► project-scaffold                    │
│                    ├──► quality-tooling                     │
│                    ├──► dev-environment                     │
│                    └──► Creates design task                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      TASK WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  task-start-preflight                                        │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │  Do Work    │  ◄─── Implement, test, commit               │
│  └─────────────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  task-close-preflight ───► Create/Update PR                  │
│                                  │                           │
│                                  ▼                           │
│                           CI gate (required)                 │
│                                  │                           │
│                                  ▼                           │
│                          request-review                      │
│                                  │                           │
│                                  ▼                           │
│                          pr-review (other agent)             │
│                                  │                           │
│                                  ▼                           │
│                  Wait for human merge approval (required)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Skills Reference

| Skill | Trigger Phrases |
|-------|-----------------|
| `project-init` | "create a new project", "init project", "start new app" |
| `project-scaffold` | "scaffold project", "add README", "create project files" |
| `quality-tooling` | "add linting", "set up eslint", "configure testing" |
| `dev-environment` | "set up dev environment", "add Makefile", "add docker" |
| `task-start-preflight` | "start task #X", "work on task #X", "begin task" |
| `task-close-preflight` | "close task #X", "complete task", "finish task" |
| `request-review` | "request review", "get this reviewed", "need review" |
| `pr-review` | "review PR #X", "review pull request", "check PR" |

## Best Practices

### Always Use Preflights

- **Starting**: `task-start-preflight` ensures you understand the task and have clean git state
- **Closing**: `task-close-preflight` verifies you've met acceptance criteria

### Keep PRs Focused

- One task per PR
- Small, reviewable changes
- Clear commit messages

### Run Quality Checks

Before creating a PR:

```bash
./scripts/pre-pr.sh
```

Or:

```bash
make pre-pr
```

### Three Attempts Rule

If stuck after 3 attempts:

1. Stop trying the same approach
2. Document what was tried
3. Ask for guidance or suggest alternatives
