from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Sequence, TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import ValidationSeverity, ValidatorName

if TYPE_CHECKING:
    # Manifest types are owned by manifest.py (canonical). Use TYPE_CHECKING
    # imports to avoid runtime circular imports while keeping type hints.
    from .manifest import QualityManifestEntry


class QualityIssue(BaseModel):
    id: str
    validator: ValidatorName
    severity: ValidationSeverity
    title: str
    description: str
    affected_items: Sequence[str] = Field(default_factory=list)
    remediation: Optional[str]
    is_actionable: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class ScoringDimension(BaseModel):
    dimension_name: str
    weight: float
    score: float
    explanation: Optional[str]
    weak_spots: Sequence[str] = Field(default_factory=list)
    suggestions: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class CompletenessReport(BaseModel):
    required_files_present: Dict[str, bool] = Field(default_factory=dict)
    required_sections_present: Dict[str, bool] = Field(default_factory=dict)
    expected_diagram_count: int = 0
    actual_diagram_count: int = 0
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class SemanticReport(BaseModel):
    total_claims: int = 0
    claims_with_justification: int = 0
    claims_without_justification: int = 0
    circular_dependencies_detected: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class CitationReport(BaseModel):
    total_citations_in_output: int = 0
    total_citations_in_snapshot: int = 0
    citations_resolved: int = 0
    citations_unresolved: int = 0
    coverage_percent: float = 100.0
    unresolved_citations: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class DeterminismReport(BaseModel):
    determinism_baseline_version: Optional[str]
    current_build_hash: Optional[str]
    files_matching_baseline: Dict[str, bool] = Field(default_factory=dict)
    non_deterministic_files: Sequence[str] = Field(default_factory=list)
    root_causes: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class AccessibilityReport(BaseModel):
    wcag_level: Optional[str]
    contrast_pass_count: int = 0
    contrast_fail_count: int = 0
    keyboard_nav_pass: bool = True
    screen_reader_compatible: bool = True
    axe_violations_count: int = 0
    axe_violations: Sequence[Dict[str, object]] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class SecurityReport(BaseModel):
    secrets_detected: Sequence[str] = Field(default_factory=list)
    external_urls_in_offline_bundle: Sequence[str] = Field(default_factory=list)
    csp_headers_correct: Optional[bool]
    sanitization_applied: Optional[bool]
    xss_vectors_detected: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class PerformanceReport(BaseModel):
    bundle_size_bytes: Optional[int]
    bundle_size_mb: Optional[float]
    generation_time_seconds: Optional[float]
    portal_tti_seconds: Optional[float]
    diagram_render_times: Dict[str, float] = Field(default_factory=dict)
    budget_violations: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreReport(BaseModel):
    total_dimensions: int
    dimensions: Sequence[ScoringDimension] = Field(default_factory=list)
    composite_score: float
    health_status: Optional[str]
    score_trend: Optional[str]
    low_scoring_dimensions: Sequence[str] = Field(default_factory=list)
    high_priority_improvements: Sequence[str] = Field(default_factory=list)
    issues: Sequence[QualityIssue] = Field(default_factory=list)
    verdict: ValidationSeverity

    model_config = {"extra": "forbid", "frozen": True}


class QualityReport(BaseModel):
    report_id: str
    engagement_id: str
    bundle_version: int
    generated_at: datetime
    overall_verdict: ValidationSeverity

    completeness: CompletenessReport
    semantic: SemanticReport
    citation: CitationReport
    determinism: DeterminismReport
    accessibility: AccessibilityReport
    security: SecurityReport
    performance: PerformanceReport
    scoring: ArchitectureScoreReport

    all_issues: Sequence[QualityIssue] = Field(default_factory=list)
    blockers: Sequence[QualityIssue] = Field(default_factory=list)
    errors: Sequence[QualityIssue] = Field(default_factory=list)
    warnings: Sequence[QualityIssue] = Field(default_factory=list)

    validators_run: Dict[str, datetime] = Field(default_factory=dict)
    total_duration_seconds: float

    model_config = {"extra": "forbid", "frozen": True}


class QualityArtifact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    path: Optional[str]
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class QualityBundle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    artifacts: Sequence[QualityArtifact] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class QualityResult(BaseModel):
    report: QualityReport
    bundle: Optional[QualityBundle]

    model_config = {"extra": "forbid", "frozen": True}


# Canonical request/response contracts live in contracts.py. Duplicates removed.


class QualityGenerationOptions(BaseModel):
    run_determinism: bool = True
    run_accessibility: bool = True
    run_security: bool = True
    run_performance: bool = True

    model_config = {"extra": "forbid", "frozen": True}


# QualityManifestEntry is defined canonically in manifest.py; reference by
# forward annotation below to avoid duplicating the contract.


class QualityManifestMetadata(BaseModel):
    created_at: datetime
    created_by: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class QualityManifest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    entries: Sequence["QualityManifestEntry"] = Field(default_factory=list)
    metadata: Optional[QualityManifestMetadata]

    model_config = {"extra": "forbid", "frozen": True}


# QualityManifestIntegrity is owned by manifest.py; duplicate removed.
