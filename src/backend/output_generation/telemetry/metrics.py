"""Metrics collection utilities for output generation telemetry."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass(slots=True)
class MetricPoint:
    """Single metric observation point."""

    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Thread-safe in-memory metric collector with counter and latency helpers."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._counters: dict[str, float] = {}
        self._gauges: dict[str, float] = {}
        self._durations: dict[str, list[float]] = {}

    def emit_metric(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Backwards-compatible metric emission method used by legacy callers."""

        self.increment_counter(name=name, amount=value, tags=tags)

    def increment_counter(
        self,
        name: str,
        amount: float = 1.0,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Increment a counter metric."""

        key = self._normalize_key(name, tags)
        with self._lock:
            self._counters[key] = self._counters.get(key, 0.0) + amount

    def set_gauge(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Set a gauge metric to the latest value."""

        key = self._normalize_key(name, tags)
        with self._lock:
            self._gauges[key] = value

    def record_duration(
        self,
        name: str,
        duration_seconds: float,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Record latency values for duration-based metrics."""

        key = self._normalize_key(name, tags)
        with self._lock:
            values = self._durations.setdefault(key, [])
            values.append(duration_seconds)

    def increment_error_counter(self, stage: str) -> None:
        """Increment standardized stage error counter."""

        self.increment_counter("pipeline.errors.total", tags={"stage": stage})

    def increment_retry_counter(self, stage: str) -> None:
        """Increment standardized stage retry counter."""

        self.increment_counter("pipeline.retries.total", tags={"stage": stage})

    def pipeline_statistics(self) -> dict[str, Any]:
        """Return computed pipeline metric summary for reporting."""

        with self._lock:
            duration_points = [value for values in self._durations.values() for value in values]
            avg_duration = (
                sum(duration_points) / len(duration_points)
                if duration_points
                else 0.0
            )
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "duration_points": len(duration_points),
                "average_duration_seconds": avg_duration,
            }

    def snapshot(self) -> tuple[MetricPoint, ...]:
        """Return point-in-time metric snapshot for diagnostics."""

        points: list[MetricPoint] = []
        with self._lock:
            for name, value in self._counters.items():
                points.append(MetricPoint(name=name, value=value))
            for name, value in self._gauges.items():
                points.append(MetricPoint(name=name, value=value))
            for name, values in self._durations.items():
                points.append(MetricPoint(name=f"{name}.count", value=float(len(values))))
        return tuple(points)

    @staticmethod
    def _normalize_key(name: str, tags: dict[str, str] | None) -> str:
        """Build deterministic key from metric name and optional tags."""

        if not tags:
            return name
        normalized_tags = ",".join(f"{key}={tags[key]}" for key in sorted(tags))
        return f"{name}|{normalized_tags}"
