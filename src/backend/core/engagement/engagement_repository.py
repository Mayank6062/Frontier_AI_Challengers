from __future__ import annotations

from typing import Iterable, Optional

from backend.core.interfaces.storage_interface import StorageInterface
from .models import Engagement


class EngagementNotFoundError(Exception):
    pass


class EngagementRepository:
    """Repository abstraction for persisting Engagement domain objects.

    Uses constructor injection for the storage adapter implementing
    `StorageInterface`.
    """

    def __init__(self, storage: StorageInterface, prefix: str = "eng:") -> None:
        self._storage = storage
        self._prefix = prefix

    def _key(self, engagement_id: Optional[str]) -> str:
        if engagement_id is None:
            raise ValueError("engagement_id required")
        return f"{self._prefix}{engagement_id}"

    def save(self, engagement: Engagement) -> None:
        data = engagement.to_dict()
        self._storage.put(self._key(engagement.id), data)

    def get(self, engagement_id: str) -> Engagement:
        data = self._storage.get(self._key(engagement_id))
        if data is None:
            raise EngagementNotFoundError(engagement_id)
        return Engagement.from_dict(data)

    def list(self) -> Iterable[Engagement]:
        for obj in self._storage.query(self._prefix):
            yield Engagement.from_dict(obj)

    def delete(self, engagement_id: str) -> None:
        self._storage.delete(self._key(engagement_id))
