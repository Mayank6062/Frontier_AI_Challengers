from __future__ import annotations

import html

from ..architecture_score.models import ArchitectureScore


class ScoreHtmlRenderer:
    """Render the score portal view as a deterministic HTML fragment."""

    def render(self, score: ArchitectureScore, template_version: str = "v1") -> str:
        hero = (
            f"<section class='score-hero'>"
            f"<h1>Architecture Score</h1>"
            f"<div class='composite'>{score.composite_score:.1f}</div>"
            f"<div class='grade'>{score.composite_grade.value}</div>"
            f"<div class='health'>{html.escape(score.health_status.value)}</div>"
            f"</section>"
        )
        details = "".join(
            f"<li>{html.escape(dim.dimension_name)}: {dim.raw_score or 0:.1f}</li>"
            for dim in score.all_dimensions
        )
        return f"<article class='score-report'>{hero}<ul>{details}</ul></article>"
