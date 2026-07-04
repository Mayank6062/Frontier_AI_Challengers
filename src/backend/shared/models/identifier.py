"""
Identifier — Canonical UUID wrapper and validator.

Provides immutable, validated identifier wrapper for platform-wide use.
Responsibility: Generate and validate stable, globally unique identifiers.
"""

import uuid
from typing import Optional


class Identifier:
    """
    Immutable, validated identifier wrapper.

    Features:
    - Canonical UUID v4 generation.
    - String validation and conversion.
    - Immutable after construction.
    - Hashable for use in sets and dict keys.
    """

    __slots__ = ("_value",)

    def __init__(self, value: Optional[str] = None):
        """
        Construct an Identifier.

        Args:
            value: Optional UUID string. If None, generates a new UUID v4.

        Raises:
            ValueError: If value is not a valid UUID string.
        """
        if value is None:
            self._value = str(uuid.uuid4())
        else:
            # Validate UUID format
            try:
                uuid.UUID(value)
                self._value = str(value)
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid UUID: {value}") from e

    @property
    def value(self) -> str:
        """Get the identifier string value."""
        return self._value

    def __str__(self) -> str:
        """String representation is the UUID value."""
        return self._value

    def __repr__(self) -> str:
        """Representation."""
        return f"Identifier('{self._value}')"

    def __eq__(self, other: object) -> bool:
        """Equality by value."""
        if not isinstance(other, Identifier):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Hash by value for use in sets and dicts."""
        return hash(self._value)

    def __lt__(self, other: "Identifier") -> bool:
        """Lexicographic comparison."""
        if not isinstance(other, Identifier):
            return NotImplemented
        return self._value < other._value
