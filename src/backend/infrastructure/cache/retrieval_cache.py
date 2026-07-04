"""Retrieval cache helper for read-through caching using a CacheService.

Simple helper that delegates to a provided `CacheService` via constructor
injection.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from .cache_service import CacheService


class RetrievalCache:
    def __init__(self, cache: CacheService) -> None:
        self._cache = cache

    def get_or_set(
        self, key: str, loader: Callable[[], Any], ttl_seconds: Optional[int] = None
    ) -> Any:
        value = self._cache.get(key)
        if value is not None:
            return value
        value = loader()
        self._cache.set(key, value, ttl_seconds=ttl_seconds)
        return value


__all__ = ["RetrievalCache"]
