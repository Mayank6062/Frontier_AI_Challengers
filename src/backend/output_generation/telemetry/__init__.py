"""Telemetry runtime package for Output Generation Chapter 18."""

from __future__ import annotations

from .health_check import HealthCheckService
from .metrics import MetricsCollector
from .structured_logging import StructuredLogger
from .tracing import TracingService

_GLOBAL_METRICS: MetricsCollector | None = None


def get_metrics() -> MetricsCollector:
    """Return shared metrics collector for backwards-compatible callers."""

    global _GLOBAL_METRICS
    if _GLOBAL_METRICS is None:
        _GLOBAL_METRICS = MetricsCollector()
    return _GLOBAL_METRICS


__all__ = [
    "HealthCheckService",
    "MetricsCollector",
    "StructuredLogger",
    "TracingService",
    "get_metrics",
]
