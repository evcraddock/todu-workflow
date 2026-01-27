---
name: pr-review
description: Review a pull request from another agent. Use when asked to "review PR", "review pull request", "check PR #X", or similar.
---

# PR Review

Guide for reviewing another agent's pull request before human approval.

## When to Use

When a human asks you to review a PR that was created by a different agent. You should NOT review PRs you created yourself.

## Host Detection

Detect the git host from the remote URL:

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if echo "$REMOTE_URL" | grep -q "github.com"; then
  HOST="github"
else
  HOST="forgejo"
fi
```

## CLI Commands by Host

| Operation | GitHub | Forgejo |
|-----------|--------|---------|
| View PR | `gh pr view <num>` | `zsh -ic "fj pr view <num>"` |
| View diff | `gh pr diff <num>` | `zsh -ic "fj pr view <num> diff"` |
| Comment on PR | `gh pr comment <num> --body-file <file>` | `zsh -ic "fj pr comment <num> --body-file <file>"` |

**Note:** Forgejo CLI (`fj`) requires `zsh -ic` wrapper for keyring access.

## Review Process

### 1. Fetch PR Details

**GitHub:**
```bash
gh pr view <number>
gh pr diff <number>
```

**Forgejo:**
```bash
zsh -ic "fj pr view <number>"
zsh -ic "fj pr view <number> diff"
```

### 2. Understand the Change

Before reviewing code, understand context:

- **Read the PR description** - What does it claim to do?
- **Identify the task** - What task/issue does it address?
- **Scope check** - Are changes focused or sprawling?

### 3. Find Project Standards

Look for code standards in the project:

```bash
# Common locations
cat docs/CODE_STANDARDS.md 2>/dev/null || \
cat CODE_STANDARDS.md 2>/dev/null || \
cat CONTRIBUTING.md 2>/dev/null || \
echo "No standards doc found"
```

### 4. Review Checklist

Go through each item:

**PR Quality:**
- [ ] PR description clearly explains the change
- [ ] Changes match the linked task requirements
- [ ] No unrelated changes included
- [ ] Commits are focused and well-messaged

**Code Quality:**
- [ ] Code follows project standards (if doc exists)
- [ ] TypeScript strict mode respected (no `any`, no `@ts-ignore`)
- [ ] Functions are small and focused
- [ ] Names are clear and descriptive
- [ ] No obvious logic errors or potential bugs

**Testing:**
- [ ] Tests added for code with logic (REQUIRED - see Approval Criteria)
- [ ] Edge cases considered
- [ ] Tests actually test the behavior (not just coverage)

**Security:**
- [ ] No secrets or credentials in code
- [ ] User input is validated
- [ ] No obvious injection vulnerabilities

**Documentation:**
- [ ] README updated if needed
- [ ] Comments explain "why" not "what"
- [ ] API changes documented

### 5. Approval Criteria

**CRITICAL: Do not approve unless you are CERTAIN all requirements are met.**

Identifying a problem and approving anyway is contradictory. When in doubt, request changes.

**Approve ONLY when:**
- All acceptance criteria from the task are verified complete
- All checklist items pass
- No potential bugs identified
- No policy violations
- Tests exist for any code with logic

**Request changes when ANY of these apply:**
- Missing tests for code with logic (functions, conditionals, loops)
- Potential bugs identified, even if "minor"
- Acceptance criteria unclear or unverified
- Policy violations (even if "could be fixed later")
- Any correctness concerns

**"Non-blocking" is ONLY for:**
- Style preferences (naming, formatting beyond linter)
- Optional refactoring suggestions
- "Nice to have" improvements

**"Non-blocking" is NEVER for:**
- Missing tests
- Potential bugs
- Logic errors
- Policy violations
- Correctness issues

### 6. Post Review

**IMPORTANT: Use `gh pr comment`, NOT `gh pr review`.**

Write your review to a temp file for proper markdown formatting:

```bash
cat > /tmp/review-<number>.md << 'EOF'
## Code Review: [Approved ✅ | Changes Requested ❌]

### Summary
Brief summary of what you reviewed.

### Checklist
- [x] Item passed
- [ ] Item failed - reason

### Issues (if any)
1. **file.ts:42** - Description
2. **file.ts:87** - Description

### Suggestions (optional)
- Non-blocking improvement ideas

### Verdict
LGTM / Please address the issues above
EOF
```

Then post to the PR:

**GitHub:**
```bash
gh pr comment <number> --body-file /tmp/review-<number>.md
```

**Forgejo:**
```bash
zsh -ic "fj pr comment <number> --body-file /tmp/review-<number>.md"
```

Do NOT use `gh pr review` - it doesn't work for self-reviews.

### 7. Add Task Comment

**If a task ID was provided in your prompt, you MUST also add the review to the task:**

```bash
todu task comment <task-id> -m "## PR Review for #<pr-number>

<same review content>"
```

This keeps the task history complete with review feedback.

## Review Templates

**If all good:**
```markdown
## Code Review: Approved ✅

### Checklist
- [x] PR description clear
- [x] Code follows standards  
- [x] Tests present for code with logic
- [x] No potential bugs identified
- [x] No security concerns

LGTM 🚀
```

**If issues found (missing tests, bugs, policy violations):**
```markdown
## Code Review: Changes Requested ❌

### Issues Found

1. **[File:Line]** Description of issue
   - Why it's a problem
   - Suggested fix

### Checklist Failures
- [ ] Issue 1
- [ ] Issue 2

Please address these and push updates.
```

**If style suggestions only (NO correctness issues):**
```markdown
## Code Review: Approved ✅

### Style Suggestions (non-blocking)
1. Consider doing X instead of Y (style preference)
2. Could rename Z for clarity (optional)

These are optional style improvements only. No correctness issues found.

LGTM 🚀
```

**WARNING:** Do NOT use "Approved with suggestions" if you identified:
- Missing tests for code with logic
- Potential bugs (even "minor" ones)
- Policy violations
- Any correctness concerns

If you found ANY of the above, use "Changes Requested" instead.

## Things CI Can't Catch

Focus your review on what automation misses:

- **Logic errors** - Code compiles but does the wrong thing
- **Missing edge cases** - Happy path works, edge cases don't
- **Poor abstractions** - Code works but is hard to understand/maintain
- **Security issues** - Injection, auth bypass, data exposure
- **Performance** - O(n²) when O(n) is possible
- **Race conditions** - Async code that might fail intermittently
- **Error handling** - Errors swallowed or poorly messaged

## Notes

- Be constructive, not critical
- Explain why, not just what
- Acknowledge good patterns you see
- If unsure, ask rather than assume
- Remember: a different agent wrote this, not the human
- **Run the signal command when done** - Your prompt will include a `tmux wait-for -S` command to run when the review is complete. Execute it using bash after posting the review. This signals the calling agent that you're finished.
