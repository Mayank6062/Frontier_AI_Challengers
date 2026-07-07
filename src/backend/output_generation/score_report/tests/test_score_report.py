import asyncio
from datetime import datetime, UTC

from src.backend.output_generation.architecture_score.models import (
    ArchitectureScore,
    ArchitectureScoreMetadata,
    ScoreCategory,
    ScoreDimension,
)
from src.backend.output_generation.architecture_score.enums import (
    ScoreGrade,
    ScoreHealthStatus,
    ScoreSchemaVersion,
)
from src.backend.output_generation.score_report.score_report_generator import ScoreReportGenerator


def test_score_report_generator_renders_all_outputs() -> None:
    score = ArchitectureScore(
        metadata=ArchitectureScoreMetadata(
            engagement_id="eng-1",
            engagement_version=1,
            produced_by="tests",
            produced_at=datetime.now(UTC),
            model_version="test",
            score_schema_version=ScoreSchemaVersion.V2,
        ),
        composite_score=83.5,
        composite_grade=ScoreGrade.B,
        health_status=ScoreHealthStatus.GOOD,
        confidence=0.9,
        categories=[
            ScoreCategory(category_id="c1", category_name="Architecture", dimensions=[ScoreDimension(dimension_id="d1", dimension_name="Clarity", category="Architecture", weight=1.0)], category_score=83.5, category_weight=1.0)
        ],
        all_dimensions=[ScoreDimension(dimension_id="d1", dimension_name="Clarity", category="Architecture", weight=1.0)],
        top_strengths=["Clear structure"],
        critical_improvements=["Improve evidence"],
    )

    generator = ScoreReportGenerator()
    report = asyncio.run(generator.generate(score, "v1", "trace-1"))

    assert report.status == "SUCCESS"
    assert report.html_score_view.startswith("<")
    assert "Architecture Score Summary" in report.score_markdown
    assert report.score_json.startswith("{")
