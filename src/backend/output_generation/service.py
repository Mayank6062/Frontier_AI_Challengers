"""Main OutputGeneratorService orchestrator implementing Chapter 18 pipeline.

This service orchestrates the complete pipeline in the canonical order and
emits a GenerationResult. It relies on a configured OutputGeneratorFactory,
manifest builder, bundle assembler and quality orchestrator provided via DI.
"""

from __future__ import annotations

import asyncio
from typing import List
from datetime import datetime

from .factory import OutputGeneratorFactory
from .schemas import GenerationContext, FormatGenerationResult, GenerationResult, GenerationSummary, GenerationStatus, OutputArtifact
from .exceptions import OrchestrationError, GenerationError


class OutputGeneratorService:
    """Orchestrates the full generation pipeline in canonical order.

    The service follows the pipeline order defined in Chapter 18.
    """

    PIPELINE_STAGES = [
        "validation",
        "markdown",
        "html",
        "portal",
        "diagrams",
        "presentation",
        "quality",
        "manifest",
        "bundle",
        "storage",
        "score_report",
        "export",
    ]

    def __init__(
        self,
        generator_factory: OutputGeneratorFactory,
        quality_orchestrator: object | None = None,
        manifest_builder: object | None = None,
        bundle_assembler: object | None = None,
    ) -> None:
        self.factory = generator_factory
        self.quality = quality_orchestrator
        self.manifest_builder = manifest_builder
        self.bundle_assembler = bundle_assembler

    async def generate(self, context: GenerationContext) -> GenerationResult:
        started = datetime.utcnow()
        artifacts: List[OutputArtifact] = []
        stage_results: dict = {}

        # Execute each stage in order; generators may raise — map to GenerationError
        for stage in self.PIPELINE_STAGES:
            try:
                gen = self.factory.get_generator(stage)
            except KeyError:
                # Missing generator is a configuration error — treat as orchestration error
                raise OrchestrationError(f"missing generator for stage: {stage}")

            # call generate (async) and merge artifacts
            result: FormatGenerationResult = await gen.generate(context)
            stage_results[stage] = result
            for a in result.artifacts:
                artifacts.append(a)

            # If the generator produced errors and it's not optional -> stop
            if result.errors and not gen.is_optional():
                raise GenerationError(f"generator {stage} failed", details={"errors": result.errors})

        # After all stages completed, build summary
        status = GenerationStatus.SUCCEEDED
        errors = []
        warnings = []
        for r in stage_results.values():
            if r.errors:
                errors.extend(r.errors)
            if r.warnings:
                warnings.extend(r.warnings)

        if errors:
            status = GenerationStatus.PARTIAL

        summary = GenerationSummary(
            request_id=context.request_id,
            status=status,
            artifacts_count=len(artifacts),
            errors=[],
            warnings=warnings,
        )

        result = GenerationResult(summary=summary, artifacts=artifacts)
        return result


__all__ = ["OutputGeneratorService"]
from __future__ import annotations

import asyncio
from uuid import uuid4
from datetime import datetime

from .contracts import (
    BundleGenerationRequest,
    BundleGenerationResponse,
    GenerationResult,
    GenerationMetrics,
    BundleGenerationStatus,
    GenerationStatus,
)
from .bundle.schemas import BundleManifest, BundleAssemblyRequest
from .exceptions import StorageError, GenerationError, ValidationError
from .enums import BundleStatus


class OutputGeneratorServiceImpl:
    """Concrete OutputGeneratorService implementation for Phase 1.

    This implementation wires into existing repository primitives (storage,
    bundle assembler, metrics) and orchestrates a simple synchronous
    generation flow that delegates heavy lifting to the canonical
    `BundleAssembler` implemented in the `bundle` package.
    """

    def __init__(
        self,
        storage: object,
        bundle_assembler: object,
        metrics: object,
        logger: object | None = None,
    ) -> None:
        self.storage = storage
        self.bundle_assembler = bundle_assembler
        self.metrics = metrics
        self.logger = logger

    def _log(self, message: str) -> None:
        if self.logger is not None:
            try:
                # infra Logger exposes `emit_log(level, message, metadata)`
                if hasattr(self.logger, "emit_log"):
                    self.logger.emit_log("info", message)
                elif hasattr(self.logger, "info"):
                    self.logger.info(message)
            except Exception:
                pass

    def generate_bundle(self, request: BundleGenerationRequest) -> BundleGenerationResponse:
        # Basic validations
        if not request.approved_snapshot_reference:
            raise ValidationError("approved_snapshot_reference is required")

        # Retrieve approved snapshot manifest from storage
        try:
            snapshot = None
            if hasattr(self.storage, "get"):
                snapshot = self.storage.get(request.approved_snapshot_reference)
            else:
                raise StorageError("Storage backend does not implement `get`")
        except Exception as exc:  # noqa: BLE001 - domain boundary
            raise StorageError("failed to retrieve approved snapshot", details={"cause": str(exc)})

        if snapshot is None:
            # Build a formal error response
            result = GenerationResult()
            result.status = GenerationStatus.FAILED
            result.partial = None
            result.provenance = {"reason": "snapshot_not_found"}

            status = BundleGenerationStatus(bundle_id=result.bundle_id, status=BundleStatus.FAILED, started_at=datetime.utcnow())
            # Fabricate a response consistent with contracts
            response = BundleGenerationResponse(request_id=result.bundle_id, result=result, status=status)
            return response

        # Convert snapshot dict to BundleManifest (bundle package canonical model)
        try:
            manifest = BundleManifest.model_validate(snapshot) if hasattr(BundleManifest, "model_validate") else BundleManifest.parse_obj(snapshot)
        except Exception as exc:
            raise ValidationError("invalid snapshot manifest", details={"cause": str(exc)})

        # Build assembly request
        assembly_request = BundleAssemblyRequest(
            engagement_id=getattr(manifest, "engagement_id", "unknown"),
            engagement_version=getattr(manifest, "engagement_version", 1),
            approved_snapshot_id=request.approved_snapshot_reference,
            trace_id=str(uuid4()),
            requested_personas=[str(p) for p in request.personas] if getattr(request, "personas", None) else [],
            output_format="zip",
            compress_on_download=True,
        )

        # Delegate to bundle assembler (async) — run synchronously for this service API
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = None

        async def _assemble():
            return await self.bundle_assembler.assemble([], manifest, assembly_request)

        try:
            if loop and loop.is_running():
                # Running inside an async loop; create a new one for blocking call
                new_loop = asyncio.new_event_loop()
                try:
                    res = new_loop.run_until_complete(_assemble())
                finally:
                    new_loop.close()
            else:
                loop = loop or asyncio.new_event_loop()
                try:
                    res = loop.run_until_complete(_assemble())
                finally:
                    if not loop.is_running():
                        loop.close()
        except Exception as exc:
            raise GenerationError("bundle assembly failed", details={"cause": str(exc)})

        # Map BundleAssemblyResult → GenerationResult
        gen_result = GenerationResult()
        gen_result.bundle_id = res.bundle_id
        gen_result.status = GenerationStatus.SUCCEEDED if getattr(res, "generation_errors", None) == [] else GenerationStatus.PARTIAL
        gen_result.artifacts = []
        gen_result.metrics = GenerationMetrics(elapsed_seconds=getattr(res, "total_duration_seconds", 0.0))

        status = BundleGenerationStatus(bundle_id=gen_result.bundle_id, status=BundleStatus.COMPLETED, started_at=datetime.utcnow())

        response = BundleGenerationResponse(request_id=gen_result.bundle_id, result=gen_result, status=status)
        return response


__all__ = ["OutputGeneratorServiceImpl"]
