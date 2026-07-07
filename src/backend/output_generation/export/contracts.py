from __future__ import annotations

from typing import Dict, Optional, Sequence
from uuid import UUID

from pydantic import BaseModel

from .models import (
    ExportBundleReference,
    ExportManifestReference,
    ExportResult,
    ExportSummary,
)


class ExportGenerationRequest(BaseModel):
    manifest_ref: ExportManifestReference
    bundle_ref: Optional[ExportBundleReference]
    requested_formats: Sequence[str]
    requester_id: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportGenerationResponse(BaseModel):
    request_id: UUID
    result: ExportResult
    summary: Optional[ExportSummary]

    model_config = {"extra": "forbid", "frozen": True}


class ExportContext(BaseModel):
    trace_id: Optional[str]
    user_id: Optional[str]
    feature_flags: Optional[Dict[str, bool]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportPipelineContext(BaseModel):
    stage: Optional[str]
    context: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportPipelineStage(BaseModel):
    name: str
    status: str
    details: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportPipelineResult(BaseModel):
    stages: Sequence[ExportPipelineStage]
    final_summary: Optional[ExportSummary]

    model_config = {"extra": "forbid", "frozen": True}


class ExportPipelineSummary(BaseModel):
    total_stages: int
    succeeded: int
    failed: int

    model_config = {"extra": "forbid", "frozen": True}


class ExportGenerationOptions(BaseModel):
    timeout_seconds: Optional[int]
    retry_mode: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportGenerationStatistics(BaseModel):
    attempts: int
    total_duration_seconds: Optional[float]

    model_config = {"extra": "forbid", "frozen": True}


class ExportGenerationMetrics(BaseModel):
    metrics: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportExecutionMetadata(BaseModel):
    started_at: Optional[str]
    ended_at: Optional[str]
    engine_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class FeatureFlagContext(BaseModel):
    flags: Optional[Dict[str, bool]]

    model_config = {"extra": "forbid", "frozen": True}


class ConverterContext(BaseModel):
    converter_type: Optional[str]
    settings: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}
