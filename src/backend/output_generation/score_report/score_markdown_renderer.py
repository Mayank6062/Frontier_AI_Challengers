from __future__ import annotations

from ..architecture_score.models import ArchitectureScore


class ScoreMarkdownRenderer:
    """Render a markdown summary for the score report."""

    def render(self, score: ArchitectureScore) -> str:
        lines = [
            "## Architecture Score Summary",
            "",
            f"**Composite Score:** {score.composite_score:.1f}/100",
            f"**Grade:** {score.composite_grade.value}",
            f"**Health:** {score.health_status.value}",
            "",
            "### Top Strengths",
            *[f"- {item}" for item in score.top_strengths],
            "",
            "### Critical Improvements",
            *[f"1. {item}" for item in score.critical_improvements],
        ]
        return "\n".join(lines)
