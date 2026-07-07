from __future__ import annotations

from typing import Dict, List, Optional, Protocol
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class SearchEntry(BaseModel):
    entry_id: UUID = Field(default_factory=uuid4)
    title: str
    snippet: Optional[str] = None
    path: str
    section_id: Optional[str] = None
    payload: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class SearchResult(BaseModel):
    entry: SearchEntry
    score: float

    model_config = {"extra": "forbid", "frozen": True}


class SearchIndex(BaseModel):
    index_id: UUID = Field(default_factory=uuid4)
    entries: List[SearchEntry] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class SearchEngine(Protocol):
    def index(self, index: SearchIndex) -> None:
        """Load an index into the search engine."""

    def query(self, q: str, top_k: int = 10) -> List[SearchResult]:
        """Query the index and return top-k results."""

    def add_entry(self, entry: SearchEntry) -> None:
        """Add a single entry to the index."""
