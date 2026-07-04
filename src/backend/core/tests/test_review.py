from __future__ import annotations

from backend.core.review.review_manager import ReviewManager
from backend.core.review.approval_workflow import ApprovalWorkflow
from backend.core.review.models import ApprovalDecision
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


def test_review_flow() -> None:
    store = InMemoryStorage()
    mgr = ReviewManager(
        store, prefix="r:", workflow=ApprovalWorkflow(required_approvals=1)
    )
    r = mgr.create_review("eng1")
    assert r.target_engagement_id == "eng1"
    # pending
    assert r.id is not None
    assert mgr.evaluate(r.id) == "pending"
    # add approval
    r2 = mgr.add_approval(r.id, "rev1", ApprovalDecision.APPROVE)
    assert r2.closed is True
    assert mgr.evaluate(r.id) == "approved"


def test_review_reject() -> None:
    store = InMemoryStorage()
    mgr = ReviewManager(store)
    r = mgr.create_review("e2")
    assert r.id is not None
    r2 = mgr.add_approval(r.id, "rev", ApprovalDecision.REJECT)
    assert r2.closed is True
    assert mgr.evaluate(r.id) == "rejected"
