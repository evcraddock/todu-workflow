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

Use [task-authoring](skills/task-authoring/SKILL.md) to capture the problem, desired outcome, relevant context, and explicit user constraints without inventing scope. Concise prose or bullets are enough; there are no mandatory sections or bug templates. Keep agent suggestions distinct from user decisions, and leave detailed requirements clarification and implementation planning for pickup. The skill returns content; the caller handles any requested backend creation or update.

## Task Comments

Draft comments directly in chat or the posting workflow; no separate authoring skill is needed. Keep updates factual and proportional, preserve supplied constraints, and include relevant verification evidence without inventing results. One sentence can be enough; there is no mandatory generic template. Draft-only requests do not authorize posting. An explicit posting request or an already-authorized workflow uses native `task_comment_create` with the resolved task ID and `content`, without another default approval step. Confirm success before claiming the comment was posted; a comment request alone does not authorize starting or closing a task.

## 2) Task Workflow pipeline

Purpose: pick up a task, execute it using project-owned rules, and close it correctly.

`task-perform` is the single lifecycle entry point for do, work-on, start, and pickup requests:
1. load the task/project instructions, check shared readiness (`task-start-preflight`), and obtain any required plan approval
2. confirm `inprogress` before work and post a starting/resuming comment
3. execute the agreed work and record meaningful progress, decisions, and blockers
4. for tracked repository changes, load `task-pipeline` development guidance and default to branch/PR/independent review/human-approved merge unless explicit project policy permits another delivery path
5. assess completion in the current session using `task-close-gate` in assessment-only mode
6. after verification and applicable gates pass, post the completion evidence and mark `done` without another default approval prompt

Explicit close/complete/verify-and-close requests use task-perform's closure-only path: assess already-delivered work without starting implementation, then perform completion writes only after evidence and applicable gates pass. Verification-only requests stop at task-close-gate's assessment; that verifier never posts comments or changes status.

Non-repository deliverables do not automatically require PR/merge stages or a particular storage destination. Failed or inconclusive verification leaves the task open. Execution and completion verification do not mandate tmux delegation; required independent review and explicit project approval gates still apply.

[task-pipeline](skills/task-pipeline/SKILL.md) contains only delivery-path selection and applicable repository development stages, then returns development evidence to task-perform. It does not restart readiness or own task status, comments, or closure. Small tracked fixes and committed documentation retain the default review/merge path unless explicit project policy permits an alternative; chat-only or untracked local results do not inherit that path.

Primary skills:
- [task-authoring](skills/task-authoring/SKILL.md)
- [task-perform](skills/task-perform/SKILL.md)
- [task-pipeline](skills/task-pipeline/SKILL.md) (development reference)
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
| [repo-create](skills/repo-create/SKILL.md) | Create/verify remote repo and clone/verify locally; no registration or scaffolding |
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate baseline project files and docs |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, testing, hooks |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up local development process management |
| [task-authoring](skills/task-authoring/SKILL.md) | Capture user intent in task descriptions without inventing scope |
| [task-pipeline](skills/task-pipeline/SKILL.md) | Development-workflow guidance loaded by task-perform |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Task readiness gate |
| [task-perform](skills/task-perform/SKILL.md) | Own task readiness, confirmed start, updates, execution, and verified completion |
| [task-close-gate](skills/task-close-gate/SKILL.md) | Evidence-based completion assessment without task mutations |
| [pr-review](skills/pr-review/SKILL.md) | PR review flow with host-specific workers |
| [tmux](skills/tmux/SKILL.md) | Run commands in separate panes/sessions and orchestrate sub-agent style workflows |
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
