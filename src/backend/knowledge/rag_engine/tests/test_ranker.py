from __future__ import annotations

from backend.knowledge.rag_engine.result_ranker import rank_by_length
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_ranker_orders() -> None:
    docs = [
        EntryModel(id="1", text="short"),
        EntryModel(id="2", text="a much longer content"),
    ]
    ranked = rank_by_length(docs)
    assert ranked[0].id == "2"
