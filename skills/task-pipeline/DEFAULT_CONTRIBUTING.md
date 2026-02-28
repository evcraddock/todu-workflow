# Default Contributing Instructions

To create project-specific instructions, copy this file to `docs/CONTRIBUTING.md` and customize it.

## Fallback Activation + Start Preview (Required)

Before doing any implementation work with this default file:
- First, print the full preview template as a normal assistant message.
- Do not put the full preview text inside a selection prompt UI.
- Display the full template exactly (all sections/lines), populate placeholders, and do not summarize or truncate.

```text
=== Task Pipeline Preview: Task #<id> ===

Task: <title>
Preflight: READY (task-start-preflight passed)
Contributing Source: DEFAULT_CONTRIBUTING.md
Project-specific option: create docs/CONTRIBUTING.md by copying/customizing this file
Task Instructions Source: task description
Closure Gate: task-close-preflight

Task Objective:
- <one-sentence summary from task description>

Acceptance Criteria:
- [ ] <criterion 1>
- [ ] <criterion 2>

Next Steps:
1. Follow default contributing instructions
2. Execute task description instructions
3. Run required verification
4. Run task-close-preflight
```

- Include all acceptance criteria from the task description when present (no omissions).
- After showing the full preview, ask a separate short confirmation question: `Continue anyway?`
- user confirms (`yes`) → return `READY` and continue
- user declines/defers (`no`) → return `BLOCKED`

## Required workflow

1. Work only within task scope.
2. Read relevant files before editing.
3. Make the smallest change that satisfies the task.
4. Set task status to `inprogress` via `task-update` when implementation starts.
5. If blocked or requirements are ambiguous, stop and report `BLOCKED` with reason.
6. Add task comments only via the `task-comment-create` skill.
7. Do not add manual line breaks in markdown paragraphs.
8. Summarize changed files and verification results.
