"""
Timestamp — UTC timestamp canonicalizer and serializer.

Provides immutable, UTC-only timestamp wrapper with canonical formatting.
Responsibility: Ensure all timestamps across the platform are in UTC with consistent serialization.
"""

from datetime import datetime, timezone
from typing import Optional


class Timestamp:
    """
    Immutable UTC timestamp wrapper with canonical formatting.

    Features:
    - UTC-only (raises error for naive or non-UTC datetimes).
    - ISO 8601 serialization.
    - Comparison and hashing support.
    - Immutable after construction.
    """

    __slots__ = ("_value",)

    def __init__(self, value: Optional[datetime] = None):
        """
        Construct a Timestamp.

        Args:
            value: Optional datetime object (must be UTC). If None, uses current UTC time.

        Raises:
            ValueError: If datetime is naive or not in UTC.
        """
        if value is None:
            self._value = datetime.now(timezone.utc)
        else:
            # Validate UTC
            if value.tzinfo is None:
                raise ValueError("Timestamp requires timezone-aware (UTC) datetime")
            if value.tzinfo != timezone.utc:
                raise ValueError("Timestamp must be in UTC timezone")
            self._value = value

    @property
    def value(self) -> datetime:
        """Get the underlying datetime object."""
        return self._value

    def iso_format(self) -> str:
        """
        Get ISO 8601 formatted string.

        Returns:
            ISO 8601 formatted timestamp string (e.g., '2026-07-04T12:34:56.123456+00:00').
        """
        return self._value.isoformat()

    def unix_timestamp(self) -> float:
        """
        Get Unix timestamp (seconds since epoch).

        Returns:
            Unix timestamp as float.
        """
        return self._value.timestamp()

    @classmethod
    def from_iso_format(cls, iso_string: str) -> "Timestamp":
        """
        Construct from ISO 8601 string.

        Args:
            iso_string: ISO 8601 formatted timestamp string.

        Returns:
            Timestamp instance.

        Raises:
            ValueError: If string is not valid ISO 8601 or not in UTC.
        """
        try:
            dt = datetime.fromisoformat(iso_string)
            return cls(dt)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid ISO format: {iso_string}") from e

    def __str__(self) -> str:
        """String representation is ISO format."""
        return self.iso_format()

    def __repr__(self) -> str:
        """Representation."""
        return f"Timestamp('{self.iso_format()}')"

    def __eq__(self, other: object) -> bool:
        """Equality by value."""
        if not isinstance(other, Timestamp):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Hash by value."""
        return hash(self._value)

    def __lt__(self, other: "Timestamp") -> bool:
        """Chronological comparison."""
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self._value < other._value

    def __le__(self, other: "Timestamp") -> bool:
        """Chronological comparison."""
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self._value <= other._value

    def __gt__(self, other: "Timestamp") -> bool:
        """Chronological comparison."""
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self._value > other._value

    def __ge__(self, other: "Timestamp") -> bool:
        """Chronological comparison."""
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self._value >= other._value
