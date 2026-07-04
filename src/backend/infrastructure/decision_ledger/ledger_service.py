"""Simple in-memory LedgerService implementing LedgerInterface.

Constructor-injected and append-only semantics; intended for local testing.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ...core.interfaces.ledger_interface import LedgerInterface


class LedgerService(LedgerInterface):
    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []

    def append(self, record: Dict[str, Any]) -> None:
        # Append-only
        self._records.append(record)

    def read_by_engagement(self, engagement_id: str) -> Iterable[Dict[str, Any]]:
        for r in self._records:
            if r.get("engagement_id") == engagement_id:
                yield r

    def query(
        self, *, start_time_iso: str = "", end_time_iso: str = ""
    ) -> Iterable[Dict[str, Any]]:
        # Minimal implementation: return all records. Time filtering is intentionally omitted.
        for r in self._records:
            yield r


__all__ = ["LedgerService"]
