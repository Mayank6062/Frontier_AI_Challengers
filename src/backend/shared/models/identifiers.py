"""
Identifier helpers for generating and validating UUIDs.
"""
from __future__ import annotations

import uuid
from typing import Final


UUID_NAMESPACE: Final[str] = "urn:uuid"


def generate_uuid4() -> str:
    """Generate a random RFC4122 UUID (version 4) and return its string form.

    Returns:
        str: UUID string, e.g. "6fa459ea-ee8a-3ca4-894e-db77e160355e".
    """
    return str(uuid.uuid4())


def is_valid_uuid(value: str) -> bool:
    """Validate that the provided string is a valid UUID.

    Args:
        value: string to validate.

    Returns:
        True if valid UUID format, False otherwise.
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False
