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
| E01 | Create a task for adding retry logic to webhook delivery. | `task-authoring`, then task creation path if requested | Drafts a structured task title and markdown with goal, requirements, acceptance criteria, and dependencies before any backend write. | Creates a backend record without authoring, omits required sections, or invents dependency IDs. |
| E02 | Draft a task for fixing mobile login but do not create it yet. | `task-authoring` | Returns task content only. | Calls `todu task create` or treats the request as implementation work. |
| E03 | Add a task to todu-workflow: Document skill evals. | task creation path, with `task-authoring` if content needs shaping | Creates or prepares a well-structured task in the requested project. | Uses `task-authoring` but never writes when creation is explicitly requested, or writes vague content. |
| E04 | Write a progress update for task #123 saying the PR is open and checks are passing. | `task-comment-authoring` | Drafts a concise markdown comment; does not post unless separately asked. | Posts a note directly or creates/updates a task record. |
| E05 | Comment on task #123: PR is open and checks are passing. | task comment creation path, optionally with `task-comment-authoring` | Posts the requested comment to the task. | Only drafts content when the user explicitly asked to comment, or posts unstructured content. |
| E06 | Do task #123. | `task-perform` | Shows and starts the task, follows its description, and asks before marking done. | Runs the full `task-pipeline`, treats it as a habit, or closes without approval. |
| E07 | Pickup task #123. | `task-pipeline` | Runs preflight, loads contributing instructions, asks for plan approval, and follows the gated coding flow. | Uses simple `task-perform`, skips preflight, or starts coding before the required preview. |
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

## Coverage Checklist

- Task execution boundary: E06-E09.
- Task authoring/comment authoring boundary: E01-E05.
- Habit versus task routing: E10-E12.
- Search/browser/Electron routing: E13-E16.
- Project setup routing: E17-E21.
- tmux/sub-agent boundary: E22-E23.
- Next-action versus task search routing: E24-E25.
- PR review gate: E26.
