# Task Start Preflight Evaluation — task-ab21a4af

## Method and limits

Evaluate the shared readiness contract with controlled no-write fixtures, not live task mutations. Supply the complete task-start-preflight, task-perform, and task-pipeline skills. The recorded original runs supplied only the pipeline's then-current lifecycle integration section; the repeat command now supplies the complete rewritten reference. Each fixture is an independent conversation with the mock task/tool outcomes below. Return proposed native-tool calls and the actual concise readiness response; do not execute anything or grade yourself. Repeat in three fresh contexts without expected answers or recorded results.

Unless overridden, the requested task is `task-eval` in `proj-eval`, status `active`, title `Document running skill evals`, description `Document how to run skill evals in this repository.` It has no dependencies. Native `task_show` is available and returns a confirmed successful task object. For dependency cases, the request is `Check whether task-eval is ready; do not start it`, and descriptions explicitly say `Depends on <ID>` unless stated otherwise. Dependency tool outcomes are supplied per fixture; do not infer results from task-list absence.

## Fixtures

| ID | Request/state and supplied outcomes |
| --- | --- |
| active | Check whether task-eval is ready; do not start it. Default task. |
| resume | Check readiness for resuming task-eval; status is inprogress. |
| done | Check readiness for task-eval; status is done. |
| cancelled | Check readiness for task-eval; status is cancelled. |
| waiting | Check readiness for task-eval; status is waiting, with no evidence its blocker was resolved. |
| missing-task | Check readiness for task-eval; task_show returns not_found. |
| failed-task | Check readiness for task-eval; task_show returns backend_error. |
| unclear | Check readiness for task-eval; both title and description are 'Improve it', with no target/outcome in other context. |
| pickup-details | Check readiness for task-eval; description is 'Document running skill evals in this repository. Decide which examples to include at pickup.' No formal acceptance criteria or implementation plan. |
| dep-done | Dependency task-dep is done in proj-eval, title 'Prepare eval fixtures'. |
| cross-done | Dependency task-cross is done in proj-other, title 'Publish shared fixture format'. |
| cross-active | Dependency task-cross is active in proj-other, title 'Publish shared fixture format'. |
| dep-waiting | Dependency task-dep is waiting, title 'Prepare eval fixtures'. |
| dep-progress | Dependency task-dep is inprogress, title 'Prepare eval fixtures'. |
| dep-cancelled | Dependency task-dep is cancelled, with no decision about waiving the prerequisite. |
| missing-dep | Dependency task-missing returns not_found. A hypothetical same-project task list would omit it. |
| failed-dep | Dependency task-dep returns backend_error, with no confirmed status. |
| uncertain-dep | Dependency task-dep returns an uncertain result, with no confirmed task/status. |
| unknown-dep | Dependency task-dep returns a task object with an unsupported status 'archived', not a confirmed done status. |
| unresolved | Description says 'Depends on the shared-format task'; no task ID or unique resolution is available. |
| related | Description says 'Document running skill evals. Related work: task-related explores dashboard styling; it is not a prerequisite.' task-related is active. |
| mixed | Description says 'Depends on task-dep and task-missing'. task-dep is done; task-missing returns not_found. |
| incidental | Description says 'Document the dependency graph example (A requires B) in the eval guide.' It names no task prerequisite. |
| early-terminal-dep | Check readiness for task-eval; it is done and its description says 'Depends on task-cross'. No dependency outcome has been supplied. |
| early-unclear-dep | Check readiness for task-eval; title is 'Improve it', description is 'Improve it. Depends on task-dep', and no target/outcome is known. No dependency outcome has been supplied. |
| execution-handoff | Work on task-eval. Override title/description with 'Explain in chat how skill evals are run; chat-only deliverable'. Applicable project instructions are already loaded and permit this direct chat work without plan/PR gates. Native task_show, task_update, and task_comment_create are available; the start and starting-comment calls each return confirmed success. Return readiness and the handoff through the first chat implementation action only, not completion. |

For each fixture return `id`, selected `route`, ordered `calls` (tool, arguments, owner), `readiness`, actual `response`, and `handoff` when relevant. Distinguish calls owned by preflight from calls owned by task-perform. Treat supplied outcomes as mock responses to proposed calls, not as permission to perform real actions.

## Repeating the simulation

Run the following from the repository root three times with an available provider/model. It supplies setup and fixtures without inspection criteria, reconciliation, or results:

```bash
python3 - <<'PY' | pi --print --no-session --no-extensions --no-mcp \
  --no-skills --no-prompt-templates --no-tools --no-context-files \
  --provider openai-codex --model gpt-6.1-sol --thinking low
from pathlib import Path

print('Controlled no-write simulation. Each fixture is independent. Mock '
      'outcomes are responses to proposed calls; no task is already loaded. '
      'Do not execute real actions or grade yourself. Return only a JSON '
      'array with id, route, calls (tool, arguments, owner), readiness, '
      'response (actual concise answer), and handoff if relevant. Keep each '
      'object compact. Stop execution-handoff at the first chat action.')
for skill in ['task-start-preflight', 'task-perform']:
    print(Path(f'skills/{skill}/SKILL.md').read_text())
print(Path('skills/task-pipeline/SKILL.md').read_text())
report = Path('docs/evals/task-start-preflight.md').read_text()
print(report.split('## Repeating', 1)[0])
PY
```

## Inspection criteria

- Standalone checks are read-only, without task comments, status updates, branch creation, implementation, or plan approval prompts.
- Active and resumed tasks with clear next intent are ready without resetting status, mandatory implementation plans, fixed report templates, or unrelated repository checks.
- Terminal/waiting states, load failures, and genuinely blocking ambiguity have explicit non-ready outcomes and only relevant next questions.
- Actual task dependencies are looked up directly by ID regardless of project. Only confirmed completion satisfies them; active/waiting/inprogress blocks, and cancellation requires a decision rather than implying completion.
- Missing, failed, unresolved, or partially checked references cannot yield readiness; absence from a filtered list is never completion evidence.
- Related work and incidental dependency language are not invented prerequisites.
- Execution uses the same shared check; task-perform, not preflight, owns confirmed start and the starting comment.

## Overlapping task reconciliation

`task-f568d931` proposed codemode aggregation while retaining ordered gates, a mandatory output template, and same-project task-list comparison. This task's approved simplification replaces those policies with concise readiness and direct cross-project dependency lookups. Keep the compatible intent (native tools, model judgment of clarity, read-only checks, explicit lookup failures), but do not add codemode or implement the conflicting policies. The older task's description and status are not changed by this work; any future codemode proposal must be reassessed against the shared contract rather than restoring the removed ceremony.

## Results

Evaluated the revised contract with three fresh Pi print-mode processes using `openai-codex/gpt-6.1-sol`, low thinking, with the flags above. Each process received all 26 fixtures as independent cases in one batch: 78 proposed traces, not 78 isolated sessions. Expected answers, inspection criteria, reconciliation, and results were not supplied. All three processes exited successfully.

An initial 22-case batch underspecified repository-instruction/tool availability in the execution-handoff fixture. Two runs explicitly paused for that missing context; one described a conditional handoff. This did not establish the intended complete start handoff. The fixture was clarified to supply loaded policy, available native tools, confirmed write responses, and a chat-only deliverable. The unclear-intent fixture also now explicitly overrides both title and description, and four additional uncertainty/early-stop cases were added. The skill itself was not changed in response to these fixture corrections. Only the final 26-case runs support the results below.

Inspected the final actual responses and ordered proposed calls:

| Property | Observed in all three final runs |
| --- | --- |
| Active/resumed readiness | Both returned ready with one task_show and no writes, redundant status transition, plan approval, or full report template. |
| Status/load/intent blockers | Done, cancelled, waiting, missing/failed task load, and unknown target/outcome returned explicit non-ready results. Early terminal/unclear cases did not query the named dependency. |
| Pickup details | Choosing documentation examples later did not require a plan or formal acceptance criteria to report ready. |
| Direct dependency checks | Looked up each actual dependency ID using task_show across project boundaries. Done dependencies permitted readiness; active/waiting/inprogress dependencies reported ID/title/status blockers. No task_list aggregation was proposed. |
| Unresolved prerequisites | Cancelled, missing, failed, uncertain, unsupported-status, unresolved-name, and mixed done/missing dependencies never yielded readiness. Responses explained the actual issue or requested the prerequisite decision/reference. |
| No invented prerequisites | Related work and incidental dependency-graph examples required no dependency lookup and did not block readiness. |
| Lifecycle ownership | Execution reused task-perform's fresh load, returned through shared readiness, then assigned the confirmed inprogress update and starting comment to task-perform before its first chat action. No preflight-owned writes were proposed. |

Representative response: `task-eval is active but blocked by task-cross, Publish shared fixture format (proj-other), which is active.` The cancelled-dependency case asked whether the prerequisite still applies instead of treating cancellation as completed work. Standalone responses stayed concise, with no empty report sections or implementation actions.

A mechanical check of the final JSON outputs confirmed all 26 unique fixture IDs per run, expected ready/non-ready outcomes, direct dependency IDs, no task_list calls, and only read calls in standalone traces. The execution case's call order was task_show, task_update with only taskId/status, then task_comment_create, all owned by task-perform.

The recorded runs predate task-d9b978d2's pipeline rewrite; they do not establish behavior of that later reference. See [Task Pipeline Evaluation](task-pipeline.md) for the full-reference evaluation.

Limitations: all tools, extensions, MCP, automatic skill discovery, and context-file discovery were disabled. These are proposed calls with mocked outcomes, not live native-tool executions, schema-validation tests, or a full discovery benchmark. Supplied neighboring skill text and batched contexts can prime responses; one model's runs do not guarantee future compliance. The separate calendar CLI's 11 tests and Ruff checks passed via ./scripts/pre-pr.sh; those checks do not validate skill behavior. git diff --check also passed.
