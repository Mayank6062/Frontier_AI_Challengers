"""Tracing utilities for output generation telemetry."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Iterator
from uuid import uuid4

from backend.infrastructure.observability.tracer import start_trace


@dataclass(slots=True)
class TraceSpan:
    """Represents a single measured trace span."""

    name: str
    trace_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0


class TracingService:
    """Create trace IDs and duration-aware spans for orchestration stages."""

    def new_trace_id(self) -> str:
        """Create deterministic UUID string for a new trace context."""

        return str(uuid4())

    @contextmanager
    def start_span(
        self,
        name: str,
        trace_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[TraceSpan]:
        """Start a span and emit infrastructure trace completion signal."""

        span = TraceSpan(
            name=name,
            trace_id=trace_id,
            metadata={} if metadata is None else dict(metadata),
        )
        start = perf_counter()
        with start_trace(name, {"trace_id": trace_id, **span.metadata}):
            try:
                yield span
            finally:
                span.duration_seconds = perf_counter() - start
