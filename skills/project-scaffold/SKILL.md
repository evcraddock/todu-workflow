---
name: project-scaffold
description: Generate basic project scaffolding files (README, LICENSE, .gitignore, AGENTS.md, docs/, PR template). Use when setting up a new project or asked to "scaffold project", "create project files", or similar.
---

# Project Scaffold

Generate foundational project files appropriate for the tech stack.

## When to Use

After a repository has been created and cloned, use this skill to generate scaffolding files.

## Required Inputs

- `name` - Project name
- `description` - Brief project description
- `stack` - typescript, go, python, or rust
- `framework` - (optional) hono, express, gin, echo, fastapi, flask, actix, etc.
- `host` - github or forgejo (determines PR template location)
- `localPath` - Where to write files
- `dev_task_url` - URL to the "Set up dev environment" task (for README link)

## Files to Generate

| File | Template | Notes |
|------|----------|-------|
| LICENSE | `templates/license/MIT.txt` | Replace `{year}`, `{author}` |
| .gitignore | `templates/gitignore/{stack}.gitignore` | |
| README.md | `templates/readme/{stack}.md` | Replace `{name}`, `{description}` |
| AGENTS.md | `templates/agents/{stack}.md` | Replace `{name}`, `{description}`, `{framework}` |
| docs/CONTRIBUTING.md | `templates/docs/CONTRIBUTING.md` | |
| docs/CODE_STANDARDS.md | `templates/docs/CODE_STANDARDS-{stack}.md` | |
| PR template | `templates/pr-template/pull_request_template.md` | Location: `.github/` or `.forgejo/` based on host |

## Process

1. Change to project directory: `cd {localPath}`
2. For each file:
   - Read the appropriate template
   - Replace placeholders with actual values
   - Write to destination using `write` tool (overwrites existing files)
3. Verify files were created

## Re-running on Existing Projects

All scaffold files are **overwritten** when re-running. This ensures projects stay in sync with the current templates.

## Placeholders

| Placeholder | Value |
|-------------|-------|
| `{name}` | Project name |
| `{description}` | Project description |
| `{stack}` | Language (typescript, go, python, rust) |
| `{framework}` | Framework name or "None" |
| `{host}` | Source control host (`github` or `forgejo`) |
| `{year}` | Current year |
| `{author}` | From `git config user.name` |
| `{dev_task_url}` | URL to "Set up dev environment" task |

## Verification

After generating files:

```bash
ls -la {localPath}
ls -la {localPath}/docs/
```

## Notes

- All templates are in the `templates/` subdirectory of this skill
- PR template goes to `.github/` for GitHub, `.forgejo/` for Forgejo
- AGENTS.md should be genuinely useful for future AI work
