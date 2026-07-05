from __future__ import annotations

from typing import Callable


class ApprovalGate:
    """Human approval gate abstraction. Caller supplies an approver callable.

    The approver is a callable taking a document string and returning bool.
    """

    def __init__(self, approver: Callable[[str], bool]) -> None:
        self._approver = approver

    def approve(self, document: str) -> bool:
        return bool(self._approver(document))
