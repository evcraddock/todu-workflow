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
→ Creates initial design/backlog task
```

### Add to Existing Project

Use individual skills to add specific capabilities:

| Need | Skill |
|------|-------|
| README, LICENSE, AGENTS.md, docs/ | `project-scaffold` |
| Linting, formatting, testing | `quality-tooling` |
| Makefile, Procfile, Docker | `dev-environment` |

## Task Authoring

### Create Better Task Content

```
"Create a task for adding webhook retries"
→ Triggers task-authoring skill
→ Gathers only the missing context
→ Produces a better title and structured markdown description
→ Uses implementation or bug structure as appropriate
→ Returns authored task content
```

Use `task-authoring` for task-creation entry points when the request needs shaping, requirements gathering, acceptance criteria drafting, dependency capture, bug-report structure, or title improvement. Implementation tasks should include `## Goal`, `## Requirements`, `## Acceptance criteria`, and `## Dependencies`, using real task IDs when known.

## Task Comment Authoring

### Draft Better Task Comments

```
"Write a progress update for task #1234"
→ Triggers task-comment-authoring skill
→ Gathers only the missing context
→ Produces structured markdown comment content
→ Returns authored comment content without posting it
```

Use `task-comment-authoring` when the request needs a clearer progress update, blocker note, completion summary, or review summary before handing the markdown to comment or note tooling.

## Task Workflow

### 1. Start a Task

```
"Start task #1234" / "Do task #1234" / "Pickup task #1234"
→ Triggers task-perform
→ Loads task/project instructions and uses shared read-only readiness checks
→ Obtains required plan approval
→ Confirms inprogress before work, then posts a starting/resuming comment
```

### 2. Do the Work

```
task-perform owns the lifecycle for every execution wording
→ Follows the agreed deliverable and project instructions
→ Records meaningful progress, decisions, and blockers
→ Loads task-pipeline development guidance for applicable repository changes
→ Verifies completion and closes only after evidence and applicable gates pass
```

### 3. Verify Before Closing

```
At the end of execution:
→ task-perform uses task-close-gate in assessment-only mode in the current session
→ Verifies the agreed outcome and any acceptance criteria with proportional evidence
→ Requires merge completion when the delivery workflow calls for it
→ Posts completion evidence, then marks done without another default approval prompt
→ Leaves the task open with an explanation when blocked or evidence is inconclusive

Standalone "Close task #1234" requests still use the close gate without starting execution.
```

### 4. Development Delivery Stages (Required When Applicable)

For planned tracked repository changes, default to branch/PR/independent review/human-approved merge unless explicit project policy permits another delivery path. Resolve unclear policy before editing; small or documentation-only changes do not silently bypass applicable gates. Non-repository work does not automatically require these stages, and brainstorming has no fixed storage destination.

`task-perform` owns lifecycle state and uses `task-pipeline` as development guidance, not as a competing executor. Execution and completion verification do not require tmux delegation. Independent review must remain independent; report unavailable required review rather than substitute self-review silently.

For work using the PR delivery path, after implementation is complete, agents MUST execute these steps in order.
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
   - If CI status is not available on the host (for example, local Forgejo without CI integration):
     - apply a documented standing policy (continue / wait / stop), or
     - ask the human how to proceed if no standing policy exists.

4. **Request independent review**

   ```
   "Request review for this PR"
   → Triggers pr-review skill
   ```

5. **Report review result to human**
   - Summarize whether review is approved, warnings, or changes requested.
   - If warnings are present, list them explicitly and fix them by default, then return to step 1.
   - Human may explicitly waive warnings ("ignore warnings") and proceed without fixing.
   - If changes are requested, fix and return to step 1.

6. **Stop and wait for explicit human merge approval**
   - Never merge automatically.
   - Merge only after explicit human approval ("merge", "approved", "LGTM", etc.).

7. **Execute merge and post-merge normalization**
   - Merge the approved PR.
   - Switch to `main` and fast-forward/update local `main`.
   - Clean up the feature branch by default:
     - delete local feature branch
     - delete remote feature branch
   - If cleanup policy is unclear for the host/workflow, ask the human before deleting branches.

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
- `ci=fail` (with failure details)
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
- If `ci=unavailable-needs-human-decision`, either apply a documented standing policy or ask the human before review request.

### 7. Complete the Task Lifecycle

```
task-perform completion
→ Confirm the agreed outcome and applicable delivery gates, including merge/cleanup when required
→ Obtain a completion assessment without lifecycle writes from the verifier
→ Post a completion comment with evidence and confirm success
→ Mark done and report the actual result; no additional default completion approval

If comment posting or the status update fails or has an uncertain outcome, report the partial result and reconcile before retrying. Never duplicate comments blindly or claim closure without confirmation.
```

## Workflow Diagram

```text
Project initialization
  project-init -> repo/scaffold/tooling/dev-environment helpers

Task execution (task-perform owns every lifecycle write)
  task + project instructions
    -> shared readiness + required plan approval
    -> confirmed inprogress + starting/resuming comment
    -> agreed work + meaningful updates
    -> applicable delivery path:
         repository PR path -> checks -> independent review
                            -> human merge approval -> merge/cleanup
         non-repository or explicit alternate policy -> agreed deliverable
    -> current-session completion assessment (no lifecycle writes)
    -> confirmed completion comment -> done

Any unresolved readiness, verification, write, or approval issue
  -> explain/record the issue, keep the task open, and reconcile before retry
```

## Skills Reference

| Skill | Trigger Phrases |
|-------|-----------------|
| `project-init` | "create a new project", "init project", "start new app" |
| `project-scaffold` | "scaffold project", "add README", "create project files" |
| `quality-tooling` | "add linting", "set up eslint", "configure testing" |
| `dev-environment` | "set up dev environment", "add Makefile", "add docker" |
| `task-authoring` | "create a task", "new issue", "create bug", "draft a task", "help me write a task" |
| `task-comment-authoring` | "draft a task comment", "write a task update", "help me write a note for task #X", "summarize progress for task #X" |
| `task-start-preflight` | "check readiness", "run preflight" (read-only) |
| `task-pipeline` | Development reference loaded by task-perform, not a direct execution trigger |
| `task-perform` | "do/perform/execute/handle/start task #X", "work on task #X", "pickup task #X", "get started on task #X" |
| `habit-perform` | "do habit #X", "perform habit #X", "handle habit #X", "work on habit #X" |
| `task-close-gate` | "close task #X", "complete task", "finish task" |
| `pr-review` | "request review", "get this reviewed", "need review", "review PR #X", "review pull request", "check PR" |

## Best Practices

### Always Use Preflights

- **Readiness**: `task-start-preflight` checks readiness without implementation or status mutations; plan approval is separate.
- **Execution**: `task-perform` confirms inprogress before work, records meaningful comments, and loads applicable development guidance.
- **Completion**: `task-close-gate` assesses evidence for the lifecycle owner, which posts completion and marks done only after applicable gates pass. Standalone close requests do not start execution.

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
