---
name: task-start-preflight
description: Verify a task is ready to be worked on. Use when user says "start preflight", "run preflight", "task preflight", or similar.
---

# Task Start Preflight

Preflight is a readiness gate. It does **not** plan implementation and does **not** execute work.

## Purpose

Confirm whether a task is ready to be worked on by checking:
1. task status (`active` only),
2. task requirements (not empty/ambiguous),
3. dependency blockers (none may be `active`, `waiting`, or `inprogress`).

## Execution Contract (Required)

- Input: task ID.
- Gate 0 must load task details by delegating to the `task-show` skill.
- Run the 3 gates in order.
- Stop on first failed gate.
- Do not make side-effecting changes in preflight unless user explicitly asks.
- Always output the preflight summary template.

## Gate 0: Load Task Details via `task-show`

Invoke the `task-show` skill with `<task-id>` and use its returned task object as the source of truth for this preflight.

If `task-show` cannot find or load the task, fail preflight immediately and stop.

Collect at minimum:
- `id`
- `title`
- `status`
- `description`
- `project` (name or ID)

## Gate 1: Is Active

Preflight only applies to tasks with status `active`.

- If status is `active`: pass.
- If status is anything else: fail and stop.

When failed, report current status and ask user what to do:
- set status to `active` and rerun preflight,
- proceed without preflight,
- stop.

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

Use the project from Gate 0 and delegate list queries to the `task-list` skill.

Run `task-list` scoped to the same project for statuses:
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
- For non-`active` status and missing/ambiguous requirements, ask user what to do next.
- For dependency blockers, do not continue until blockers are resolved or user explicitly overrides policy.
