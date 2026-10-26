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

Return a clear title of 60 characters or fewer and a concise markdown description. Use polished, direct language that defines the work rather than informal planning notes.

When helpful, separate **Purpose** (why the work matters or the desired outcome) from **Scope** (what work is included), or use another structure suited to the task. Use prose or bullets for simple tasks; do not add headings that merely repeat the same information. No mandatory sections, including requirements or acceptance criteria; no empty placeholders or implementation-ready specification.

For example, for “Help Drew set up his personal blog website,” the purpose is to create a Slugkit blog and introduce AI-assisted application development; the scope is helping Drew set up and customize the site. Use this distinction to organize supplied intent, not to add goals or work the user did not provide.

This skill drafts task content, not progress comments or execution plans. Draft-only requests stop at the draft; requested backend creation or updates use native task tools separately.
