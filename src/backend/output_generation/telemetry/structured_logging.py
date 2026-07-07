"""Structured logging utilities for output generation runtime."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any


class StructuredLogger:
    """Emit structured logs with consistent context keys and masking."""

    _SENSITIVE_KEYS: frozenset[str] = frozenset(
        {
            "approved_by",
            "email",
            "user_email",
            "token",
            "secret",
            "password",
            "api_key",
        }
    )

    def __init__(self, logger_name: str = "output_generation") -> None:
        self._logger = logging.getLogger(logger_name)

    def info(
        self,
        message: str,
        trace_id: str | None = None,
        stage: str | None = None,
        attempt: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Emit an info-level structured message."""

        data = self._build_extra(trace_id, stage, metadata)
        if attempt is not None:
            data["attempt"] = attempt
        self._logger.info(message, extra=data)

    def warning(
        self,
        message: str,
        trace_id: str | None = None,
        stage: str | None = None,
        attempt: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Emit a warning-level structured message."""

        data = self._build_extra(trace_id, stage, metadata)
        if attempt is not None:
            data["attempt"] = attempt
        self._logger.warning(message, extra=data)

    def error(
        self,
        message: str,
        trace_id: str | None = None,
        stage: str | None = None,
        attempt: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Emit an error-level structured message."""

        data = self._build_extra(trace_id, stage, metadata)
        if attempt is not None:
            data["attempt"] = attempt
        self._logger.error(message, extra=data)

    def _build_extra(
        self,
        trace_id: str | None,
        stage: str | None,
        metadata: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Build standardized and sanitized structured logging payload."""

        payload: dict[str, Any] = {
            "trace_id": trace_id,
            "stage": stage,
            "metadata": self._sanitize_dict(metadata or {}),
        }
        return payload

    def _sanitize_dict(self, value: Mapping[str, Any]) -> dict[str, Any]:
        """Mask sensitive keys recursively before logging."""

        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            lower_key = key.lower()
            if lower_key in self._SENSITIVE_KEYS:
                sanitized[key] = "***"
                continue
            if isinstance(item, Mapping):
                sanitized[key] = self._sanitize_dict(item)
                continue
            sanitized[key] = item
        return sanitized
