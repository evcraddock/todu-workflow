#!/bin/bash
set -e

echo "Running pre-PR checks..."

echo "→ Formatting..."
ruff format .

echo "→ Linting..."
ruff check .

echo "→ Type checking..."
mypy .

echo "→ Running tests..."
pytest

echo "✓ All checks passed!"
