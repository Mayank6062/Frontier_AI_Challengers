from __future__ import annotations

from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_entry_model_immutable() -> None:
    e = EntryModel(id="1", text="hello", metadata={"k": "v"})
    assert e.id == "1"
    # ensure frozen dataclass behavior
    try:
        e.id = "2"
        raised = False
    except Exception:
        raised = True
    assert raised
