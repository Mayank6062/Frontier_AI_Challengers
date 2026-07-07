"""Telemetry facade used by the output generation orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..telemetry.health_check import HealthCheckService
from ..telemetry.metrics import MetricsCollector
from ..telemetry.structured_logging import StructuredLogger
from ..telemetry.tracing import TracingService


@dataclass(slots=True)
class OrchestrationTelemetry:
    """Aggregates telemetry dependencies for orchestrator/runtime handlers."""

    metrics: MetricsCollector
    tracer: TracingService
    logger: StructuredLogger
    health: HealthCheckService

    def emit_stage_latency(
        self,
        stage: str,
        duration_seconds: float,
        trace_id: str,
    ) -> None:
        """Record stage duration and emit structured stage completion log."""

        self.metrics.record_duration(
            "pipeline.stage.duration.seconds",
            duration_seconds,
            tags={"stage": stage},
        )
        self.logger.info(
            "stage latency recorded",
            trace_id=trace_id,
            stage=stage,
            metadata={"duration_seconds": duration_seconds},
        )

    def emit_pipeline_summary(
        self,
        trace_id: str,
        total_stages: int,
        succeeded_stages: int,
        failed_stages: int,
        retries: int,
        total_duration_seconds: float,
    ) -> None:
        """Emit pipeline summary counters and structured summary log."""

        self.metrics.increment_counter("pipeline.summary.total", tags={"trace_id": trace_id})
        self.metrics.set_gauge("pipeline.summary.total_stages", float(total_stages))
        self.metrics.set_gauge("pipeline.summary.succeeded_stages", float(succeeded_stages))
        self.metrics.set_gauge("pipeline.summary.failed_stages", float(failed_stages))
        self.metrics.set_gauge("pipeline.summary.retries", float(retries))
        self.metrics.record_duration(
            "pipeline.total.duration.seconds",
            total_duration_seconds,
            tags={"trace_id": trace_id},
        )
        self.logger.info(
            "pipeline summary",
            trace_id=trace_id,
            metadata={
                "total_stages": total_stages,
                "succeeded_stages": succeeded_stages,
                "failed_stages": failed_stages,
                "retries": retries,
                "duration_seconds": total_duration_seconds,
            },
        )

    def audit_failure(self, trace_id: str, stage: str, error: BaseException) -> None:
        """Emit consistent structured failure event and counters."""

        self.metrics.increment_counter("pipeline.errors.total", tags={"stage": stage})
        self.logger.error(
            "pipeline stage failure",
            trace_id=trace_id,
            stage=stage,
            metadata={"error": str(error), "error_type": type(error).__name__},
        )

    def health_snapshot(self) -> dict[str, Any]:
        """Return a health snapshot from telemetry health checks."""

        return self.health.run_check()
