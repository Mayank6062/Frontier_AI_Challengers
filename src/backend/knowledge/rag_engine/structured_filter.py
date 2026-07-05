from __future__ import annotations

from typing import Dict, Iterable, List, Any

from ..knowledge_base.entry_model import EntryModel


def apply_metadata_filter(
    entries: Iterable[EntryModel], filter_spec: Dict[str, Any]
) -> List[EntryModel]:
    out: List[EntryModel] = []
    for e in entries:
        ok = True
        for k, v in filter_spec.items():
            if e.metadata.get(k) != v:
                ok = False
                break
        if ok:
            out.append(e)
    return out
