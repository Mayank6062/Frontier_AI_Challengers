"""
Validation-related exceptions for Shared layer.
"""
from __future__ import annotations

from .base_exception import SharedError


class ValidationError(SharedError):
    """Raised when validation of input data fails."""

