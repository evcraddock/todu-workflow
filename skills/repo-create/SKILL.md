---
name: repo-create
description: Create a remote repository, clone locally, and register with todu. Use when asked to "create a repo", "new repository", "init repo", or as part of project-init.
---

# Repo Create

Create a new repository on GitHub or Forgejo, clone it locally, and register it with todu.

## Prerequisites

Verify the required CLI is installed and authenticated:

**For GitHub:**
```bash
# Check installed
command -v gh &>/dev/null && echo "OK" || echo "MISSING: install from https://cli.github.com/"

# Check authenticated
gh auth status
```

**For Forgejo:**
```bash
# Check installed
command -v fj &>/dev/null && echo "OK" || echo "MISSING: cargo install forgejo-cli"

# Check authenticated (needs zsh -ic for keyring)
zsh -ic "fj whoami"
```

## Usage

Run the script with required parameters:

```bash
/path/to/todu-workflow/skills/repo-create/scripts/repo-create \
  --name NAME \
  --host HOST \
  --description "DESCRIPTION" \
  --path LOCAL_PATH
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name`, `-n` | Yes | Repository name |
| `--host`, `-h` | Yes | `github` or `forgejo` |
| `--description`, `-d` | Yes | Brief description |
| `--path`, `-p` | Yes | Local path to clone to |

### Examples

**GitHub:**
```bash
repo-create --name myapp --host github --description "My application" --path ~/code/github/myapp
```

**Forgejo:**
```bash
repo-create --name myapp --host forgejo --description "My application" --path ~/code/forgejo/myapp
```

## What It Does

1. **Validates inputs** - Checks all required parameters
2. **Checks CLI** - Verifies gh/fj is installed and authenticated
3. **Creates remote repo** - Uses `gh repo create` or `fj repo create`
4. **Clones locally** - Clones to the specified path
5. **Registers with todu** - Adds project to todu (non-fatal if fails)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Directory already exists" | Path already taken | Choose different path or remove existing |
| "CLI not installed" | gh/fj missing | Install the CLI (see Prerequisites) |
| "CLI not authenticated" | Not logged in | Run `gh auth login` or `fj auth login` |
| "Repository already exists" | Name taken on remote | Choose different name or delete existing |
| "Failed to clone" | Network or permissions | Check URL and try manual clone |

## Integration with project-init

When used as part of `project-init`, the skill is called after gathering project info:

```bash
# Variables from Phase 1a
NAME="myproject"
HOST="github"
DESCRIPTION="My project description"
LOCAL_PATH="$GITHUB_PROJECTS_DIR/$NAME"

# Run repo-create
/path/to/skills/repo-create/scripts/repo-create \
  --name "$NAME" \
  --host "$HOST" \
  --description "$DESCRIPTION" \
  --path "$LOCAL_PATH"
```

On success, proceed to project scaffolding. On failure, show the error and stop.

## Manual Usage

The script can be run directly from the command line without an agent:

```bash
# Add to PATH (optional)
export PATH="$PATH:~/.local/share/todu-workflow/skills/repo-create/scripts"

# Then use directly
repo-create -n myapp -h github -d "My app" -p ~/code/github/myapp
```

## Notes

- GitHub repos are created as public by default
- Forgejo commands use `zsh -ic` wrapper for keyring access
- The todu registration step is non-fatal (continues on failure)
- Parent directories are created automatically if needed
