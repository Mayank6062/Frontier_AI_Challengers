from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..architecture_score.models import ArchitectureScore
from .score_html_renderer import ScoreHtmlRenderer
from .score_json_serializer import ScoreJsonSerializer
from .score_markdown_renderer import ScoreMarkdownRenderer
from .score_validator import ScoreValidator


@dataclass(slots=True)
class ScoreReportResult:
    status: str
    html_score_view: str = ""
    score_json: str = ""
    score_markdown: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class ScoreReportGenerator:
    """Generate HTML, JSON, and Markdown artifacts for an ArchitectureScore."""

    def __init__(
        self,
        validator: Optional[ScoreValidator] = None,
        html_renderer: Optional[ScoreHtmlRenderer] = None,
        json_serializer: Optional[ScoreJsonSerializer] = None,
        markdown_renderer: Optional[ScoreMarkdownRenderer] = None,
    ) -> None:
        self.validator = validator or ScoreValidator()
        self.html_renderer = html_renderer or ScoreHtmlRenderer()
        self.json_serializer = json_serializer or ScoreJsonSerializer()
        self.markdown_renderer = markdown_renderer or ScoreMarkdownRenderer()

    async def generate(
        self,
        score: ArchitectureScore,
        template_version: str,
        trace_id: str,
    ) -> ScoreReportResult:
        validation_result = self.validator.validate(score)
        if validation_result.severity == "BLOCKER":
            return ScoreReportResult(
                status="FAILED",
                errors=validation_result.errors,
                warnings=validation_result.warnings,
            )

        html_view = self.html_renderer.render(score, template_version)
        json_payload = self.json_serializer.serialize(score)
        markdown_summary = self.markdown_renderer.render(score)
        return ScoreReportResult(
            status="SUCCESS",
            html_score_view=html_view,
            score_json=json_payload,
            score_markdown=markdown_summary,
            warnings=validation_result.warnings,
        )
