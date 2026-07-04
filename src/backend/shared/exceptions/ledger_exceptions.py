"""
Ledger-related exceptions for Shared layer.
"""
from __future__ import annotations

from .base_exception import SharedError


class LedgerError(SharedError):
    """Errors raised for decision ledger operations."""

