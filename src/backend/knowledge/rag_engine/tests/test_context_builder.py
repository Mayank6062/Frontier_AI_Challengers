from __future__ import annotations

from backend.knowledge.rag_engine.context_builder import build_context
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_context_builder_truncation() -> None:
    entries = [EntryModel(id="1", text="x" * 10), EntryModel(id="2", text="y" * 2000)]
    ctx = build_context(entries, max_chars=50)
    assert len(ctx) <= 50
