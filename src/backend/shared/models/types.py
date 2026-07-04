from __future__ import annotations

from dataclasses import dataclass

# Simple alias for UUID strings used across the application
UUIDStr = str


@dataclass(frozen=True)
class Citation:
    citation_id: UUIDStr
    knowledge_entry_id: UUIDStr
    knowledge_entry_type: str
    relevance_score: float
    cited_claim: str
    source_title: str
    source_excerpt: str


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
