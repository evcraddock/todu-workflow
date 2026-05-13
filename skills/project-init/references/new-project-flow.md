# New Project Flow

Use this reference when `project-check` reports that the current directory is not a registered project.

## Gather Project Inputs

Ask these questions sequentially and store the answers:

1. Project name:

   ```text
   What is the project name?
   ```

2. Host:

   ```text
   Where will this project be hosted?
   Options: forgejo, github
   ```

3. Tech stack:

   ```text
   What tech stack will you use?
   Options: typescript, go, python, rust
   ```

4. Framework:

   ```text
   What framework? (optional)

   For TypeScript: none, hono, express
   For Go: none, gin, echo
   For Python: none, fastapi, flask
   For Rust: none, axum

   Use "none" for CLI tools or libraries.
   ```

5. Description:

   ```text
   Brief project description:
   ```

6. Database:

   ```text
   Database needed?
   Options: none, postgres, sqlite
   ```

7. Additional services:

   ```text
   Additional services?
   Options: none, redis, s3
   ```

After gathering, the flow should have `name`, `host`, `stack`, `framework`, `description`, `database`, and `services`.

## Determine Location

Follow `project-location.md` to determine `baseDir` and `localPath`.

If `{localPath}` already exists, use the existing directory. This allows rerunning project-init after partial setup.

## Create Repository

Apply `repo-create` with:

- `name`
- `host`
- `description`
- `localPath`

Handle common errors this way:

| Error | Action |
| ----- | ------ |
| CLI not installed | Show install instructions, then stop. |
| Not authenticated | Show auth instructions, then stop. |
| Repo already exists | Use the existing repo when that matches the user's intent. |
| Directory exists | Use the existing directory and skip clone. |

## Register Project

Apply the `project-register` skill after repository creation.

For hosted repositories, register as an external repo using:

- provider: `host`
- target repository: `{owner}/{name}`
- suggested project name: `name`
- description: `description`

If the project name already exists in Todu, follow `project-register` conflict resolution.

## Scaffold and Tooling

Change to `{localPath}` before invoking downstream setup skills.

Apply `project-scaffold` with:

- `name`
- `description`
- `stack`
- `framework`
- `host`
- `localPath`

This generates foundational files such as `LICENSE`, `.gitignore`, `README.md`, `AGENTS.md`, `docs/`, and the host-specific PR template.

Apply `quality-tooling` with:

- `name`
- `stack`
- `localPath`

This generates linter, formatter, test, TypeScript, pre-PR, and example test files according to the selected stack.

Apply `dev-environment` with:

- `name`
- `stack`
- `framework`
- `database`
- `services`
- `localPath`

This generates `.env.example` and `Makefile`, then creates or reuses the "Set up dev environment" follow-up task. Store the returned task URL as `dev_task_url`.

## Finish

Follow `commit-and-tasks.md` for README task-link replacement, initial commit/push, design/backlog task creation/update, and final summary.
