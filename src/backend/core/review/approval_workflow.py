from __future__ import annotations

from typing import List

from .models import ApprovalDecision, ApprovalRecord


class ApprovalError(Exception):
    pass


class ApprovalWorkflow:
    """Simple approval workflow that requires a minimum number of approvals.

    The workflow is stateless; it evaluates a set of approval records and
    determines whether the review is approved or rejected.
    """

    def __init__(self, required_approvals: int = 1) -> None:
        if required_approvals < 1:
            raise ValueError("required_approvals must be >= 1")
        self.required_approvals = required_approvals

    def evaluate(self, approvals: List[ApprovalRecord]) -> str:
        approves = [a for a in approvals if a.decision == ApprovalDecision.APPROVE]
        rejects = [a for a in approvals if a.decision == ApprovalDecision.REJECT]
        if len(rejects) > 0:
            return "rejected"
        if len(approves) >= self.required_approvals:
            return "approved"
        return "pending"
