---
name: task-pipeline
description: Development-workflow guidance loaded by task-perform for applicable repository changes. Not a separate task execution entry point; route do, work-on, and pickup requests to task-perform.
---

# task-pipeline

Development stages for repository work owned by [task-perform](../task-perform/SKILL.md).

## Lifecycle integration

`task-perform` is the single execution entry point and owns readiness, planning, confirmed start, task comments, and verified closure. For direct pickup/work-on requests, enter through that skill; do not recursively invoke it after it has loaded this reference.

When loaded by `task-perform`, use only the applicable development instructions in steps 3–5 below, subject to explicit project policy. Return development/merge evidence to the caller. Do not repeat steps 1–2 or run step 6: the caller owns those lifecycle actions, uses completion verification in the current session, and does not require tmux delegation or an extra default completion approval. Required independent review and explicit human merge approval remain effective.

The fuller reference cleanup is tracked separately in task-d9b978d2; the retained steps below are not a second execution entry point.

## Steps

1. Check task readiness with `task-start-preflight`.
   - `READY` → continue
   - `BLOCKED` → stop

2. Load instructions and task description.
   - Use `docs/CONTRIBUTING.md` if it exists.
   - Otherwise use `DEFAULT_CONTRIBUTING.md` in this skill directory.
   - If neither can be loaded, return `BLOCKED`.
   - Load the task description for the selected task.
   - If the task description cannot be loaded, return `BLOCKED`.
   - Determine the concrete steps to take from the contributing instructions and task description.
   - Ask the user to approve the planned steps before proceeding.
   - If the user does not approve, return `BLOCKED`.

3. Follow contributing instructions.
   - Treat loaded contributing instructions as active constraints.
   - If instructions are ambiguous/conflicting, return `BLOCKED`.

4. Follow the instructions in the task description.
   - Implement exactly what the task asks for.
   - If task instructions are ambiguous/conflicting, return `BLOCKED`.

5. Complete merge flow before closure.
   - Open or update the PR for the task branch.
   - Run required review flow and wait for explicit human merge approval.
   - Do not merge without explicit approval.
   - If merge is not completed, return `BLOCKED` and do not continue to closure.
   - After merge, switch to `main` and fast-forward/update local `main`.
   - Perform feature branch cleanup by default:
     - delete local feature branch
     - delete remote feature branch
   - If branch cleanup policy is uncertain for the current host/workflow, ask the user before deleting.

6. Ensure the task is closed correctly.
   - This closure step is mandatory for every `task-pipeline` run and is not defined by contributing instructions.
   - Ask the user for explicit approval before running the close gate.
   - If approval is not given, return `BLOCKED` and do not run close gate.
   - Run `task-close-gate` for the task in a hidden tmux sub-agent session (detached) via the `tmux` skill only after merge and after approval.
   - Use the sub-agent result as the close gate.
   - Move task status to `done` only when explicit approval was given and close gate passes.

## Rules

- Do not move to the next step until the current step is `READY`.
- The lifecycle owner posts task comments with the native `task_comment_create` tool.
- Do not add manual line breaks in markdown paragraphs.
