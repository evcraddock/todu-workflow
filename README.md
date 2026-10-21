# todu-workflow

Reusable AI skills for project setup, task authoring, and development delivery. Compatible with [pi](https://github.com/badlogic/pi-mono), Claude Code, and Codex CLI.

Project instructions define the workflow policy. Ordinary task execution uses native task tools; `task-pipeline` runs only when explicitly requested or selected by project instructions. It covers implementation, checks, PR, independent review, and human-approved merge—not task status or comments. Without project contributing instructions, it uses [DEFAULT_CONTRIBUTING.md](skills/task-pipeline/DEFAULT_CONTRIBUTING.md).

## Skills

| Skill | Purpose |
|---|---|
| [project-init](skills/project-init/SKILL.md) | Initialize a project end-to-end |
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate baseline files and documentation |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, tests, and hooks |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up local development processes |
| [task-authoring](skills/task-authoring/SKILL.md) | Draft task titles and descriptions without inventing scope |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Check explicit prerequisites from supplied context when requested or required |
| [task-pipeline](skills/task-pipeline/SKILL.md) | Deliver development work through review and approved merge |
| [nextactions](skills/nextactions/SKILL.md) | Recommend work by priority and dependencies |
| [pr-review](skills/pr-review/SKILL.md) | Review PRs for actionable findings |
| [tmux](skills/tmux/SKILL.md) | Manage explicitly requested terminal sessions |
| [electron-testing](skills/electron-testing/SKILL.md) | Test Electron apps with Playwright |
| [radicale-calendar](skills/radicale-calendar/SKILL.md) | Manage CalDAV events with the bundled `radicale-calendar` CLI |

## Installation

```bash
git clone https://github.com/evcraddock/todu-workflow ~/.local/share/todu-workflow
```

### pi or Claude Code

Run the commands for your agent:

```bash
# pi
mkdir -p ~/.pi/agent/skills
ln -s ~/.local/share/todu-workflow/skills ~/.pi/agent/skills/todu-workflow

# Claude Code
mkdir -p ~/.claude/skills
ln -s ~/.local/share/todu-workflow/skills ~/.claude/skills/todu-workflow
```

Restart the agent to load the skills.

### Codex

Add this entry to the `plugins` array in `~/.agents/plugins/marketplace.json`, preserving existing entries. Set the marketplace's top-level `name` to `local`.

```json
{
  "name": "todu-workflow",
  "source": {
    "source": "local",
    "path": "./.local/share/todu-workflow"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

The source path is relative to your home directory. Install and verify:

```bash
codex plugin add todu-workflow@local
codex plugin list --marketplace local
```

Restart Codex and open a new chat. After updating the checkout, rerun the install command to refresh the cached plugin. Avoid also linking the skills under `~/.codex/skills`, which would create duplicates.

## Requirements

Install the tools needed by the skills you use:

- [todu](https://github.com/evcraddock/todu): task management
- [gh](https://cli.github.com/): GitHub operations
- [fj](https://codeberg.org/Cyborus/forgejo-cli): Forgejo operations
- [tmux](https://github.com/tmux/tmux): terminal sessions

## License

MIT
