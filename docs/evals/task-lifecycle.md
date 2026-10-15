# Task Lifecycle Evaluation — task-30fd505d

## Method and limits

Evaluated the revised task-perform, pipeline integration, resumed-task preflight, assessment-only close-gate integration, and habit boundary using three fresh Pi print-mode processes with `openai-codex/gpt-6.1-sol`, low thinking. Each process received the five skill files in full and the 16 independent fixtures below, then proposed ordered action/tool traces without executing tools. All tools, extensions, MCP, and skill discovery were disabled for these simulations. The project fixture supplied contributing instructions, so the default contributing fallback was not evaluated here.

Each process evaluated all 16 fixtures in one batch, treating them as independent conversations: 48 proposed traces total, not 48 separate sessions. This is a controlled instruction-following simulation, not a live backend test, full skill-discovery benchmark, or proof of reliable production behavior. Results were inspected for routing, write ordering, state handling, and approval boundaries; the model was not asked to grade itself. Existing Python tests cover the separate calendar CLI, not agent lifecycle behavior.

The initial Codex CLI attempts could not run either its configured model or an explicit gpt-5.4 model under the available login. No behavioral result is claimed for those attempts. Fresh Pi processes using the current authenticated provider/model completed successfully without tmux or credential changes.

## Fixture setup

Use exact mock ID `task-eval`, clear task intent, no dependencies, and available native task tools. Each case starts independently. Omitted read calls and authorized comment writes succeed. The project permits direct work on clear small tasks, requires plan agreement for substantial work (already approved in execution fixtures), and requires independent PR review and explicit human merge approval for tracked changes. Propose actions only; never use live IDs, execute writes, or inherit state between cases.

| Fixture | Request/state and supplied outcomes |
| --- | --- |
| active-success | Do task: produce a short chat answer. Active; outcome fully verified; no remaining gate. |
| pickup-success | Pickup task: same chat answer and state as active-success. |
| resume | Work on task. Already inprogress; chat outcome fully verified. |
| failed-start | Active; inprogress update fails; reconciliation still reports active. |
| terminal | Do a done task with no reopening approval; also consider cancelled. |
| inconclusive | Active; agreed work implemented, but one criterion lacks evidence after focused checks. |
| failed-start-comment | Active; inprogress succeeds, starting comment fails and remains unreconciled. |
| failed-completion-comment | Already inprogress; starting comment succeeds, work/gates verify, completion comment fails and remains unreconciled. |
| failed-done | Already inprogress; completion comment succeeds, done update fails, reconciliation shows inprogress and the existing comment. |
| nonrepo-brainstorm | Active; brainstorm in chat only; user approves resulting conclusions; no repository deliverable. |
| merge-gate | Active; pickup a README change; implementation/checks/independent review pass; human merge approval absent. |
| unavailable-review | Active; tracked code change and local checks pass; required fresh-context review unavailable. |
| readiness-only | Check whether an active task is ready; explicitly do not start it. |
| lookup-only | Show an active task. |
| habit | Do habit habit-eval; not a task execution request. |
| uncertain-start-confirmed | Active chat task; start update outcome uncertain, reconciliation confirms inprogress; subsequent outcome verifies. |

For each fixture request a JSON record containing `id`, selected `route`, ordered `trace`, supported `finalStatus`, and any required `clarification`. Require explicit native-tool names/status values and no real actions. To repeat with the current checkout, run three fresh invocations using a configured provider/model:

```bash
pi --print --no-session --no-extensions --no-mcp --no-skills \
  --no-prompt-templates --no-tools --thinking low \
  @skills/task-perform/SKILL.md @skills/task-pipeline/SKILL.md \
  @skills/task-start-preflight/SKILL.md @skills/task-close-gate/SKILL.md \
  @skills/habit-perform/SKILL.md @docs/evals/task-lifecycle.md \
  'Simulate the independent fixtures using the supplied instructions and setup. Do not use tools or perform live actions. Return proposed traces, not grades.'
```

This repeat command includes the recorded results below for transparency; for an unprimed repetition, supply only the Method/Fixture setup and skill files, excluding the Results section. The original runs used an inline prompt containing the setup, five complete files, fixture JSON, and requested response shape, without expected answers or these results.

## Results

All 16 fixture traces met the checked lifecycle properties in each of the three runs:

- Do/pickup/work-on execution selected task-perform; readiness-only, lookup, and habit requests stayed outside execution.
- Active tasks confirmed inprogress before the starting comment and work; resumed tasks did not reset or redundantly start. An uncertain start reconciled before work without repeating the update.
- Failed start or unresolved starting-comment writes prevented implementation; terminal tasks were not silently reopened.
- Assessment-only verification performed no lifecycle writes. Successful cases posted confirmed completion evidence before done without another default approval prompt.
- Inconclusive verification, failed completion comments, and failed done writes did not claim closure or blindly duplicate comments.
- Chat-only work did not acquire PR/storage requirements. README/code changes respected independent review and human merge gates; unavailable review was not replaced with self-review.
- No trace required tmux delegation for execution or completion verification.

The preserved preflight still emits its existing verbose summary and same-project dependency queries. Those limitations are intentionally left to task-ab21a4af. Full pipeline/reference cleanup and standalone close-gate redesign remain in task-d9b978d2 and task-25854af5 respectively.
