"""Metrics emission implementation for the observability package.

Contains metrics-only responsibilities. Exposes `Metrics` with
`emit_metric` and an in-memory metric store for testing.
"""

from __future__ import annotations

from typing import Dict, Optional


class InMemoryMetricStore:
    def __init__(self) -> None:
        self._metrics: Dict[str, float] = {}

    def record(self, name: str, value: float) -> None:
        self._metrics[name] = value

    def get(self, name: str) -> Optional[float]:
        return self._metrics.get(name)


class Metrics:
    def __init__(self) -> None:
        self._metrics = InMemoryMetricStore()

    def emit_metric(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        # Tags accepted but ignored by in-memory store.
        self._metrics.record(name, value)


__all__ = ["Metrics", "InMemoryMetricStore"]
