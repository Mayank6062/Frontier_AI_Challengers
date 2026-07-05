from __future__ import annotations

from backend.knowledge.rag_engine.rag_engine import RAGEngine
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_rag_engine_composition() -> None:
    entries = [
        EntryModel(id="1", text="hello world", metadata={"cat": "a"}),
        EntryModel(id="2", text="hello", metadata={"cat": "b"}),
    ]
    engine = RAGEngine(entries)
    out = engine.query("hello", filter_spec={"cat": "a"}, top_k=1)
    assert out["count"] == 1
