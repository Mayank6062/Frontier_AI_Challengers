from __future__ import annotations


from backend.core.interfaces.storage_interface import StorageInterface
from .models import Review, ApprovalRecord, ApprovalDecision
from .approval_workflow import ApprovalWorkflow


class ReviewError(Exception):
    pass


class ReviewManager:
    """Manages review lifecycle. Persists reviews via injected StorageInterface."""

    def __init__(
        self,
        storage: StorageInterface,
        prefix: str = "rev:",
        workflow: ApprovalWorkflow | None = None,
    ) -> None:
        self._storage = storage
        self._prefix = prefix
        self._workflow = workflow or ApprovalWorkflow(required_approvals=1)

    def _key(self, review_id: str | None) -> str:
        if review_id is None:
            raise ValueError("review_id required")
        return f"{self._prefix}{review_id}"

    def create_review(self, target_engagement_id: str) -> Review:
        if not target_engagement_id:
            raise ReviewError("target_engagement_id required")
        r = Review(target_engagement_id=target_engagement_id)
        self._storage.put(self._key(r.id), r.to_dict())
        return r

    def get_review(self, review_id: str) -> Review:
        data = self._storage.get(self._key(review_id))
        if data is None:
            raise ReviewError("not found")
        return Review.from_dict(data)

    def add_approval(
        self,
        review_id: str,
        reviewer_id: str,
        decision: ApprovalDecision,
        reason: str | None = None,
    ) -> Review:
        r = self.get_review(review_id)
        if r.closed:
            raise ReviewError("review closed")
        rec = ApprovalRecord(reviewer_id=reviewer_id, decision=decision, reason=reason)
        approvals = []
        for a in r.approvals or []:
            if isinstance(a, dict):
                approvals.append(ApprovalRecord.from_dict(a))
            elif isinstance(a, ApprovalRecord):
                approvals.append(a)
            else:
                approvals.append(ApprovalRecord.from_dict(a))
        approvals.append(rec)
        r = Review.from_dict(
            {**r.to_dict(), "approvals": [a.to_dict() for a in approvals]}
        )
        # Evaluate workflow
        state = self._workflow.evaluate(approvals)
        if state in ("approved", "rejected"):
            r = Review.from_dict({**r.to_dict(), "closed": True})
        self._storage.put(self._key(r.id), r.to_dict())
        return r

    def evaluate(self, review_id: str) -> str:
        r = self.get_review(review_id)
        approvals: list[ApprovalRecord] = []
        for a in r.approvals or []:
            if isinstance(a, ApprovalRecord):
                approvals.append(a)
            else:
                approvals.append(ApprovalRecord.from_dict(a))
        return self._workflow.evaluate(approvals)
