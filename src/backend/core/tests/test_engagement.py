from __future__ import annotations

import pytest

from backend.core.engagement.engagement_repository import (
    EngagementRepository,
)
from backend.core.engagement.engagement_manager import (
    EngagementManager,
    ValidationError,
)
from backend.core.engagement.models import EngagementState
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


def test_create_and_get_engagement() -> None:
    store = InMemoryStorage()
    repo = EngagementRepository(store, prefix="e:")
    mgr = EngagementManager(repo)
    e = mgr.create("Title", "Desc")
    assert e.id is not None
    assert e.title == "Title"
    assert e.id is not None
    fetched = mgr.get(e.id)
    assert fetched.id == e.id


def test_invalid_title() -> None:
    store = InMemoryStorage()
    repo = EngagementRepository(store)
    mgr = EngagementManager(repo)
    with pytest.raises(ValidationError):
        mgr.create("  ")


def test_state_transitions() -> None:
    store = InMemoryStorage()
    repo = EngagementRepository(store)
    mgr = EngagementManager(repo)
    e = mgr.create("T")
    assert e.id is not None
    with pytest.raises(Exception):
        mgr.transition(e.id, EngagementState.PUBLISHED)
    # valid transition
    e2 = mgr.transition(e.id, EngagementState.DESIGN)
    assert e2.state == EngagementState.DESIGN
