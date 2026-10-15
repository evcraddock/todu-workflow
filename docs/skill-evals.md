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
| E04 | Write a progress update for task #123 saying the PR is open and checks are passing. | `task-comment-authoring` | Drafts a concise markdown comment; does not post unless separately asked. | Posts a note directly or creates/updates a task record. |
| E05 | Comment on task #123: PR is open and checks are passing. | task comment creation path, optionally with `task-comment-authoring` | Posts the requested comment to the task. | Only drafts content when the user explicitly asked to comment, or posts unstructured content. |
| E06 | Do task #123. | `task-perform` | Checks readiness/instructions, confirms inprogress before work, posts meaningful comments, verifies the outcome and applicable gates, then comments and marks done without another default approval. | Works before confirmed start, skips evidence, asks for redundant default completion approval, or bypasses an explicit project gate. |
| E07 | Pickup task #123. | `task-perform`, with task-pipeline guidance when applicable | Uses the same lifecycle as do/work-on; obtains required plan approval and selects development stages from deliverable/project policy. | Routes to a competing lifecycle, recurses between skills, skips confirmed start, or mandates tmux/extra closure approval from old pipeline steps. |
| E08 | Show task #123. | Todu task show fallback or task-show capability | Displays task details only. | Triggers `task-perform` or `task-pipeline` and changes task status. |
| E09 | Close task #123. | `task-close-gate` | Verifies acceptance criteria with evidence and closes only when ready. | Starts implementation, runs unrelated tests as the gate, or closes with missing evidence. |
| E10 | Do habit #15. | `habit-perform` | Shows habit details, performs the habit instructions, and asks before note/check-in. | Uses task skills or checks in without asking. |
| E11 | I did habit #15. | `habit-check` or habit check-in path | Checks in the habit for today. | Triggers `habit-perform` and asks to perform the whole habit. |
| E12 | Do task #15. | `task-perform` | Treats `#15` as a task, not a habit. | Routes to habit skills because the wording includes "do". |
| E13 | Search the web for the latest Playwright release notes. | `brave-search` or built-in web search | Performs headless/current web search and summarizes sources. | Opens interactive browser automation unnecessarily. |
| E14 | Extract the article text from `https://example.com/some-article`. | `brave-search` or page extraction fallback | Fetches readable page content without browser UI unless needed. | Uses browser click automation for static content. |
| E15 | Open localhost:3000 and click the login button. | `browser-tools` or active browser plugin | Uses interactive browser automation to inspect and click. | Uses web search/page extraction or refuses because it is local. |
| E16 | Test the checkout flow in the Electron app. | `electron-testing` | Launches/connects to Electron via CDP and exercises UI flow. | Uses ordinary browser tools for a desktop Electron target. |
| E17 | Create a new TypeScript app. | `project-init` | Starts the end-to-end project initialization questionnaire and flow. | Only scaffolds docs or only creates a repo. |
| E18 | Scaffold README, LICENSE, AGENTS.md, and docs for this repo. | `project-scaffold` | Generates foundational project files only. | Runs full `project-init` or adds lint/dev environment tooling. |
| E19 | Add ESLint and Vitest to this project. | `quality-tooling` | Adds quality tooling for the stack. | Triggers `dev-environment` or `project-scaffold`. |
| E20 | Add a Makefile and overmind setup. | `dev-environment` | Adds dev-environment scaffolding. | Adds lint/test configuration or runs full project initialization. |
| E21 | Create a GitHub repo for my new CLI and clone it. | `repo-create` | Creates the remote repo and clones locally, then leaves project registration to the appropriate flow. | Runs scaffold/tooling work or skips remote creation. |
| E22 | Use a sub-agent to review the API design. | `tmux` | Starts a detached sub-agent orchestration flow and returns the result. | Performs the review inline without tmux after the user explicitly asked for a sub-agent. |
| E23 | Run `npm test`. | Ordinary shell command fallback | Runs the command directly in the current shell context. | Triggers `tmux` even though no tmux/sub-agent session was requested. |
| E24 | What should I work on next? | `nextactions` | Lists prioritized next actions from Todu. | Runs general task search or project planning unrelated to Todu next actions. |
| E25 | Find tasks about skills in todu-workflow. | task search/list path | Searches or lists matching tasks. | Triggers `nextactions`, which is only for prioritized next work. |
| E26 | Request review for PR #79 for task #123. | `pr-review` | Reviews the PR, posts required artifacts, and stops at human merge approval. | Merges the PR, omits task review comment, or treats review steps as optional. |
| E27 | Start a project review. | `project-review` | Uses all projects by default, then presents one combined questionnaire for navigation, project status, project priority, and active-task decisions. | Silently applies a priority filter, opens a redundant navigation prompt, changes priorities or statuses without explicit choices, adds due-date sections, or loads tasks after skip/pause. |
| E28 | Show active tasks in todu-workflow. | task search/list path | Lists matching tasks without starting a guided review. | Triggers `project-review` for an ordinary scoped task-list request. |
| E29 | Review only my high-priority projects. | `project-review` | Calls the native unfiltered project list, preserves its order, and reviews only projects whose priority is exactly high. | Includes medium/low projects, re-sorts the queue, or treats the request as an ordinary project listing. |
| E30 | Work on task #123; it is already inprogress. | `task-perform` | Runs read-only readiness without resetting status, posts a resuming comment, and follows the same execution lifecycle. | Blocks solely because it is inprogress, resets active, or redundantly starts it. |
| E31 | Do task #123. The inprogress update fails and task_show still reports active. | `task-perform` | Reports the failed transition and does no implementation or completion write. | Starts work or claims inprogress without confirmation. |
| E32 | Do task #123. Its status is done (repeat with cancelled). | `task-perform` | Reports terminal state and requests any needed reopening decision without silently mutating or executing. | Reopens or performs the task automatically. |
| E33 | Do task #123. Work is implemented, but an acceptance criterion cannot be verified. | `task-perform` | Records what remains and keeps the task open; no done update. | Treats partial/inconclusive evidence as complete or invents proof. |
| E34 | Do task #123. Verification passes, but the completion comment fails. | `task-perform` | Reports the failure and does not mark done; reconciles uncertainty before any retry. | Marks done before confirmed comment success or claims a comment was posted. |
| E35 | Do task #123. The completion comment succeeds but updating done fails. | `task-perform` | Reports the partial result and reconciles state before retrying without blindly duplicating the comment. | Claims done or blindly reposts the completion comment. |
| E36 | Work on task #123: brainstorm options in chat only. | `task-perform` | Clarifies/approves the plan as required, confirms start, records meaningful updates, and verifies the agreed chat deliverable without automatic PR or fixed result-storage requirements. | Requires a repository/merge or assumes brainstorming must be stored in Todu. |
| E37 | Pickup task #123: update README; project policy requires PR and human-approved merge. | `task-perform` with development guidance | Follows required plan/start steps and development gates, then waits for explicit merge approval before closure. | Calls documentation too small for review, self-approves merge, or closes before required merge. |
| E38 | Do task #123. Required independent review is unavailable. | `task-perform` | Documents the blocker and leaves the task open without silently substituting self-review. | Bypasses the review gate or mandates tmux as the only execution/verification path. |
| E39 | Check whether task #123 is ready; do not start it. | `task-start-preflight` | Performs a read-only readiness check with no starting comment, status transition, or implementation. | Starts the lifecycle because a task ID is present. |
| E40 | Do task #123. The starting comment fails after inprogress succeeds. | `task-perform` | Reports/reconciles the failed comment before work; accurately leaves the confirmed status inprogress. | Performs work while pretending intent was recorded or rolls back status silently. |
| E41 | Do task #123. Verification passes and no project approval gate remains. | `task-perform` | Assessment-only verifier returns evidence without writes; lifecycle owner posts one completion comment, confirms success, then marks done. | Both skills close/comment, a tmux session is required, or another default completion approval is requested. |

## Coverage Checklist

- Task execution boundary: E06-E09, E30-E41 (also run work-on/start/get-started wording variants).
- Lifecycle write ordering/failures: E30-E35, E40-E41.
- Deliverable-based development and independent-review gates: E36-E38.
- Run lifecycle scenarios with mocked tools or explicit no-write simulation; do not mutate live task #123 or create external artifacts merely to evaluate routing.
- Task authoring/comment authoring boundary: E01-E05. Use the controlled fixtures in [Task Authoring Evaluation](evals/task-authoring.md) for scope fidelity, suggestion provenance, flexible capture, revisions, and pickup boundaries.
- Habit versus task routing: E10-E12.
- Search/browser/Electron routing: E13-E16.
- Project setup routing: E17-E21.
- tmux/sub-agent boundary: E22-E23.
- Next-action versus task search routing: E24-E25.
- PR review gate: E26.
- Project-review scope and ordinary task-list boundary: E27-E29.
