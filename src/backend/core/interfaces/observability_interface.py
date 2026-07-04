from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ObservabilityInterface(ABC):
    """Contract for structured logging, tracing, and metric emission.

    Implementations provide methods to emit logs, metrics and traces in a
    structured, correlation-id aware manner. No implementation logic belongs
    in the interface module.
    """

    @abstractmethod
    def emit_log(
        self, level: str, message: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def emit_metric(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def start_trace(
        self, name: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Any:  # pragma: no cover - interface only
        """Start a trace/span and return a trace handle/context managed by the implementor."""

        raise NotImplementedError()
