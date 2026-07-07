from __future__ import annotations

import logging
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import ArchitectureScoreReport, QualityIssue, ScoringDimension


class ArchitectureScorer:
    """Generate a deterministic architecture quality score from bundle heuristics."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def score(self, bundle: object, approved_snapshot: Optional[object] = None) -> ArchitectureScoreReport:
        texts = self._extract_texts(bundle)
        joined = "\n".join(texts).lower()
        completeness_score = 1.0 if "architecture" in joined else 0.5
        evidence_score = 1.0 if "citation" in joined or "evidence" in joined else 0.4
        security_score = 1.0 if "security" in joined or "secrets" not in joined else 0.2
        composite_score = round((completeness_score + evidence_score + security_score) / 3.0 * 100.0, 2)

        dimensions = [
            ScoringDimension(dimension_name="Architecture Completeness", weight=0.4, score=completeness_score * 100.0, explanation="Checks whether the bundle contains architecture-related content.", suggestions=[], weak_spots=[]),
            ScoringDimension(dimension_name="Evidence Coverage", weight=0.3, score=evidence_score * 100.0, explanation="Measures whether the output contains evidence or citation references.", suggestions=[], weak_spots=[]),
            ScoringDimension(dimension_name="Security Readiness", weight=0.3, score=security_score * 100.0, explanation="Measures whether the bundle appears to be free of obvious secret leakage.", suggestions=[], weak_spots=[]),
        ]

        issues: list[QualityIssue] = []
        if composite_score < 70.0:
            issues.append(
                QualityIssue(
                    id="QUAL-SCOR-001",
                    validator=ValidatorName.SCORING,
                    severity=ValidationSeverity.WARN,
                    title="Architecture quality score is below target",
                    description="The generated bundle scored below the expected architecture quality threshold.",
                    remediation="Improve architecture completeness and evidence coverage before approval.",
                    is_actionable=True,
                )
            )

        return ArchitectureScoreReport(
            total_dimensions=len(dimensions),
            dimensions=dimensions,
            composite_score=composite_score,
            health_status="healthy" if composite_score >= 70.0 else "needs_attention",
            score_trend="stable",
            low_scoring_dimensions=[dimension.dimension_name for dimension in dimensions if dimension.score < 70.0],
            high_priority_improvements=[],
            issues=issues,
            verdict=ValidationSeverity.WARN if issues else ValidationSeverity.INFO,
        )

    def _extract_texts(self, bundle: object) -> list[str]:
        if isinstance(bundle, dict):
            payload = bundle.get("content") or bundle.get("text") or []
            if isinstance(payload, list):
                return [str(item) for item in payload]
            if isinstance(payload, str):
                return [payload]

        content = getattr(bundle, "content", None)
        if isinstance(content, str):
            return [content]
        if isinstance(content, list):
            return [str(item) for item in content]
        return []
