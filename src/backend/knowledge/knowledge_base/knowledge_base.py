from __future__ import annotations

from typing import Iterable, List, Optional

from .entry_model import EntryModel
from .indexer import InMemoryIndexer


class KnowledgeBase:
    """Abstraction over a collection of knowledge entries with index management.

    Constructor injection allows custom index implementations for testing.
    """

    def __init__(self, indexer: Optional[InMemoryIndexer] = None) -> None:
        self._indexer = indexer or InMemoryIndexer()

    def add_entry(self, entry: EntryModel) -> None:
        self._indexer.add(entry)

    def remove_entry(self, entry_id: str) -> None:
        self._indexer.remove(entry_id)

    def get_entries_for_query(self, query: str) -> List[EntryModel]:
        return list(self._indexer.search(query))

    def list_all(self) -> Iterable[EntryModel]:
        # expose entries from indexer via safe getattr to satisfy type checkers
        entries = getattr(self._indexer, "_entries", {})
        return list(entries.values())
