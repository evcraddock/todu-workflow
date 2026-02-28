# todu-workflow

AI workflow skills for running projects through two connected pipelines:

1. **Project Initialization pipeline** (create a usable project baseline)
2. **Task Workflow pipeline** (execute and close individual tasks)

Compatible with [pi](https://github.com/badlogic/pi-mono), Claude Code, and Codex CLI.

## Core idea

This repo separates **pipeline mechanics** from **project policy**.

- Pipelines define _when_ work phases happen.
- Project documents define _how_ work should be done for that specific project.

That separation is the point.

## Pipeline model

## 1) Project Initialization pipeline

Purpose: set sane defaults based on project type and context.

Initialization handles things like:
- language/framework defaults
- source control host conventions
- quality tooling setup
- optional dev environment/process management
- starter project docs

Projects can be code-heavy, service-heavy, CI/CD-enabled, or text-only. Initialization gives a strong starting point, then the project customizes from there.

Primary skills:
- [project-init](skills/project-init/SKILL.md)
- [repo-create](skills/repo-create/SKILL.md)
- [project-scaffold](skills/project-scaffold/SKILL.md)
- [quality-tooling](skills/quality-tooling/SKILL.md)
- [dev-environment](skills/dev-environment/SKILL.md)

## 2) Task Workflow pipeline

Purpose: pick up a task, execute it using project-owned rules, and close it correctly.

Primary flow:
1. readiness gate (`task-start-preflight`)
2. load project contributing instructions (`docs/CONTRIBUTING.md`, fallback to default)
3. execute task instructions
4. close readiness/verification (`task-close-gate`)

Primary skills:
- [task-pipeline](skills/task-pipeline/SKILL.md)
- [task-start-preflight](skills/task-start-preflight/SKILL.md)
- [task-close-gate](skills/task-close-gate/SKILL.md)
- [pr-review](skills/pr-review/SKILL.md)

## How the pipelines depend on each other

The task pipeline depends on artifacts created by initialization, especially:
- `docs/CONTRIBUTING.md`
- `docs/CODE_STANDARDS.md`

If a project has no `docs/CONTRIBUTING.md`, task workflow can use:
- [`skills/task-pipeline/DEFAULT_CONTRIBUTING.md`](skills/task-pipeline/DEFAULT_CONTRIBUTING.md)

That fallback is intentionally minimal. Real projects should customize their own docs.

## Project-owned policy (important)

Task execution behavior should be owned by the project's documentation, not hardcoded into a global pipeline.

That means each project is expected to customize:
- contributing workflow
- code standards
- verification strategy (format/lint/test)
- review/merge expectations
- environment/runtime assumptions

## Skill index

| Skill | Description |
|---|---|
| [project-init](skills/project-init/SKILL.md) | Initialize a new project end-to-end |
| [repo-create](skills/repo-create/SKILL.md) | Create remote repo, clone locally, register with todu |
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate baseline project files and docs |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, testing, hooks |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up local development process management |
| [task-pipeline](skills/task-pipeline/SKILL.md) | Gated task execution flow |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Task readiness gate |
| [task-close-gate](skills/task-close-gate/SKILL.md) | Close-readiness verification |
| [pr-review](skills/pr-review/SKILL.md) | PR review flow with host-specific workers |
| [tmux](skills/tmux/SKILL.md) | Run commands in separate panes/sessions and orchestrate sub-agent style workflows |
| [electron-testing](skills/electron-testing/SKILL.md) | Electron app testing workflows |

## Quick start

```bash
# Clone
git clone https://github.com/evcraddock/todu-workflow ~/.local/share/todu-workflow

# pi
mkdir -p ~/.pi/agent/skills
ln -s ~/.local/share/todu-workflow/skills ~/.pi/agent/skills/todu-workflow

# Claude Code
mkdir -p ~/.claude/skills
ln -s ~/.local/share/todu-workflow/skills ~/.claude/skills/todu-workflow

# Codex CLI
mkdir -p ~/.codex/skills
ln -s ~/.local/share/todu-workflow/skills ~/.codex/skills/todu-workflow
```

Restart your agent after installing.

## Requirements

- [todu](https://github.com/evcraddock/todu) (task management)
- [gh](https://cli.github.com/) (GitHub operations)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) (Forgejo operations, optional)
- [tmux](https://github.com/tmux/tmux) (interactive session orchestration)

## License

MIT
