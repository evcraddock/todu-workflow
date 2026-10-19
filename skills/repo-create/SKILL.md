---
name: repo-create
description: Create a remote repository and clone it locally. Use for explicit new repo requests or project-init. Do not use for local-only scaffolding.
---

# Repo Create

Create and clone a GitHub or Forgejo repository. This skill does **not** register a Todu project, scaffold files, commit, or push. `project-init` coordinates those later phases; perform registration separately only when requested.

## Resolve intent before creation

Establish the repository name, description, local path, provider, owner (user or organization), instance, and visibility from the user's request or established preferences. Ask for any missing identity or visibility decision before invoking the helper. Never silently select public visibility. State the selected target and visibility before a remote write; follow any caller approval gate. An explicit repository-creation request authorizes its ordinary creation/cloning steps, not unrelated registration or scaffolding.

## Helper

Run `scripts/repo-create` relative to this skill directory. Git and Bash are required, plus authenticated `gh` for GitHub or `fj` and interactive `zsh` for Forgejo. The helper checks authentication for the selected instance and reports installation/login instructions on failure.

| Option | Meaning |
| ------ | ------- |
| `--name`, `-n` | Required repository name, without owner prefix |
| `--host`, `-h` | Required provider: `github` or `forgejo` |
| `--owner` | Required intended user/organization |
| `--instance` | HTTPS `host[:port]`; defaults to `github.com` only for GitHub; required for Forgejo |
| `--visibility` | Required `private` or `public`; GitHub also accepts `internal` where supported |
| `--description`, `-d` | Required nonempty description, quoted as one argument |
| `--path`, `-p` | Required local destination |
| `--reuse-existing` | Explicit recovery/reuse mode; verifies an existing remote, never creates one |

Names start with an ASCII letter/digit and contain only letters/digits/`._-`, without a `.git` suffix. Owners start with an ASCII letter/digit and contain only letters/digits/`_-`. Invalid identities are rejected before host commands; description quotes and shell characters stay literal arguments. Instances with schemes, credentials, IPv6 literals, or subpaths are not supported by this helper; stop rather than reinterpret them.

```bash
# GitHub organization, explicit private visibility
/path/to/skills/repo-create/scripts/repo-create \
  --name myapp --host github --owner my-team --visibility private \
  --description "My application" --path "$HOME/code/github/my-team/myapp"

# Forgejo organization on an explicit instance
/path/to/skills/repo-create/scripts/repo-create \
  --name myapp --host forgejo --instance forge.example.org --owner my-team \
  --visibility private --description "My application" \
  --path "$HOME/code/forgejo/my-team/myapp"
```

For GitHub Enterprise, supply its hostname with `--instance`; the helper sets `GH_HOST` explicitly, overriding ambient host selection. GitHub metadata is read using `gh repo view --json`; the returned owner/name, HTTPS URL, and visibility must match the selected target before cloning.

Forgejo uses the `fj` 0.5.x CLI contract (`whoami`, `repo create/view`, and `org repo create`). Commands run through a constant `zsh -ic` program with positional arguments to preserve keyring access without shell interpolation. The selected instance is passed to **every** command, and the login/instance is verified. If the owner matches that login, create a personal repository; otherwise use the organization endpoint. Creating for another individual user is not supported. The helper re-reads `repo view`, checks the full name and final API-returned `View online at` URL, and uses that verified HTTPS Git endpoint for cloning. Unexpected output fails closed; no URL is guessed from the login. `fj` view does not expose visibility: reuse does not verify or change existing Forgejo privacy settings, so check them separately if that matters to the request.

## Recovery and conflicts

A normal run refuses an existing local path and does not silently reuse a remote. If remote creation fails, it may be a conflict or an uncertain request outcome: inspect the selected owner/instance/repository before retrying. If creation succeeds but verification, directory setup, or cloning fails, the error explicitly reports remote-created/local-not-completed state. Do not create another remote to recover a clone failure.

When the existing remote is confirmed to be the intended one, repeat the same inputs with `--reuse-existing`:

```bash
/path/to/skills/repo-create/scripts/repo-create \
  --name myapp --host github --owner my-team --visibility private \
  --description "My application" --path "$HOME/code/github/my-team/myapp" \
  --reuse-existing
```

Recovery verifies the remote before cloning or accepting a local checkout. It can clone into a missing or empty destination. For nonempty paths, it requires the exact Git worktree root and an origin matching the verified HTTPS endpoint (with optional `.git` suffix), or the SSH URL returned by GitHub metadata. Forgejo SSH/custom clone endpoints are not inferred; use a fresh destination or verify/manage those checkouts separately. Dirty/untracked files in a matching checkout are left untouched; no fetch, reset, checkout, or overwrite occurs. Symlinks, files, unrelated checkouts, nested directories, missing/multiple origins, and unverifiable partial clones stop the helper. Leave their contents intact and choose a fresh path or resolve them separately.

A remote lookup failure in recovery mode never falls back to creation. For conflicts, verify identity and reuse only when intended, or choose another name/path. Deleting an existing repository is not a routine recovery step.

## Integration boundary

`project-init` must resolve and pass `name`, `host`, `owner`, `instance`, `visibility`, `description`, and `localPath`. If recovering partial setup, it must establish reuse intent and pass `--reuse-existing`; never skip verification merely because a directory exists. Stop the orchestration on helper failure. On success, return the verified remote URL and local path to the caller. `project-init` then owns Todu registration and scaffolding; a standalone repo-create request ends after creation/cloning or verified reuse.
