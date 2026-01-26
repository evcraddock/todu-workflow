#!/bin/bash
set -e

echo "Running pre-PR checks..."

echo "→ Formatting..."
cargo fmt --check

echo "→ Linting..."
cargo clippy -- -D warnings

echo "→ Running tests..."
cargo test

echo "✓ All checks passed!"
