# AI Agent Guidelines for {name}

## Required Reading

- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) - workflow and PR process
- [docs/CODE_STANDARDS.md](docs/CODE_STANDARDS.md) - code style and patterns

## Project Overview

{description}

## Tech Stack

- Language: Go
- Framework: {framework}

## Task Lifecycle

- **Starting**: Run `task-start-preflight` skill
- **Closing**: Run `task-close-preflight` skill

## PR Workflow

1. Create feature branch: `feat/<task-id>-<description>`
2. Run `./scripts/pre-pr.sh` before opening PR
3. After CI passes, request review

## Conventions

- Follow standard Go project layout
- Use gofmt for formatting
- Handle errors explicitly, don't ignore them
- Use table-driven tests
- Document exported functions
