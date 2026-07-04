from __future__ import annotations

from typing import Iterable

from backend.core.interfaces.storage_interface import StorageInterface
from .models import Session


class SessionNotFoundError(Exception):
    pass


class SessionRepository:
    def __init__(self, storage: StorageInterface, prefix: str = "sess:") -> None:
        self._storage = storage
        self._prefix = prefix

    def _key(self, session_id: str | None) -> str:
        if session_id is None:
            raise ValueError("session_id required")
        return f"{self._prefix}{session_id}"

    def save(self, session: Session) -> None:
        self._storage.put(self._key(session.id), session.to_dict())

    def get(self, session_id: str) -> Session:
        data = self._storage.get(self._key(session_id))
        if data is None:
            raise SessionNotFoundError(session_id)
        return Session.from_dict(data)

    def delete(self, session_id: str) -> None:
        self._storage.delete(self._key(session_id))

    def list_by_user(self, user_id: str) -> Iterable[Session]:
        for obj in self._storage.query(self._prefix):
            s = Session.from_dict(obj)
            if s.user_id == user_id:
                yield s
