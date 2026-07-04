"""
Base shared exceptions for the Shared layer.
"""

from __future__ import annotations

from typing import Optional


class SharedError(Exception):
    """Base class for all shared-layer errors."""

    def __init__(self, message: str, *, cause: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.cause = cause
