---
name: quality-tooling
description: Set up linting, formatting, testing, and pre-commit hooks for a project. Use when asked to "add linting", "set up quality tools", "configure eslint", "add pre-commit hooks", or similar.
---

# Quality Tooling

Set up code quality tools (linting, formatting, testing, pre-commit hooks) for a project.

## When to Use

- After project scaffolding to add quality tools
- On existing projects to add/update quality configuration
- When asked to set up linting, formatting, or testing

## Required Inputs

- `stack` - typescript, go, python, or rust
- `name` - Project name (for config placeholders)
- `localPath` - Where to write files

## Files to Generate

### TypeScript

| File | Template | Notes |
|------|----------|-------|
| eslint.config.js | `templates/typescript/eslint.config.js` | Modern flat config |
| .prettierrc | `templates/typescript/prettierrc.json` | Rename to .prettierrc |
| tsconfig.json | `templates/typescript/tsconfig.json` | |
| vitest.config.ts | `templates/typescript/vitest.config.ts` | |
| src/__tests__/example.test.ts | `templates/typescript/example.test.ts` | |
| scripts/pre-pr.sh | `templates/typescript/pre-pr.sh` | Make executable |

Also add to package.json scripts:
```json
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

And devDependencies:
```json
{
  "devDependencies": {
    "eslint": "^9.0.0",
    "typescript-eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0",
    "@vitest/coverage-v8": "^1.0.0"
  }
}
```

### Go

| File | Template | Notes |
|------|----------|-------|
| .golangci.yml | `templates/go/golangci.yml` | Replace {owner}/{name} |
| *_test.go | `templates/go/example_test.go` | Example test |
| scripts/pre-pr.sh | `templates/go/pre-pr.sh` | Make executable |

### Python

| File | Template | Notes |
|------|----------|-------|
| ruff.toml | `templates/python/ruff.toml` | Replace {name} |
| pyproject.toml | `templates/python/pyproject.toml` | Replace {name}, {description} |
| tests/test_example.py | `templates/python/test_example.py` | |
| scripts/pre-pr.sh | `templates/python/pre-pr.sh` | Make executable |

### Rust

| File | Template | Notes |
|------|----------|-------|
| rustfmt.toml | `templates/rust/rustfmt.toml` | |
| clippy.toml | `templates/rust/clippy.toml` | |
| scripts/pre-pr.sh | `templates/rust/pre-pr.sh` | Make executable |

Rust tests go in src/ with `#[cfg(test)]` - no separate file needed.

### All Stacks (Optional)

| File | Template | Notes |
|------|----------|-------|
| .pre-commit-config.yaml | `templates/pre-commit-config.yaml` | Add stack-specific hooks |

## Process

1. Change to project directory: `cd {localPath}`
2. **Check for existing configs** (see below)
3. Read and write config files from templates
4. Replace placeholders: `{name}`, `{owner}`, `{description}`
5. Create scripts directory if needed: `mkdir -p scripts`
6. Make pre-pr.sh executable: `chmod +x scripts/pre-pr.sh`
7. For TypeScript: update package.json with scripts and devDependencies

## Existing Config Detection

Before writing any file, check if it already exists:

```bash
ls -la {localPath}/{config_file} 2>/dev/null
```

**If config exists, ask the user:**
- "Found existing {file}. Should I: (1) Overwrite, (2) Skip, (3) Show diff?"

**Common existing configs to check:**

| Stack | Check For |
|-------|-----------|
| TypeScript | `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `prettier.config.*`, `tsconfig.json`, `jest.config.*`, `vitest.config.*` |
| Go | `.golangci.yml`, `.golangci.yaml` |
| Python | `pyproject.toml`, `setup.py`, `setup.cfg`, `.flake8`, `ruff.toml`, `mypy.ini`, `pytest.ini` |
| Rust | `rustfmt.toml`, `.rustfmt.toml`, `clippy.toml` |

**Special case - pyproject.toml:**
- Often contains project metadata, not just tool config
- If exists, offer to merge tool sections rather than overwrite
- Read existing file, add/update `[tool.pytest]`, `[tool.mypy]`, `[tool.ruff]` sections

## Placeholders

| Placeholder | Value |
|-------------|-------|
| `{name}` | Project name |
| `{owner}` | Repository owner (from git remote or ask) |
| `{description}` | Project description |

## Verification

After generating files:

```bash
ls -la {localPath}
cat {localPath}/scripts/pre-pr.sh
```

For TypeScript, also verify package.json was updated.

## Notes

- TypeScript uses modern ESLint flat config (not legacy .eslintrc)
- Python uses Ruff for both linting and formatting (faster than Black + isort)
- Go and Rust have built-in formatters, just need linter config
- pre-commit hooks are optional but recommended
- All pre-pr.sh scripts follow the same pattern: format, lint, typecheck, test
