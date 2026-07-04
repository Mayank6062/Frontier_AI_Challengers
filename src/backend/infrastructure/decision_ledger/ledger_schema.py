"""Ledger record schema definitions.

Lightweight dataclass used by the Decision Ledger implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class LedgerRecord:
    engagement_id: str
    timestamp_iso: str
    payload: Dict[str, Any]


__all__ = ["LedgerRecord"]
