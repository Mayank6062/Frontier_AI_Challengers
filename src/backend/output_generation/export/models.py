from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import ExportFormat, ExportSeverity


class ExportArtifact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    path: str
    format: ExportFormat
    size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportMetadata(BaseModel):
    generated_at: datetime
    generator_version: Optional[str]
    template_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportStatistics(BaseModel):
    artifacts_produced: int
    total_size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportMetrics(BaseModel):
    duration_seconds: Optional[float]
    retry_count: int = 0
    warnings: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class ExportManifestReference(BaseModel):
    manifest_id: UUID
    manifest_path: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportBundleReference(BaseModel):
    bundle_id: UUID
    bundle_path: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportConfigurationReference(BaseModel):
    config_id: Optional[str]
    config_source: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportTemplateReference(BaseModel):
    template_id: Optional[str]
    template_path: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportSourceArtifact(BaseModel):
    id: UUID
    path: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportTargetArtifact(BaseModel):
    id: UUID
    path: str
    format: ExportFormat

    model_config = {"extra": "forbid", "frozen": True}


class ExportTimeout(BaseModel):
    seconds: int

    model_config = {"extra": "forbid", "frozen": True}


class ExportWarning(BaseModel):
    code: str
    message: str
    severity: ExportSeverity = ExportSeverity.WARNING

    model_config = {"extra": "forbid", "frozen": True}


class ExportFailure(BaseModel):
    code: str
    message: str
    reason: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportResult(BaseModel):
    artifacts: Sequence[ExportArtifact] = Field(default_factory=list)
    warnings: Sequence[ExportWarning] = Field(default_factory=list)
    failures: Sequence[ExportFailure] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class ExportSummary(BaseModel):
    manifest_ref: Optional[ExportManifestReference]
    statistics: Optional[ExportStatistics]
    metrics: Optional[ExportMetrics]

    model_config = {"extra": "forbid", "frozen": True}


class ExportHistory(BaseModel):
    events: Sequence[Dict[str, object]] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class ExportAuditRecord(BaseModel):
    event_time: datetime
    actor: Optional[str]
    action: str
    details: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class PdfExportMetadata(BaseModel):
    page_count: Optional[int]
    size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class DocxExportMetadata(BaseModel):
    has_macros: Optional[bool]
    size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PptxExportMetadata(BaseModel):
    slide_count: Optional[int]
    has_animations: Optional[bool]
    size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class DrawioExportMetadata(BaseModel):
    xml_length: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class YamlExportMetadata(BaseModel):
    parsed: Optional[bool]

    model_config = {"extra": "forbid", "frozen": True}


class CsvExportMetadata(BaseModel):
    rows: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}
