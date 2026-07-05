from __future__ import annotations

from backend.knowledge.knowledge_base.indexer import InMemoryIndexer
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_indexer_add_search_remove() -> None:
    idx = InMemoryIndexer()
    e1 = EntryModel(id="a", text="alpha beta")
    e2 = EntryModel(id="b", text="beta gamma")
    idx.add(e1)
    idx.add(e2)
    results = list(idx.search("beta"))
    assert len(results) == 2
    idx.remove("a")
    results2 = list(idx.search("alpha"))
    assert len(results2) == 0
