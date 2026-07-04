"""
Text Utils — Safe text formatting and manipulation helpers.

Provides side-effect-free text utility functions for shared use.
Responsibility: Offer text formatting primitives without external dependencies.
"""

import re
from typing import Optional


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text by removing control characters and excessive whitespace.

    Args:
        text: Input text to sanitize.
        max_length: Optional maximum length; text is truncated if exceeded.

    Returns:
        Sanitized text string.

    Raises:
        ValueError: If text is empty after sanitization.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Remove control characters (keep newlines and common whitespace)
    cleaned = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)

    # Normalize whitespace: collapse multiple spaces, trim ends
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if not cleaned:
        raise ValueError("text becomes empty after sanitization")

    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip()

    return cleaned


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with optional suffix.

    Args:
        text: Text to truncate.
        max_length: Maximum length including suffix.
        suffix: Suffix to append if text is truncated.

    Returns:
        Truncated text.

    Raises:
        ValueError: If max_length is too small for suffix.
    """
    if max_length <= len(suffix):
        raise ValueError(f"max_length ({max_length}) must be > suffix length ({len(suffix)})")

    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def escape_markdown(text: str) -> str:
    """
    Escape Markdown special characters.

    Args:
        text: Text to escape.

    Returns:
        Escaped text safe for Markdown rendering.
    """
    special_chars = r"[\\\`*_{}[\]()#+\-.!|]"
    return re.sub(special_chars, r"\\\g<0>", text)


def pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
    """
    Get plural form of word based on count.

    Args:
        count: Count to determine pluralization.
        singular: Singular form.
        plural: Optional explicit plural form (default: singular + 's').

    Returns:
        Appropriately pluralized string.
    """
    if count == 1:
        return singular
    return plural or (singular + "s")
