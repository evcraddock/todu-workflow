---
name: task-authoring
description: Draft and refine task titles and structured markdown task content.
---

# Task Authoring

Use this skill to author task content.

It produces:
- a better title
- a structured markdown description
- an inferred task type when useful (`implementation` or `bug`)

It does not create the task record.

## When to use

Use `task-authoring` when:
- a user asks to create a task or bug
- a draft title or description is weak
- a workflow wants better task content before writing the record

## Rules

- gather only the missing context
- do not invent facts
- do not invent dependency IDs
- keep the title to 60 characters or fewer
- output proper markdown
- prefer clear headings and lists
- avoid placeholder text like `TODO` or `TBD`

## Implementation task shape

```md
## Goal

<desired outcome>

## Requirements

- <requirement>

## Acceptance criteria

- [ ] <observable outcome>

## Dependencies

- <task-id or None>
```

`Requirements`, `Acceptance criteria`, and `Dependencies` are required. Use real task IDs when known.

## Bug task shape

```md
## Summary

<what is broken>

## Steps to reproduce

1. <step>

## Expected behavior

- <expected>

## Actual behavior

- <actual>

## Acceptance criteria

- [ ] <resolved outcome>
```

`Steps to reproduce`, `Expected behavior`, and `Actual behavior` are required.

## Process

1. Infer `implementation` or `bug`.
2. Ask only for missing task-defining details, including dependencies when they affect execution order or readiness.
3. Draft the title and markdown description.
4. Check that the title is 60 characters or fewer and the required sections exist.
5. Return the authored content.
