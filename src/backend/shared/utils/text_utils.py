"""
Text-related utilities used across backend modules.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_whitespace(s: str) -> str:
    """Normalize all whitespace sequences into single spaces and strip ends."""
    return _WHITESPACE_RE.sub(" ", s).strip()


def safe_truncate(s: str, max_len: int) -> str:
    """Truncate string to `max_len` preserving whole words when possible."""
    if len(s) <= max_len:
        return s
    truncated = s[:max_len].rsplit(" ", 1)[0]
    return truncated or s[:max_len]


def to_json(obj: Dict[str, Any]) -> str:
    """Stable JSON serialization used by tests and logging.

    This provides deterministic key ordering for stable snapshots.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def from_json(s: str) -> Dict[str, Any]:
    """Parse stable-serialized JSON into a dictionary.

    Raises ValueError when the decoded object is not a mapping.
    """
    obj = json.loads(s)
    if not isinstance(obj, dict):
        raise ValueError("JSON did not decode to an object")
    return obj
