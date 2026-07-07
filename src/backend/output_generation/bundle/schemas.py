from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class BundleStatus(str, Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    VALIDATION_PASSED = "VALIDATION_PASSED"
    QUALITY_CHECKED = "QUALITY_CHECKED"
    MANIFEST_CREATED = "MANIFEST_CREATED"
    INTEGRITY_SIGNED = "INTEGRITY_SIGNED"
    PERSONAS_BUILT = "PERSONAS_BUILT"
    BUNDLE_COMPLETE = "BUNDLE_COMPLETE"
    BUNDLE_BLOCKED = "BUNDLE_BLOCKED"
    BUNDLE_PARTIAL = "BUNDLE_PARTIAL"
    GENERATION_FAILED = "GENERATION_FAILED"
    ARCHIVED = "ARCHIVED"


class FileStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class RelationshipType(str, Enum):
    DERIVED_FROM = "derived_from"
    RENDERS_AS = "renders_as"
    REFERENCES = "references"
    SUMMARIZED_BY = "summarized_by"


class ArtifactRelationship(BaseModel):
    type: RelationshipType
    target_file_id: str

    model_config = {"extra": "forbid"}


class ManifestFileEntry(BaseModel):
    file_id: str
    relative_path: str
    file_type: str
    media_type: str
    size_bytes: int = Field(..., ge=0)
    content_hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    status: FileStatus
    generation_timestamp: datetime
    generator: str
    template_version: str
    persona_scope: List[str] = Field(default_factory=list)
    relationships: List[ArtifactRelationship] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)

    model_config = {"extra": "forbid"}


class BundleProvenance(BaseModel):
    approved_by: str
    approved_at: datetime
    approval_ledger_hash: str
    snapshot_version: str
    trace_id: str
    generation_environment: Optional[str] = None
    pipeline_version: Optional[str] = None

    model_config = {"extra": "forbid"}


class BundleManifest(BaseModel):
    manifest_version: str = Field(default="2.0.0")
    bundle_id: str
    engagement_id: str
    engagement_version: int = Field(..., ge=1)
    bundle_version: int = Field(..., ge=1)
    status: str
    generated_at: datetime
    generation_duration_seconds: float = Field(..., ge=0)
    generator_versions: Dict[str, str]
    template_versions: Dict[str, str]
    files: List[ManifestFileEntry]
    composite_hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    provenance: BundleProvenance
    personas: List[str]
    quality_gate_result: Optional[Dict] = None
    architecture_score: Optional[Dict] = None
    archive_format: str = "zip"
    compression_enabled: bool = False
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class BundleAssemblyRequest(BaseModel):
    engagement_id: str
    engagement_version: int
    approved_snapshot_id: str
    trace_id: str
    requested_personas: List[str]
    output_format: str = "zip"
    compress_on_download: bool = True

    model_config = {"extra": "forbid"}


class BundleAssemblyResult(BaseModel):
    bundle_id: str
    status: BundleStatus
    master_bundle_path: str
    persona_bundle_paths: Dict[str, str]
    manifest: BundleManifest
    generation_errors: List[str] = Field(default_factory=list)
    generation_warnings: List[str] = Field(default_factory=list)
    total_duration_seconds: float = 0.0

    model_config = {"extra": "forbid"}
