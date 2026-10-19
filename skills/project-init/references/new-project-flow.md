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

After gathering, the flow should have `name`, `host`, `stack`, `framework`, `description`, `database`, and `services`. Before repository creation, also resolve the intended `owner` (user/organization), `instance` (GitHub defaults to `github.com`; Forgejo requires an explicit host), and `visibility` from the request or an established preference. Ask when unspecified; never silently default to public.

## Determine Location

Follow `project-location.md` to determine `baseDir` and `localPath`.

If `{localPath}` already exists, do not assume it belongs to the intended repository. Verify it in the repository phase before continuing after partial setup.

## Create Repository

Use the installed host CLI (`gh` or `fj`) directly to create/inspect the remote and clone it locally. Inspect CLI help as needed and follow environment-specific tool instructions for authentication/keyring behavior; do not add a replacement skill or script.

- Before creation, confirm the selected instance, owner/organization, name, and visibility, honoring the remote-creation approval gate. Never silently select public visibility.
- Pass names, descriptions, and other inputs as literal arguments. If a shell wrapper is required by the environment, use positional arguments rather than interpolating values into shell code.
- Obtain the actual repository URL from host metadata and verify its instance and owner/name before cloning; do not guess it from the authenticated username.
- For existing repositories/directories or partial failure, establish reuse intent and verify remote identity plus the local checkout root/origin before reusing anything. Preserve local files, do not blindly retry remote creation or overwrite an unrelated path, and do not suggest repository deletion as routine recovery. Report remote creation and local cloning outcomes separately; stop on unavailable tools, authentication failure, or uncertain identity.

After verified creation/cloning or intended reuse, continue with registration below. Registration and scaffolding remain this orchestrator's responsibility, not implicit side effects of ordinary standalone repository creation.

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
