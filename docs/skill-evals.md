# Skill Evaluation Matrix

Use this matrix when changing skill descriptions, trigger wording, or routing-sensitive skill bodies.

The goal is not to prove that the model followed one exact path. The goal is to check whether the expected skill is selected, whether nearby skills stay out of the way, and whether the final behavior matches the user's intent.

## Manual Eval Process

1. Start from a clean session or a fresh agent context when practical.
2. Run each prompt as written.
3. Record the selected skill, whether the expected outcome happened, and any confusing routing.
4. Repeat high-risk prompts at least three times because agent routing can vary.
5. If routing fails, fix the relevant skill description first. Only change the skill body when the description is already clear and the loaded instructions are the problem.

## Grading

| Result | Meaning |
| ------ | ------- |
| Pass | The expected skill or fallback was used and the expected outcome happened. |
| Warning | The outcome was acceptable, but routing was hesitant, noisy, or depended on extra clarification. |
| Fail | The wrong skill handled the prompt, a required skill did not trigger, or the outcome violated the expected boundary. |

## Prompt Matrix

Rows that name a skill are should-trigger cases. Rows that expect an ordinary fallback, task search/list path, or backend write path are should-not-trigger cases for nearby skills that should stay out of the way.

| ID | Prompt | Expected skill or fallback | Expected outcome | Failure signals |
| -- | ------ | -------------------------- | ---------------- | --------------- |
| E01 | Create a task for adding retry logic to webhook delivery. | `task-authoring`, then task creation path if requested | Captures known intent and explicit constraints in a clear title and concise description, then hands content to the backend creation path. | Invents retry policy, production validation, acceptance criteria, or dependencies; forces empty sections; or never hands off explicit creation. |
| E02 | Draft a task for fixing mobile login but do not create it yet. | `task-authoring` | Captures known bug details without mandatory reproduction steps; asks only if missing intent prevents a useful draft. Returns content only. | Invents diagnostics or scope, blocks capture on a complete bug template, writes a task record, or starts implementation. |
| E03 | Add a task to todu-workflow: Document skill evals. | task creation path, with `task-authoring` if content needs shaping | Captures the concise documentation intent and uses the requested backend creation path once the project is resolved. | Pads the task with speculative requirements or empty sections, or never writes when creation is explicitly requested. |
| E04 | Write a progress update for task #123 saying the PR is open and checks are passing. | Ordinary drafting, no skill handoff | Returns a concise factual draft without posting; no mandatory template. | Invokes a standalone comment-authoring skill, invents results, posts without authorization, or changes the task. |
| E05 | Comment on task #123: PR is open and checks are passing. | Native task_comment_create | Posts the authorized factual comment directly, confirms success, and permits a one-sentence update. | Only drafts, adds a redundant authoring/approval step, invents results, or starts/closes the task. |
| E06 | Do task #123. | `task-perform` | Checks readiness/instructions, confirms inprogress before work, posts meaningful comments, verifies the outcome and applicable gates, then comments and marks done without another default approval. | Works before confirmed start, skips evidence, asks for redundant default completion approval, or bypasses an explicit project gate. |
| E07 | Pickup task #123. | `task-perform`, with task-pipeline guidance when applicable | Uses the same lifecycle as do/work-on; obtains required plan approval and selects development stages from deliverable/project policy. | Routes to a competing lifecycle, repeats lifecycle actions when loading the reference, skips confirmed start, or mandates tmux/extra completion-verification approval. |
| E08 | Show task #123. | Todu task show fallback or task-show capability | Displays task details only. | Triggers `task-perform` or `task-pipeline` and changes task status. |
| E09 | Close task #123. | `task-perform` closure-only path with `task-close-gate` assessment | Verifies the agreed outcome and applicable gates without starting work; the owner confirms completion comment before done only when ready. | Starts implementation/preflight, sets inprogress, lets the verifier write, or closes with missing evidence. |
| E10 | Do habit #15. | Ordinary agent handling; no dedicated repository skill | Remains outside the task lifecycle; no habit-execution workflow is prescribed by this repository. | Selects a removed or invented replacement habit skill, or invokes task-perform for a habit. |
| E11 | I did habit #15. | Native habit-tool path or ordinary agent handling | Treats this as a habit report, not a task execution request or a dedicated repository workflow. | Requires an unavailable habit skill or starts the task lifecycle. |
| E12 | Do task #15. | `task-perform` | Treats `#15` as a task, not a habit. | Routes to habit skills because the wording includes "do". |
| E13 | Search the web for the latest Playwright release notes. | Configured web-search capability, if available | Uses available search tooling and summarizes sources; reports a missing capability honestly. | Invokes a removed skill, installs a replacement without approval, or invents search results when no capability is available. |
| E14 | Extract the article text from `https://example.com/some-article`. | Configured page-fetch/extraction capability, if available | Uses available static extraction without requiring browser UI; reports unavailable access honestly. | Invokes a removed skill, installs a replacement without approval, or claims content was fetched without evidence. |
| E15 | Open localhost:3000 and click the login button. | Configured external browser integration, if available | Uses the available browser capability; reports a missing capability honestly when none is configured. | Invokes a removed skill, installs a replacement without approval, substitutes static extraction for interaction, or claims success without browser evidence. |
| E16 | Test the checkout flow in the Electron app. | `electron-testing` | Launches/connects to Electron via CDP and exercises UI flow. | Uses ordinary browser tools for a desktop Electron target. |
| E17 | Create a new TypeScript app. | `project-init` | Starts the end-to-end project initialization questionnaire and flow. | Only scaffolds docs or only creates a repo. |
| E18 | Scaffold README, LICENSE, AGENTS.md, and docs for this repo. | `project-scaffold` | Generates foundational project files only. | Runs full `project-init` or adds lint/dev environment tooling. |
| E19 | Add ESLint and Vitest to this project. | `quality-tooling` | Adds quality tooling for the stack. | Triggers `dev-environment` or `project-scaffold`. |
| E20 | Add a Makefile and overmind setup. | `dev-environment` | Adds dev-environment scaffolding. | Adds lint/test configuration or runs full project initialization. |
| E21 | Create a GitHub repo for my new CLI and clone it. | Ordinary agent handling with available host CLI | Handles repository creation/cloning without a dedicated repository skill; resolves missing target/visibility decisions and leaves registration/scaffolding out of scope. | Invokes a removed or replacement repository skill, silently selects public visibility, or runs registration/scaffolding without a separate request. |
| E22 | Use a sub-agent to review the API design. | `tmux` | Starts a detached sub-agent orchestration flow and returns the result. | Performs the review inline without tmux after the user explicitly asked for a sub-agent. |
| E23 | Run `npm test`. | Ordinary shell command fallback | Runs the command directly in the current shell context. | Triggers `tmux` even though no tmux/sub-agent session was requested. |
| E24 | What should I work on next? | `nextactions` | Recommends ready work by high/medium/low priority and explicit dependencies, including useful prerequisites, with honest blockers/uncertainty and no writes. | Excludes undated medium/low work, uses urgency-only filters, recommends blocked goals, treats unknown dependencies as done, widens project scope silently, or starts/modifies tasks. |
| E25 | Find tasks about skills in todu-workflow. | task search/list path | Searches or lists matching tasks. | Triggers `nextactions`, which is only for prioritized next work. |
| E26 | Request review for PR #79 for task #123. | `pr-review` | Obtains fresh-context evidence-based review, confirms PR/task artifacts, reports limitations accurately, and stops before remediation or merge. | Substitutes unlabeled self-review, defaults unknown hosts to Forgejo, blocks on speculation alone, automatically fixes suggestions, merges, or claims completion with unconfirmed artifacts. |
| E27 | Start a project review. | Ordinary agent handling; no dedicated repository skill | Handles the project request without assuming a prescribed repository review workflow. | Selects a removed or invented replacement project skill, or misroutes to PR review or task execution. |
| E28 | Show active tasks in todu-workflow. | task search/list path | Lists matching tasks without starting a guided review. | Starts a guided review or changes task state for a listing request. |
| E29 | Review only my high-priority projects. | Ordinary agent handling; no dedicated repository skill | Handles the supplied project request without assuming a prescribed repository review workflow. | Selects a removed or invented replacement project skill, or misroutes to PR review or task execution. |
| E30 | Work on task #123; it is already inprogress. | `task-perform` | Runs read-only readiness without resetting status, posts a resuming comment, and follows the same execution lifecycle. | Blocks solely because it is inprogress, resets active, or redundantly starts it. |
| E31 | Do task #123. The inprogress update fails and task_show still reports active. | `task-perform` | Reports the failed transition and does no implementation or completion write. | Starts work or claims inprogress without confirmation. |
| E32 | Do task #123. Its status is done (repeat with cancelled). | `task-perform` | Reports terminal state and requests any needed reopening decision without silently mutating or executing. | Reopens or performs the task automatically. |
| E33 | Do task #123. Work is implemented, but an acceptance criterion cannot be verified. | `task-perform` | Records what remains and keeps the task open; no done update. | Treats partial/inconclusive evidence as complete or invents proof. |
| E34 | Do task #123. Verification passes, but the completion comment fails. | `task-perform` | Reports the failure and does not mark done; reconciles uncertainty before any retry. | Marks done before confirmed comment success or claims a comment was posted. |
| E35 | Do task #123. The completion comment succeeds but updating done fails. | `task-perform` | Reports the partial result and reconciles state before retrying without blindly duplicating the comment. | Claims done or blindly reposts the completion comment. |
| E36 | Work on task #123: brainstorm options in chat only. | `task-perform` | Clarifies/approves the plan as required, confirms start, records meaningful updates, and verifies the agreed chat deliverable without automatic PR or fixed result-storage requirements. | Requires a repository/merge or assumes brainstorming must be stored in Todu. |
| E37 | Pickup task #123: update README; project policy requires PR and human-approved merge. | `task-perform` with development guidance | Follows required plan/start steps and development gates, then waits for explicit merge approval before closure. | Calls documentation too small for review, self-approves merge, or closes before required merge. |
| E38 | Do task #123. Required independent review is unavailable. | `task-perform` | Documents the blocker and leaves the task open without silently substituting self-review. | Bypasses the review gate or mandates tmux as the only execution/verification path. |
| E39 | Check whether task #123 is ready; do not start it. | `task-start-preflight` | Returns concise read-only readiness with actual blockers or clarification, without a mandatory report or start action. | Starts the lifecycle, posts comments, changes status, or requires plan approval merely to check readiness. |
| E40 | Do task #123. The starting comment fails after inprogress succeeds. | `task-perform` | Reports/reconciles the failed comment before work; accurately leaves the confirmed status inprogress. | Performs work while pretending intent was recorded or rolls back status silently. |
| E41 | Do task #123. Verification passes and no project approval gate remains. | `task-perform` | Assessment-only verifier returns evidence without writes; lifecycle owner posts one completion comment, confirms success, then marks done. | Both skills close/comment, a tmux session is required, or another default completion approval is requested. |
| E42 | Check readiness for task #123; it depends on task-cross, active in another project. | `task-start-preflight` | Directly loads task-cross with native task_show and reports its ID/title/status as a blocker. | Only lists same-project tasks, treats list absence as completion, or reports ready. |
| E43 | Check readiness for task #123; its prerequisite returns not_found or a backend error. | `task-start-preflight` | Reports the unresolved reference or failed lookup explicitly; does not approve readiness. | Silently counts missing, failed, or unchecked references as satisfied. |
| E44 | Check readiness: document running skill evals; examples will be chosen at pickup. | `task-start-preflight` | Clear intent is ready without a fully specified implementation or acceptance-criteria template. | Treats nonblocking pickup details as missing requirements or plans/implements during preflight. |
| E45 | Check readiness for task #123; its prerequisite was cancelled, with no waiver decision. | `task-start-preflight` | Explains that cancellation does not prove completion and requests the prerequisite decision. | Silently treats cancelled as done or changes either task. |
| E46 | Check readiness for task #123; its only prerequisite is done in another project. | `task-start-preflight` | Confirms the prerequisite directly, then reports ready without status/comment writes. | Blocks cross-project resolution, resets inprogress, or substitutes project-local aggregation. |
| E47 | Pickup task #123: fix one tracked typo; no explicit project exception. | `task-perform` with task-pipeline guidance | Keeps the default branch/PR/independent review/human-approved merge requirements despite the tiny change. | Treats size or documentation as permission to bypass applicable review. |
| E48 | Work on task #123: brainstorm and save conclusions only to Todu. | `task-perform` | Honors the agreed backend-only deliverable without automatic repository gates or a fixed general storage rule. | Imposes PR/merge or assumes all brainstorming must use this destination. |
| E49 | Work on task #123: tracked change; explicit project policy permits direct local commit. | `task-perform` with applicable development guidance | Uses the explicit alternative while preserving its approval and verification requirements. | Invents an exception or ignores an explicit applicable delivery policy. |
| E50 | Pickup task #123: conflicting applicable PR policies, no resolved precedence. | `task-perform` | Resolves policy during planning before editing. | Silently chooses a convenient policy or starts editing before resolution. |
| E51 | task-perform has already started task #123 and loaded task-pipeline. | `task-pipeline` as reference only | Continues applicable development stages and returns evidence to the lifecycle owner. | Restarts readiness/status/comments, recursively invokes task-perform, or owns task closure. |
| E52 | Verify completion of task #123 only; do not close it. | `task-close-gate` | Returns evidence and concise readiness without lifecycle writes or closure claims. | Posts a comment, changes status, or hands off for unauthorized closure. |
| E53 | Verify task #123; its only evidence is a comment saying done. | `task-close-gate` | Finds supporting evidence or returns not ready with the actual gap; the claim alone is insufficient. | Treats unsupported prior claims as proof or invents completion evidence. |
| E54 | Verify task #123; one relevant non-destructive targeted check can resolve missing evidence. | `task-close-gate` | Runs the permitted proportionate check, then reports the supported assessment without implementation or unrelated exploration. | Prohibits all commands, adds default approval merely to verify, implements a fix, or runs an unrelated full suite. |
| E55 | Verify task #123; it has an agreed chat outcome but no acceptance-criteria section. | `task-close-gate` | Assesses the agreed outcome against relevant evidence without requiring sections or inventing scope. | Requires a template or creates new acceptance obligations. |
| E56 | Verify and close an active task #123 whose agreed deliverable is already evidenced. | `task-perform` closure-only path | Assesses existing work, preserves gates, then records completion and done without an intermediate start transition. | Sets inprogress, starts work, silently reopens terminal tasks, or duplicates lifecycle writes. |

## Coverage Checklist

- Task execution boundary: E06-E09, E30-E41 (also run work-on/start/get-started wording variants).
- Shared read-only readiness and direct dependencies: E39, E42-E46; use [Task Start Preflight Evaluation](evals/task-start-preflight.md) for the full status, ambiguity, reference, and execution-handoff fixtures.
- Lifecycle write ordering/failures: E30-E35, E40-E41.
- Shared completion assessment and closure-only ownership: E09, E41, E52-E56; use [Task Close Gate Evaluation](evals/task-close-gate.md) for unsupported/stale/partial evidence, targeted checks, status handling, and closure write failures.
- Deliverable-based development and independent-review gates: E36-E38, E47-E51; use [Task Pipeline Evaluation](evals/task-pipeline.md) for complete-reference policy, planning, ownership, and completion-handoff cases.
- Run lifecycle scenarios with mocked tools or explicit no-write simulation; do not mutate live task #123 or create external artifacts merely to evaluate routing.
- Task descriptions versus ordinary comments: E01-E05. Use [Task Authoring Evaluation](evals/task-authoring.md) for scope fidelity, suggestion provenance, flexible capture, revisions, and pickup boundaries; use [Task Comment Evaluation](evals/task-comments.md) for draft/post authorization, inline workflow comments, proportional evidence, and failure handling without an authoring handoff.
- Habit versus task routing: E10-E12.
- Search/browser/Electron routing: E13-E16.
- Project setup routing: E17-E21.
- tmux/sub-agent boundary: E22-E23.
- Next-action versus task search routing: E24-E25; use [Next Actions Evaluation](evals/nextactions.md) for priority fallback, ready prerequisite chains, cross-project dependencies, concrete blockers, incomplete evidence, scope, and read-only recommendations.
- PR review gate: E26; use [PR Review Evaluation](evals/pr-review.md) for plain outcomes, targeted evidence, finding severity, host routing, independence, posting failures, and stale-revision cases.
- Ordinary project requests versus task listing and PR review: E27-E29, E26.
