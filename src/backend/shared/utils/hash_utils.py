"""
Hash utilities for small stable hashing needs.
"""

from __future__ import annotations

import hashlib
from typing import Iterable


def stable_hash(*parts: Iterable[str]) -> str:
    """Return a stable hex digest for the provided string parts.

    Args:
        parts: sequences of string parts to include in hash.

    Returns:
        Lower-case hex digest string.
    """
    h = hashlib.sha256()
    for p in parts:
        if isinstance(p, (list, tuple)):
            for item in p:
                h.update(str(item).encode("utf-8"))
        else:
            h.update(str(p).encode("utf-8"))
    return h.hexdigest()
