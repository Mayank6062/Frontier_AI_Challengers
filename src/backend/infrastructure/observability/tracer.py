"""Tracing implementation for the observability package.

Contains tracing-only responsibilities. Exposes `TraceHandle` and a
`start_trace` helper that returns the context manager.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger("architectiq.observability")
logger.addHandler(logging.NullHandler())


class TraceHandle:
    def __init__(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.metadata = metadata or {}
        self.start_ts: Optional[float] = None

    def __enter__(self) -> "TraceHandle":
        self.start_ts = time.time()
        return self

    def __exit__(
        self, exc_type: Optional[type], exc: Optional[BaseException], tb: Optional[Any]
    ) -> None:
        end = time.time()
        duration = end - (self.start_ts or end)
        logger.info(
            "trace.complete",
            extra={
                "trace_name": self.name,
                "duration_seconds": duration,
                "metadata": self.metadata,
            },
        )


def start_trace(name: str, metadata: Optional[Dict[str, Any]] = None) -> TraceHandle:
    return TraceHandle(name, metadata)


__all__ = ["TraceHandle", "start_trace"]
