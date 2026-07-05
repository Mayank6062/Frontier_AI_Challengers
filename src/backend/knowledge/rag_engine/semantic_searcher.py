from __future__ import annotations

from typing import Iterable, List

from ..knowledge_base.entry_model import EntryModel


class SemanticSearcher:
    """Abstract semantic searcher; here a very small, deterministic implementation.

    It accepts a list of entries and returns those that best match query tokens.
    """

    def __init__(self, entries: Iterable[EntryModel]) -> None:
        self._entries = list(entries)

    def search(self, query: str) -> List[EntryModel]:
        q = query.lower()
        matches: List[EntryModel] = []
        for e in self._entries:
            if q in e.text.lower():
                matches.append(e)
        return matches
