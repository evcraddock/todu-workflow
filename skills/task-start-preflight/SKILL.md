---
name: task-start-preflight
description: Verify a Todu task is ready to be worked on. Use for "start preflight", "run preflight", or pipeline readiness checks. Do not implement the task.
---

# Task Start Preflight

Preflight is a readiness gate. It does **not** plan implementation and does **not** execute work.

## Purpose

Confirm whether a task is ready to be worked on by checking:
1. task status (`active`, or `inprogress` when resuming),
2. task requirements (not empty/ambiguous),
3. dependency blockers (none may be `active`, `waiting`, or `inprogress`).

## Execution Contract (Required)

- Input: task ID.
- Gate 0 must load task details using the native `task_show` tool.
- Run the 3 gates in order.
- Stop on first failed gate.
- Do not make side-effecting changes in preflight unless user explicitly asks.
- Always output the preflight summary template.

## Gate 0: Load Task Details

Call the native `task_show` tool with `taskId` and use its returned task object as the source of truth for this preflight.

If `task_show` cannot find or load the task, fail preflight immediately and stop.

Collect at minimum:
- `id`
- `title`
- `status`
- `description`
- `project` (name or ID)

## Gate 1: Is Active

Preflight applies to starting `active` tasks and resuming `inprogress` tasks.

- If status is `active` or `inprogress`: pass without changing status.
- If status is anything else: fail and stop. Explain the current status and request the decision needed; never silently reopen a terminal task or reset a resumed task to `active`.

Preflight does not own the start transition. When called during execution, return readiness to `task-perform`, which confirms `inprogress` before work.

## Gate 2: Has Requirements

Use the task description as the source of truth for now.

Pass if description is:
- non-empty, and
- specific enough that the agent does not have to guess what to do.

Fail if description is empty or effectively ambiguous, for example:
- blank / whitespace-only,
- placeholder-only (`TODO`, `TBD`, etc.),
- vague-only text (for example: "fix this", "cleanup", "refactor it") without target/outcome.

When failed, stop and ask the user to explain what the task should do.

## Gate 3: Look for Dependencies

Dependencies are expected to be listed in the description, but format is free-form.

### 1) Parse dependency IDs from description

Look for dependency cues (for example: "depends on", "blocked by", "requires", "after") and task references like `#123`.

### 2) Build in-flight task set (same project)

Use the project from Gate 0 and the native `task_list` tool.

Run `task_list` scoped to the same project for statuses:
- `active`
- `waiting`
- `inprogress`

Combine those results into one in-flight task set.

### 3) Check blockers

If any parsed dependency ID is present in the in-flight set above, preflight fails.

- Report each blocking dependency with ID, status, and title.
- Do **not** continue.

If no parsed dependencies are in `active|waiting|inprogress`, pass.

## Required Output Template

Always print this template with all fields present.

```text
=== Task Start Preflight: Task #<id> ===

Task: <title>
Status: <status>

Gate 1 - Is Active: ✅ Pass | ❌ Fail - <reason>
Gate 2 - Has Requirements: ✅ Pass | ❌ Fail - <reason>
Gate 3 - Dependencies Clear: ✅ Pass | ❌ Fail - <reason>

Dependencies Found: <none | #123, #456 | N/A>
Blocking Dependencies:
- <none | #123 <status> - <title>>

Readiness: ✅ READY | ❌ BLOCKED

Next Action: <proceed to next pipeline step | user decision required>
```

## Decision Rules

- If all 3 gates pass: task is READY.
- If any gate fails: task is BLOCKED and preflight stops.
- For status other than `active|inprogress` and missing/ambiguous requirements, ask user what to do next.
- For dependency blockers, do not continue until blockers are resolved or user explicitly overrides policy.
