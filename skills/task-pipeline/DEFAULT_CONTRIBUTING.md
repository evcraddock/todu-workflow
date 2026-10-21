# Default Contributing Instructions

To create project-specific instructions, copy this file to `docs/CONTRIBUTING.md` and customize it.

## Start-of-Work Preview (Required)

Before implementation, print the full preview as a normal assistant message (not in a selection prompt UI).

Use this template:

```text
=== Work Preview ===

Work Item: <title>
Contributing Source: DEFAULT_CONTRIBUTING.md
Implementation Input Source: <request/spec/issue description>

Objective:
- <one-sentence objective>

Acceptance Criteria:
- [ ] <criterion 1>
- [ ] <criterion 2>

Planned Steps:
1. <step 1>
2. <step 2>
3. <step 3>
```

- Include all acceptance criteria from the implementation input when present (no omissions).
- After showing the preview, ask a separate short confirmation question: `Continue?`
- user confirms (`yes`) → return `READY` and continue
- user declines/defers (`no`) → return `BLOCKED`
- After confirmation and before implementation, if the work is associated with a task, add a comment to that task containing the confirmed implementation plan using the preview template above.

## Required workflow

1. Make the smallest change that satisfies the request.
2. If blocked by missing information, ambiguity, or conflicts, stop and report `BLOCKED` with reason.
3. Report changed files and verification results clearly, including whether the request appears satisfied. If the work is associated with a todu task, also add a comment to that task containing this report.
