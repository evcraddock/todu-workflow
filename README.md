# todu-workflow

Development workflow skills for AI coding agents. Compatible with [pi](https://github.com/badlogic/pi-mono), Claude Code, and Codex CLI.

## Skills

| Skill | Description |
|-------|-------------|
| [project-init](skills/project-init/SKILL.md) | Initialize a new project end-to-end |
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate project scaffolding files |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, testing |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up Procfile, Makefile, Docker services |
| [repo-create](skills/repo-create/SKILL.md) | Create remote repo, clone locally, register with todu |
| [pr-review](skills/pr-review/SKILL.md) | Review a pull request from another agent |
| [request-review](skills/request-review/SKILL.md) | Spawn a separate agent to review a PR |
| [task-close-preflight](skills/task-close-preflight/SKILL.md) | Verify work is complete before closing a task |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Prepare to work on a task |
| [tmux](skills/tmux/SKILL.md) | Control interactive CLIs (python, gdb, lldb) via tmux |

## Quick Start

```bash
# Clone
git clone https://github.com/evcraddock/todu-workflow ~/.local/share/todu-workflow

# Install skills (pi)
mkdir -p ~/.pi/agent/skills
ln -s ~/.local/share/todu-workflow/skills ~/.pi/agent/skills/todu-workflow

# Or for Claude Code
mkdir -p ~/.claude/skills
ln -s ~/.local/share/todu-workflow/skills ~/.claude/skills/todu-workflow

# Or for Codex CLI
mkdir -p ~/.codex/skills
ln -s ~/.local/share/todu-workflow/skills ~/.codex/skills/todu-workflow
```

Restart your agent to load the skills.

## Requirements

- [todu](https://github.com/evcraddock/todu) - Task management CLI
- [gh](https://cli.github.com/) - GitHub CLI (for PR and repo operations)
- [tmux](https://github.com/tmux/tmux) - Terminal multiplexer (for tmux skill and request-review)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) - Forgejo CLI (optional, for Forgejo support)

## License

MIT
