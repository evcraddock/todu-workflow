# Vendored skills

This repository vendors a small set of third-party Pi skills so they can be installed and maintained from `todu-workflow` without extra symlinks beyond the normal top-level `skills/` install.

## Included

| Local path | Upstream source | Notes |
|---|---|---|
| `skills/brave-search` | `github.com/badlogic/pi-skills/brave-search` | Copied locally with its scripts and npm metadata. |
| `skills/browser-tools` | `github.com/badlogic/pi-skills/browser-tools` | Copied locally with its scripts and npm metadata. Setup instructions were adjusted to use `cd {baseDir}` so the vendored copy works directly from its local folder. |

## Omitted

| Skill | Decision |
|---|---|
| `vscode` | Omitted for now. This task only vendors `brave-search` and `browser-tools`, and `vscode` is not needed to remove the external skill dependency being addressed here. |

## Maintenance

When updating a vendored skill, copy the upstream directory contents into the matching local `skills/` folder and review `SKILL.md` for any path assumptions that do not fit the local layout.
