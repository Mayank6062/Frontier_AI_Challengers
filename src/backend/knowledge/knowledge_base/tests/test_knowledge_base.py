from __future__ import annotations

from backend.knowledge.knowledge_base.knowledge_base import KnowledgeBase
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_knowledge_base_basic() -> None:
    kb = KnowledgeBase()
    e = EntryModel(id="x", text="find me")
    kb.add_entry(e)
    res = kb.get_entries_for_query("find")
    assert len(res) == 1
    assert res[0].id == "x"
