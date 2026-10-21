#!/usr/bin/env bash
set -euo pipefail

uv run ruff format --check src
uv run ruff check src
