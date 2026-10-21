# Working on todu-workflow

These instructions apply to agents developing this repository, not machine-wide configuration or the behavior of its distributed workflow skills.

## Codex plugin version bumps

- Before merging changes to bundled skills or other distributed plugin behavior/configuration, bump `version` in `.codex-plugin/plugin.json` in the same PR. Do not defer the bump to a follow-up after merging.
- Repository-only documentation, evaluation reports, and agent working instructions do not require a plugin bump unless they also change distributed plugin behavior or configuration.
- Default to a patch bump for fixes and instruction corrections, such as `0.1.1` to `0.1.2`. Use a minor bump for new backward-compatible features/skills and a major bump for breaking changes. Ask when the intended release level is unclear rather than guessing.
- Compare semantic versions against the latest target branch, normally `main`. The PR's final plugin version must be greater than the target branch's version. Do not compare version strings lexicographically, lower an existing version, or assume the branch's original base is still current.
- Use one appropriate final version for the PR; a bump is not required for every intermediate commit. If the target branch advances to that version before merge, update the PR to a newer appropriate version.
- Keep unrelated package versions independent. In particular, do not change the calendar CLI version in `pyproject.toml` merely to match the Codex plugin.

## Verify before merging

- Include the old and new plugin versions in the PR summary when a bump is required. For a repository-only change, explain why no plugin bump is needed.
- Parse `.codex-plugin/plugin.json` as JSON and confirm its `version` is the intended semantic version. Run the applicable local checks, including `./scripts/pre-pr.sh` under the existing development workflow.
- Review the version bump as part of the final PR revision. If a later version adjustment changes the reviewed revision, rerun applicable checks and obtain review of the updated changes; do not append an unreviewed bump immediately before merging.
- Recheck the version against the latest target branch before merging. A valid version bump does not replace required independent review or explicit human merge approval.
