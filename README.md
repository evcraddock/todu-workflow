# todu-workflow

AI workflow skills for running projects through two connected pipelines:

1. **Project Initialization pipeline** (create a usable project baseline)
2. **Development Delivery pipeline** (when explicitly requested or selected by project policy)

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
- [project-scaffold](skills/project-scaffold/SKILL.md)
- [quality-tooling](skills/quality-tooling/SKILL.md)
- [dev-environment](skills/dev-environment/SKILL.md)

## Task Authoring

Use the authoring skill when capturing or refining task content.

Use [task-authoring](skills/task-authoring/SKILL.md) to capture the problem, desired outcome, relevant context, and explicit user constraints without inventing scope. Concise prose or bullets are enough; there are no mandatory sections or bug templates. Keep agent suggestions distinct from user decisions, and leave detailed requirements clarification and implementation planning for pickup. The skill returns content; the caller handles any requested backend creation or update.

## Task Comments

Draft comments directly in chat or the posting workflow; no separate authoring skill is needed. Keep updates factual and proportional, preserve supplied constraints, and include relevant verification evidence without inventing results. One sentence can be enough; there is no mandatory generic template. Draft-only requests do not authorize posting. An explicit posting request or an already-authorized workflow uses native `task_comment_create` with the resolved task ID and `content`, without another default approval step. Confirm success before claiming the comment was posted; a comment request alone does not authorize starting or closing a task.

## 2) Development Delivery pipeline

Ordinary task execution and completion use native task tools and project instructions. There is no dedicated task-execution skill or replacement workflow.

[task-pipeline](skills/task-pipeline/SKILL.md) is a separate development delivery workflow, selected only when the user/task requests that pipeline or project instructions explicitly select it—not by repository changes or individual PR/merge requirements alone. It owns development planning and delivery stages (checks, PR, independent review, human-approved merge) and returns the result without changing task status or posting task comments. `task-start-preflight` and `task-close-gate` remain available for requested read-only assessments; neither is mandatory for ordinary execution.

Primary skills:
- [task-authoring](skills/task-authoring/SKILL.md)
- [task-pipeline](skills/task-pipeline/SKILL.md) (requested development delivery)
- [task-start-preflight](skills/task-start-preflight/SKILL.md)
- [task-close-gate](skills/task-close-gate/SKILL.md)
- [pr-review](skills/pr-review/SKILL.md)

## How the pipelines depend on each other

The task pipeline depends on artifacts created by initialization, especially:
- `docs/CONTRIBUTING.md`
- `docs/CODE_STANDARDS.md`

When task-pipeline is selected and a project has no `docs/CONTRIBUTING.md`, the development pipeline uses:
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
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate baseline project files and docs |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, testing, hooks |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up local development process management |
| [task-authoring](skills/task-authoring/SKILL.md) | Capture user intent in task descriptions without inventing scope |
| [task-pipeline](skills/task-pipeline/SKILL.md) | Development delivery when requested or required by project policy |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Requested read-only readiness assessment |
| [task-close-gate](skills/task-close-gate/SKILL.md) | Evidence-based completion assessment without task mutations |
| [pr-review](skills/pr-review/SKILL.md) | PR review flow with host-specific workers |
| [tmux](skills/tmux/SKILL.md) | Explicit tmux/terminal sessions with exact owned-resource handling; not generic agent delegation |
| [electron-testing](skills/electron-testing/SKILL.md) | Electron app testing workflows |
| [radicale-calendar](skills/radicale-calendar/SKILL.md) | Safely manage Radicale CalDAV events through a structured JSON CLI |

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
```

Restart your agent after installing.

### Codex plugin

This repository is a Codex plugin containing all bundled skills. It uses `.codex-plugin/plugin.json` and does not need a link under `~/.codex/skills`.

To install from a local checkout, add an entry to the `plugins` array in `~/.agents/plugins/marketplace.json` (preserve any existing entries):

```json
{
  "name": "todu-workflow",
  "source": {
    "source": "local",
    "path": "./path/from/home/to/todu-workflow"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

The personal marketplace should have a top-level `"name": "local"` and a `plugins` array. The source path is relative to your home directory and must point to this repository's root. Then install and verify:

```bash
codex plugin add todu-workflow@local
codex plugin list --marketplace local
```

Restart the desktop app and open a new chat to load the plugin skills. The plugin appears as **Todu Workflow** under **Local Plugins**. After updating the checkout, rerun the install command to refresh the cached copy. Remove an old `~/.codex/skills/todu-workflow` symlink, if present, to avoid duplicate skills.

## Radicale calendar CLI

This repository also ships the installable `radicale-calendar` Python CLI and its globally discoverable pi skill. See [Radicale Calendar CLI](docs/radicale-calendar.md) for secure configuration, JSON schemas, supported recurrence behavior, and test instructions.

## Requirements

- [todu](https://github.com/evcraddock/todu) (task management)
- [gh](https://cli.github.com/) (GitHub operations)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) (Forgejo operations, optional)
- [tmux](https://github.com/tmux/tmux) (interactive session orchestration)

## License

MIT
