"""Observability package exports.

This `__init__` exposes the package-level symbols and contains no business
logic. Implementations live in the dedicated modules per
REPOSITORY_MASTER_STRUCTURE.md.
"""

from .logger import Logger
from .metrics import Metrics, InMemoryMetricStore
from .tracer import TraceHandle, start_trace
from .correlation import CorrelationManager

__all__ = [
    "Logger",
    "Metrics",
    "InMemoryMetricStore",
    "TraceHandle",
    "start_trace",
    "CorrelationManager",
]
