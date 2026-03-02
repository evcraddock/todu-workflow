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

## Required workflow

1. Work only within the requested scope.
2. Read relevant files before editing.
3. Make the smallest change that satisfies the request.
4. If blocked by missing information, ambiguity, or conflicts, stop and report `BLOCKED` with reason.
5. Do not add manual line breaks in markdown paragraphs.
6. Run relevant verification for the change.
7. Report changed files and verification results clearly, including whether the request appears satisfied.
