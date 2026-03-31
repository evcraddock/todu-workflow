---
name: habit-perform
description: Perform a habit by reading its details and optionally checking in for today. Use when user says "do habit #*", "perform habit #*", "handle habit #*", "work on habit #*", or similar. Do not use for task requests. (plugin:todu)
allowed-tools: todu, Bash, Read, Write, Edit, AskUserQuestion
---

# Perform Habit

Views a habit, follows the instructions in its description, and asks before checking it in for today.

## Process

1. View the habit: `todu habit show <id>`
2. Read and understand the habit description
3. Perform the habit
4. Ask the user if they want to record a note about the session
5. If yes, run `todu note add --habit <id> "<content>"`
6. Ask the user if they want to check in for today
7. If yes, run `todu habit check <id>`

## CLI Commands

```bash
# Habit flow

todu habit show <id>
todu note add --habit <id> "<content>"
todu habit check <id>
```

## Example

### Perform a habit

**User**: "Do habit 15"

1. Runs `todu habit show 15` to view details
2. Follows instructions in the habit description
3. Asks: "Record a note about this session?" (Yes / No)
4. If yes, runs `todu note add --habit 15 "Completed 10 min session"`
5. Asks: "Check in habit #15 for today?" (Yes / No)
6. If yes, runs `todu habit check 15`

## Notes

- Ask the user before recording a note or checking in a habit
- Use `todu note add --habit <id> "<content>"` to record notes (not `todu habit comment`)
- Use `task-perform` or `task-pipeline` for task requests
- Use `habit-check` when the user only wants to check in or undo a check-in
