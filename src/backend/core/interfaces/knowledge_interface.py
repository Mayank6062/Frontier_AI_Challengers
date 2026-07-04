from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .types import Citation, UUIDStr


@dataclass(frozen=True)
class RetrievedItem:
    entry_id: UUIDStr
    entry_type: str
    title: str
    excerpt: str
    relevance: float


@dataclass(frozen=True)
class RetrievedContext:
    query: str
    items: List[RetrievedItem]
    citations: List[Citation]
    average_relevance: Optional[float] = None


class KnowledgeInterface(ABC):
    """Contract for the Knowledge Layer retrieval service.

    Implementations provide retrieval, filtering, and metadata for RAG operations.
    """

    @abstractmethod
    def retrieve(
        self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> RetrievedContext:  # pragma: no cover - interface only
        """Run a retrieval query and return a normalized RetrievedContext."""

        raise NotImplementedError()
