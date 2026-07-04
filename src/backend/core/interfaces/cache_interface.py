"""
Cache Interface Contract.

Defines the normalized abstraction for all cache adapters. Application modules
that require caching never interact with a specific cache technology — they use
this interface. The cache is a performance layer; its absence degrades
performance but never corrupts correctness.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 7.6 (CacheProvider contract)

Implementors:
    src/backend/infrastructure/cache_service.py (Redis-compatible adapter)

Consumers:
    src/backend/core/session/ (session context caching)
    src/backend/core/workspace/ (workspace state caching)
    src/backend/knowledge/rag_engine/ (retrieval result caching)
    src/backend/infrastructure/llm_gateway/ (deterministic response caching)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CacheInterface(ABC):
    """
    Abstract contract for all cache adapters.

    Provides a minimal key-value cache API: get, set with TTL, delete, and
    prefix-based invalidation. The cache is a best-effort layer — a cache
    miss must always be recoverable from the authoritative source.

    Contract invariants:
        - get() returns None for a cache miss rather than raising.
        - set() with a TTL of 0 or negative must not store the value.
        - delete() is idempotent — deleting a non-existent key succeeds.
        - invalidate_prefix() removes ALL keys with the given prefix.
        - Cache failures must never propagate as application errors — the
          caller falls through to the primary source on any cache error.

    Raises:
        CacheConnectionError: When the cache backend is unavailable.
            Implementors must catch and convert lower-level errors.
    """

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """
        Retrieve a value from the cache by its key.

        Args:
            key: The cache key to retrieve.

        Returns:
            The cached value if found, None on cache miss or cache unavailability.
        """

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """
        Store a value in the cache with a time-to-live.

        Args:
            key: The cache key to store under.
            value: The value to cache. Must be serializable by the adapter.
            ttl_seconds: Seconds until the entry expires. A value of 0 or
                negative must not persist the entry.

        Raises:
            CacheConnectionError: On cache backend failure.
        """

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Remove a single entry from the cache.

        Idempotent: succeeds if the key does not exist.

        Args:
            key: The cache key to remove.
        """

    @abstractmethod
    async def invalidate_prefix(self, prefix: str) -> int:
        """
        Remove all cache entries whose key starts with the given prefix.

        Used to invalidate groups of related entries (e.g., all cached
        retrieval results for a given knowledge base segment after an update).

        Args:
            prefix: The key prefix to match for deletion.

        Returns:
            int: The number of entries removed.
        """

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Check whether a key exists in the cache without fetching its value.

        Args:
            key: The cache key to check.

        Returns:
            bool: True if the key exists and has not expired, False otherwise.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the cache backend is currently operational.

        Must not raise on connectivity failure — must return False instead.

        Returns:
            bool: True if the cache backend is reachable and operational.
        """
