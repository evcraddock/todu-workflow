---
name: task-authoring
description: Draft and refine task titles and structured markdown descriptions before creating tasks. Use for task-creation flows that benefit from authoring help.
---

# Task Authoring

Create high-quality task descriptions as a workflow layer above low-level task creation.

## Purpose

Use this workflow whenever a task-creation flow should apply authoring policy before persistence.

This workflow is responsible for:
- gathering or confirming the minimum context needed to write a solid task
- improving or normalizing the title when needed
- shaping the description into proper markdown
- applying task-type-specific structure
- getting user approval on the authored result when appropriate for the calling flow
- delegating the final create operation to a low-level tool

This workflow is **not** responsible for backend record creation policy. It should delegate creation instead of duplicating backend write logic.

## When to use this workflow

Use `task-authoring` when:
- the user directly asks to create a task, issue, or bug report
- a higher-level workflow entry point wants better title/description shaping
- the task description is incomplete, vague, or only partially structured
- the agent needs to ask follow-up questions before a task can be created
- the user already supplied most fields, but the request should still go through the authoring policy before creation
- the user wants help drafting or normalizing a better task description
- a workflow-generated task would benefit from improved title or markdown structure before being written

Examples:
- "Create a task for adding webhook retries"
- "Help me write a bug report for the login crash"
- "Add an issue for improving sync conflict handling"

## Low-level create delegation

Low-level create tools are persistence backends. They add the record; they should not be the place where task meaning is authored.

Preferred model:
- use `task-authoring` to determine or refine what the task actually is
- then delegate the final record write to any available low-level create path

A caller may skip this skill only when equivalent authoring policy has already been applied elsewhere and only persistence remains.

Examples:
- `task-authoring` has already produced the final payload and is handing off to the backend create step
- a migration or importer must preserve an already-authored external task verbatim
- another workflow has already applied equivalent title/description shaping and is now only writing the record

Do **not** bypass `task-authoring` for a task-creation entry point just because `projectId`, title, or a draft description are already present.

## Required inputs before create

Do not create the task until these are known:
- `projectId` (explicit, never guessed silently)
- `title`
- `description` in proper markdown

Optional inputs when available:
- task type (`implementation` or `bug`)
- any extra metadata supported by the selected low-level create tool

## Context gathering rules

Gather only the missing information needed to produce a good task.

1. Reuse explicit context from the user first.
2. Infer task type when the signal is strong.
   - words like `bug`, `crash`, `fails`, `regression`, `broken` => `bug`
   - feature/change/build/add/implement style requests => `implementation`
3. If `projectId` is missing, ask for it. Do not guess silently.
4. Ask focused follow-up questions only for missing task-defining information.
5. Stop asking once the workflow has enough information to produce a concrete markdown draft.

Minimum follow-up topics when missing:
- for implementation tasks: desired outcome, concrete requirements, boundaries, acceptance criteria
- for bug tasks: reproduction steps, expected behavior, actual behavior, impact/context, acceptance criteria for resolution

## Output requirements

Every authored task description must be valid markdown and readable on its own.

Rules:
- use markdown headings and lists
- do not return plain unstructured prose when a structured task is appropriate
- include only sections supported by the available information
- do not invent facts; ask when a missing detail is necessary
- avoid placeholder-only sections like `TODO` or `TBD`

## Task type templates

### Implementation task template

Use this structure for implementation-oriented work.

```md
## Goal

<one short paragraph describing the desired outcome>

## Background

<optional context, constraints, links, or current behavior>

## Requirements

- <requirement 1>
- <requirement 2>

## Scope

- In scope:
  - <item>
- Out of scope:
  - <item>

## Acceptance criteria

- [ ] <observable outcome 1>
- [ ] <observable outcome 2>
```

Requirements:
- `## Requirements` is mandatory
- `## Acceptance criteria` is mandatory
- `## Background` and `## Scope` are recommended when helpful

### Bug task template

Use this structure for bug reports and bug-fix tasks.

```md
## Summary

<short description of the bug and why it matters>

## Environment

- App/version: <if known>
- Platform: <if known>
- Context: <if known>

## Steps to reproduce

1. <step 1>
2. <step 2>
3. <step 3>

## Expected behavior

- <expected result>

## Actual behavior

- <actual result>

## Impact

- <user/system impact>

## Acceptance criteria

- [ ] <documented reproduction path is addressed>
- [ ] <expected behavior is restored>
- [ ] <relevant regression protection exists or the task explains why not>
```

Requirements:
- reproduction-oriented sections are mandatory: `## Steps to reproduce`, `## Expected behavior`, `## Actual behavior`
- `## Acceptance criteria` should be included when the task is to fix or verify the bug
- omit unknown environment details instead of fabricating them

## Authoring process

1. Identify task type.
   - `implementation` or `bug`
   - if unclear, ask a short clarifying question
2. Gather minimum context.
   - ask only for missing information required by the chosen template
3. Draft the markdown description.
4. Validate the draft.
   - implementation tasks must include `Requirements` and `Acceptance criteria`
   - bug tasks must include reproduction-oriented structure
   - markdown must be clean and complete enough that another agent can act without guessing
5. Preview the final task payload for the user.
6. Ask for approval before creation.
7. Delegate creation to the low-level tool.

## Create handoff

Preferred handoff:
- delegate to whichever low-level create capability is available in the environment
- if native `task_create` exists, it is a good handoff target
- if another backend-specific create tool or skill exists, that is also acceptable

Example low-level payload shape:

```text
create_task_like_backend_call({
  title: <title>,
  projectId: <explicit project id>,
  description: <final markdown description>
})
```

Pass only fields the selected low-level create path explicitly supports.

Compatibility rule:
- do not hard-depend on `todu-pi-extensions` or any other specific backend provider from this skill
- keep the authoring policy reusable across environments with different create backends
- do not duplicate storage write logic in this authoring workflow unless the environment explicitly requires a low-level fallback

## Approval step

Before creating the task, show the user:
- title
- `projectId`
- task type
- final markdown description
- any extra fields that will be sent through a richer backend-specific create tool, if applicable

Then ask for explicit approval.

If the user does not approve, revise the draft or stop.

## Suggested prompts

Use short, targeted prompts such as:
- "What project should this task belong to? I need the explicit project ID."
- "Is this an implementation task or a bug report?"
- "What are the must-have requirements?"
- "What should be true for this task to count as done?"
- "What are the exact steps to reproduce the bug?"
- "What did you expect to happen, and what happened instead?"

## Example decision guide

### Example A: use `task-authoring`

User: "Create a task for improving sync conflict handling"

Reason:
- project may be missing
- requirements are underspecified
- acceptance criteria still need shaping

### Example B: backend handoff only

Caller already has:
- `projectId: todu-workflow`
- title: `Design initial sync API`
- complete markdown description produced by `task-authoring` or equivalent policy

Reason:
- authoring is already done
- only persistence remains
