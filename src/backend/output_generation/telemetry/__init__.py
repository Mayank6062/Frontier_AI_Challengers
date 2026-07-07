from __future__ import annotations

from typing import Optional

from backend.infrastructure.observability.metrics import Metrics

"""Telemetry wrapper for output_generation.

This module wraps the infrastructure observability `Metrics` implementation
and exposes a single `get_metrics()` factory that returns a shared
`Metrics` instance. It deliberately re-uses the infra implementation rather
than duplicating metrics code.
"""


_GLOBAL_METRICS: Optional[Metrics] = None


def get_metrics() -> Metrics:
    """Return a singleton Metrics instance for output generation.

    Consumers may call this from DI wiring or directly in small scripts.
    """
    global _GLOBAL_METRICS
    if _GLOBAL_METRICS is None:
        _GLOBAL_METRICS = Metrics()
    return _GLOBAL_METRICS


__all__ = ["get_metrics", "Metrics"]
