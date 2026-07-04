"""
Observability Interface Contract.

Defines the abstraction for all structured logging, distributed tracing, and
metrics emission. Every backend module emits observability through this
interface — no module has a direct dependency on a specific observability SDK.

The observability service is a passive recipient: it receives events and
records them. It never makes decisions based on what it receives and never
blocks the critical path.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.14 (observability_service module)
    SYSTEM_ARCHITECTURE.md Section 15 (Observability)

Implementors:
    src/backend/infrastructure/observability_service.py

Consumers:
    Every backend module that emits logs, traces, or metrics.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Observability models (interface-local DTOs)
# ---------------------------------------------------------------------------


class LogLevel(str, Enum):
    """Standard log severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class LogRecord:
    """
    A structured log record with mandatory platform fields.

    Attributes:
        level: Log severity level.
        message: Human-readable log message.
        module: The source module emitting this record (e.g., "engagement").
        operation: The specific operation within the module.
        correlation_id: The request correlation ID for distributed tracing.
        engagement_id: Optional engagement context.
        session_id: Optional session context.
        user_id: Optional actor identity.
        agent_id: Optional agent context for agent-emitted records.
        extra: Additional structured fields specific to the operation.
    """

    level: LogLevel
    message: str
    module: str
    operation: str
    correlation_id: str
    engagement_id: str = ""
    session_id: str = ""
    user_id: str = ""
    agent_id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TraceSpan:
    """
    A distributed trace span representing a unit of work.

    Attributes:
        span_id: Unique identifier for this span.
        trace_id: The trace this span belongs to.
        parent_span_id: The parent span ID for nested operations.
        operation_name: The operation this span represents.
        service_name: The service emitting this span.
        correlation_id: Request correlation ID.
        started_at_utc: ISO 8601 UTC timestamp of span start.
        attributes: Key-value attributes for span annotation.
    """

    span_id: str
    trace_id: str
    parent_span_id: str
    operation_name: str
    service_name: str
    correlation_id: str
    started_at_utc: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricDataPoint:
    """
    A single metric observation.

    Attributes:
        name: The metric name (e.g., "agent.execution.latency_ms").
        value: The numeric metric value.
        metric_type: "counter", "gauge", or "histogram".
        labels: Key-value labels for metric dimensionality.
        recorded_at_utc: ISO 8601 UTC timestamp.
    """

    name: str
    value: float
    metric_type: str
    labels: dict[str, str] = field(default_factory=dict)
    recorded_at_utc: str = ""


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class ObservabilityInterface(ABC):
    """
    Abstract contract for all observability emission.

    Provides structured logging, distributed tracing, and metrics emission.
    All emissions are asynchronous and fire-and-forget — a failure in the
    observability backend must not propagate to the application.

    Contract invariants:
        - log() must never raise to the caller, even on backend failure.
        - span operations must never block the critical path.
        - metrics must never raise to the caller.
        - Implementations must never log secret values or PII beyond what
          is explicitly included in the LogRecord fields.
        - Correlation IDs must be propagated through all emitted records.
    """

    @abstractmethod
    def log(self, record: LogRecord) -> None:
        """
        Emit a structured log record.

        Fire-and-forget. Must never raise to the caller.

        Args:
            record: The structured log record to emit.
        """

    @abstractmethod
    def start_span(self, span: TraceSpan) -> TraceSpan:
        """
        Start a distributed trace span.

        Args:
            span: The span configuration. The returned span may have the
                span_id and started_at_utc fields populated by the
                implementation.

        Returns:
            TraceSpan: The started span (for use with end_span).
        """

    @abstractmethod
    def end_span(
        self,
        span: TraceSpan,
        status: str = "ok",
        error_message: str = "",
    ) -> None:
        """
        End and emit a distributed trace span.

        Args:
            span: The span started by start_span.
            status: Completion status — "ok", "error".
            error_message: Error description if status is "error".
        """

    @abstractmethod
    def record_metric(self, data_point: MetricDataPoint) -> None:
        """
        Emit a metric data point.

        Fire-and-forget. Must never raise to the caller.

        Args:
            data_point: The metric observation to record.
        """

    @abstractmethod
    def assign_correlation_id(self) -> str:
        """
        Generate and register a new correlation ID for a request.

        Returns:
            str: A new unique correlation ID (UUID v4 format).
        """

    @abstractmethod
    def get_correlation_id(self) -> str:
        """
        Retrieve the active correlation ID for the current execution context.

        Returns:
            str: The current correlation ID, or an empty string if not set.
        """
