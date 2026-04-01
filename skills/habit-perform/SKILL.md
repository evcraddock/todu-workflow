---
name: habit-perform
description: Perform a habit by reading its details and optionally checking in for today. Use when user says "do habit #*", "perform habit #*", "handle habit #*", "work on habit #*", or similar. Do not use for task requests. (plugin:todu)
allowed-tools: habit_show, habit_note_add, habit_check, Read, Write, Edit, AskUserQuestion
---

# Perform Habit

Views a habit, follows the instructions in its description, and asks before checking it in for today.

## Process

1. View the habit with `habit_show` using the habit ID
2. Read and understand the habit description
3. Perform the habit
4. Ask the user if they want to record a note about the session
5. If yes, run `habit_note_add` with the habit ID and note content
6. Ask the user if they want to check in for today
7. If yes, run `habit_check` with the habit ID

## Native Tools

- `habit_show` to view habit details
- `habit_note_add` to record a note about the session
- `habit_check` to check in or toggle today's check-in

## Example

### Perform a habit

**User**: "Do habit 15"

1. Runs `habit_show` with `habitId: "15"` to view details
2. Follows instructions in the habit description
3. Asks: "Record a note about this session?" (Yes / No)
4. If yes, runs `habit_note_add` with `habitId: "15"` and `content: "Completed 10 min session"`
5. Asks: "Check in habit #15 for today?" (Yes / No)
6. If yes, runs `habit_check` with `habitId: "15"`

## Notes

- Ask the user before recording a note or checking in a habit
- Use `habit_note_add` to record notes on habits
- Use `task-perform` or `task-pipeline` for task requests
- Use `habit-check` when the user only wants to check in or undo a check-in
