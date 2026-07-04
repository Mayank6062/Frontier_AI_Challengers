from __future__ import annotations

import pytest
from time import sleep

from backend.core.session.session_repository import (
    SessionRepository,
    SessionNotFoundError,
)
from backend.core.session.session_manager import SessionManager, SessionValidationError
from backend.core.interfaces.storage_interface import StorageInterface


class InMemoryStorage(StorageInterface):
    def __init__(self) -> None:
        self._data: dict[str, dict[str, object]] = {}

    def get(self, key: str) -> dict[str, object] | None:
        return self._data.get(key)

    def put(self, key: str, value: dict[str, object]) -> None:
        self._data[key] = value

    def query(self, prefix: str) -> list[dict[str, object]]:
        return [v for k, v in self._data.items() if k.startswith(prefix)]

    def delete(self, key: str) -> None:
        self._data.pop(key, None)


def test_session_lifecycle() -> None:
    store = InMemoryStorage()
    repo = SessionRepository(store)
    mgr = SessionManager(repo, default_ttl_seconds=1)
    s = mgr.create_session("user1")
    assert s.user_id == "user1"
    assert s.id is not None
    got = mgr.get_session(s.id)
    assert got.id == s.id
    # expire
    sleep(1.1)
    with pytest.raises(SessionValidationError):
        mgr.get_session(s.id)


def test_touch_and_invalidate() -> None:
    store = InMemoryStorage()
    repo = SessionRepository(store)
    mgr = SessionManager(repo, default_ttl_seconds=60)
    s = mgr.create_session("u2")
    assert s.id is not None
    t = mgr.touch_session(s.id, ttl_seconds=60)
    assert t.last_accessed is not None
    mgr.invalidate(s.id)
    with pytest.raises(SessionNotFoundError):
        assert s.id is not None
        repo.get(s.id)
