from __future__ import annotations

from typing import Iterable, Dict, Any

from ..knowledge_base.entry_model import EntryModel
from .semantic_searcher import SemanticSearcher
from .structured_filter import apply_metadata_filter
from .result_ranker import rank_by_length
from .context_builder import build_context


class RAGEngine:
    """Retrieve-and-Generate engine orchestration at an algorithmic level.

    This implementation is decoupled from LLMs and simply composes search,
    filtering, ranking and context building for unit testing.
    """

    def __init__(self, entries: Iterable[EntryModel]):
        self._entries = list(entries)

    def query(
        self, query_text: str, filter_spec: Dict[str, Any] | None = None, top_k: int = 5
    ) -> Dict[str, Any]:
        searcher = SemanticSearcher(self._entries)
        results = searcher.search(query_text)
        if filter_spec:
            results = apply_metadata_filter(results, filter_spec)
        ranked = rank_by_length(results)[:top_k]
        context = build_context(ranked)
        return {"count": len(ranked), "context": context, "ids": [e.id for e in ranked]}
