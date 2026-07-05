from __future__ import annotations

from typing import Iterable, List

from ..knowledge_base.entry_model import EntryModel


def build_context(entries: Iterable[EntryModel], max_chars: int = 1000) -> str:
    parts: List[str] = []
    total = 0
    for e in entries:
        if total + len(e.text) > max_chars:
            break
        parts.append(e.text)
        total += len(e.text)
    return "\n\n".join(parts)
