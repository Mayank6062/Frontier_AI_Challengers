"""Generation orchestration runtime for the complete output pipeline."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any, Awaitable, Callable

from .generation_event_handlers import (
    GenerationEventHandlers,
    PipelineEvent,
    PipelineEventType,
)
from .telemetry import OrchestrationTelemetry

StageExecutor = Callable[["GenerationOrchestratorContext"], Awaitable["StageExecutionResult"]]


@dataclass(slots=True, frozen=True)
class GenerationOrchestratorConfig:
    """Runtime configuration for orchestration behavior."""

    retry_attempts: int = 3
    retry_backoff_seconds: float = 0.5
    optional_stages: frozenset[str] = field(default_factory=frozenset)


@dataclass(slots=True)
class GenerationOrchestratorContext:
    """Execution context for a single pipeline run."""

    trace_id: str
    engagement_id: str
    payload: dict[str, Any]
    cancelled: bool = False


@dataclass(slots=True, frozen=True)
class StageExecutionResult:
    """Normalized stage execution result."""

    stage: str
    success: bool
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    artifacts: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class PipelineExecutionResult:
    """Pipeline execution summary with per-stage outcomes."""

    trace_id: str
    started_at: datetime
    completed_at: datetime
    success: bool
    stage_results: tuple[StageExecutionResult, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]


class GenerationOrchestrator:
    """Coordinate all Chapter 18 output-generation stages with telemetry."""

    PIPELINE_STAGES: tuple[str, ...] = (
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
    )

    def __init__(
        self,
        telemetry: OrchestrationTelemetry,
        event_handlers: GenerationEventHandlers,
        stage_executors: dict[str, StageExecutor] | None = None,
        config: GenerationOrchestratorConfig | None = None,
    ) -> None:
        self._telemetry = telemetry
        self._event_handlers = event_handlers
        self._executors = stage_executors or {}
        self._config = config or GenerationOrchestratorConfig()

    async def run(self, context: GenerationOrchestratorContext) -> PipelineExecutionResult:
        """Run full deterministic pipeline with retries and failure recovery."""

        started_at = datetime.now(UTC)
        pipeline_start = perf_counter()
        stage_results: list[StageExecutionResult] = []
        warnings: list[str] = []
        errors: list[str] = []
        retry_total = 0

        await self._event_handlers.dispatch(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_STARTED,
                trace_id=context.trace_id,
                metadata={"engagement_id": context.engagement_id},
            )
        )

        with self._telemetry.tracer.start_span(
            "output_generation.pipeline",
            trace_id=context.trace_id,
            metadata={"engagement_id": context.engagement_id},
        ):
            for index, stage in enumerate(self.PIPELINE_STAGES, start=1):
                if context.cancelled:
                    await self._event_handlers.dispatch(
                        PipelineEvent(
                            event_type=PipelineEventType.CANCELLATION,
                            trace_id=context.trace_id,
                            stage=stage,
                            message="pipeline cancelled by caller",
                        )
                    )
                    errors.append("pipeline cancelled")
                    break

                executor = self._executors.get(stage)
                if executor is None:
                    message = f"missing executor for stage '{stage}'"
                    if stage in self._config.optional_stages:
                        warnings.append(message)
                        stage_results.append(
                            StageExecutionResult(
                                stage=stage,
                                success=False,
                                warnings=(message,),
                            )
                        )
                        await self._event_handlers.dispatch(
                            PipelineEvent(
                                event_type=PipelineEventType.WARNING,
                                trace_id=context.trace_id,
                                stage=stage,
                                message=message,
                            )
                        )
                        continue
                    errors.append(message)
                    stage_results.append(
                        StageExecutionResult(
                            stage=stage,
                            success=False,
                            errors=(message,),
                        )
                    )
                    await self._event_handlers.dispatch(
                        PipelineEvent(
                            event_type=PipelineEventType.STAGE_FAILED,
                            trace_id=context.trace_id,
                            stage=stage,
                            message=message,
                        )
                    )
                    break

                await self._event_handlers.dispatch(
                    PipelineEvent(
                        event_type=PipelineEventType.STAGE_STARTED,
                        trace_id=context.trace_id,
                        stage=stage,
                        attempt=1,
                    )
                )

                stage_outcome, retries = await self._execute_with_retry(
                    context=context,
                    stage=stage,
                    executor=executor,
                )
                retry_total += retries
                stage_results.append(stage_outcome)
                warnings.extend(stage_outcome.warnings)
                errors.extend(stage_outcome.errors)

                await self._event_handlers.dispatch(
                    PipelineEvent(
                        event_type=(
                            PipelineEventType.STAGE_COMPLETED
                            if stage_outcome.success
                            else PipelineEventType.STAGE_FAILED
                        ),
                        trace_id=context.trace_id,
                        stage=stage,
                        metadata=stage_outcome.metadata,
                    )
                )

                await self._event_handlers.dispatch(
                    PipelineEvent(
                        event_type=PipelineEventType.PROGRESS,
                        trace_id=context.trace_id,
                        stage=stage,
                        progress=index / len(self.PIPELINE_STAGES),
                    )
                )

                if not stage_outcome.success and stage not in self._config.optional_stages:
                    break

        completed_at = datetime.now(UTC)
        success = all(result.success or result.stage in self._config.optional_stages for result in stage_results)
        pipeline_duration = perf_counter() - pipeline_start

        self._telemetry.emit_pipeline_summary(
            trace_id=context.trace_id,
            total_stages=len(self.PIPELINE_STAGES),
            succeeded_stages=sum(1 for item in stage_results if item.success),
            failed_stages=sum(1 for item in stage_results if not item.success),
            retries=retry_total,
            total_duration_seconds=pipeline_duration,
        )

        await self._event_handlers.dispatch(
            PipelineEvent(
                event_type=PipelineEventType.PIPELINE_COMPLETED,
                trace_id=context.trace_id,
                metadata={"success": success, "duration_seconds": pipeline_duration},
            )
        )

        return PipelineExecutionResult(
            trace_id=context.trace_id,
            started_at=started_at,
            completed_at=completed_at,
            success=success,
            stage_results=tuple(stage_results),
            warnings=tuple(warnings),
            errors=tuple(errors),
        )

    async def _execute_with_retry(
        self,
        context: GenerationOrchestratorContext,
        stage: str,
        executor: StageExecutor,
    ) -> tuple[StageExecutionResult, int]:
        """Execute one stage with configured retry attempts and backoff."""

        retries = 0
        last_error: BaseException | None = None

        for attempt in range(1, self._config.retry_attempts + 1):
            stage_start = perf_counter()
            try:
                with self._telemetry.tracer.start_span(
                    f"output_generation.stage.{stage}",
                    trace_id=context.trace_id,
                    metadata={"attempt": attempt},
                ):
                    result = await executor(context)

                duration = perf_counter() - stage_start
                self._telemetry.emit_stage_latency(
                    stage=stage,
                    duration_seconds=duration,
                    trace_id=context.trace_id,
                )

                if result.success:
                    return result, retries

                result_error = "; ".join(result.errors) or "stage returned unsuccessful result"
                raise RuntimeError(result_error)
            except Exception as error:  # noqa: BLE001
                retries = attempt - 1
                last_error = error
                self._telemetry.audit_failure(context.trace_id, stage, error)
                if attempt >= self._config.retry_attempts:
                    break

                await self._event_handlers.dispatch(
                    PipelineEvent(
                        event_type=PipelineEventType.RETRY,
                        trace_id=context.trace_id,
                        stage=stage,
                        attempt=attempt + 1,
                        message=str(error),
                    )
                )
                await asyncio.sleep(self._config.retry_backoff_seconds * attempt)

        final_error = "unknown failure" if last_error is None else str(last_error)
        return (
            StageExecutionResult(
                stage=stage,
                success=False,
                errors=(final_error,),
            ),
            retries,
        )
