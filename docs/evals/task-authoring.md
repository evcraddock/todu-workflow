# Task Authoring Evaluation — task-7278018a

## Method and limits

Use the fixtures below to evaluate intent capture, not implementation readiness. Supply the complete task-authoring skill and the descriptions of task-perform and task-comment-authoring to a fresh context. Treat every fixture as an independent conversation. No real tasks, files, or external artifacts may be created or updated. Propose the response and any tool/action trace only. Do not supply expected answers or the Results section to the evaluated model.

Repeat the batch in three fresh processes. Inspect the actual drafts for invented requirements, lost constraints, suggestion/decision confusion, unnecessary clarification, empty template sections, and authoring-versus-execution boundaries. A no-tool simulation tests instruction following, not live backend behavior or automatic skill discovery. The Python tests cover the separate calendar CLI, not skill compliance.

## Fixtures

| ID | Independent request/context |
| --- | --- |
| capture | Draft a task for adding retries to webhook delivery. Failed deliveries currently disappear; I want transient failures retried. Capture it for later, don't plan it now. |
| suggestion | Draft a task: webhook failures should be retried. An earlier agent suggested a dead-letter queue and production validation; I haven't agreed to either. |
| short | Draft a task: document how to run skill evals in todu-workflow. Keep it short; don't create it. |
| bug | Draft a bug: on iOS 18, tapping Sign in returns to the login screen instead of opening the dashboard. That's all I know; capture it for later. |
| constraints | Draft a task to add webhook retries. Only retry HTTP 503, keep the existing request timeout, and acceptance is that a 503 followed by 200 delivers once. It depends on task-eval-dependency. |
| open-question | Draft a task to make the settings dialog keyboard accessible. We haven't decided whether Escape should close it; record that question for pickup, don't block capture. |
| approved-validation | Draft a task to fix duplicate webhook delivery. I explicitly require production validation before completion. Preserve that requirement. |
| unclear | Draft a task to improve it. No earlier context is available. |
| update | Revise this existing draft to say retries apply only to HTTP 503. Existing text: 'Retry failed webhooks. Keep the existing timeout. Depends on task-eval-dependency.' Change nothing else. |
| create | Create a task in the already resolved project proj-eval: document how to run skill evals. Native task_create is available. Simulate the authored content and the handoff, without actually writing. |
| pickup | Pickup task-eval. Do not draft a new task; the requested work is execution of the existing task. |
| comment | Draft a progress comment for task-eval: the PR is open and checks are passing. |

For each fixture return `id`, selected `route`, actual `response` (draft title/description or clarification), and proposed `actions`. Keep each response concise; do not grade yourself.

## Repeating the simulation

Run from the repository root with an available provider/model. This supplies the fixtures without the inspection criteria or recorded results:

```bash
python3 - <<'PY' | pi --print --no-session --no-extensions --no-mcp \
  --no-skills --no-prompt-templates --no-tools --no-context-files \
  --provider openai-codex --model gpt-6.1-sol --thinking low
from pathlib import Path

print('Controlled no-write simulation. Treat each fixture as independent. '
      'Follow the supplied skills. Return only a JSON array with id, route, '
      'response (actual concise draft or clarification), and proposed actions. '
      'Do not grade yourself. Caller has native task tools.')
print(Path('skills/task-authoring/SKILL.md').read_text())
for skill in ['task-perform', 'task-comment-authoring']:
    print(Path(f'skills/{skill}/SKILL.md').read_text().split('---')[1])
report = Path('docs/evals/task-authoring.md').read_text()
print(report.split('## Fixtures\n', 1)[1].split('## Repeating', 1)[0])
PY
```

## Inspection criteria

- Captures known problem, desired outcome, relevant context, and explicit constraints without filling gaps with speculative implementation or verification work.
- Suggestions remain explicitly unapproved (or are omitted), not requirements. Explicitly requested validation and acceptance conditions are preserved.
- Brief captures and incomplete bug reports remain useful without mandatory headings, empty sections, invented reproduction steps, or a task-type questionnaire.
- Useful open questions can remain for pickup; genuinely missing task intent prompts a focused clarification.
- Revisions preserve unaffected intent, constraints, and explicit dependency IDs; missing IDs are never invented.
- Draft-only requests do not write; explicit creation hands authored content to the backend path. Pickup and comment requests route to their own skills.

## Results

Ran three fresh Pi print-mode processes with `openai-codex/gpt-6.1-sol`, low thinking, using the flags above. Each process received the complete revised task-authoring skill, neighboring skill descriptions, and all 12 fixtures without expected answers or results. All processes exited successfully. Inspected all 36 returned drafts/action proposals against the criteria above:

| Property | Observed in all three runs |
| --- | --- |
| Minimal intent capture | Webhook retry drafts retained the problem/outcome without adding retry policy, infrastructure, testing, rollout, or production obligations. Short documentation captures stayed one sentence. |
| Suggestion provenance | Dead-letter queues and production validation were explicitly not approved scope. The separate user-required production validation fixture preserved that requirement. |
| Flexible bug capture | Preserved iOS 18, the Sign in action, actual return to login, and expected dashboard without invented diagnostics or extra questions. |
| Constraints and revisions | Preserved the 503-only condition, existing timeout, supplied acceptance condition, and exact dependency ID. Revisions retained the unaffected timeout/dependency. |
| Questions | Retained Escape behavior as a question for pickup without blocking capture. Asked what to improve and the desired change only in the context-free ambiguous fixture. |
| Boundaries | Drafts proposed no backend writes. Creation proposed caller handoff to task_create; pickup selected task-perform and comments selected task-comment-authoring. |

Representative observed output was `Retry transient webhook failures` with `Failed webhook deliveries currently disappear. Retry transient failures so those deliveries are not lost.` The open-question fixture appended `Question for pickup: should Escape close the dialog?` rather than choosing a behavior. No run introduced empty template sections or invented dependency IDs; all returned titles were within 60 characters.

These are 36 responses across three batched contexts, not 36 isolated sessions. The retry example in the skill overlaps the capture fixture, so that case is not an independent generalization test. Neighbor descriptions were supplied explicitly and all tools, extensions, MCP, skill discovery, and context-file discovery were disabled. Creation was a proposed handoff, not a validated native-tool call or live write. No claim is made about automatic discovery, complete tool schemas, other models, or guaranteed future scope fidelity.

Local regression verification also passed `./scripts/pre-pr.sh` (Ruff format/lint and 11 calendar CLI tests) and `git diff --check`. Those checks do not establish skill compliance.
