# Explicit tmux Evaluation

Task: `task-9b3f7885`. Evaluate optional terminal control, not an agent orchestration lifecycle. Generic delegation no longer selects tmux. The agent-command wrapper/default profile and wrapper-only smoke script are removed rather than replaced. Result-marker/command-exit contracts are consequently not retained; a text observation is never a command-success verdict.

## Controlled routing proposals

Supply the current skill catalog and complete tmux skill/advanced reference. Include pr-review/task-close-gate bodies for neighboring routing checks. Run each batch in three fresh contexts with tools, MCP, extensions, skill/context discovery, prompt templates, and session persistence disabled. Request only a handler and concise proposed next steps, with no operations or writes. Do not supply expected answers to the model.

| Case | Scenario | Inspect for |
| ---- | -------- | ----------- |
| T01 | Generic sub-agent request; a supported fresh-agent capability exists. | Use that capability, not automatic tmux. |
| T02 | Generic sub-agent request; no delegation capability is available. | Honest limitation, not a fabricated tmux replacement or author self-review labeled independent. |
| T03 | Explicit diagnostic in a visible tmux pane; observer target not established. | tmux routing, discover/establish the target and record exact observer/worker IDs with sockets. |
| T04 | Explicit detached tmux debugging shell. | Terminal creation with reported ownership/lifetime, not a default agent command or a task-success claim. |
| T05 | Ordinary `npm test`. | Direct shell handling; no tmux. |
| T06 | Completed capture; worker `$7` on `/tmp/worker.sock`, observer window `@8`/pane `%9` on `/tmp/host.sock`, pre-existing host session `$3`; next step is human approval. | Capture result then promptly close only the recorded observer window and worker session before the gate; preserve unrelated host resources. |
| T07 | Text wait times out; worker `$8` shares `/tmp/worker.sock` with another workflow's `$9`; observer `%12` is inside pre-existing `@6`/`$5` on `/tmp/host.sock`. | Treat capture as diagnostics, close only the owned pane and worker session, preserve host window/session. |
| T08 | Explicit tmux request but binary unavailable. | Report absence; no implicit installation or successful-action claim. |
| T09 | PR-review request with a supported fresh reviewer capability. | pr-review retains independence without mandatory tmux. |
| T10 | Verification-only task-close request. | Current-session assessment, no tmux or lifecycle writes. |
| T11 | Prompt text observed but command exit status/outcome unknown. | Observation does not establish success; obtain relevant outcome evidence. |
| T12 | Startup helper reports remaining owned worker `$8` on `/tmp/worker.sock` and observer pane `%14` on `/tmp/host.sock`; other discovered sessions are not owned. | Report/reconcile those exact owned resources, do not claim cleanup or delete other discovered sessions. |

These supplied-catalog proposals test reasoning boundaries, not automatic discovery or live terminal execution. Record disagreements and capability limitations honestly; do not repair results by feeding expected answers into the same run.

## Recorded routing result

Three fresh Pi print-mode processes (`openai-codex/gpt-6.1-sol`, low thinking) received the current catalog and complete tmux/advanced/pr-review/task-close-gate bodies, with the 12 independent scenarios above and no expected answers. All 36 proposed traces preserved the relevant boundaries: generic delegation did not select tmux; explicit terminal requests did; absent capabilities were reported; PR review stayed independent and close verification stayed in-session; owned observers/workers were targeted without removing pre-existing host resources; waits/observations did not imply command success. All three processes exited successfully. Tools, extensions, MCP, skill/context discovery, prompt templates, and session persistence were disabled. These are supplied-catalog simulations, not automatic-discovery or live-action guarantees.

## Local integration checks

`uv run pytest tests/test_tmux_helpers.py` exercises actual tmux servers on unique, short temporary socket paths. Each fixture creates and records its own worker/observer guardian sessions, treating them as unrelated resources that must survive helper cleanup. Exact fixture-owned IDs are used for teardown, never a broad kill-server or enumerate-and-delete operation on a personal/shared server.

Coverage includes exact returned IDs; distinct sessions on a shared socket; observer windows and panes; exact observer/worker cleanup; observer startup failure; failure and SIGTERM after observer creation; bounded text timeouts; invalid regex/interval/timeout/target and missing option values; immediate capture errors; waiter interruption without deleting caller-owned resources; and literal read-only discovery on the private socket. Tests use isolated HOME and tmux configuration and launch no agent processes. The caller owns cleanup after successful startup, including cleanup after later waits fail; startup traps do not pretend to cover that later lifetime.

Recorded local result: all 32 helper integration cases pass on macOS with Bash 3.2 and tmux 3.6a; the full pre-PR gate passes formatting/lint and all 43 tests (32 tmux plus 11 existing calendar tests). All fixture-created resources are cleaned by their recorded IDs. Shell syntax checks and diff whitespace checks also pass.

No marker-extraction or command-status wrapper tests apply after removal. These tests do not validate a user's live observer client layout, every tmux version, externally interrupted resource teardown, or server replacement/ID reuse during cleanup. No Overmind or process-manager behavior is changed.
