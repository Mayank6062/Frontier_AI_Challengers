from __future__ import annotations

import logging
from typing import Optional


class BaseExporter:
    """Simple deterministic exporter base class used by all format-specific exporters."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def export(self, payload: object) -> bytes:
        text = self._coerce_text(payload)
        self.logger.debug("Exported payload", extra={"payload_length": len(text)})
        return text.encode("utf-8")

    def _coerce_text(self, payload: object) -> str:
        if isinstance(payload, bytes):
            return payload.decode("utf-8")
        if isinstance(payload, str):
            return payload
        return str(payload)
