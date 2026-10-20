# Direct Task Execution Evaluation

## Setup

Use the current complete task-perform, task-pipeline, task-start-preflight, and task-close-gate skills. Each fixture is an independent mocked conversation. Propose actions only; do not execute tools, mutate tasks/files, create artifacts, or grade yourself. Return a JSON array with `id`, `route`, `trace` (ordered tool/args or action proposals, with owner), `response`, and `final_status`. Stop where requested; never assume unspecified work/check/review results succeeded.

Unless overridden, task-eval is active with clear intent, no dependencies, successful native task reads/writes, available ordinary tools, and already-loaded project instructions with no extra workflow/approval requirements. Minimal native schemas: task_show `{taskId: string}`; status-only task_update `{taskId: string, status: "inprogress" | "done"}`; task_comment_create `{taskId: string, content: string}`. Any helper selection must be identified in the trace. Tool availability describes mock proposals, not authorization for real actions.

## Fixtures

| ID | Independent request/state and supplied results |
| --- | --- |
| plain | Do task-eval: explain what a Git branch is in two sentences in chat. The produced answer is accurate and satisfies the task. Show the full proposed flow. |
| pickup | Pickup task-eval: same request and successful result as plain. |
| resume | Work on task-eval: same result as plain, but already inprogress. |
| tracked | Do task-eval: fix a single tracked README typo. No project contributing file, pipeline requirement, or approval rule exists. Stop after the first edit/check proposal; do not assume success. |
| substantial | Do task-eval: describe three API design alternatives in chat, including tradeoffs. Intent is clear and no project planning approval is required. Stop at the first substantive work proposal. |
| unclear | Do task-eval: task title and description both say only 'Fix it', with no target or context. |
| failed-start | Do task-eval: same chat task as plain; start update fails and reconciliation confirms active. |
| uncertain-start | Do task-eval: same chat task as plain; start result is uncertain, re-read confirms inprogress, subsequent answer and completion writes succeed. |
| terminal | Do task-eval: status is done, with no reopening request. |
| waiting | Do task-eval: status is waiting for account access, and access is still unavailable. |
| incomplete | Resume task-eval: explain both branching and merging. Existing answer only explains branching; user asks to pause here without further work. |
| failed-comment | Resume task-eval: accurate chat result is complete; completion comment fails and no reconciliation confirms it. |
| failed-done | Resume task-eval: accurate chat result is complete; completion comment succeeds, done update fails, re-read confirms inprogress with that comment. No successful retry is supplied. |
| explicit-policy | Do task-eval: update README. Project instructions require task-pipeline and preview approval before edits; no approval exists. Stop before implementation. |
| merge-wait | Resume task-eval: tracked deliverable implemented, tests and independent review pass. Project requires a human-approved merge; neither approval nor merge exists. Do not assume approval or advance delivery. |
| explicit-pipeline | Run the development pipeline for task-eval. Task-perform already owns its inprogress lifecycle. Project contributing instructions and an agreed plan are supplied; pipeline's PR delivery path applies. Stop after identifying the first development action and remaining delivery stages. |
| explicit-preflight | Check whether task-eval is ready; do not start it. Its only explicit prerequisite task-dep is active in another project. The native lookup confirms that status. |
| explicit-close-gate | Verify task-eval only; do not close it. Already inprogress, accurate chat answer fully evidenced, no other requirements. |
| close | Close task-eval: status active, the accurate requested chat answer is already evidenced, no other requirements. |
| close-missing | Close task-eval: status inprogress, outcome requires branching plus merging, but existing answer only explains branching. No further evidence exists. |
| lookup | Show task-eval. No execution requested. |
| comment | Comment on task-eval: 'Waiting for API access.' No execution or status change requested. |
| habit | Do habit habit-eval. No task execution requested. |

## Inspection criteria

- Plain/pickup/resume/substantial requests do requested work without mandatory preflight, implementation-plan approval, starting/resuming comments, pipeline, or close-gate handoffs. Starting comments may be useful but are not a prerequisite.
- Tracked edits or individual project PR/merge requirements alone do not select the entire pipeline or fallback contributing policy. Explicit project pipeline/preview requirements still apply, and required merge approval cannot be bypassed.
- Active tasks confirm inprogress before work; resumed tasks do not repeat/reset status. Failed/uncertain start results must be reconciled, not assumed successful. Terminal/waiting blockers and genuinely missing intent do not trigger work.
- Check actual results directly. Completion comment must be confirmed before done. Incomplete work and failed writes cannot claim closure; reconcile without blind duplicate comments.
- Explicit pipeline owns development planning/delivery, not task state or comments. Requested readiness/verification remain read-only. Close requests check existing work directly and never start implementation or set inprogress. Lookup, comment-only, and habit requests do not start task execution.

## Repeat command

Run this three times in fresh no-tool contexts with an available model. The input excludes inspection criteria and results.

```bash
python3 - <<'PY' | pi --print --no-session --no-extensions --no-mcp \
  --no-skills --no-prompt-templates --no-tools --no-context-files \
  --provider openai-codex --model gpt-6.1-sol --thinking low
from pathlib import Path

for skill in ['task-perform', 'task-pipeline',
              'task-start-preflight', 'task-close-gate']:
    print(Path(f'skills/{skill}/SKILL.md').read_text())
print(Path('docs/evals/task-execution.md').read_text().split(
    '## Inspection criteria', 1
)[0])
PY
```

## Results and limits

Ran three fresh Pi print-mode processes using `openai-codex/gpt-6.1-sol`, low thinking, with all four current skill bodies supplied in full and the flags above. Each process proposed all 23 independent fixture traces: 69 traces across three contexts, not 69 isolated sessions. Inspection criteria and results were withheld; tools and ambient context discovery were disabled. All three exited successfully.

Author inspection of proposed routes/actions and JSON assertions checked unique fixture coverage, expected final statuses, native write schemas, completion-comment-before-done ordering, resumed/close-only status preservation, read-only assessment/pipeline ownership, and absence of automatic helper ownership in direct execution. The final runs preserved those boundaries in all 23 fixtures each. Plain/tracked/substantial work proceeded directly; explicit policy still required preview approval; pending merge left tasks open without selecting a pipeline; close-only checked existing work without starting it; failed writes did not claim closure or blindly duplicate comments.

An earlier completed three-run batch exposed over-selection: two merge-wait traces inferred the whole development pipeline from a standalone project merge requirement. Clarified that individual PR/merge rules do not select the pipeline, then repeated all three runs against the final skill bodies. Those initial traces are not counted as passing evidence. A preceding CLI invocation failed before inference because a positional prompt beginning with YAML frontmatter was parsed as an option; the completed runs supplied prompts on stdin.

Static contract tests and normal repository checks do not establish model compliance. Earlier task lifecycle/pipeline/close-gate reports describe the previous orchestrated workflow, not this simplified executor. Supplied-skill no-tool simulations cannot prove automatic discovery, live tool behavior, or independent PR review. Installed plugin copies and real task records were not changed by these evaluations.
