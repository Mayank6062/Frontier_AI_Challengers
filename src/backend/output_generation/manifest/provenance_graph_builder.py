"""Provenance graph builder to represent provenance relationships."""

from __future__ import annotations

from typing import Dict, Any
from .schemas import BundleProvenance


def build_provenance_graph(prov: BundleProvenance) -> Dict[str, Any]:
    # Simple canonical provenance graph representation
    return {
        "approved_by": prov.approved_by,
        "approved_at": prov.approved_at.isoformat(),
        "approval_ledger_hash": prov.approval_ledger_hash,
        "snapshot_version": prov.snapshot_version,
        "trace_id": prov.trace_id,
    }


__all__ = ["build_provenance_graph"]
