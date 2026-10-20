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

### Execute a Task

```
"Start task #1234" / "Do task #1234" / "Pickup task #1234"
→ task-perform reads the task and project instructions
→ Confirms inprogress (or resumes without another status update)
→ Does what the task says and checks the result
→ Comments with the result, then marks done if finished
→ Otherwise explains the gap and leaves the task open
```

A starting comment is optional. There is no automatic preflight, implementation-plan approval, close-gate handoff, or fallback contributing policy. Ask only for an actual ambiguity, blocker, or explicitly required approval.

Explicit close/complete/verify-and-close requests check already-delivered work and finish without starting implementation or setting inprogress. Readiness-only and verification-only requests use their assessment skills and make no task writes. Lookup, comment-only, and habit requests do not start task execution.

### Development Delivery

`task-pipeline` owns development planning and delivery when the user/task requests it or project instructions explicitly select it. Ordinary task execution, repository changes, or individual PR/merge requirements do not automatically select the whole pipeline. Follow project contributing instructions; only this selected development pipeline uses `skills/task-pipeline/DEFAULT_CONTRIBUTING.md` when no project contributing file exists. It returns the delivery result without changing task status or posting task comments.

**For agents developing this repository**, the branch/PR/independent-review/human-approved-merge path below remains required for tracked changes. This repository policy does not impose a development pipeline on every task handled by the distributed skills. Small fixes and documentation changes still follow this repository's delivery rules. Resolve real scope or policy conflicts before editing; obtain any required plan/preview approval.

For work using the PR delivery path, after implementation is complete, execute these steps in order. Do not treat required next steps as optional.

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

### CI Failure Path (Required)

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

### PR Pipeline Output Contract (Required)

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

### Completion and Write Failures

Check the actual requested outcome and explicit project requirements, including merge when required. Task-perform records completion with a confirmed comment before marking done; it does not require another skill or default approval. If unfinished, blocked, or unverified, record the gap and leave the task open. Reconcile failed/uncertain writes without blindly duplicating comments or claiming success.

## Workflow Diagram

```text
Project initialization
  project-init -> repo/scaffold/tooling/dev-environment helpers

Task execution
  read task/instructions -> confirm inprogress -> do requested work
    -> check result -> completion comment -> done
    -> unfinished/blocked: explain and leave open

Development delivery (only when requested or required by project instructions)
  task-pipeline -> plan -> implement/checks -> PR -> independent review
                -> human merge approval -> merge/cleanup -> return result

Requested readiness or completion assessment
  task-start-preflight or task-close-gate -> read-only assessment
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
| `task-pipeline` | "run the development pipeline", or task/project instructions explicitly requiring it |
| `task-perform` | Execution: "do/work on/start/pickup task #X"; closure-only: "close/complete/verify and close task #X" |
| `task-close-gate` | "verify completion only", "is task #X complete?"; requested assessment, never lifecycle writes |
| `pr-review` | "request review", "get this reviewed", "need review", "review PR #X", "review pull request", "check PR" |

## Best Practices

### Keep Task Execution Direct

- Do the requested work without adding workflow stages. Use readiness/completion assessment skills only when requested or explicitly required.
- Follow actual task/project requirements; simplifying task-perform does not waive approval, review, or verification rules.
- Check results proportionally. An unsupported "done" claim is not evidence, and explicit close requests never start missing implementation.

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
