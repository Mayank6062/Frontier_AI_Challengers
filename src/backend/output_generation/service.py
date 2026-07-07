"""Main OutputGeneratorService orchestrator implementing Chapter 18 pipeline.

This service is the main orchestration point for the output generation pipeline,
delegating to bundle assembler, storage, and supporting quality/manifest builders.
"""

from __future__ import annotations

import asyncio
from typing import List
from datetime import datetime
from uuid import uuid4

from .factory import OutputGeneratorFactory
from .schemas import GenerationContext, FormatGenerationResult, GenerationResult, GenerationSummary, GenerationStatus as SchemaGenerationStatus, OutputArtifact
from .exceptions import OrchestrationError, GenerationError, StorageError, ValidationError
from .contracts import (
    BundleGenerationRequest,
    BundleGenerationResponse,
    GenerationMetrics,
    BundleGenerationStatus,
)
from .bundle.schemas import BundleManifest, BundleAssemblyRequest
from .enums import BundleStatus, GenerationStatus


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
            stage_result: FormatGenerationResult = await gen.generate(context)
            stage_results[stage] = stage_result
            for a in stage_result.artifacts:
                artifacts.append(a)

            # If the generator produced errors and it's not optional -> stop
            if stage_result.errors and not gen.is_optional():
                raise GenerationError(f"generator {stage} failed", details={"errors": stage_result.errors})

        # After all stages completed, build summary
        status = SchemaGenerationStatus.SUCCEEDED
        errors = []
        warnings = []
        for r in stage_results.values():
            if r.errors:
                errors.extend(r.errors)
            if r.warnings:
                warnings.extend(r.warnings)

        if errors:
            status = SchemaGenerationStatus.PARTIAL

        summary = GenerationSummary(
            request_id=context.request_id,
            status=status,
            artifacts_count=len(artifacts),
            errors=errors,
            warnings=warnings,
        )

        result = GenerationResult(summary=summary, artifacts=artifacts)
        return result


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
        """Generate a bundle from an approved snapshot reference.

        This method handles bundle assembly workflow including manifest validation,
        snapshot retrieval, persona filtering, and storage.
        """
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
            # Build a formal error response using contracts.GenerationResult
            from .contracts import GenerationResult as ContractGenerationResult
            result = ContractGenerationResult()
            bundle_uuid = uuid4()
            result.status = GenerationStatus.FAILED
            result.bundle_id = bundle_uuid

            status = BundleGenerationStatus(bundle_id=bundle_uuid, status=BundleStatus.FAILED, started_at=datetime.utcnow())
            response = BundleGenerationResponse(request_id=bundle_uuid, result=result, status=status)
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

        # Map BundleAssemblyResult → GenerationResult using contracts.GenerationResult
        from .contracts import GenerationResult as ContractGenerationResult
        gen_result = ContractGenerationResult()
        bundle_uuid = getattr(res, "bundle_id", uuid4())
        if isinstance(bundle_uuid, str):
            from uuid import UUID
            bundle_uuid = UUID(bundle_uuid)
        gen_result.bundle_id = bundle_uuid
        gen_result.status = GenerationStatus.SUCCEEDED if getattr(res, "generation_errors", None) == [] else GenerationStatus.PARTIAL
        gen_result.metrics = GenerationMetrics(elapsed_seconds=getattr(res, "total_duration_seconds", 0.0))

        status = BundleGenerationStatus(bundle_id=bundle_uuid, status=BundleStatus.COMPLETED, started_at=datetime.utcnow())
        response = BundleGenerationResponse(request_id=bundle_uuid, result=gen_result, status=status)
        return response


__all__ = ["OutputGeneratorService", "OutputGeneratorServiceImpl"]
