"""In-memory StorageService implementing StorageInterface.

Provides minimal CRUD and prefix query semantics for sessions/engagements.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from ...core.interfaces.storage_interface import StorageInterface


class StorageService(StorageInterface):
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def put(self, key: str, value: Dict[str, Any]) -> None:
        self._store[key] = value

    def query(self, prefix: str) -> Iterable[Dict[str, Any]]:
        for k, v in list(self._store.items()):
            if k.startswith(prefix):
                yield v

    def delete(self, key: str) -> None:
        self._store.pop(key, None)


__all__ = ["StorageService"]
