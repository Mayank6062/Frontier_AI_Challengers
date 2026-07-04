"""Correlation ID management for the observability package.

Provides a minimal correlation ID helper consistent with architecture
expectations. This is intentionally small and non-opinionated.
"""

from __future__ import annotations

import uuid
from typing import Optional


class CorrelationManager:
    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def validate(cid: Optional[str]) -> bool:
        if cid is None:
            return False
        try:
            uuid.UUID(cid)
            return True
        except Exception:
            return False


__all__ = ["CorrelationManager"]
