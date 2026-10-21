---
name: perform-task
description: Find a todu task and follow its instructions. Use for "handle task", "do task", or "perform task".
---

# Perform Task

Find the requested todu task. Before starting work, set its status to `inprogress` using its explicit task ID and verify the update succeeded. If it is already `inprogress`, leave its status unchanged. Then follow the task's instructions.

Once all task instructions are complete, add a comment to the task summarizing the completed work, then close the task by setting its status to `done`. Use the explicit task ID for both actions and verify they succeeded. If any instructions remain incomplete, do not mark the task `done`; inform the user which instructions remain incomplete and ask for guidance.
