# todu-workflow

Development workflow skills for AI coding agents. Compatible with [pi](https://github.com/badlogic/pi-mono), Claude Code, and Codex CLI.

## Skills

| Skill | Description |
|-------|-------------|
| [project-init](skills/project-init/SKILL.md) | Initialize a new project end-to-end |
| [project-scaffold](skills/project-scaffold/SKILL.md) | Generate project scaffolding files |
| [quality-tooling](skills/quality-tooling/SKILL.md) | Set up linting, formatting, testing |
| [dev-environment](skills/dev-environment/SKILL.md) | Set up Procfile, Makefile, Docker services |
| [pr-review](skills/pr-review/SKILL.md) | Review a pull request from another agent |
| [request-review](skills/request-review/SKILL.md) | Spawn a separate agent to review a PR |
| [task-close-preflight](skills/task-close-preflight/SKILL.md) | Verify work is complete before closing a task |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Prepare to work on a task |
| [tmux](skills/tmux/SKILL.md) | Control interactive CLIs (python, gdb, lldb) via tmux |

## Extensions

| Extension | Description |
|-----------|-------------|
| [repo-create](extensions/repo-create.ts) | Create remote repo, clone locally, register with todu |

## Quick Start (pi)

```bash
# Clone
git clone https://github.com/evcraddock/todu-workflow ~/.local/share/todu-workflow

# Install skills
mkdir -p ~/.pi/agent/skills
ln -s ~/.local/share/todu-workflow/skills ~/.pi/agent/skills/todu-workflow

# Install extensions (symlink each file individually)
mkdir -p ~/.pi/agent/extensions
ln -s ~/.local/share/todu-workflow/extensions/repo-create.ts ~/.pi/agent/extensions/
```

Restart pi to load the new skills and extensions.

## Other Agents

### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s ~/.local/share/todu-workflow/skills ~/.claude/skills/todu-workflow
```

Note: The `repo_create` extension is not available in Claude Code, so project-init Phase 2-3 (repo creation) requires manual steps or using `gh`/`fj` CLI directly. All other skills work fully.

### Codex CLI

```bash
mkdir -p ~/.codex/skills
ln -s ~/.local/share/todu-workflow/skills ~/.codex/skills/todu-workflow
```

## Requirements

- [todu](https://github.com/evcraddock/todu) - Task management CLI
- [gh](https://cli.github.com/) - GitHub CLI (for PR and repo operations)
- [tmux](https://github.com/tmux/tmux) - Terminal multiplexer (for tmux skill and request-review)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) - Forgejo CLI (optional, for Forgejo support)

### Optional (pi-only features)

- [pi](https://github.com/badlogic/pi-mono) - Required for `repo_create` extension (used by project-init)

## License

MIT
