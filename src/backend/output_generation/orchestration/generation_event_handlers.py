"""Pipeline event handlers for Output Generation orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from .telemetry import OrchestrationTelemetry


class PipelineEventType(StrEnum):
    """Canonical pipeline event types for orchestration telemetry and auditing."""

    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    STAGE_FAILED = "stage_failed"
    RETRY = "retry"
    WARNING = "warning"
    CANCELLATION = "cancellation"
    PROGRESS = "progress"


@dataclass(slots=True, frozen=True)
class PipelineEvent:
    """Immutable pipeline event payload."""

    event_type: PipelineEventType
    trace_id: str
    stage: str | None = None
    attempt: int | None = None
    message: str | None = None
    progress: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    event_time: datetime = field(default_factory=lambda: datetime.now(UTC))


class GenerationEventHandlers:
    """Handle and publish canonical generation orchestration events."""

    def __init__(self, telemetry: OrchestrationTelemetry) -> None:
        self._telemetry = telemetry

    async def dispatch(self, event: PipelineEvent) -> None:
        """Dispatch a pipeline event to the matching typed handler."""

        if event.event_type == PipelineEventType.PIPELINE_STARTED:
            await self.on_pipeline_started(event)
            return
        if event.event_type == PipelineEventType.PIPELINE_COMPLETED:
            await self.on_pipeline_completed(event)
            return
        if event.event_type == PipelineEventType.STAGE_STARTED:
            await self.on_stage_started(event)
            return
        if event.event_type == PipelineEventType.STAGE_COMPLETED:
            await self.on_stage_completed(event)
            return
        if event.event_type == PipelineEventType.STAGE_FAILED:
            await self.on_stage_failed(event)
            return
        if event.event_type == PipelineEventType.RETRY:
            await self.on_retry(event)
            return
        if event.event_type == PipelineEventType.WARNING:
            await self.on_warning(event)
            return
        if event.event_type == PipelineEventType.CANCELLATION:
            await self.on_cancellation(event)
            return
        if event.event_type == PipelineEventType.PROGRESS:
            await self.on_progress(event)

    async def on_pipeline_started(self, event: PipelineEvent) -> None:
        """Handle pipeline start event."""

        self._telemetry.logger.info(
            "pipeline started",
            trace_id=event.trace_id,
            stage=event.stage,
            metadata=event.metadata,
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.started.total",
            tags={"trace_id": event.trace_id},
        )

    async def on_pipeline_completed(self, event: PipelineEvent) -> None:
        """Handle pipeline completion event."""

        self._telemetry.logger.info(
            "pipeline completed",
            trace_id=event.trace_id,
            stage=event.stage,
            metadata=event.metadata,
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.completed.total",
            tags={"trace_id": event.trace_id},
        )

    async def on_stage_started(self, event: PipelineEvent) -> None:
        """Handle stage start event."""

        stage_name = event.stage or "unknown"
        self._telemetry.logger.info(
            "stage started",
            trace_id=event.trace_id,
            stage=stage_name,
            attempt=event.attempt,
            metadata=event.metadata,
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.stage.started.total",
            tags={"stage": stage_name},
        )

    async def on_stage_completed(self, event: PipelineEvent) -> None:
        """Handle stage completion event."""

        stage_name = event.stage or "unknown"
        self._telemetry.logger.info(
            "stage completed",
            trace_id=event.trace_id,
            stage=stage_name,
            attempt=event.attempt,
            metadata=event.metadata,
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.stage.completed.total",
            tags={"stage": stage_name},
        )

    async def on_stage_failed(self, event: PipelineEvent) -> None:
        """Handle stage failure event."""

        stage_name = event.stage or "unknown"
        self._telemetry.logger.error(
            "stage failed",
            trace_id=event.trace_id,
            stage=stage_name,
            attempt=event.attempt,
            metadata={"message": event.message, **event.metadata},
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.stage.failed.total",
            tags={"stage": stage_name},
        )

    async def on_retry(self, event: PipelineEvent) -> None:
        """Handle retry event."""

        stage_name = event.stage or "unknown"
        self._telemetry.logger.warning(
            "stage retry",
            trace_id=event.trace_id,
            stage=stage_name,
            attempt=event.attempt,
            metadata={"message": event.message, **event.metadata},
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.stage.retry.total",
            tags={"stage": stage_name},
        )

    async def on_warning(self, event: PipelineEvent) -> None:
        """Handle warning event."""

        stage_name = event.stage or "unknown"
        self._telemetry.logger.warning(
            "pipeline warning",
            trace_id=event.trace_id,
            stage=stage_name,
            metadata={"message": event.message, **event.metadata},
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.warning.total",
            tags={"stage": stage_name},
        )

    async def on_cancellation(self, event: PipelineEvent) -> None:
        """Handle cancellation event."""

        self._telemetry.logger.warning(
            "pipeline cancelled",
            trace_id=event.trace_id,
            stage=event.stage,
            metadata={"message": event.message, **event.metadata},
        )
        self._telemetry.metrics.increment_counter(
            "pipeline.cancelled.total",
            tags={"trace_id": event.trace_id},
        )

    async def on_progress(self, event: PipelineEvent) -> None:
        """Handle progress event."""

        progress_value = 0.0 if event.progress is None else max(0.0, min(1.0, event.progress))
        self._telemetry.metrics.set_gauge(
            "pipeline.progress.ratio",
            progress_value,
            tags={"trace_id": event.trace_id},
        )
        self._telemetry.logger.info(
            "pipeline progress",
            trace_id=event.trace_id,
            stage=event.stage,
            metadata={"progress": progress_value, **event.metadata},
        )
