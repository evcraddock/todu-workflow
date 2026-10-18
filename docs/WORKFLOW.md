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
→ Captures known intent, context, and explicit user constraints
→ Asks only when missing intent prevents a useful capture
→ Produces a clear title and concise prose or bullets, with headings only when useful
→ Returns authored content to the caller for any requested backend write
```

Use `task-authoring` to capture a problem and desired outcome without inventing requirements, acceptance criteria, dependencies, or implementation plans. Preserve supplied constraints and known bug details; no fixed template or empty sections are required. Label retained agent suggestions as unapproved, and record useful open questions for pickup. Detailed requirements clarification and implementation planning happen when the task is picked up, not during speculative capture.

## Task Comments

Draft comments directly; there is no authoring-skill handoff or mandatory generic template. Keep content factual and proportional, retain supplied constraints, and include relevant verification evidence without inventing results. A simple update can be one sentence.

```
"Draft a progress update for task #1234"
→ Returns a concise draft without posting or starting task execution

"Comment on task #1234: the PR is open and checks passed"
→ Posts the authorized factual update directly through native task_comment_create
→ Confirms success, or reports the actual failure without claiming it was posted
```

Drafting is not permission to post. An explicit posting request or an already-authorized workflow provides that authorization without a separate default drafting/approval step. Resolve the task ID rather than guessing. Posting a comment alone does not authorize changing task status, starting implementation, or closing the task. Workflow-specific review artifacts and completion gates still apply.

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

Explicit "Close task #1234" / "Verify and close task #1234" requests use task-perform's closure-only path: shared completion assessment, then owner-controlled comment/status writes if ready. They do not run start preflight, set inprogress, post a starting comment, or implement missing work. Verification-only requests stop after task-close-gate returns its verdict, with no lifecycle writes.
```

### 4. Development Delivery Stages (Required When Applicable)

For planned tracked repository changes, default to branch/PR/independent review/human-approved merge unless explicit project policy permits another delivery path. Resolve unclear policy before editing; small or documentation-only changes do not silently bypass applicable gates. Non-repository work does not automatically require these stages, and brainstorming has no fixed storage destination.

`task-perform` owns lifecycle state and uses `task-pipeline` as development guidance, not as a competing executor. Loading the reference does not restart readiness, planning, task status, or comments. It returns development/check/review/merge evidence to the caller for current-session completion assessment, without a hidden verifier or another default approval prompt. Execution and completion verification do not require tmux delegation. Independent review must remain independent; report unavailable required review rather than substitute self-review silently.

| Agreed deliverable/policy | Delivery path |
| --- | --- |
| Tracked code, a tiny fix, or committed documentation; no explicit alternative policy | Default branch/PR/independent review/human-approved merge |
| Tracked change with an explicit applicable alternative policy | The permitted alternative, preserving its verification and approval gates |
| Chat-only brainstorming, Todu-only conclusions, or an explicitly untracked local note | No automatic repository gates or fixed storage requirement |
| Unclear/conflicting policy or substantial/ambiguous work without plan agreement | Resolve the decision/plan with task-perform before editing |

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
| Ordinary comment handling (no skill handoff) | "draft a task comment" returns content only; "comment on task #X" uses native task_comment_create when authorized |
| `task-start-preflight` | "check readiness", "run preflight" (read-only) |
| `task-pipeline` | Development reference loaded by task-perform, not a direct execution trigger |
| `task-perform` | Execution: "do/work on/start/pickup task #X"; closure-only: "close/complete/verify and close task #X" |
| `task-close-gate` | "verify completion only", "is task #X complete?"; shared assessment for task-perform, never lifecycle writes |
| `pr-review` | "request review", "get this reviewed", "need review", "review PR #X", "review pull request", "check PR" |

## Best Practices

### Always Use Preflights

- **Readiness**: `task-start-preflight` is the shared read-only check for starting active tasks, resuming inprogress tasks, and standalone readiness requests. Return a concise explanation of status, intent, and actual blockers; implementation-ready specifications and a full report template are not required. Resolve explicit dependencies directly with native `task_show`, including cross-project references; missing or failed lookups never imply completion. Project planning/approval and execution remain separate.
- **Execution**: `task-perform` confirms inprogress before work, records meaningful comments, and loads applicable development guidance.
- **Completion**: `task-close-gate` always returns an assessment without task mutations. It assesses formal criteria or the agreed outcome, reuses relevant evidence, and permits targeted proportionate checks when needed. task-perform owns explicit and automatic closure after applicable gates pass; verification-only requests stop at the verdict. An unsupported done claim is not evidence, and explicit close requests never start implementation.

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
