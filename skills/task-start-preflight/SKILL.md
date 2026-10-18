---
name: task-start-preflight
description: Check whether a Todu task is ready to start or resume without starting work. Use for "check readiness", "start preflight", "run preflight", or shared readiness checks from task-perform/task-pipeline. Do not plan or implement the task.
---

# Task Start Preflight

One shared, read-only readiness check for standalone requests and task execution. Determine whether the next action is clear and unblocked, not whether a complete implementation plan exists.

## Check readiness

1. Load the requested task with the native `task_show` tool (`taskId`). A fresh successful result already loaded by the caller may be reused. If the task is missing or cannot be loaded, report that explicitly and stop; do not guess its state.
2. Check status: `active` can start and `inprogress` can resume without a reset. For `waiting`, explain the blocker/decision needed before starting; for `done` or `cancelled`, report terminal status and any reopening decision needed. Do not silently reopen or transition any task.
3. Check intent using the description and relevant supplied context. A known target and desired outcome sufficient for the next action are enough; do not require a formal requirements checklist, acceptance-criteria section, or implementation-ready specification. If missing intent prevents progress, ask only for that clarification and report not ready. Details that can be resolved at pickup are not readiness blockers.
4. Identify explicit task prerequisites in the description/context (for example, "depends on", "blocked by", or "after task-X"). Interpret the references, not just keywords: related work, examples, and optional suggestions are not automatically dependencies. Resolve actual dependencies as described below.

Stop when status or missing intent already prevents progress; do not run dependency queries or unrelated checks just to fill a report.

## Resolve dependencies directly

- Use native `task_show` for each explicit dependency ID, including IDs in other projects. Do not substitute a same-project or in-flight `task_list` comparison; absence from a list is not evidence of completion.
- Confirmed `done` satisfies a dependency. `active`, `waiting`, and `inprogress` dependencies block readiness: report their IDs, titles, and statuses.
- A cancelled dependency is not completed work. Report the decision needed about whether the prerequisite still applies; do not silently waive it.
- A missing task, failed/uncertain lookup, unknown status, or reference that cannot be resolved to a task ID remains unresolved. Explain the actual problem and ask only for the missing reference/decision when needed. Never count unresolved or unchecked dependencies as satisfied.
- If there are no explicit prerequisites, no dependency lookup or task-list query is needed. Do not invent dependencies or require a dependency section.

## Return a concise result

State ready to start/resume or not ready, identify the task/status, and briefly explain the evidence or actual blockers. Include dependency IDs/statuses or a focused clarification only when relevant. No mandatory report template, empty sections, numbered gate ceremony, or default approval prompt.

A ready result returns control to the caller; it is not permission to mutate or evidence that work has started. For execution, [task-perform](../task-perform/SKILL.md) owns the confirmed `inprogress` transition and starting/resuming comment. [task-pipeline](../task-pipeline/SKILL.md) uses this same contract rather than maintaining another readiness definition. Standalone checks end with the readiness result.

Preflight never changes task metadata, posts comments, plans implementation, creates branches, or performs the work. Keep required project planning/approval separate in the execution workflow; do not turn a readiness-only request into execution.
