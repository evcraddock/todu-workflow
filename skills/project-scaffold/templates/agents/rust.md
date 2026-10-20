# AI Agent Guidelines for {name}

## Required Reading

Before working, read and follow:
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) - workflow and PR process
- [docs/CODE_STANDARDS.md](docs/CODE_STANDARDS.md) - code style and patterns

You MUST follow these guidelines throughout your work.

## Project Overview

{description}

## Tech Stack

- Language: Rust
- Framework: {framework}

## Development

**ALWAYS start the dev server using `make dev`** - this runs all services (app, database, etc.) via the Makefile.

Key Makefile targets:
- `make dev` - Start development server (REQUIRED)
- `make test` - Run tests
- `make lint` - Run linter
- `make fmt` - Format code

Read the Makefile to understand available commands before starting work.

## Dependencies

When adding crates:
- Use latest **STABLE** versions only
- Reject canary/beta/alpha/rc versions unless user explicitly approves
- Check crates.io for stable releases

Non-stable versions (canary, beta, alpha, rc) can have bugs or incomplete features. Always ask before using them.

## Task Lifecycle

Use `task-perform` to execute Todu tasks as written, record results, and close finished work. Readiness and completion-assessment skills are available when explicitly requested; they are not automatic steps. Follow the project development requirements below for repository changes.

## PR Workflow (Mandatory Sequence)

After implementation is complete, execute this exact order:

1. Run `./scripts/pre-pr.sh`
2. Push branch and open/update PR
3. Resolve CI gate:
   - If checks exist: wait for green
   - If checks fail: fetch failures, fix, rerun `./scripts/pre-pr.sh`, push, re-check
   - If checks cannot be verified automatically (e.g., Forgejo without CI integration): stop and ask the human whether to continue without a CI signal
4. Run the `pr-review` skill for independent review
5. Report review result with explicit pipeline state
6. Stop and wait for explicit human merge approval

Do not ask "want me to...?" for required next steps.

## Conventions

- Use rustfmt for formatting
- Run clippy for linting
- Handle errors with Result, avoid unwrap()
- Document public items with ///
- Write tests in the same file with #[cfg(test)]
