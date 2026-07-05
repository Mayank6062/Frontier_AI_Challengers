from __future__ import annotations

from typing import List

from ..knowledge_base.entry_model import EntryModel
from .document_parser import simple_document_parser
from .chunk_splitter import simple_chunk_splitter
from .embedder import DummyEmbedder
from .approval_gate import ApprovalGate


class IngestionPipeline:
    """Pipeline that parses raw input into entries, splits into chunks, and
    embeds content. All dependencies are injected or local-testable.
    """

    def __init__(self, embedder: DummyEmbedder, approver: ApprovalGate) -> None:
        self._embedder = embedder
        self._approver = approver

    async def ingest(self, raw: str) -> List[EntryModel]:
        docs = simple_document_parser(raw)
        out: List[EntryModel] = []
        for i, d in enumerate(docs):
            if not self._approver.approve(d):
                continue
            chunks = simple_chunk_splitter(d)
            for j, c in enumerate(chunks):
                eid = f"doc-{i}-{j}"
                out.append(EntryModel(id=eid, text=c, metadata={"source_doc": i}))
                # embedding is async but not stored here; call for side-effect validation
                await self._embedder.embed(c)
        return out
