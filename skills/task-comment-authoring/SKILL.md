---
name: task-comment-authoring
description: Draft and refine structured markdown task notes and comments.
---

# Task Comment Authoring

Use this skill to author task comment content.

It produces:

- a clearer markdown task comment
- an inferred comment type when useful

Possible types: `status-update`, `completion`, `blocker`, `review-summary`

It does not post the task comment.

## When to use

Use `task-comment-authoring` when:

- a user wants help writing a task update or note
- a workflow needs clean markdown before handing it to task comment or note tooling
- a draft task comment is vague, unstructured, or too long

## Rules

- gather only the missing context
- do not invent facts
- output proper markdown
- prefer a short heading and bullets for non-trivial updates
- allow one-line comments for small updates
- keep comments professional and specific about what changed
- avoid placeholder text like `TODO` or `TBD`

## Status update shape

```md
### Update

- Completed <work item>
- Verified <check or evidence>
- Next: <next step>
```

`Verified` and `Next` are optional, but include them when they add useful context.

## Completion summary shape

```md
### Completed

- Implemented <change>
- Verified <check or evidence>
```

`Verified` is strongly preferred for completion comments.

## Blocker update shape

```md
### Blocker

- Blocked by <issue>
- Impact: <what cannot proceed>
- Need: <decision, dependency, or fix>
```

## Review summary shape

```md
### Review update

- PR: <status or link>
- Result: <approved | warnings | changes requested>
- Follow-up: <next action>
```

## Process

1. Infer the comment type.
2. Ask only for missing comment-defining details.
3. Draft the markdown comment.
4. Check that longer comments use a short heading and bullets.
5. Return the authored comment content.
