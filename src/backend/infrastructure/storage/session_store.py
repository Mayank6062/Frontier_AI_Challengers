"""SessionStore helper using StorageService via constructor injection.

Keeps session-specific helpers separate from the storage adapter.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .storage_service import StorageService


class SessionStore:
    def __init__(self, storage: StorageService, prefix: str = "session:") -> None:
        self._storage = storage
        self._prefix = prefix

    def _key(self, session_id: str) -> str:
        return f"{self._prefix}{session_id}"

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._storage.get(self._key(session_id))

    def put_session(self, session_id: str, payload: Dict[str, Any]) -> None:
        self._storage.put(self._key(session_id), payload)

    def delete_session(self, session_id: str) -> None:
        self._storage.delete(self._key(session_id))


__all__ = ["SessionStore"]
