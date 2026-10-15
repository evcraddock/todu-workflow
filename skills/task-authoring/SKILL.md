---
name: task-authoring
description: Capture and refine task titles and markdown descriptions from user intent without inventing scope. Use before creating or updating task content. Does not create backend task records.
---

# Task Authoring

Capture enough intent for a later session to understand the task, without treating agent assumptions as user-approved scope. Return a clear title and markdown description; creating or updating the backend record belongs to the caller.

## When to use

- A user asks to create or draft a task or bug.
- A draft title or description needs clarification or refinement.
- A workflow needs authored content before writing the task record.

Execution/pickup requests belong to `task-perform`; progress notes and comments are not task descriptions.

## Capture intent, not an implementation plan

Use the conversation and existing task content to capture what is known:

- **Problem:** what is wrong or why the work matters.
- **Desired outcome:** what the user wants to change.
- **Relevant context:** facts, observations, references, and explicit dependencies.
- **User constraints:** agreed scope, exclusions, requirements, and acceptance conditions, when supplied.

Do not require every item when it is unknown or unnecessary. Preserve the user's intent and explicit constraints when refining an existing task; change only what was requested.

Do not invent facts, dependency IDs, requirements, acceptance criteria, or additional deliverables. Do not add production validation, rollout work, testing obligations, or other plausible best practices as approved scope unless the user requested or agreed to them. Preserve such requirements when they are explicit.

Distinguish user decisions from agent suggestions. Omit unneeded suggestions; if useful to retain, label them as unapproved suggestions rather than placing them among requirements or acceptance criteria. A prior agent recommendation is not user agreement.

Detailed requirements clarification, implementation choices, and execution planning belong at pickup. Ask a focused question only when missing task-defining intent prevents a useful capture (for example, the target or desired change is unknown). Do not require implementation-ready specifications to save a task. Record unresolved questions only when useful, clearly as questions for pickup rather than decisions or blockers.

For bugs, capture the observed and expected behavior, environment, and reproduction details when known. Missing diagnostics or reproduction steps do not justify inventing them or requiring a completed bug template.

## Flexible output

- Keep the title clear and 60 characters or fewer.
- Use concise prose or bullets in proper markdown. Add headings only when they improve readability.
- No task-type classification, fixed template, or mandatory sections. Omit empty sections and placeholder text such as `TODO` or `TBD`.
- Include supplied acceptance criteria and dependencies where useful without generating them to fill a template.

A short capture can be enough:

```md
Title: Retry transient webhook failures

Failed webhook deliveries currently disappear. Retry transient failures so those deliveries are not lost.
```

Use more detail only when the conversation supplies it. Do not infer a retry policy, infrastructure, or production-validation requirement from this example.

## Process

1. Identify the user's problem, desired outcome, relevant context, and explicit constraints from the available conversation or existing draft.
2. Ask only for missing intent that prevents useful capture; leave useful nonblocking questions for pickup.
3. Draft the title and description in the simplest useful form.
4. Check that facts and constraints are faithful, suggestions are not presented as decisions, and no speculative scope or empty sections were added.
5. Return the authored content to the caller. Draft-only requests stop here; an explicit request to create or update the task continues through the caller's backend task tools, not this skill itself.
