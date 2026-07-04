from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable


class LedgerInterface(ABC):
    """Contract for the Decision Ledger append-only storage adapter.

    Implementations must provide an append operation and read/query operations
    scoped by engagement or time range.
    """

    @abstractmethod
    def append(
        self, record: Dict[str, Any]
    ) -> None:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def read_by_engagement(
        self, engagement_id: str
    ) -> Iterable[Dict[str, Any]]:  # pragma: no cover - interface only
        raise NotImplementedError()

    @abstractmethod
    def query(
        self, *, start_time_iso: str = "", end_time_iso: str = ""
    ) -> Iterable[Dict[str, Any]]:  # pragma: no cover - interface only
        raise NotImplementedError()
