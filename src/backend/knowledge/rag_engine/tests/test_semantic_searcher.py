from __future__ import annotations

from backend.knowledge.rag_engine.semantic_searcher import SemanticSearcher
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_semantic_searcher_matches() -> None:
    entries = [
        EntryModel(id="1", text="Find me now"),
        EntryModel(id="2", text="Other text"),
    ]
    s = SemanticSearcher(entries)
    res = s.search("find")
    assert len(res) == 1
