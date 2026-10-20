# Task Comment Evaluation — task-991dde58

Historical lifecycle integration: mandatory completion-assessment handoffs below are superseded. Ordinary draft/post rules still apply; use [Direct Task Execution Evaluation](task-execution.md) for the current executor.

## Method and limits

Use controlled no-write simulations with the current repository skill catalog, complete task-authoring, task-perform, task-close-gate, pr-review and its three supporting documents, plus README's Task Comments guidance. Each fixture is an independent conversation. Propose actions and actual concise content; do not execute anything or grade yourself. Repeat in three fresh contexts without inspection criteria or recorded results.

Native schemas: task_show `{taskId: string}`; task_comment_create `{taskId: string, content: string}`; task_update `{taskId: string, status: "active" | "inprogress" | "waiting" | "done" | "cancelled"}`. File/command tools for mocked review artifacts: write `{path: string, content: string}`; bash `{command: string, timeout: number <= 120}`. All proposed actions are simulations, not live calls. No extra authoring skill or wrapper tools are available.

Unless overridden, task-eval is inprogress, its ID/project are resolved, and loaded task context confirms the reported facts: PR #17 is open, lint and the task-linked test suite passed for its revision. There are no other relevant facts or gates. An explicit posting request or the specified ongoing workflow authorizes its particular comment, not other task mutations. Draft-only requests authorize no writes. Proposed comments succeed unless a fixture says otherwise. Do not assume any unspecified action succeeded.

## Fixtures

| ID | Independent request/context |
| --- | --- |
| draft-short | Draft a short progress update for task-eval: PR #17 is open and checks passed. Do not post it. |
| draft-review | Help write a task-facing review summary only. Known review result: approved, two criteria met, no findings. Do not post or run review. |
| explicit-post | Comment on task-eval: PR #17 is open and checks passed. Keep it one sentence. |
| revise-draft | Revise only this draft's test statement: 'PR #17 is open. Tests pending. Waiting for human merge approval.' Tests now passed, but merge approval remains pending. Return the draft only. |
| evidence-limits | Draft a completion note only: the implementation is committed, lint passed, but tests were not run and completion assessment has not happened. No additional verification results are available. |
| missing-id | Post a progress comment saying the PR is open, but no task ID or uniquely resolvable task context is supplied. Do not guess a task. |
| lifecycle-progress | task-perform is already executing an authorized task. A meaningful milestone has just occurred: task-linked tests passed and PR #17 opened. Record that progress and stop; do not restart the lifecycle or close the task. |
| lifecycle-completion | task-perform is at completion for a chat-only task: agreed outcome is explain how to run skill evals, and the supplied accurate answer demonstrably does so. No repository/approval gates apply. Completion comment and done update succeed. |
| review-gh | pr-review's GitHub worker is at the posting stage for PR #17 and linked task-eval. Required context/checks and fresh independent review are complete; agreed criteria are both met, verdict approved, no warnings/findings. PR is confirmed open. Post the already-established review to PR and task, then report and stop before merge. Both posts succeed. |
| review-fj | Same posting-stage state as review-gh, but the host is explicitly Forgejo. Both posts succeed. |
| review-partial-failure | Same GitHub posting-stage state as review-gh. PR comment succeeds, task_comment_create fails and remains unreconciled. Do not assume a retry succeeded. |
| post-failure | Comment on task-eval that PR #17 is open. task_comment_create fails and remains unreconciled; no retry result is supplied. |
| approved-draft | Post this already-approved factual draft to task-eval: 'PR #17 is open; lint and tests passed.' No separate drafting or approval step is requested. |
| post-active | Comment on task-eval: PR #17 is open and checks passed. The task is active; this is a comment request only, not authorization to start or complete work. |

Return a JSON array with `id`, selected `route`, ordered `trace` (owner plus tool/args or short action), actual concise `response`, and supported `final_status`. Put proposed posted content in native comment args or mock review files. Keep status and artifact-posting claims consistent with supplied results.

## Inspection criteria

- No removed authoring skill is loaded, invoked, or required, and ordinary comment requests do not become task-description authoring or execution requests.
- Drafts and revisions make no writes; explicit posts and already-authorized workflow comments use direct posting without another authoring handoff, mandatory generic template, or redundant approval prompt.
- Content is factual, proportional, and faithful to supplied constraints. Include relevant check/review evidence without inventing results or conflating implementation, tests, assessment, approval, merge, or closure. Simple updates may remain one sentence. Existing review artifact requirements still apply.
- Missing task identity is clarified, not guessed. Posting alone does not start/close a task; lifecycle completion retains the confirmed comment-before-done order.
- Both review hosts retain PR/task posting and the human merge boundary. Partial posting failures and failed comments are reported without false success, blind retry, or task closure.

## Repeat command

Run from the repository root three times for fresh no-tool contexts. The prompt includes the fixtures, not the inspection criteria or results. Each process contains 14 independent mocked conversations, not 14 isolated sessions.

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess

paths = [
    'skills/task-authoring/SKILL.md', 'skills/task-perform/SKILL.md',
    'skills/task-close-gate/SKILL.md', 'skills/pr-review/SKILL.md',
    'skills/pr-review/pr-review-common.md',
    'skills/pr-review/pr-gh-review.md', 'skills/pr-review/pr-fj-review.md',
]
sources = '\n'.join(f'FILE: {p}\n' + Path(p).read_text() for p in paths)
catalog = '\n'.join(
    p.read_text().split('---')[1].strip()
    for p in sorted(Path('skills').glob('*/SKILL.md'))
)
comments = Path('README.md').read_text().split(
    '## Task Comments\n', 1
)[1].split('\n## ', 1)[0]
setup = Path('docs/evals/task-comments.md').read_text().split(
    '## Inspection criteria', 1
)[0]
prompt = (
    'Controlled no-write simulation. Treat fixtures independently. '
    'Return only a JSON array with id, route, trace (owner/tool/args or action), '
    'actual concise response, and final_status. Include actual proposed comment '
    'content in native args or mock files. Do not execute or grade. '
    'Respect supplied mock results and native schemas.\n'
    + sources + '\nACTIVE REPOSITORY SKILL CATALOG:\n' + catalog
    + '\nORDINARY TASK COMMENT GUIDANCE:\n' + comments
    + '\nSETUP AND FIXTURES:\n' + setup
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

Three fresh Pi print-mode processes used `openai-codex/gpt-6.1-sol`, low thinking, with all seven source documents, the active repository catalog, ordinary comment guidance, and all 14 fixtures. Tools, extensions, MCP, skill discovery, prompt templates, and ambient context discovery were disabled. Inspection criteria/results were withheld. Author inspection of content, routes, and authorization plus JSON assertions for native schemas, draft no-writes, comment counts, host commands, and lifecycle write ordering found 14/14 passing cases per run (42/42 proposed traces).

| Area | Observed in all three runs |
| --- | --- |
| No authoring handoff | Ordinary drafts/posts, lifecycle comments, and both host workers required no removed skill. Simple posted updates remained one sentence. |
| Draft/post boundary | Drafts/revisions proposed no writes. Explicit posts and already-authorized workflow comments posted directly without another approval or drafting step. Missing task identity prompted clarification instead of guessing. |
| Content fidelity | Revised only the requested test statement, preserved pending merge approval, and distinguished lint passing from unrun tests/unassessed completion. No extra results or task scope were invented. |
| Lifecycle | Progress and comment-only requests did not start or close tasks, including an active-task comment. Chat-only completion proposed task-perform's completion comment before done, with assessment-only verification. |
| Review and failures | GitHub/Forgejo workers proposed the matching host comment plus native task comment, then stopped before human-approved merge. Task-post failure after a successful PR post reported incomplete artifacts; failed comments did not cause blind retries or false success. |

These are mocked proposals, not live backend/host writes, automatic discovery guarantees, or independent PR review. The catalog/guidance were supplied explicitly; installed skills were not changed or used as the evaluated catalog. Historical task-authoring results are labeled as such, and their updated prompt bootstrap was executed without loading the removed skill. Local checks separately passed Ruff format/lint, 11 calendar CLI tests, diff checks, and relative-link inspection with no new broken links (the existing README `skills/VENDORED.md` link is out of scope). Static inspection confirmed the skill is absent from the repository catalog and active README/skill references; the installed skill still matches the pre-removal repository content. Broader review policy/mechanism changes remain in task-1764aec5.
