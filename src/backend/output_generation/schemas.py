"""Common DTOs for the Output Generation pipeline.

These Pydantic models represent requests, results, artifacts and context for
the pipeline. They are used across the factory, service, and manifest layers.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from ..manifest.schemas import ManifestFileEntry
from datetime import datetime
from ..manifest.schemas import BundleProvenance


class GenerationStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class OutputArtifact(BaseModel):
    relative_path: str
    media_type: str
    content_bytes: bytes
    size_bytes: int
    content_hash: str


class FormatGenerationResult(BaseModel):
    artifacts: List[OutputArtifact]
    generator_name: str
    generator_version: str
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class GenerationMetadata(BaseModel):
    started_at: datetime
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None


class GenerationOptions(BaseModel):
    personas: List[str] = Field(default_factory=list)
    output_format: str = "zip"
    compress_on_download: bool = True


class GenerationContext(BaseModel):
    approved_snapshot: Dict
    request_id: str
    options: GenerationOptions


class GenerationError(BaseModel):
    code: str
    message: str
    details: Optional[Dict] = None


class GenerationSummary(BaseModel):
    request_id: str
    status: GenerationStatus
    artifacts_count: int
    errors: List[GenerationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class GenerationRequest(BaseModel):
    approved_snapshot: Dict
    request_id: str
    personas: List[str] = Field(default_factory=list)


class GenerationResult(BaseModel):
    summary: GenerationSummary
    artifacts: List[OutputArtifact] = Field(default_factory=list)
    manifest: Optional[dict] = None
    bundle_reference: Optional[str] = None


__all__ = [
    "GenerationRequest",
    "GenerationResult",
    "GenerationContext",
    "GenerationOptions",
    "GenerationMetadata",
    "GenerationStatus",
    "OutputArtifact",
    "FormatGenerationResult",
    "GenerationSummary",
    "GenerationError",
]
from __future__ import annotations

# Re-export core contracts
from .contracts import (
    BundleGenerationRequest,
    BundleGenerationResponse,
    GenerationResult,
    BundleGenerationStatus,
    GenerationMetrics,
)

# Re-export bundle manifest model from the bundle subpackage
from .bundle.schemas import BundleManifest as BundleManifestModel
from .bundle.schemas import BundleAssemblyRequest, BundleAssemblyResult

"""Schema re-exports and lightweight adapters used across output_generation.

These intentionally reuse canonical models defined elsewhere in the package to
avoid duplication. Import here to provide a single import surface for
consumers created in Phase 1.
"""

__all__ = [
    "BundleGenerationRequest",
    "BundleGenerationResponse",
    "GenerationResult",
    "BundleGenerationStatus",
    "GenerationMetrics",
    "BundleManifestModel",
    "BundleAssemblyRequest",
    "BundleAssemblyResult",
]
