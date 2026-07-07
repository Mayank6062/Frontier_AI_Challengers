from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Protocol, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import (
    ArtifactStatus,
    ArtifactType,
    BundleStatus,
    DensityType,
    ExecutionMode,
    FailureCategory,
    FailureOrigin,
    FailureSeverity,
    GenerationStatus,
    PersonaType,
    RecoveryMode,
    StageType,
)


class ArtifactMetadata(BaseModel):
    artifact_id: UUID = Field(default_factory=uuid4)
    name: str
    type: ArtifactType
    size_bytes: Optional[int] = None
    media_type: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class OutputArtifact(BaseModel):
    metadata: ArtifactMetadata
    status: ArtifactStatus = ArtifactStatus.CREATED
    reference: Optional[str] = None

    model_config = {"extra": "forbid"}


class GenerationMetrics(BaseModel):
    elapsed_seconds: float = 0.0
    artifacts_generated: int = 0
    artifacts_failed: int = 0
    artifacts_skipped: int = 0

    model_config = {"extra": "forbid"}


class BundleStatistics(BaseModel):
    total_size_bytes: int = 0
    artifact_count: int = 0
    manifest_entries: int = 0

    model_config = {"extra": "forbid"}


class ExecutionMetadata(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    executed_by: Optional[str] = None

    model_config = {"extra": "forbid"}


class FailureReason(BaseModel):
    code: str
    message: str
    category: FailureCategory
    origin: FailureOrigin
    severity: FailureSeverity

    model_config = {"extra": "forbid"}


class RetryPolicy(BaseModel):
    max_retries: int = 0
    backoff_seconds: int = 0

    model_config = {"extra": "forbid"}


class RecoveryStrategy(BaseModel):
    mode: RecoveryMode
    retry_policy: Optional[RetryPolicy] = None
    description: Optional[str] = None

    model_config = {"extra": "forbid"}


class GenerationFailure(BaseModel):
    failure_id: UUID = Field(default_factory=uuid4)
    reason: FailureReason
    recoverable: bool = False
    strategy: Optional[RecoveryStrategy] = None

    model_config = {"extra": "forbid"}


class GenerationWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid"}


class PartialGenerationResult(BaseModel):
    artifacts: List[OutputArtifact] = Field(default_factory=list)
    failures: List[GenerationFailure] = Field(default_factory=list)
    warnings: List[GenerationWarning] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class GenerationResult(BaseModel):
    bundle_id: UUID = Field(default_factory=uuid4)
    status: GenerationStatus = GenerationStatus.PENDING
    artifacts: List[OutputArtifact] = Field(default_factory=list)
    metrics: GenerationMetrics = Field(default_factory=GenerationMetrics)
    statistics: BundleStatistics = Field(default_factory=BundleStatistics)
    partial: Optional[PartialGenerationResult] = None
    provenance: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class BundleGenerationRequest(BaseModel):
    approved_snapshot_reference: str
    requested_formats: Sequence[str] = Field(default_factory=list)
    personas: Sequence[PersonaType] = Field(default_factory=list)
    options: Optional[Dict[str, object]] = None
    deterministic: bool = True
    execution_mode: ExecutionMode = ExecutionMode.SYNC

    model_config = {"extra": "forbid"}


class BundleGenerationStatus(BaseModel):
    bundle_id: UUID
    status: BundleStatus
    started_at: datetime
    updated_at: Optional[datetime] = None
    message: Optional[str] = None

    model_config = {"extra": "forbid"}


class BundleGenerationResponse(BaseModel):
    request_id: UUID
    result: GenerationResult
    status: BundleGenerationStatus

    model_config = {"extra": "forbid"}


class GenerationOptions(BaseModel):
    portal_mode: Optional[bool] = False
    single_file_threshold_bytes: Optional[int] = None
    feature_flags: Optional[Dict[str, bool]] = None

    model_config = {"extra": "forbid"}


class ValidationSummary(BaseModel):
    valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class ValidationResult(BaseModel):
    artifact_id: Optional[UUID] = None
    summary: ValidationSummary = Field(default_factory=ValidationSummary)

    model_config = {"extra": "forbid"}


class ManifestReference(BaseModel):
    manifest_id: UUID = Field(default_factory=uuid4)
    path: str
    hash: Optional[str] = None

    model_config = {"extra": "forbid"}


class ProvenanceReference(BaseModel):
    provenance_id: UUID = Field(default_factory=uuid4)
    source: str
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class GenerationContext(BaseModel):
    request: BundleGenerationRequest
    approved_snapshot_manifest: ManifestReference
    execution: ExecutionMetadata = Field(default_factory=ExecutionMetadata)
    options: GenerationOptions = Field(default_factory=GenerationOptions)

    model_config = {"extra": "forbid"}


class OutputGenerationContext(BaseModel):
    context_id: UUID = Field(default_factory=uuid4)
    generation: GenerationContext
    persona: Optional[PersonaType] = None
    locale: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class ManifestEngine(Protocol):
    def assemble(self, manifest_ref: ManifestReference) -> ManifestReference:
        """Assemble a manifest into an artifact set and return a canonical manifest reference."""


class SnapshotValidator(Protocol):
    def validate(self, snapshot_reference: str) -> ValidationResult:
        """Validate an approved snapshot and return results."""


class OutputGeneratorService(Protocol):
    def generate_bundle(
        self, request: BundleGenerationRequest
    ) -> BundleGenerationResponse:
        """Generate a bundle from an approved snapshot reference."""


class PipelineStageMetadata(BaseModel):
    stage: StageType
    name: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Optional[GenerationStatus] = None
    details: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class PipelineEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    stage: Optional[StageType] = None
    message: Optional[str] = None
    details: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class PipelineResult(BaseModel):
    result: GenerationResult
    events: List[PipelineEvent] = Field(default_factory=list)
    metrics: GenerationMetrics = Field(default_factory=GenerationMetrics)

    model_config = {"extra": "forbid"}


class PipelineFailure(BaseModel):
    failure: GenerationFailure
    stage: Optional[StageType] = None

    model_config = {"extra": "forbid"}


class PipelineContext(BaseModel):
    context_id: UUID = Field(default_factory=uuid4)
    generation_context: GenerationContext
    current_stage: Optional[StageType] = None
    stages: List[PipelineStageMetadata] = Field(default_factory=list)
    events: List[PipelineEvent] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class PipelineStatus(BaseModel):
    pipeline_id: UUID = Field(default_factory=uuid4)
    status: GenerationStatus = GenerationStatus.PENDING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    model_config = {"extra": "forbid"}


class PipelineAuditMetadata(BaseModel):
    audit_id: UUID = Field(default_factory=uuid4)
    user: Optional[str] = None
    details: Optional[Dict[str, object]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"extra": "forbid"}


class PipelineMetrics(BaseModel):
    stages_executed: int = 0
    successful_stages: int = 0
    failed_stages: int = 0
    retries: int = 0

    model_config = {"extra": "forbid"}


class PersonaMetadata(BaseModel):
    persona_id: PersonaType
    landing_view: Optional[str] = None
    visible_sections: Optional[List[str]] = None
    hidden_sections: Optional[List[str]] = None
    theme_default: Optional[str] = None
    density: Optional[DensityType] = None
    navigation_profile: Optional[str] = None

    model_config = {"extra": "forbid"}


class PersonaRegistryInterface(Protocol):
    def register(self, persona: PersonaMetadata) -> None:
        """Register persona metadata."""

    def resolve(self, persona_id: PersonaType) -> Optional[PersonaMetadata]:
        """Resolve persona metadata by id."""


class PersonaResolverInterface(Protocol):
    def resolve_visibility(self, persona: PersonaType, section_id: str) -> bool:
        """Return whether a given section is visible for persona."""


class VisibilityResolver(Protocol):
    def is_section_visible(self, persona: PersonaType, section: str) -> bool:
        """Determine section visibility for a persona."""


class GenerationState(BaseModel):
    state_id: UUID = Field(default_factory=uuid4)
    status: GenerationStatus = GenerationStatus.PENDING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    model_config = {"extra": "forbid"}


class Transition(BaseModel):
    transition_id: UUID = Field(default_factory=uuid4)
    transition_type: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class StateHistory(BaseModel):
    transitions: List[Transition] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class ExecutionHistory(BaseModel):
    executions: List[ExecutionMetadata] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class LifecycleEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: Optional[str] = None
    details: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


# End of contracts
