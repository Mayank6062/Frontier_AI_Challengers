"""
Timestamps utilities for consistent UTC handling.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Final


ISO_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S.%fZ"


def now_iso() -> str:
    """Return the current UTC time formatted as an ISO-8601 string with Zulu suffix.

    Returns:
        str: ISO formatted UTC timestamp.
    """
    return datetime.now(timezone.utc).strftime(ISO_FORMAT)


def parse_iso(timestamp: str) -> datetime:
    """Parse an ISO-8601 Zulu timestamp produced by :func:`now_iso`.

    Args:
        timestamp: ISO formatted timestamp.

    Returns:
        datetime: timezone-aware UTC datetime.
    """
    # Support inputs with or without fractional seconds
    try:
        dt = datetime.strptime(timestamp, ISO_FORMAT)
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        # Try a more forgiving parse
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)
