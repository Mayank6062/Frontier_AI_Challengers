from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheInterface(ABC):
    """Abstract contract for cache adapters used by the Application Core.

    Minimal operations required: get, set, delete. Implementations should
    support TTL where applicable.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def set(
        self, key: str, value: Any, ttl_seconds: Optional[int] = None
    ) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()
