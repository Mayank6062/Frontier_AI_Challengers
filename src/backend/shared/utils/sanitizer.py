"""
Sanitizer — Input sanitizer for prompts and free text.

Provides pure sanitization functions for prompt and user-input text.
Responsibility: Prevent injection attacks and malformed input through deterministic sanitization.
"""

import re
from typing import Optional


def sanitize_prompt_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input for use in prompts.

    Removes:
    - Control characters
    - Excessive whitespace
    - Potentially dangerous Unicode sequences
    - Truncates to max_length

    Args:
        text: Input text to sanitize.
        max_length: Maximum allowed length after sanitization.

    Returns:
        Sanitized text safe for prompt use.

    Raises:
        ValueError: If text is empty after sanitization or max_length is too small.
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if max_length < 1:
        raise ValueError("max_length must be >= 1")

    # Remove control characters (keep newlines and tabs)
    cleaned = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)

    # Remove zero-width characters and other invisible Unicode
    cleaned = re.sub(r"[\u200b-\u200d\ufeff]", "", cleaned)

    # Normalize whitespace: collapse multiple spaces/newlines
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n\n+", "\n", cleaned)
    cleaned = cleaned.strip()

    if not cleaned:
        raise ValueError("text becomes empty after sanitization")

    # Truncate if needed
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip()

    if not cleaned:
        raise ValueError("text becomes empty after truncation")

    return cleaned


def sanitize_json_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string for safe JSON serialization.

    Ensures proper escaping of special characters.

    Args:
        text: Input text to sanitize.
        max_length: Maximum allowed length.

    Returns:
        Sanitized text safe for JSON.

    Raises:
        ValueError: If text is invalid after sanitization.
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if max_length < 1:
        raise ValueError("max_length must be >= 1")

    # Remove control characters
    cleaned = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)
    cleaned = cleaned.strip()

    if not cleaned:
        raise ValueError("text becomes empty after sanitization")

    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip()

    if not cleaned:
        raise ValueError("text becomes empty after truncation")

    return cleaned


def sanitize_identifier(text: str) -> str:
    """
    Sanitize string for use as identifier (variable name, key, etc).

    Allows only alphanumeric characters, underscores, and hyphens.
    Must start with letter or underscore.

    Args:
        text: Input text to sanitize.

    Returns:
        Sanitized identifier.

    Raises:
        ValueError: If text cannot be converted to valid identifier.
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Allow only alphanumeric, underscore, hyphen
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", text)

    if not cleaned:
        raise ValueError("text contains no valid identifier characters")

    # Must start with letter or underscore
    if not re.match(r"^[a-zA-Z_]", cleaned):
        cleaned = "_" + cleaned

    return cleaned
