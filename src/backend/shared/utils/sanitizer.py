"""
Input sanitization helpers.
"""

from __future__ import annotations


def ensure_non_empty_string(value: str) -> str:
    """Ensure a string is not empty or whitespace-only.

    Raises ValueError when invalid.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("String must be non-empty")
    return value


def sanitize_whitespace(value: str) -> str:
    """Trim and normalize internal whitespace to single spaces."""
    return " ".join(value.split())
