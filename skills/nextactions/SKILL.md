---
name: nextactions
description: Recommend what to work on next by priority and dependencies, within a project or across projects. Use for "next actions", "what's next", or "what should I work on". (plugin:todu)
---

# Next Actions

1. Resolve a requested project with `project_show`, reusing a known project ID. Use `task_list` with statuses `active`, `inprogress`, and `waiting`, across all priorities and dates. Scope the query to that project when supplied.
2. Reuse available task details. Use `task_show` for missing context and explicit prerequisites, including cross-project dependencies. Confirm prerequisite completion; surface unfinished, cancelled, or unresolved prerequisites as blockers or decisions.
3. Consider high, then medium, then low priority. Favor ready work, including a lower-priority prerequisite that advances a higher-priority goal. Follow relevant dependency chains to actionable work, identifying cycles and checking alternative prerequisites when one is blocked.
4. Recommend a task to start or resume with its title, ID, project, status, priority, and a brief reason. Explain relevant blockers and the higher-priority goal a prerequisite advances.

When a recommendation is unavailable, distinguish blocked work, incomplete evidence, and an empty backlog. Label recommendations based on incomplete evidence as provisional.
