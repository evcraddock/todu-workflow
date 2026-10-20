"""Static routing guardrails, not evidence of model instruction-following."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_task_perform_has_no_automatic_workflow_dependencies():
    skill = (ROOT / "skills/task-perform/SKILL.md").read_text()
    # A plain execution request must not import another workflow or its fallback.
    for dependency in (
        "../task-start-preflight/",
        "../task-close-gate/",
        "../task-pipeline/DEFAULT_CONTRIBUTING.md",
    ):
        assert dependency not in skill
    assert "only when" in skill.split("task-pipeline", 1)[1]
    assert len(skill.splitlines()) <= 40


def test_pipeline_does_not_delegate_its_own_planning_or_completion():
    skill = (ROOT / "skills/task-pipeline/SKILL.md").read_text()
    assert "DEFAULT_CONTRIBUTING.md" in skill
    assert "../task-start-preflight/" not in skill
    assert "../task-close-gate/" not in skill
    assert "explicitly requested" in skill


@pytest.mark.parametrize("language", ["go", "python", "rust", "typescript"])
def test_scaffold_does_not_reintroduce_automatic_task_gates(language):
    template = (ROOT / f"skills/project-scaffold/templates/agents/{language}.md").read_text()
    assert "task-perform" in template
    assert "ALWAYS use the `task-start-preflight`" not in template
    assert "ALWAYS run `task-start-preflight`" not in template
    assert "**Closing**: Run `task-close-gate`" not in template
    # Removing task-level ceremony must not erase explicit project PR policy.
    assert "## PR Workflow (Mandatory Sequence)" in template
    assert "explicit human merge approval" in template
