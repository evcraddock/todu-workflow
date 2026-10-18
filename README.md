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

## Task Authoring

Before a task enters the execution pipeline, task-creation entry points should prefer a higher-level authoring workflow.

Use [task-authoring](skills/task-authoring/SKILL.md) to improve what the task says: refine the title, normalize the markdown description, and apply a bug-specific structure when needed. It should be the preferred path for direct user requests and other task-creation flows that benefit from authoring help.

## Task Comment Authoring

Use [task-comment-authoring](skills/task-comment-authoring/SKILL.md) to shape progress updates, blockers, completion notes, and review summaries before posting them to a task. It should be the preferred path when a workflow needs well-structured markdown comment content without creating the task note record itself.

## 2) Task Workflow pipeline

Purpose: pick up a task, execute it using project-owned rules, and close it correctly.

Primary flow:
1. readiness gate (`task-start-preflight`)
2. load project contributing instructions (`docs/CONTRIBUTING.md`, fallback to default)
3. execute task instructions
4. run PR/review/merge flow with explicit human merge approval
5. normalize post-merge repo state (switch to `main`, update, clean up feature branch)
6. close readiness/verification (`task-close-gate`)

Primary skills:
- [task-authoring](skills/task-authoring/SKILL.md)
- [task-comment-authoring](skills/task-comment-authoring/SKILL.md)
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
| [task-authoring](skills/task-authoring/SKILL.md) | Draft structured markdown task descriptions before creation |
| [task-comment-authoring](skills/task-comment-authoring/SKILL.md) | Draft structured markdown task notes and comments before posting |
| [task-pipeline](skills/task-pipeline/SKILL.md) | Gated task execution flow |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Task readiness gate |
| [task-perform](skills/task-perform/SKILL.md) | Perform a single task directly from its description |
| [habit-perform](skills/habit-perform/SKILL.md) | Perform a habit and optionally check in |
| [task-close-gate](skills/task-close-gate/SKILL.md) | Close-readiness verification |
| [pr-review](skills/pr-review/SKILL.md) | PR review flow with host-specific workers |
| [tmux](skills/tmux/SKILL.md) | Run commands in separate panes/sessions and orchestrate sub-agent style workflows |
| [electron-testing](skills/electron-testing/SKILL.md) | Electron app testing workflows |
| [brave-search](skills/brave-search/SKILL.md) | Vendored Brave Search skill for headless web search |
| [browser-tools](skills/browser-tools/SKILL.md) | Vendored browser automation skill using Chrome DevTools Protocol |

## Vendored external skills

This repo also includes local copies of `brave-search` and `browser-tools` under `skills/` so they can be used without depending on separately installed or symlinked third-party skill folders. `vscode` is intentionally omitted for now. See [skills/VENDORED.md](skills/VENDORED.md) for source and maintenance notes.

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

This repository is a Codex plugin containing all 18 skills. It uses
`.codex-plugin/plugin.json` and does not need a link under `~/.codex/skills`.

To install from a local checkout, add an entry to the `plugins` array in
`~/.agents/plugins/marketplace.json` (preserve any existing entries):

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

The personal marketplace should have a top-level `"name": "local"` and a
`plugins` array. The source path is relative to your home directory and must
point to this repository's root. Then install and verify:

```bash
codex plugin add todu-workflow@local
codex plugin list --marketplace local
```

Restart the desktop app and open a new chat to load the plugin skills. The
plugin appears as **Todu Workflow** under **Local Plugins**. After updating the
checkout, rerun the install command to refresh the cached copy. Remove an old
`~/.codex/skills/todu-workflow` symlink, if present, to avoid duplicate skills.


## Requirements

- [todu](https://github.com/evcraddock/todu) (task management)
- [gh](https://cli.github.com/) (GitHub operations)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) (Forgejo operations, optional)
- [tmux](https://github.com/tmux/tmux) (interactive session orchestration)

## License

MIT
