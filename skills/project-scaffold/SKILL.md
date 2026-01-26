---
name: project-scaffold
description: Generate basic project scaffolding files (README, LICENSE, .gitignore, AGENTS.md, docs/, PR template). Use when setting up a new project or asked to "scaffold project", "create project files", or similar.
---

# Project Scaffold

Generate foundational project files appropriate for the tech stack.

## When to Use

After a repository has been created and cloned, use this skill to generate:
- README.md
- LICENSE
- .gitignore
- AGENTS.md
- docs/CONTRIBUTING.md
- docs/CODE_STANDARDS.md
- PR template

## Required Inputs

Before generating files, you need:
- `name` - Project name
- `description` - Brief project description
- `stack` - typescript, go, python, or rust
- `framework` - (optional) hono, express, gin, echo, fastapi, flask, actix, etc.
- `host` - github or forgejo (determines PR template location)
- `localPath` - Where to write files

## File Generation

Generate each file using the `write` tool. Change to the project directory first:

```bash
cd {localPath}
```

### 1. LICENSE (MIT)

Use the template from `templates/license/MIT.txt`.

Replace placeholders:
- `{year}` - Current year
- `{author}` - Get from `git config user.name` or use project owner

### 2. .gitignore (Stack-Specific)

Use the appropriate template from `templates/gitignore/`:

| Stack | Template |
|-------|----------|
| typescript | `templates/gitignore/typescript.gitignore` |
| go | `templates/gitignore/go.gitignore` |
| python | `templates/gitignore/python.gitignore` |
| rust | `templates/gitignore/rust.gitignore` |

Read the template file and write it to `.gitignore` in the project.

### 3. README.md

```markdown
# {name}

{description}

## Getting Started

### Prerequisites

{prerequisites based on stack}

### Installation

{install commands based on stack}

### Development

{dev commands based on stack}

## Testing

{test commands based on stack}

## License

MIT
```

**Stack-specific sections:**

#### TypeScript Prerequisites
```markdown
- Node.js 20+ or Bun 1.0+
- npm, yarn, or bun
```

#### TypeScript Installation
```markdown
```bash
# Using npm
npm install

# Or using bun
bun install
```
```

#### TypeScript Development
```markdown
```bash
npm run dev
# or
bun run dev
```
```

#### Go Prerequisites
```markdown
- Go 1.21+
```

#### Go Installation
```markdown
```bash
go mod download
```
```

#### Go Development
```markdown
```bash
go run .
```
```

#### Python Prerequisites
```markdown
- Python 3.11+
- pip or uv
```

#### Python Installation
```markdown
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or with uv
uv pip install -r requirements.txt
```
```

#### Python Development
```markdown
```bash
python -m {name}
# or for web frameworks
uvicorn app.main:app --reload
```
```

#### Rust Prerequisites
```markdown
- Rust 1.75+ (via rustup)
```

#### Rust Installation
```markdown
```bash
cargo build
```
```

#### Rust Development
```markdown
```bash
cargo run
```
```

### 4. AGENTS.md

```markdown
# AI Agent Guidelines for {name}

## Required Reading

- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) - workflow and PR process
- [docs/CODE_STANDARDS.md](docs/CODE_STANDARDS.md) - code style and patterns

## Project Overview

{description}

## Tech Stack

- Language: {stack}
- Framework: {framework or "None"}

## Task Lifecycle

- **Starting**: Run `task-start-preflight` skill
- **Closing**: Run `task-close-preflight` skill

## PR Workflow

1. Create feature branch: `feat/<task-id>-<description>`
2. Run `./scripts/pre-pr.sh` before opening PR
3. After CI passes, request review

## Conventions

{stack-specific conventions}
```

**Stack-specific conventions:**

#### TypeScript Conventions
```markdown
- Use TypeScript strict mode
- Prefer named exports over default exports
- Use path aliases for imports (@/...)
- Handle null explicitly with ?? and ?.
- Write tests with Vitest or Jest
```

#### Go Conventions
```markdown
- Follow standard Go project layout
- Use gofmt for formatting
- Handle errors explicitly, don't ignore them
- Use table-driven tests
- Document exported functions
```

#### Python Conventions
```markdown
- Use type hints for all functions
- Format with Ruff (ruff format)
- Lint with Ruff (ruff check)
- Use pytest for testing
- Follow PEP 8 naming conventions
```

#### Rust Conventions
```markdown
- Use rustfmt for formatting
- Run clippy for linting
- Handle errors with Result, avoid unwrap()
- Document public items with ///
- Write tests in the same file with #[cfg(test)]
```

### 5. docs/CONTRIBUTING.md

```markdown
# Contributing

This project uses an AI-first development process. Agents do the work, automation enforces quality, humans approve.

## Workflow

### 1. Pick Up a Task

Get assigned a task or pick from available tasks. Understand requirements before starting.

### 2. Create a Branch

```bash
git checkout main && git pull
git checkout -b feat/{task-id}-short-description
```

Branch prefixes:
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `chore/` - Maintenance

### 3. Implement

- Follow [CODE_STANDARDS.md](CODE_STANDARDS.md)
- Write tests as you go
- Commit frequently with clear messages

Commit format:
```
<type>: <short description>

Task: #<task-id>
```

### 4. Verify Quality

Before opening a PR:

```bash
./scripts/pre-pr.sh
```

Do not open a PR if this fails.

### 5. Open PR

Push and create PR with clear description linking to the task.

### 6. Review and Merge

- CI must pass
- Address review feedback
- Squash and merge after approval

## When Stuck

After 3 failed attempts at the same problem:

1. Stop - Don't keep trying the same approach
2. Document - What was tried and why it failed
3. Ask - Request guidance or suggest alternatives
```

### 6. docs/CODE_STANDARDS.md

Generate appropriate standards for the stack. Use the TypeScript example as a template but adapt for:

- **Go**: gofmt, golangci-lint, error handling patterns, table tests
- **Python**: Ruff, type hints, pytest patterns, PEP 8
- **Rust**: rustfmt, clippy, Result handling, documentation

Keep it concise but useful. Focus on:
- Formatting (what tool, how to run)
- Linting (what tool, common issues)
- Type safety (strict mode, type hints, etc.)
- Error handling patterns
- Testing patterns
- File organization

### 7. PR Template

Create at `.github/pull_request_template.md` for GitHub or `.forgejo/pull_request_template.md` for Forgejo:

```markdown
## Summary

<!-- Brief description of changes -->

## Task

<!-- Link to task: #123 -->

## Changes

<!-- List key changes -->
- 

## Testing

<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Manual testing performed

## Checklist

- [ ] `./scripts/pre-pr.sh` passes
- [ ] Documentation updated (if needed)
- [ ] No unrelated changes included
```

## Verification

After generating all files, verify:

```bash
ls -la {localPath}
ls -la {localPath}/docs/
cat {localPath}/AGENTS.md
```

## Notes

- Use current year for LICENSE copyright
- Adapt language to match project context
- Keep files concise but complete
- AGENTS.md should be genuinely useful for future AI work on this project
