"""EngagementStore helper using StorageService via constructor injection.

Provides simple helpers for engagement records.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable

from backend.core.interfaces.storage_interface import StorageInterface


class EngagementStore:
    def __init__(self, storage: StorageInterface, prefix: str = "engagement:") -> None:
        self._storage = storage
        self._prefix = prefix

    def _key(self, engagement_id: str) -> str:
        return f"{self._prefix}{engagement_id}"

    def put_engagement(self, engagement_id: str, payload: Dict[str, Any]) -> None:
        self._storage.put(self._key(engagement_id), payload)

    def get_engagement(self, engagement_id: str) -> Dict[str, Any] | None:
        return self._storage.get(self._key(engagement_id))

    def list_engagements(self) -> Iterable[Dict[str, Any]]:
        return self._storage.query(self._prefix)


__all__ = ["EngagementStore"]
