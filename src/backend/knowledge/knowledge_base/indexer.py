from __future__ import annotations

from typing import Dict, Iterable, List

from ..knowledge_base.entry_model import EntryModel


class InMemoryIndexer:
    """Simple in-memory index for testing and local usage.

    Builds a mapping from token -> set of entry ids (very small-scale, naive tokenizer).
    """

    def __init__(self) -> None:
        self._index: Dict[str, List[str]] = {}
        self._entries: Dict[str, EntryModel] = {}

    def add(self, entry: EntryModel) -> None:
        self._entries[entry.id] = entry
        for token in self._tokenize(entry.text):
            self._index.setdefault(token, []).append(entry.id)

    def remove(self, entry_id: str) -> None:
        entry = self._entries.pop(entry_id, None)
        if not entry:
            return
        for token in self._tokenize(entry.text):
            ids = self._index.get(token)
            if ids:
                try:
                    ids.remove(entry_id)
                except ValueError:
                    pass

    def search(self, query: str) -> Iterable[EntryModel]:
        tokens = list(self._tokenize(query))
        if not tokens:
            return []
        # naive intersection by counting matches
        scores: Dict[str, int] = {}
        for t in tokens:
            for eid in self._index.get(t, []):
                scores[eid] = scores.get(eid, 0) + 1
        # order by score desc
        ordered = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        return [self._entries[eid] for eid, _ in ordered]

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [p.lower() for p in text.replace("/", " ").split() if p]
