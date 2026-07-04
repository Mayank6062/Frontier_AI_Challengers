"""Structured logging implementation for the observability package.

Contains logging-only responsibilities. Exposes `Logger` with an
`emit_log` method matching the ObservabilityInterface contract for logs.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("architectiq.observability")
logger.addHandler(logging.NullHandler())


class Logger:
    def emit_log(
        self, level: str, message: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        record = {"log_message": message, "metadata": metadata or {}}
        level_lower = (level or "info").lower()
        if level_lower == "debug":
            logger.debug(message, extra=record)
        elif level_lower == "warning" or level_lower == "warn":
            logger.warning(message, extra=record)
        elif level_lower == "error":
            logger.error(message, extra=record)
        elif level_lower == "critical":
            logger.critical(message, extra=record)
        else:
            logger.info(message, extra=record)


__all__ = ["Logger"]
