from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Optional


class StorageInterface(ABC):
    """Abstract contract for persistent storage adapters used by the Application Core.

    This interface declares the minimal set of operations required by the core
    services (sessions, engagements, and reference data). Implementations may
    expose richer APIs but must at least satisfy these methods.
    """

    @abstractmethod
    def get(
        self, key: str
    ) -> Optional[Dict[str, Any]]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def put(
        self, key: str, value: Dict[str, Any]
    ) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def query(
        self, prefix: str
    ) -> Iterable[Dict[str, Any]]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()
