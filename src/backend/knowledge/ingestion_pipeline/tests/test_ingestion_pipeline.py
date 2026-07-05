from __future__ import annotations

import asyncio

from backend.knowledge.ingestion_pipeline.ingestion_pipeline import IngestionPipeline
from backend.knowledge.ingestion_pipeline.embedder import DummyEmbedder
from backend.knowledge.ingestion_pipeline.approval_gate import ApprovalGate
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_pipeline_ingests() -> None:
    async def runner() -> list[EntryModel]:
        approver = ApprovalGate(lambda d: True)
        p = IngestionPipeline(DummyEmbedder(), approver)
        out = await p.ingest("doc1---doc2")
        return out

    results = asyncio.get_event_loop().run_until_complete(runner())
    assert len(results) >= 1
