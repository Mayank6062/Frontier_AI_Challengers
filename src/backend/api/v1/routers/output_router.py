from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from typing import Any, List
from datetime import datetime
import base64

from pydantic import BaseModel

from ...schemas.output_schemas import OutputRequest, OutputResponse
from ...dependencies.service_deps import DIContainer
from backend.output_generation.bundle.schemas import (
    BundleAssemblyRequest as BG_BundleAssemblyRequest,
    BundleManifest,
    ManifestFileEntry,
    BundleProvenance,
    FileStatus,
)
from backend.output_generation.bundle.integrity import compute_content_hash

router = APIRouter()


def _logger_provider(request: Request) -> Any:
    provided: DIContainer.Provided = request.app.state.di_provided
    return provided.logger


@router.post("/render", response_model=OutputResponse)
def render_output(
    req: OutputRequest, logger: Any = Depends(_logger_provider)
) -> OutputResponse:
    # The API layer logs the request and returns a simple acknowledgement.
    logger.emit_log("info", "render_output", {"size": len(req.payload)})
    return OutputResponse(status="accepted")


class ArtifactUpload(BaseModel):
    relative_path: str
    content_b64: str
    media_type: str | None = None


class GenerateBundleRequest(BaseModel):
    engagement_id: str
    engagement_version: int
    bundle_id: str
    bundle_version: int
    personas: List[str] = []
    artifacts: List[ArtifactUpload] = []
    approved_snapshot_id: str
    trace_id: str


@router.post("/generate_bundle", response_model=OutputResponse)
async def generate_bundle(req: GenerateBundleRequest, logger: Any = Depends(_logger_provider)) -> OutputResponse:
    provided: DIContainer.Provided = logger  # passed via Depends wrapper; grab from request in provider if needed
    # Actually retrieve DI provided from the FastAPI request state
    # FastAPI dependency provider returns logger only; access app.state instead
    # Workaround: use starlette Request in dependency would be cleaner; here we fetch via global DIContainer

    # Build manifest
    files = []
    generation_results = []
    for a in req.artifacts:
        raw = base64.b64decode(a.content_b64)
        content_hash = compute_content_hash(raw)
        entry = ManifestFileEntry(
            file_id=a.relative_path.replace('/', '_'),
            relative_path=a.relative_path,
            file_type="generated",
            media_type=a.media_type or "application/octet-stream",
            size_bytes=len(raw),
            content_hash=content_hash,
            status=FileStatus.SUCCESS,
            generation_timestamp=datetime.utcnow(),
            generator="api",
            template_version="v1",
            persona_scope=[],
        )
        files.append(entry)

        class GR:
            def __init__(self, relative_path, content_bytes):
                self.relative_path = relative_path
                self.content_bytes = content_bytes

        generation_results.append(GR(a.relative_path, raw))

    provenance = BundleProvenance(
        approved_by="api",
        approved_at=datetime.utcnow(),
        approval_ledger_hash="",
        snapshot_version=req.approved_snapshot_id,
        trace_id=req.trace_id,
    )

    manifest = BundleManifest(
        bundle_id=req.bundle_id,
        engagement_id=req.engagement_id,
        engagement_version=req.engagement_version,
        bundle_version=req.bundle_version,
        status="PENDING",
        generated_at=datetime.utcnow(),
        generation_duration_seconds=0.0,
        generator_versions={"api": "1"},
        template_versions={"v1": "1"},
        files=files,
        composite_hash="",
        provenance=provenance,
        personas=req.personas,
        archive_format="zip",
        compression_enabled=True,
    )

    # Build BundleAssemblyRequest for assembler
    assembly_req = BG_BundleAssemblyRequest(
        engagement_id=req.engagement_id,
        engagement_version=req.engagement_version,
        approved_snapshot_id=req.approved_snapshot_id,
        trace_id=req.trace_id,
        requested_personas=req.personas,
        output_format="zip",
        compress_on_download=True,
    )

    # Acquire DI-provided assembler
    # access DI container via import of main app state
    from ... import main as api_main

    provided = api_main.app.state.di_provided
    assembler = getattr(provided, "bundle_assembler", None)
    if assembler is None:
        logger.emit_log("error", "assembler_missing", {})
        return OutputResponse(status="error:assembler_missing")

    result = await assembler.assemble(generation_results, manifest, assembly_req)
    if result.generation_errors:
        logger.emit_log("error", "bundle_errors", {"errors": result.generation_errors})
        return OutputResponse(status="failed")

    return OutputResponse(status="success")
