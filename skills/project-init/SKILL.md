---
name: project-init
description: "Initialize a project end-to-end: repo, registration, scaffold, quality tooling, and dev environment. Use for new project/app setup. Do not use for one-off setup changes."
---

# Project Init

Initialize a project from scratch, or rerun the project baseline on an already registered project. This skill is the orchestrator; load the focused references only when their flow is needed.

## References

- `references/new-project-flow.md` - questionnaire, repository creation, project registration, scaffold/tooling/dev environment, and initial summary.
- `references/existing-project-rerun.md` - rerun behavior for an already registered project.
- `references/project-location.md` - project directory environment variables and shell config persistence.
- `references/commit-and-tasks.md` - initial commit/push, README task link update, and design/backlog task creation or update.

## Preconditions

Verify required CLIs before the phase that needs them:

```bash
command -v gh &>/dev/null && echo "OK: gh" || echo "MISSING: gh"
command -v fj &>/dev/null && echo "OK: fj" || echo "MISSING: fj"
command -v todu &>/dev/null && echo "OK: todu" || echo "MISSING: todu"
```

Use the host-specific CLI only when that host is selected. For Forgejo authentication checks, use `zsh -ic "fj whoami"` so keyring access works.

## Approval Gates

Ask before actions with external or hard-to-reverse side effects:

- writing shell config for project directory preferences
- creating a remote repository
- registering or updating a project in Todu when the user did not explicitly ask for it
- committing generated files
- pushing to a remote
- creating or updating the design/backlog task

Local generated scaffold/tooling files are part of this requested setup flow. Follow the downstream skills' own overwrite behavior and stop if local project state makes the requested setup ambiguous.

## Orchestration

1. Detect whether the current directory is already registered:
   - Apply the `project-check` skill.
   - If registered, follow `references/existing-project-rerun.md`.
   - If not registered, follow `references/new-project-flow.md`.
2. For new projects, gather project inputs and determine `localPath` using `references/project-location.md`.
3. Apply helper skills in order:
   - `repo-create`
   - `project-register`
   - `project-scaffold`
   - `quality-tooling`
   - `dev-environment`
4. Use `references/commit-and-tasks.md` for README task-link replacement, initial commit/push, and design task creation/update.
5. Stop and report the first blocking failure. The user can rerun this skill after fixing the issue.

## Shared Inputs

Track these variables across the flow:

- `name` - project name
- `host` - `github` or `forgejo`
- `stack` - `typescript`, `go`, `python`, or `rust`
- `framework` - stack-appropriate framework or `none`
- `description` - project description
- `database` - `none`, `postgres`, or `sqlite`
- `services` - `none`, `redis`, or `s3`
- `localPath` - target local repository path
- `dev_task_url` - URL for the dev environment setup task
- `design_task_url` - URL for the design/backlog task

## Behavior to Preserve

- New projects: create/clone repo, register project, scaffold files, add quality tooling, add dev environment scaffolding, commit/push, and create the design/backlog task.
- Existing projects: reuse current project metadata, detect or confirm stack, and rerun scaffold/tooling/dev environment phases without repo creation or project registration.
- Dev environment setup creates or reuses the follow-up "Set up dev environment" task.
- Design/backlog task creation/update is non-critical; warn and continue if it fails.

## Scripts

This refactor does not add project-init-specific scripts. Deterministic file generation remains owned by downstream skills such as `project-scaffold`, `quality-tooling`, and `dev-environment`.
