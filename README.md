# todu-workflow

Development workflow skills for AI coding agents. Compatible with [pi](https://github.com/badlogic/pi-mono), Claude Code, and Codex CLI.

## Skills

| Skill | Description |
|-------|-------------|
| [pr-review](skills/pr-review/SKILL.md) | Review a pull request from another agent |
| [request-review](skills/request-review/SKILL.md) | Spawn a separate agent to review a PR |
| [task-close-preflight](skills/task-close-preflight/SKILL.md) | Verify work is complete before closing a task |
| [task-start-preflight](skills/task-start-preflight/SKILL.md) | Prepare to work on a task |

## Installation

### pi-coding-agent

Clone the repo and symlink into pi's user skills directory:

```bash
# Clone to a convenient location
git clone https://github.com/evcraddock/todu-workflow ~/todu-workflow

# Create symlinks (pi scans recursively, so one symlink works)
mkdir -p ~/.pi/agent/skills
ln -s ~/todu-workflow/skills ~/.pi/agent/skills/todu-workflow
```

Or symlink individual skills:

```bash
ln -s ~/todu-workflow/skills/pr-review ~/.pi/agent/skills/
ln -s ~/todu-workflow/skills/request-review ~/.pi/agent/skills/
ln -s ~/todu-workflow/skills/task-close-preflight ~/.pi/agent/skills/
ln -s ~/todu-workflow/skills/task-start-preflight ~/.pi/agent/skills/
```

#### Required Extensions

Some skills use pi extensions for interactive workflows. Install from pi's example extensions:

```bash
# Find pi's installation path
PI_PATH=$(dirname $(which pi))/../lib/node_modules/@mariozechner/pi-coding-agent

# Install questionnaire extension (used by project-init)
mkdir -p ~/.pi/agent/extensions
cp $PI_PATH/examples/extensions/questionnaire.ts ~/.pi/agent/extensions/
```

### Claude Code

Claude Code only looks one level deep, so symlink individual skills:

```bash
mkdir -p ~/.claude/skills
ln -s ~/todu-workflow/skills/pr-review ~/.claude/skills/
ln -s ~/todu-workflow/skills/request-review ~/.claude/skills/
ln -s ~/todu-workflow/skills/task-close-preflight ~/.claude/skills/
ln -s ~/todu-workflow/skills/task-start-preflight ~/.claude/skills/
```

### Codex CLI

```bash
mkdir -p ~/.codex/skills
ln -s ~/todu-workflow/skills ~/.codex/skills/todu-workflow
```

## Requirements

- [todu](https://github.com/evcraddock/todu) - Task management CLI
- [gh](https://cli.github.com/) - GitHub CLI (for PR operations)
- [tmux](https://github.com/tmux/tmux) - Terminal multiplexer (for request-review)
- [pi](https://github.com/badlogic/pi-mono) - Required for skills that use pi extensions (project-init)
- [fj](https://codeberg.org/Cyborus/forgejo-cli) - Forgejo CLI (for project-init with Forgejo)

## License

MIT
