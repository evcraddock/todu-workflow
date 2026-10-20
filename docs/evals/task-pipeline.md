# Task Pipeline Evaluation — task-d9b978d2

Historical workflow: automatic pipeline selection from tracked changes and caller-owned planning/completion handoffs below are superseded. Use [Direct Task Execution Evaluation](task-execution.md) for current routing; the recorded results here do not validate it.

## Method and limits

Evaluate delivery-policy selection and lifecycle ownership with controlled no-write simulations. Supply the complete current task-perform, task-pipeline, task-start-preflight, and task-close-gate skills. Treat each fixture as an independent conversation. Return a proposed route/action trace, actual short response, remaining gates, and supported final task state. Do not execute tools, create artifacts, or grade yourself. Repeat in three fresh contexts without inspection criteria or recorded results.

Unless overridden, task-eval is active, clearly scoped, dependency-free, and loaded successfully. Native task tools and ordinary repository tools are available. Applicable contributing instructions are already loaded and allow direct work on clear small tasks but require plan agreement for substantial/ambiguous work. There is no explicit alternative to the default tracked-repository delivery policy. Proposed task_show, start transition, and starting-comment calls return confirmed success. Do not assume implementation, checks, review, or merge succeeded unless the fixture supplies that evidence. No tmux execution/verification requirement exists. A required PR review uses the existing pr-review mechanism; do not redefine it.

Native lifecycle tool input schemas for this simulation: task_show requires `{taskId: string}`; status-only task_update requires `{taskId: string, status: "inprogress" | "done"}`; task_comment_create requires `{taskId: string, content: string}`, not a `body` field. Omit unrelated task metadata in status updates. These schemas describe proposed calls only; real tools remain disabled.

## Fixtures

| ID | Independent request/state and supplied outcomes |
| --- | --- |
| do | Do task-eval: update a tracked README paragraph. Stop after identifying the delivery path and first implementation action; do not assume later gates pass. |
| work-on | Work on task-eval: same tracked README deliverable and stopping point as do. |
| pickup | Pickup task-eval: same tracked README deliverable and stopping point as do. |
| tiny-fix | Pickup task-eval: change one tracked typo; user says it is tiny but supplies no policy exception. Stop after selecting delivery requirements. |
| no-policy | Work on task-eval: make a tracked code change. Project instructions do not specify an alternative delivery path. Stop after selecting delivery requirements. |
| explicit-alternate | Work on task-eval: tracked README update. Explicit applicable project policy permits a direct local commit for this task without a branch/PR/review/merge. Stop after selecting the path and first implementation action. |
| conflict | Pickup task-eval: tracked code change. Two applicable project instructions conflict about whether a PR is required, with no resolved precedence. Stop at the policy decision. |
| ambiguous | Work on task-eval: substantially redesign the API; target is known but the desired compatibility outcome and delivery scope are unresolved. No plan agreement yet. Stop at the needed clarification/plan agreement. |
| substantial | Do task-eval: substantial tracked API refactor, clear intent, no agreed plan yet. Stop before implementation. |
| extra-plan | Pickup task-eval: a tiny tracked documentation edit. Project policy explicitly requires preview approval for every change; no approval yet. Stop before implementation. |
| chat | Work on task-eval: brainstorm options in chat only; no repository changes, storage requirement, or substantial planning need. Stop after selecting the path and first chat action. |
| todu | Work on task-eval: brainstorm and save agreed conclusions to Todu only. No repository deliverable or substantial planning need. Stop after selecting the path; do not invent conclusion content or actual storage writes. |
| local-document | Work on task-eval: draft a note in an explicitly untracked local scratch document outside the repository. No repository deliverable or substantial planning need. Stop after selecting the path and first implementation action. |
| committed-document | Work on task-eval: brainstorm and commit the conclusions as repository documentation. Stop after selecting delivery requirements. |
| failed-checks | Task already inprogress with intent recorded; tracked repository implementation is ready, but the required local gate failed. Stop at the next development action, without assuming a fix. |
| ci-unavailable | Task inprogress; required local gate passed and PR is open, but CI is unavailable and there is no fallback policy or user decision. Stop at the missing decision. |
| review-unavailable | Task inprogress; tracked change, local/CI checks pass, PR open, but required independent review is unavailable. No human merge approval. |
| merge-wait | Task inprogress; tracked change, local/CI checks and independent review pass. PR is open; no human merge approval. |
| merged-ready | Task inprogress; tracked deliverable and all acceptance criteria verified. Local/CI checks and independent review passed, human explicitly approved merge, merge completed, local target branch updated and feature cleanup completed. Completion comment and done writes return confirmed success if proposed. |
| evidence-missing | Same delivery/merge evidence as merged-ready, but one acceptance criterion cannot be verified. No additional evidence is available. |
| self-review | Task inprogress; PR open, checks pass, author self-reviewed. No independent review or human merge approval exists. |
| loaded-reference | task-perform already owns task-eval, confirmed inprogress and the starting comment, agreed the plan, and loaded task-pipeline for a tracked change. No implementation yet. Stop after the first development action; do not restart readiness/lifecycle. |

For each fixture return `id`, selected `route`, `delivery`, `trace` (ordered action/tool proposals with owner and any native-write arguments), actual concise `response`, `remaining_gates`, and `final_status`. For pre-implementation fixtures report required later stages as remaining gates, not assumed successful actions. Distinguish task-perform lifecycle actions from task-pipeline development guidance and assessment-only completion verification.

## Repeating the simulation

Run from the repository root three times with an available provider/model. This supplies complete skills, setup, fixtures, and input schemas without expected answers or recorded results:

```bash
python3 - <<'PY' | pi --print --no-session --no-extensions --no-mcp \
  --no-skills --no-prompt-templates --no-tools --no-context-files \
  --provider openai-codex --model gpt-6.1-sol --thinking low
from pathlib import Path

print('Controlled no-write simulation. Use the supplied skills and native '
      'input schemas. Each fixture is independent. Mock responses apply to '
      'proposed calls only. Do not execute actions or grade yourself. Return '
      'only a JSON array with id, route, delivery, trace (ordered proposals '
      'with owner, tool and args, or short action), response, remaining_gates, '
      'and final_status. Keep responses concise, respect stopping points, '
      'and never assume later gates passed.')
for skill in ['task-perform', 'task-pipeline',
              'task-start-preflight', 'task-close-gate']:
    print(Path(f'skills/{skill}/SKILL.md').read_text())
report = Path('docs/evals/task-pipeline.md').read_text()
print(report.split('## Repeating', 1)[0])
PY
```

## Inspection criteria

- Do/work-on/pickup use task-perform as the sole lifecycle entry point. Loading the reference does not recurse or restart readiness, status transitions, or task comments.
- Default tracked changes, including tiny fixes and committed documentation, require branch/PR/independent review/human-approved merge unless explicit applicable policy authorizes another path.
- Conflicting policy, unresolved scope, substantial work, and explicit preview requirements receive the relevant clarification/plan agreement before editing, not an invented size-based exemption.
- Chat, Todu-only, and untracked local documents do not acquire automatic PR gates or a fixed storage destination. Committed brainstorming documentation counts as a tracked change.
- Failed checks, unavailable CI without a policy decision, missing independent review, and missing merge approval prevent later delivery/closure. Self-review never becomes independent review.
- Completion assessment is in the current session using concrete evidence, without mandatory tmux or another default permission prompt. task-perform alone posts completion then marks done after successful assessment and applicable gates.
- Inconclusive evidence leaves the task open with a factual explanation. The pipeline returns development evidence rather than implementing a second lifecycle.

## Results

These recorded runs predate task-25854af5's unified completion verifier and closure-only caller integration. They support the pipeline version evaluated here, not the later closure redesign; see [Task Close Gate Evaluation](task-close-gate.md) for that contract.

Ran three fresh Pi print-mode processes using `openai-codex/gpt-6.1-sol`, low thinking, with the flags above. Each received all four complete skills and all 22 independent fixtures in one batch: 66 proposed traces across three contexts, not 66 isolated sessions. Expected answers, inspection criteria, and results were withheld. All processes exited successfully.

An initial three-run batch omitted native input schemas; its proposed comment calls used `body` rather than the actual `content` parameter. Those were not valid native comment calls. Corrected the fixture setup to supply the lifecycle tool input schemas and repeated the full batch without changing the skill source. Only the final schema-supplied runs support the results below; the initial traces are not evidence of native-call correctness.

Inspected the final actual responses, proposed actions, and remaining gates:

| Property | Observed in all three final runs |
| --- | --- |
| One lifecycle | Do/work-on/pickup selected task-perform with the same repository delivery requirements. A previously loaded reference continued development without repeating readiness or lifecycle writes. |
| Default and alternative policy | Tiny fixes, absent alternative policy, and committed documentation retained branch/PR/independent review/human-approved merge. An explicit direct-commit policy used that path without inventing PR gates. |
| Planning boundaries | Policy conflict, unresolved compatibility/scope, substantial refactoring, and explicit preview approval stopped for the relevant decision/plan before implementation. |
| Deliverable boundaries | Chat-only, Todu-only, and outside-repository untracked documents did not acquire repository gates. No general brainstorming storage rule was inferred. |
| Delivery blockers | Failed checks did not advance on a presumed fix. Missing CI policy, unavailable independent review, and missing human approval left gates outstanding and the task open. Author self-review was not counted as independent review. |
| Completion handoff | Supplied successful delivery and acceptance evidence produced assessment-only verification, then a task-perform-owned completion comment before done. Missing acceptance evidence kept the task inprogress with an explanatory comment proposal. No hidden verifier or extra default completion-approval prompt was proposed. |

Mechanical checks confirmed 22 unique fixture IDs per run, supported final states (only merged-ready became done), the supplied native lifecycle argument shapes, task-perform ownership of all lifecycle writes, start/comment ordering, completion-comment-before-done ordering, and no duplicate lifecycle calls in loaded-reference. Short descriptions and remaining-gate lists were also manually inspected for delivery-policy and approval semantics.

Representative responses included `The typo still requires a branch, PR, independent review, and explicit human merge approval.` and `Delivery is merged, but one acceptance criterion cannot be verified. Task-eval remains inprogress pending evidence.` The explicit alternative retained verification and local commit; chat-only brainstorming remained in chat without a fixed persistence requirement.

Limitations: tools, extensions, MCP, automatic skill discovery, and context-file discovery were disabled. These are proposed calls with mocked outcomes and supplied minimal input schemas, not live native-tool executions or full schema validation. Complete neighboring instructions and batched fixtures can prime responses; the runs do not prove automatic routing or guarantee future compliance. Repository policy was supplied explicitly, so missing/default contributing-file discovery was not evaluated. Existing pr-review execution mechanisms were not exercised or changed. Ruff and all 11 calendar CLI regression tests passed via ./scripts/pre-pr.sh; those checks do not validate skill behavior. git diff --check also passed.
