"""
Knowledge-layer exceptions for Shared layer.
"""
from __future__ import annotations

from .base_exception import SharedError


class KnowledgeError(SharedError):
    """Errors raised when knowledge operations fail."""

