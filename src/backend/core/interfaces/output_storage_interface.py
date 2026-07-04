from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional


class OutputStorageInterface(ABC):
    """Contract for artifact and output storage adapters.

    Stores generated artifacts (reports, diagrams, packaged outputs) and
    provides read/list/delete capabilities. Implementations handle durability
    and access control.
    """

    @abstractmethod
    def store_artifact(
        self, key: str, data: bytes, metadata: Optional[dict[str, Any]] = None
    ) -> str:  # pragma: no cover - interface only
        """Store artifact bytes and return an artifact identifier or URI."""

        raise NotImplementedError()

    @abstractmethod
    def get_artifact(
        self, key: str
    ) -> Optional[bytes]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def list_artifacts(
        self, prefix: str = ""
    ) -> Iterable[str]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def delete_artifact(self, key: str) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()
