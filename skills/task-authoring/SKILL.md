---
name: task-authoring
description: Draft or refine task titles and markdown descriptions from user intent without inventing scope. Use before creating or updating task content.
---

# Task Authoring

Write enough for a later session to understand the task. Use the conversation and existing draft to capture the problem, desired outcome, relevant context, and user constraints when known.

- Preserve supplied requirements, acceptance criteria, and dependencies. When editing, change only what was requested.
- Do not invent facts or add unapproved scope, deliverables, testing obligations, or implementation choices. Label useful agent suggestions as unapproved; suggestions are not user decisions.
- Ask only when missing intent prevents a useful draft. Leave implementation planning and nonblocking questions for pickup.
- For bugs, include observed/expected behavior, environment, and reproduction details when supplied; do not demand a bug template.

Return a clear title of 60 characters or fewer and a concise markdown description. Use prose or bullets, with headings only when helpful. No mandatory sections, empty placeholders, or implementation-ready specification.

This skill drafts task content, not progress comments or execution plans. Draft-only requests stop at the draft; requested backend creation or updates use native task tools separately.
