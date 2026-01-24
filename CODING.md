# Coding Guidelines

## Philosophy

- **Incremental progress** - Small changes that compile and pass tests
- **Learn first** - Study existing patterns before implementing
- **Pragmatic over dogmatic** - Adapt to project reality
- **Boring is good** - Clear intent over clever code

## Process

### Before Writing Code

1. Study existing patterns in the codebase
2. Find 2-3 similar implementations
3. Identify conventions and utilities already in use

### Implementation Flow

1. **Understand** - Study existing patterns
2. **Test** - Write test first (red)
3. **Implement** - Minimal code to pass (green)
4. **Refactor** - Clean up with tests passing
5. **Commit** - Clear message explaining "why"

### Complex Work

Break into 3-5 stages. For each stage:

- Define specific deliverable
- List testable success criteria
- Track status as you progress

## When Stuck (3 Attempts Max)

After 3 failed attempts, STOP and:

1. Document what was tried and why it failed
2. Research 2-3 alternative approaches
3. Question fundamentals:
   - Right abstraction level?
   - Can this be split smaller?
   - Simpler approach entirely?
4. Ask for guidance before continuing

## Technical Standards

### Architecture

- Composition over inheritance
- Interfaces over singletons
- Explicit over implicit
- Test-driven when possible

### Code Quality

Every commit must:

- Compile successfully
- Pass all existing tests
- Include tests for new functionality
- Follow project formatting/linting

Before committing:

- Run formatters/linters
- Self-review changes
- Ensure message explains "why"

### Error Handling

- Fail fast with descriptive messages
- Include context for debugging
- Handle errors at appropriate level
- Never silently swallow exceptions

## Decision Framework

When multiple approaches exist, prioritize:

1. **Testability** - Can I easily test this?
2. **Readability** - Understandable in 6 months?
3. **Consistency** - Matches project patterns?
4. **Simplicity** - Simplest solution that works?
5. **Reversibility** - How hard to change later?

## Project Integration

- Use project's existing build system
- Use project's test framework
- Use project's formatter/linter
- Follow existing test patterns
- Don't introduce new tools without justification

## Boundaries

### Never

- Use `--no-verify` to bypass hooks
- Disable tests instead of fixing them
- Commit code that doesn't compile
- Make assumptions - verify with existing code
- Silently swallow exceptions

### Always

- Commit working code incrementally
- Learn from existing implementations
- Stop after 3 failed attempts and reassess
- Run tests before committing
- Match project conventions
