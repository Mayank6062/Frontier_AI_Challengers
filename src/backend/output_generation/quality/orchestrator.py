from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any, Awaitable, Optional
from uuid import uuid4

from .architecture_scorer import ArchitectureScorer
from .accessibility_validator import AccessibilityValidator
from .citation_validator import CitationValidator
from .completeness_validator import CompletenessValidator
from .contracts import (
    QualityContext,
    QualityGenerationRequest,
    QualityGenerationResponse,
)
from .determinism_validator import DeterminismValidator
from .enums import ValidationSeverity, ValidatorName
from .models import QualityIssue, QualityReport, QualityResult
from .performance_validator import PerformanceValidator
from .quality_report_generator import QualityReportGenerator
from .security_validator import SecurityValidator
from .semantic_validator import SemanticValidator


class QualityGateOrchestrator:
    """Coordinates quality validation and produces a deterministic report."""

    def __init__(
        self,
        completeness_validator: Optional[CompletenessValidator] = None,
        semantic_validator: Optional[SemanticValidator] = None,
        citation_validator: Optional[CitationValidator] = None,
        determinism_validator: Optional[DeterminismValidator] = None,
        accessibility_validator: Optional[AccessibilityValidator] = None,
        security_validator: Optional[SecurityValidator] = None,
        performance_validator: Optional[PerformanceValidator] = None,
        architecture_scorer: Optional[ArchitectureScorer] = None,
        logger: Optional[logging.Logger] = None,
        report_generator: Optional[QualityReportGenerator] = None,
    ) -> None:
        self.completeness = completeness_validator or CompletenessValidator()
        self.semantic = semantic_validator or SemanticValidator()
        self.citation = citation_validator or CitationValidator()
        self.determinism = determinism_validator or DeterminismValidator()
        self.accessibility = accessibility_validator or AccessibilityValidator()
        self.security = security_validator or SecurityValidator()
        self.performance = performance_validator or PerformanceValidator()
        self.scoring = architecture_scorer or ArchitectureScorer()
        self.logger = logger or logging.getLogger(__name__)
        self.report_generator = report_generator or QualityReportGenerator()

    async def validate_bundle(
        self,
        bundle_content: object,
        approved_snapshot: Optional[object] = None,
        engagement_id: str = "default",
        bundle_version: int = 1,
        trace_id: Optional[str] = None,
    ) -> tuple[QualityReport, ValidationSeverity]:
        """Run quality validators in parallel and aggregate the results."""
        started_at = datetime.now(UTC)
        trace_id = trace_id or str(uuid4())
        self.logger.info(
            "Quality gate validation starting",
            extra={"engagement_id": engagement_id, "trace_id": trace_id},
        )

        try:
            tasks: list[Awaitable[object]] = [
                asyncio.to_thread(self.completeness.validate, bundle_content, approved_snapshot),
                asyncio.to_thread(self.semantic.validate, bundle_content, approved_snapshot),
                asyncio.to_thread(self.citation.validate, bundle_content, approved_snapshot),
                asyncio.to_thread(self.determinism.validate, bundle_content, approved_snapshot, bundle_version),
                asyncio.to_thread(self.accessibility.validate, bundle_content),
                asyncio.to_thread(self.security.validate, bundle_content),
                asyncio.to_thread(self.performance.validate, bundle_content, started_at),
                asyncio.to_thread(self.scoring.score, bundle_content, approved_snapshot),
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            completeness_r, semantic_r, citation_r, determinism_r, accessibility_r, security_r, performance_r, scoring_r = results

            if isinstance(completeness_r, Exception):
                completeness_r = self._build_fallback_report("completeness", completeness_r)
            if isinstance(semantic_r, Exception):
                semantic_r = self._build_fallback_report("semantic", semantic_r)
            if isinstance(citation_r, Exception):
                citation_r = self._build_fallback_report("citation", citation_r)
            if isinstance(determinism_r, Exception):
                determinism_r = self._build_fallback_report("determinism", determinism_r)
            if isinstance(accessibility_r, Exception):
                accessibility_r = self._build_fallback_report("accessibility", accessibility_r)
            if isinstance(security_r, Exception):
                security_r = self._build_fallback_report("security", security_r)
            if isinstance(performance_r, Exception):
                performance_r = self._build_fallback_report("performance", performance_r)
            if isinstance(scoring_r, Exception):
                scoring_r = self._build_fallback_report("scoring", scoring_r)

            all_issues = []
            for report in (
                completeness_r,
                semantic_r,
                citation_r,
                determinism_r,
                accessibility_r,
                security_r,
                performance_r,
                scoring_r,
            ):
                all_issues.extend(list(getattr(report, "issues", [])))

            blockers = [issue for issue in all_issues if getattr(issue, "severity", None) == ValidationSeverity.BLOCKER]
            errors = [issue for issue in all_issues if getattr(issue, "severity", None) == ValidationSeverity.ERROR]
            warnings = [issue for issue in all_issues if getattr(issue, "severity", None) == ValidationSeverity.WARN]

            if blockers:
                overall_verdict = ValidationSeverity.BLOCKER
            elif errors:
                overall_verdict = ValidationSeverity.ERROR
            elif warnings:
                overall_verdict = ValidationSeverity.WARN
            else:
                overall_verdict = ValidationSeverity.INFO

            report = QualityReport(
                report_id=str(uuid4()),
                engagement_id=engagement_id,
                bundle_version=bundle_version,
                generated_at=datetime.now(UTC),
                overall_verdict=overall_verdict,
                completeness=completeness_r if isinstance(completeness_r, type(self.completeness.validate(bundle_content, approved_snapshot))) else self._build_fallback_report("completeness", ValueError("invalid report")),
                semantic=semantic_r if isinstance(semantic_r, type(self.semantic.validate(bundle_content, approved_snapshot))) else self._build_fallback_report("semantic", ValueError("invalid report")),
                citation=citation_r if isinstance(citation_r, type(self.citation.validate(bundle_content, approved_snapshot))) else self._build_fallback_report("citation", ValueError("invalid report")),
                determinism=determinism_r if isinstance(determinism_r, type(self.determinism.validate(bundle_content, approved_snapshot, bundle_version))) else self._build_fallback_report("determinism", ValueError("invalid report")),
                accessibility=accessibility_r if isinstance(accessibility_r, type(self.accessibility.validate(bundle_content))) else self._build_fallback_report("accessibility", ValueError("invalid report")),
                security=security_r if isinstance(security_r, type(self.security.validate(bundle_content))) else self._build_fallback_report("security", ValueError("invalid report")),
                performance=performance_r if isinstance(performance_r, type(self.performance.validate(bundle_content, started_at))) else self._build_fallback_report("performance", ValueError("invalid report")),
                scoring=scoring_r if isinstance(scoring_r, type(self.scoring.score(bundle_content, approved_snapshot))) else self._build_fallback_report("scoring", ValueError("invalid report")),
                all_issues=all_issues,
                blockers=blockers,
                errors=errors,
                warnings=warnings,
                validators_run={
                    "completeness": datetime.now(UTC),
                    "semantic": datetime.now(UTC),
                    "citation": datetime.now(UTC),
                    "determinism": datetime.now(UTC),
                    "accessibility": datetime.now(UTC),
                    "security": datetime.now(UTC),
                    "performance": datetime.now(UTC),
                    "scoring": datetime.now(UTC),
                },
                total_duration_seconds=(datetime.now(UTC) - started_at).total_seconds(),
            )

            self.report_generator.generate(report)
            self.logger.info(
                "Quality gate validation complete",
                extra={"engagement_id": engagement_id, "trace_id": trace_id, "verdict": overall_verdict.value},
            )
            return report, overall_verdict
        except Exception as exc:  # pragma: no cover - defensive guard
            self.logger.exception("Quality gate orchestration failed", extra={"engagement_id": engagement_id, "trace_id": trace_id})
            completeness_r = self._build_fallback_report("completeness", exc)
            semantic_r = self._build_fallback_report("semantic", exc)
            citation_r = self._build_fallback_report("citation", exc)
            determinism_r = self._build_fallback_report("determinism", exc)
            accessibility_r = self._build_fallback_report("accessibility", exc)
            security_r = self._build_fallback_report("security", exc)
            performance_r = self._build_fallback_report("performance", exc)
            scoring_r = self._build_fallback_report("scoring", exc)
            all_issues = [
                *list(getattr(completeness_r, "issues", [])),
                *list(getattr(semantic_r, "issues", [])),
                *list(getattr(citation_r, "issues", [])),
                *list(getattr(determinism_r, "issues", [])),
                *list(getattr(accessibility_r, "issues", [])),
                *list(getattr(security_r, "issues", [])),
                *list(getattr(performance_r, "issues", [])),
                *list(getattr(scoring_r, "issues", [])),
            ]
            report = QualityReport(
                report_id=str(uuid4()),
                engagement_id=engagement_id,
                bundle_version=bundle_version,
                generated_at=datetime.now(UTC),
                overall_verdict=ValidationSeverity.BLOCKER,
                completeness=completeness_r,
                semantic=semantic_r,
                citation=citation_r,
                determinism=determinism_r,
                accessibility=accessibility_r,
                security=security_r,
                performance=performance_r,
                scoring=scoring_r,
                all_issues=all_issues,
                blockers=all_issues,
                errors=[],
                warnings=[],
                validators_run={},
                total_duration_seconds=(datetime.now(UTC) - started_at).total_seconds(),
            )
            return report, ValidationSeverity.BLOCKER

    def run(self, request: QualityGenerationRequest, context: Optional[QualityContext] = None) -> QualityGenerationResponse:
        """Synchronous convenience wrapper for dependency injection and callers."""
        report, _ = asyncio.run(
            self.validate_bundle(
                request.bundle,
                None,
                request.engagement_id,
                1,
                context.trace_id if context else request.trace_id,
            )
        )
        request_id = (context.trace_id if context else request.trace_id) or str(uuid4())
        return QualityGenerationResponse(
            request_id=request_id,
            result=QualityResult(report=report, bundle=request.bundle),
        )

    def _build_fallback_report(self, validator_name: str, exc: Exception) -> Any:
        from .models import (
            AccessibilityReport,
            ArchitectureScoreReport,
            CitationReport,
            CompletenessReport,
            DeterminismReport,
            PerformanceReport,
            SecurityReport,
            SemanticReport,
        )

        if validator_name == "completeness":
            return CompletenessReport(
                required_files_present={},
                required_sections_present={},
                expected_diagram_count=0,
                actual_diagram_count=0,
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.COMPLETENESS,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "semantic":
            return SemanticReport(
                total_claims=0,
                claims_with_justification=0,
                claims_without_justification=0,
                circular_dependencies_detected=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.SEMANTIC,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "citation":
            return CitationReport(
                total_citations_in_output=0,
                total_citations_in_snapshot=0,
                citations_resolved=0,
                citations_unresolved=0,
                coverage_percent=0.0,
                unresolved_citations=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.CITATION,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "determinism":
            return DeterminismReport(
                determinism_baseline_version="0",
                current_build_hash=None,
                files_matching_baseline={},
                non_deterministic_files=[],
                root_causes=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.DETERMINISM,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "accessibility":
            return AccessibilityReport(
                wcag_level="AA",
                contrast_pass_count=0,
                contrast_fail_count=0,
                keyboard_nav_pass=False,
                screen_reader_compatible=False,
                axe_violations_count=0,
                axe_violations=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.ACCESSIBILITY,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "security":
            return SecurityReport(
                secrets_detected=[],
                external_urls_in_offline_bundle=[],
                csp_headers_correct=True,
                sanitization_applied=True,
                xss_vectors_detected=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.SECURITY,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        if validator_name == "performance":
            return PerformanceReport(
                bundle_size_bytes=0,
                bundle_size_mb=0.0,
                generation_time_seconds=0.0,
                portal_tti_seconds=0.0,
                diagram_render_times={},
                budget_violations=[],
                issues=[
                    QualityIssue(
                        id=f"{validator_name}-error",
                        validator=ValidatorName.PERFORMANCE,
                        severity=ValidationSeverity.BLOCKER,
                        title=f"{validator_name.title()} validator failed",
                        description=str(exc),
                        remediation="Inspect the validator implementation and bundle payload.",
                        is_actionable=True,
                    )
                ],
                verdict=ValidationSeverity.BLOCKER,
            )
        return ArchitectureScoreReport(
            total_dimensions=0,
            dimensions=[],
            composite_score=0.0,
            health_status="failed",
            score_trend="stable",
            low_scoring_dimensions=[],
            high_priority_improvements=[],
            issues=[
                QualityIssue(
                    id=f"{validator_name}-error",
                    validator=ValidatorName.SCORING,
                    severity=ValidationSeverity.BLOCKER,
                    title=f"{validator_name.title()} validator failed",
                    description=str(exc),
                    remediation="Inspect the validator implementation and bundle payload.",
                    is_actionable=True,
                )
            ],
            verdict=ValidationSeverity.BLOCKER,
        )
