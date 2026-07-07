from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Optional

from .enums import ValidationSeverity, ValidatorName
from .models import PerformanceReport, QualityIssue


class PerformanceValidator:
    """Validate bundle size and generation time against simple performance thresholds."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, bundle: object, started_at: Optional[datetime] = None) -> PerformanceReport:
        contents = self._extract_texts(bundle)
        data_size = sum(len(content.encode("utf-8")) for content in contents)
        generation_time_seconds = 0.0
        if started_at is not None:
            generation_time_seconds = max((datetime.now(UTC) - started_at).total_seconds(), 0.0)

        issues: list[QualityIssue] = []
        if data_size > 5_000_000:
            issues.append(
                QualityIssue(
                    id="QUAL-PERF-001",
                    validator=ValidatorName.PERFORMANCE,
                    severity=ValidationSeverity.WARN,
                    title="Bundle size exceeds target",
                    description="The generated bundle is larger than the target threshold.",
                    remediation="Reduce bundle size by compressing assets or trimming redundant content.",
                    is_actionable=True,
                )
            )
        if generation_time_seconds > 10.0:
            issues.append(
                QualityIssue(
                    id="QUAL-PERF-002",
                    validator=ValidatorName.PERFORMANCE,
                    severity=ValidationSeverity.WARN,
                    title="Generation time exceeds target",
                    description="The quality gate took longer than the expected runtime budget.",
                    remediation="Reduce validator overhead or defer expensive checks to asynchronous background processing.",
                    is_actionable=True,
                )
            )

        return PerformanceReport(
            bundle_size_bytes=data_size,
            bundle_size_mb=data_size / (1024 * 1024),
            generation_time_seconds=generation_time_seconds,
            portal_tti_seconds=0.0,
            diagram_render_times={},
            budget_violations=[issue.title for issue in issues],
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
