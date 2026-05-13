# Existing Project Rerun Flow

Use this reference when `project-check` reports that the current directory is already registered.

## Source of Truth

Set these variables from `project-check` and the current working directory:

- `name` - project name
- `host` - project host, usually `github` or `forgejo`
- `localPath` - current working directory

Skip repository creation and project registration. The project already exists.

## Detect Stack

Detect the likely stack from project files:

```bash
if [ -f package.json ]; then detected_stack="typescript"
elif [ -f go.mod ]; then detected_stack="go"
elif [ -f pyproject.toml ]; then detected_stack="python"
elif [ -f Cargo.toml ]; then detected_stack="rust"
else detected_stack=""
fi
```

Ask the user to confirm or change the stack:

```text
Detected existing project: {name}
Stack detected: {detected_stack}

Use this stack or choose different?
Options: {detected_stack} (detected), typescript, go, python, rust
```

Store the chosen value as `stack`.

If the existing project metadata does not provide `description`, `framework`, `database`, or `services`, ask only for the values needed by the downstream skills.

## Rerun Setup Phases

Run the setup phases from the current project directory:

1. Apply `project-scaffold`.
2. Apply `quality-tooling`.
3. Apply `dev-environment`.

Use the same input names as the new project flow. Do not create a new remote repository or register a new Todu project.

## Finish

Use `commit-and-tasks.md` when the rerun should be committed or when the README needs the dev task URL. Skip design/backlog task creation for existing projects unless the user explicitly wants the project-init design task refreshed.
