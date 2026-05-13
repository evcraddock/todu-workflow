# Project Location

Use this reference to determine where a new project should be cloned or created.

## Environment Variables

Check the configured project directories:

```bash
echo "$FORGEJO_PROJECTS_DIR"
echo "$GITHUB_PROJECTS_DIR"
echo "$PROJECT_INIT_SHELL_CONFIG"
```

For `host=forgejo`, use `FORGEJO_PROJECTS_DIR`.

For `host=github`, use `GITHUB_PROJECTS_DIR`.

If the host-specific variable is set, use it as `baseDir`.

## Missing Host Directory

If the host-specific variable is not set, ask for the shell config preference if `PROJECT_INIT_SHELL_CONFIG` is also unset:

```text
Which shell config should I update to save your project directory preference?
Options: ~/.zshrc, ~/.bashrc, ~/.profile, or specify another
```

Ask for the projects directory:

```text
Where do you keep your {host} projects?
Common options: ~/Private/code/{host}, ~/Projects/{host}, ~/code/{host}
```

Before editing shell config, ask for explicit approval. This is a persistent local environment change.

Append this block to the selected shell config when approved:

```bash
# Project Init settings
export PROJECT_INIT_SHELL_CONFIG="{shell_config_path}"
export FORGEJO_PROJECTS_DIR="{projects_dir}"  # or GITHUB_PROJECTS_DIR
```

Notify the user which variable was added to which shell config.

## Compute and Validate Path

Compute:

```text
localPath = {baseDir}/{name}
```

Validate:

```bash
test -d "{localPath}" && echo "EXISTS" || echo "OK"
```

If the directory exists, use it. This allows rerunning project-init after partial setup.
