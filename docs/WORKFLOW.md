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

### 4. Create Pull Request

```bash
git push -u origin feat/1234-description
gh pr create --title "feat: description" --body "Task: #1234"
```

### 5. Request Review

```
"Request review for this PR"
→ Triggers request-review skill
→ Spawns separate agent session to review
→ Reviewer uses pr-review skill
```

### 6. Address Feedback & Merge

- Address review comments
- Push fixes
- Get approval
- Squash and merge

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
│  task-close-preflight ───► Create PR                         │
│                                  │                           │
│                                  ▼                           │
│                          request-review                      │
│                                  │                           │
│                                  ▼                           │
│                          pr-review (other agent)             │
│                                  │                           │
│                                  ▼                           │
│                          Merge & close task                  │
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
