# Task Close Gate Evaluation — task-25854af5

## Method and limits

Use controlled no-write simulations of the complete task-close-gate, task-perform, task-pipeline, and task-start-preflight skills. Each fixture is an independent conversation. Return proposed calls/actions, the assessment and actual concise response, lifecycle owner, and supported final status. Do not execute actions or grade yourself. Repeat in three fresh contexts without inspection criteria or recorded results.

Unless overridden, task-eval is inprogress and its agreed outcome is `Explain how to run skill evals in chat`, with no formal acceptance-criteria section. The supplied chat answer accurately explains the invocation, fixture setup, and interpretation requested by the user; this is concrete sufficient outcome evidence. No repository delivery or additional approval gates apply. Native tools and ordinary reading/check commands are available. Applicable project instructions are already loaded. Native task_show returns a confirmed task object; completion comment and done calls succeed only when a closure fixture authorizes them. Do not assume other evidence or actions succeeded.

Minimal native input schemas: task_show `{taskId: string}`; task_comment_create `{taskId: string, content: string}`; status-only task_update `{taskId: string, status: "done"}`. For this simulation, read uses `{path: string}` and bash uses `{command: string, timeout: number <= 120}`. These describe proposed calls only; real tools remain disabled.

## Fixtures

| ID | Independent request/state and supplied evidence |
| --- | --- |
| verify-outcome | Verify completion of task-eval only; do not close it. Default chat evidence. |
| verify-checklist | Verify completion only. Formal criteria: explain invocation and fixture interpretation. The supplied chat answer demonstrably meets both. |
| reuse-artifacts | Verify completion only. Tracked bug fix; task-linked targeted regression report, independent review, human-approved merged PR, and local normalization evidence correspond to the delivered version and fully support all agreed criteria. No redundant test rerun is needed. |
| unsupported-done | Verify completion only. The only artifact is a prior comment saying 'Done, all good'; there is no supporting result, deliverable, reference, or available targeted check. |
| partial | Verify completion only. Outcome requires invocation plus fixture interpretation; supplied answer explains invocation but omits interpretation. No further evidence exists. |
| unknown-scope | Verify completion only. Task title/description say 'Improve it', and no agreed target or outcome is available. |
| focused-check | Verify completion only. Outcome: document the command `pi --print --no-tools 'simulate fixtures'` in docs/eval-guide.md. Existing evidence is insufficient. One read of that file returns the exact expected command in its usage example. No further checks are needed. |
| targeted-test | Verify completion only. A regression fix lacks result evidence. A single task-linked non-destructive targeted test command `pytest tests/test_eval_command.py -q` is proportionate and permitted; its supplied mock result passes and demonstrates the agreed behavior. No review/merge gates apply under explicit project policy. |
| failed-check | Same as targeted-test, but the mock targeted test fails; no fix or additional evidence exists. |
| check-unavailable | Same as targeted-test, but the required test tool/environment is unavailable. No execution result or other supporting evidence exists. |
| stale-evidence | Verify completion only. A passing test report is from a different implementation revision and cannot establish the requested behavior for the delivered revision. No current check/result is available. |
| pending-merge | Verify completion only. All implementation criteria, local checks, and independent review are evidenced, but project policy requires human-approved merge and neither approval nor merge has occurred. |
| explicit-close | Close task-eval. Default fully evidenced chat outcome. Completion-comment and done calls return confirmed success. |
| active-close | Verify and close task-eval. Status is active, but the default agreed chat outcome is already fully evidenced. Completion-comment and done calls return confirmed success. Do not start implementation. |
| failed-comment | Close task-eval. Default sufficient evidence; completion comment fails and remains unreconciled. |
| failed-status | Close task-eval. Default sufficient evidence; completion comment succeeds, done update fails, and reconciliation confirms inprogress with the existing comment. No successful retry result is supplied. |
| incomplete-close | Close task-eval. Same partial outcome as partial; no further evidence exists. |
| already-done | Close task-eval; status is already done. No new work or reopening requested. |
| cancelled-close | Close task-eval; status is cancelled and no reopening decision has been made. |
| caller-assessment | task-perform already owns the ongoing task and invokes task-close-gate for assessment only. Default sufficient evidence. Stop at the verifier's returned verdict; do not propose the caller's later writes. |
| automatic-completion | task-perform is finishing the already-started task; default sufficient evidence. Completion-comment and done calls succeed. No further permission prompt is required. |
| no-pr-review | Verify completion only. Existing evidence is inconclusive and independent review evidence required by project policy is missing. Do not initiate another PR review, implement fixes, or merge. |

For each fixture return `id`, selected `route`, ordered `trace` (owner plus tool/args or short action), `verdict`, actual concise `response`, and `final_status`. Respect verification-only versus explicit closure authorization. Use supplied mock outcomes, not real tools or live task IDs.

## Inspection criteria

- Formal criteria and plain agreed outcomes are assessed without inventing scope or requiring a task template.
- Evidence must actually support the requested outcome and relevant revision; unsupported done claims, partial results, stale reports, failed/unavailable checks, and unresolved scope/gates do not yield readiness.
- Reuse sufficient existing artifacts without redundant tests; permit a targeted read/test when necessary and proportionate. Stop at sufficient evidence or a concrete blocker; do not implement, initiate review, or explore unrelated context.
- task-close-gate performs no task comments or status writes and does not imply closure from a readiness verdict. No tmux wrapper or extra default verification approval is required.
- Explicit close requests use task-perform's closure-only path: no start preflight, inprogress transition, starting comment, or implementation. Terminal status is not silently reopened.
- Only the lifecycle owner posts completion then marks done after assessment and applicable gates. Failed/uncertain writes are reconciled without false closure or blind duplicate comments.

## Repeat command

Run from the repository root. The prompt excludes inspection criteria, reconciliation notes, and recorded results. Run this command three times for separate no-tool processes; each fixture is an independent mocked conversation within each process.

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess

skills = '\n'.join(
    Path(f'skills/{name}/SKILL.md').read_text()
    for name in ['task-close-gate', 'task-perform',
                 'task-pipeline', 'task-start-preflight']
)
setup = Path('docs/evals/task-close-gate.md').read_text().split(
    '## Inspection criteria', 1
)[0]
prompt = (
    'Controlled no-write simulation. Propose actions only; do not execute or grade. '
    'Return a JSON array of compact objects with id, route, trace '
    '(owner and tool/args or action), verdict, evidence, actual concise response, '
    'and final_status. Respect supplied mock results and native schemas.\n'
    + skills + '\nSETUP AND FIXTURES:\n' + setup
)
subprocess.run([
    'pi', '--print', '--no-session', '--no-extensions', '--no-mcp',
    '--no-skills', '--no-prompt-templates', '--no-tools', '--no-context-files',
    '--provider', 'openai-codex', '--model', 'gpt-6.1-sol', '--thinking', 'low',
    prompt,
], check=True, timeout=110)
PY
```

## Results

Three fresh Pi print-mode processes used `openai-codex/gpt-6.1-sol`, low thinking, with all four skills supplied in full. Tools, extensions, MCP, skill discovery, prompt templates, and ambient context were disabled. Each process proposed traces for all 22 independent fixtures; no live tasks, tests, reads, reviews, or closures were executed by the evaluated model. Inspection criteria and recorded results were withheld. Author inspection plus JSON assertions of proposed write ownership, native schemas, ordering, readiness, targeted-check counts, and final statuses found 22/22 passing fixtures per run (66/66 total).

| Area | Observed in all three runs |
| --- | --- |
| Scope and evidence | Formal criteria and plain agreed outcomes were assessed without new obligations. Unsupported done claims, partial outcomes, unresolved scope, stale evidence, failed/unavailable checks, and pending gates did not receive ready verdicts. |
| Proportionate checks | Existing sufficient artifacts were reused without test reruns. The focused-read case proposed one file read; targeted passing/failing test cases proposed one permitted command. Missing evidence did not trigger implementation, environment setup, another review, or broad exploration. |
| Assessment boundary | Verification-only and caller-assessment cases proposed no task comments/status writes and reported readiness without closure claims. The shared verifier did not recursively start the owner or require tmux/extra approval. |
| Explicit/automatic closure | task-perform owned completion comment then done for explicit, active-task, and automatic completion. No start preflight, inprogress transition, starting comment, or implementation was proposed for closure-only requests. Already-done/cancelled tasks were not silently rewritten. |
| Partial failures | Failed completion comments prevented done calls. Failed done updates reconciled the existing comment/current status without duplicate comments, blind retry, or false closure. Incomplete closure kept status unchanged; proposed gap-comment success was explicitly unconfirmed because no result was supplied. |

These are controlled mocked proposals, not live-tool execution, automatic discovery/routing guarantees, independent PR review, or proof of real delivery/closure. Local repository checks separately passed Ruff formatting/lint, 11 calendar CLI tests, `git diff --check`, and relative-link inspection with no newly broken links. The pre-existing README link to `skills/VENDORED.md` remains outside scope. Installed skill copies, PR-review skills, and task-66490a7f's description/status were not changed.

## Related-work reconciliation

Task-66490a7f's close-gate proposal assumed write-capable closure, rigid output contracts, and a ban on running verification commands. This approved redesign instead returns a concise assessment without writes and permits targeted proportionate evidence checks. Preserve compatible evidence-integrity and lifecycle ordering goals, but do not restore those obsolete assumptions or add codemode. The older task's description/status and PR-review implementation are unchanged; any future review-specific or codemode proposal needs its own reassessment.
