"""In-memory CacheService implementing CacheInterface.

Constructor-injected and TTL-aware (basic) implementation for testing.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

from ...core.interfaces.cache_interface import CacheInterface


class CacheService(CacheInterface):
    def __init__(self) -> None:
        # key -> (value, expiry_ts_or_None)
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if item is None:
            return None
        value, expiry = item
        if expiry is not None and time.time() > expiry:
            # expired
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        expiry = None if ttl_seconds is None else (time.time() + ttl_seconds)
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)


__all__ = ["CacheService"]
