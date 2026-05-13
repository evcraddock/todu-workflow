---
name: task-perform
description: Start and perform a Todu task. Use for "do/perform/execute/handle task". Do not use for habits or the full pickup-task pipeline. (plugin:todu)
allowed-tools: todu, Bash, Read, Write, Edit, AskUserQuestion
---

# Perform Task

Views a task, follows the instructions in its description, and asks before marking it done.

## Process

1. View the task: `todu task show <id>`
2. Start the task: `todu task start <id>`
3. Read and understand the task description
4. Follow the instructions in the description
5. When work is complete, add a note using the `task-comment-create` skill
6. Ask the user if they want to mark the task done
7. If yes, run `todu task done <id>`

## CLI Commands

```bash
# Task flow

todu task show <id>
todu task start <id>
todu task done <id>
```

## Example

### Work on a task

**User**: "Do task 42"

1. Runs `todu task show 42` to view details
2. Runs `todu task start 42`
3. Follows instructions in the task description
4. When complete, uses `task-comment-create` to add a summary note
5. Asks: "Mark task #42 done?" (Yes / No)
6. If yes, runs `todu task done 42`

## Notes

- Always start a task before working on it unless it is already in progress
- Use `task-comment-create` when work on a task is complete
- Ask the user before marking a task done
- Use `habit-perform` or `habit-check` for habit requests
- Use `task-pipeline` for the full gated implementation flow
