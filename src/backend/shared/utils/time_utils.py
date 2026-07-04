"""
Time Utils — Timestamp parsing and formatting helpers.

Provides side-effect-free timestamp manipulation utilities.
Responsibility: Offer canonical timestamp operations without IO.
"""

from datetime import datetime, timezone
from typing import Optional


def parse_iso_timestamp(iso_string: str) -> datetime:
    """
    Parse ISO 8601 timestamp string to UTC datetime.

    Args:
        iso_string: ISO 8601 formatted timestamp string.

    Returns:
        UTC datetime object.

    Raises:
        ValueError: If string is not valid ISO 8601.
    """
    if not isinstance(iso_string, str):
        raise TypeError("iso_string must be a string")

    try:
        dt = datetime.fromisoformat(iso_string)
        # Convert to UTC if timezone-aware
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid ISO timestamp: {iso_string}") from e


def format_iso_timestamp(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string.

    Args:
        dt: Datetime object (must be UTC or timezone-aware).

    Returns:
        ISO 8601 formatted string.

    Raises:
        ValueError: If datetime is naive (not timezone-aware).
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime object")

    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.isoformat()


def current_utc_timestamp() -> datetime:
    """
    Get current UTC timestamp.

    Returns:
        Current UTC datetime object.
    """
    return datetime.now(timezone.utc)


def current_iso_timestamp() -> str:
    """
    Get current UTC timestamp as ISO 8601 string.

    Returns:
        ISO 8601 formatted current timestamp.
    """
    return format_iso_timestamp(current_utc_timestamp())


def parse_unix_timestamp(unix_ts: float) -> datetime:
    """
    Convert Unix timestamp (seconds since epoch) to UTC datetime.

    Args:
        unix_ts: Unix timestamp as float.

    Returns:
        UTC datetime object.

    Raises:
        (OSError, OverflowError, ValueError): If timestamp is invalid.
    """
    try:
        return datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    except (OSError, OverflowError, ValueError) as e:
        raise ValueError(f"Invalid Unix timestamp: {unix_ts}") from e


def to_unix_timestamp(dt: datetime) -> float:
    """
    Convert UTC datetime to Unix timestamp.

    Args:
        dt: Datetime object (must be UTC or timezone-aware).

    Returns:
        Unix timestamp as float.

    Raises:
        ValueError: If datetime is naive.
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime object")

    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.timestamp()
