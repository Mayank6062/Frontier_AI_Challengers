from __future__ import annotations

from typing import List

from ..knowledge_base.entry_model import EntryModel


def rank_by_length(entries: List[EntryModel]) -> List[EntryModel]:
    return sorted(entries, key=lambda e: len(e.text), reverse=True)
