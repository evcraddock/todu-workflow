---
name: nextactions
description: Show prioritized Todu next actions. Use when user asks "next actions", "what's next", or "what should I work on". Do not use for general task search. (plugin:todu)
---

# Next Actions

Shows tasks that need attention by querying:
1. Tasks with status `inprogress`
2. Tasks with status `active` and priority `high`
3. Active tasks due or scheduled today
4. Active overdue tasks

## CLI Commands

```bash
todu task list --status inprogress
todu task list --status active --priority high
todu task list --status active --today
todu task list --status active --overdue
```

## Process

1. Run the relevant queries
2. Deduplicate by task ID
3. Sort by due date (earliest first, nulls last)
4. Display as a single list or table

## Output Format

| ID  | Title               | Project | Due Date   |
|-----|---------------------|---------|------------|
| 159 | Benefits Enrollment | ntrs    | 2026-03-19 |
| 218 | Review PR           | Inbox   | -          |

If no tasks are found: `No next actions found`.
