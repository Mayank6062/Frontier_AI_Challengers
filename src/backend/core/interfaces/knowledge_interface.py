"""
Knowledge Layer Interface Contract.

Defines the abstraction for the enterprise knowledge base service consumed
by the Agent Layer (Knowledge Retrieval Agent) and the knowledge management
operations consumed by curators. Agents never access the knowledge base
implementation directly — they consume this interface.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.9 (knowledge_base module)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.10 (rag_engine module)
    BACKEND_MODULE_ARCHITECTURE.md Section 5 (KnowledgeService)
    SYSTEM_ARCHITECTURE.md Section 4.9 (Knowledge Base and RAG Engine)

Implementors:
    src/backend/knowledge/knowledge_base/ (knowledge entry management)
    src/backend/knowledge/rag_engine/ (retrieval query execution)

Consumers:
    src/backend/agents/discovery/knowledge_retrieval/ (primary consumer)
    src/backend/agents/validation/compliance/ (regulatory framework queries)
    src/backend/core/ (curator management operations)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Knowledge models (interface-local DTOs)
# ---------------------------------------------------------------------------


class KnowledgeEntryState(str, Enum):
    """
    Lifecycle state of a knowledge base entry.

    Entries must pass through PENDING_APPROVAL before becoming APPROVED
    and retrievable. DEPRECATED entries are retained for audit but excluded
    from retrieval results.
    """

    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    REJECTED = "rejected"


class KnowledgeEntryType(str, Enum):
    """
    Classification of knowledge entry content type.

    Used for structured filtering in retrieval queries.
    """

    ARCHITECTURE_PATTERN = "architecture_pattern"
    TECHNOLOGY_EVALUATION = "technology_evaluation"
    APPROVED_PRECEDENT = "approved_precedent"
    REGULATORY_FRAMEWORK = "regulatory_framework"
    SECURITY_CONTROL = "security_control"
    COST_MODEL = "cost_model"
    DOMAIN_KNOWLEDGE = "domain_knowledge"
    TECHNOLOGY_CATALOG = "technology_catalog"


@dataclass(frozen=True)
class KnowledgeCitation:
    """
    A traceable citation attached to a retrieved knowledge item.

    Every recommendation produced by an agent must be traceable to a
    KnowledgeCitation. The AgentValidator rejects outputs without citations.

    Attributes:
        entry_id: The knowledge entry this citation refers to.
        entry_title: Human-readable title of the knowledge entry.
        entry_type: The knowledge entry type classification.
        relevance_score: Similarity score from the retrieval query (0.0–1.0).
        retrieval_query: The query that produced this citation (for traceability).
        source_reference: External source reference (standard, document, URL).
    """

    entry_id: str
    entry_title: str
    entry_type: KnowledgeEntryType
    relevance_score: float
    retrieval_query: str
    source_reference: str = ""


@dataclass(frozen=True)
class KnowledgeRetrievalQuery:
    """
    Structured retrieval query specification from the Knowledge Retrieval Agent.

    Defines what to retrieve and how. The RAG Engine selects the appropriate
    retrieval strategy based on this specification.

    Attributes:
        query_text: The primary semantic search text.
        engagement_domain: The domain context for structured filtering
            (e.g., "financial_services", "healthcare", "manufacturing").
        entry_types: Knowledge entry types to include in results. Empty
            means include all approved types.
        max_results: Maximum number of items to return. Bounded by agent
            configuration to respect context window budgets.
        min_relevance_score: Minimum similarity score threshold. Items below
            this threshold are excluded regardless of ranking.
        require_citation: Whether each result must include a source reference.
        engagement_id: The requesting engagement's ID for context.
        filters: Additional structured metadata filters.
    """

    query_text: str
    engagement_domain: str
    entry_types: list[KnowledgeEntryType] = field(default_factory=list)
    max_results: int = 10
    min_relevance_score: float = 0.5
    require_citation: bool = True
    engagement_id: str = ""
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeRetrievalResult:
    """
    The assembled context package returned from a retrieval query.

    Attributes:
        items: The retrieved knowledge items with their content.
        citations: Citation records for each retrieved item.
        total_candidates: Total candidates evaluated before filtering.
        retrieval_strategy: The strategy used for this query.
        retrieval_latency_ms: Time to execute the retrieval query.
        query_hash: SHA-256 hash of the query for cache keying.
    """

    items: list[dict[str, Any]]
    citations: list[KnowledgeCitation]
    total_candidates: int
    retrieval_strategy: str
    retrieval_latency_ms: float
    query_hash: str


@dataclass(frozen=True)
class KnowledgeEntry:
    """
    A knowledge base entry with its full metadata.

    Attributes:
        entry_id: Globally unique entry identifier.
        title: Human-readable entry title.
        content: The knowledge entry content text.
        entry_type: Classification of this entry's knowledge type.
        domain: The business domain this entry applies to.
        state: The lifecycle state of this entry.
        submitted_by: User ID of the submitter.
        approved_by: User ID of the curator who approved this entry.
        embedding_id: Reference to the stored embedding vector.
        source_reference: External source (standard, document, URL).
        created_at_utc: ISO 8601 UTC creation timestamp.
        approved_at_utc: ISO 8601 UTC approval timestamp.
        tags: Categorical tags for structured filtering.
        metadata: Additional structured metadata.
    """

    entry_id: str
    title: str
    content: str
    entry_type: KnowledgeEntryType
    domain: str
    state: KnowledgeEntryState
    submitted_by: str
    approved_by: str
    embedding_id: str
    source_reference: str
    created_at_utc: str
    approved_at_utc: str
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class KnowledgeInterface(ABC):
    """
    Abstract contract for the enterprise knowledge base service.

    Exposes two capability surfaces: retrieval (consumed by agents) and
    management (consumed by curators and the ingestion pipeline). Both
    surfaces are accessible through this single interface.

    Contract invariants:
        - query() returns only APPROVED entries.
        - query() attaches citations to every returned item.
        - submit_entry() places entries in PENDING_APPROVAL state.
        - approve_entry() transitions entries to APPROVED.
        - get_entry() returns None for non-existent entry_id.
        - deprecate_entry() is the only permitted terminal operation —
          entries are never deleted.

    Raises:
        KnowledgeQueryError: On retrieval execution failure.
        KnowledgeEntryNotFoundError: When a requested entry does not exist.
        KnowledgeWriteError: On entry write failure.
        KnowledgeConnectionError: When the knowledge backend is unavailable.
    """

    @abstractmethod
    async def query(
        self, retrieval_query: KnowledgeRetrievalQuery
    ) -> KnowledgeRetrievalResult:
        """
        Execute a retrieval query against the knowledge base.

        Returns only APPROVED entries. The RAG Engine selects the optimal
        retrieval strategy based on the query specification.

        Args:
            retrieval_query: The structured query specification from the
                Knowledge Retrieval Agent.

        Returns:
            KnowledgeRetrievalResult: Ranked context package with citations.

        Raises:
            KnowledgeQueryError: On query execution failure.
        """

    @abstractmethod
    async def get_entry(self, entry_id: str) -> KnowledgeEntry | None:
        """
        Retrieve a single knowledge entry by its identifier.

        Returns entries regardless of their lifecycle state (used for
        management operations and audit queries).

        Args:
            entry_id: The unique knowledge entry identifier.

        Returns:
            KnowledgeEntry: The entry if found, None if not found.

        Raises:
            KnowledgeReadError: On storage backend failure.
        """

    @abstractmethod
    async def submit_entry(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        """
        Submit a new knowledge entry for curator approval.

        Places the entry in PENDING_APPROVAL state. The entry is not
        retrievable until a curator approves it.

        Args:
            entry: The knowledge entry to submit. Must not include entry_id
                (assigned by the implementation).

        Returns:
            KnowledgeEntry: The submitted entry with its assigned entry_id.

        Raises:
            KnowledgeWriteError: On storage write failure.
        """

    @abstractmethod
    async def approve_entry(
        self, entry_id: str, curator_id: str
    ) -> KnowledgeEntry:
        """
        Approve a pending knowledge entry for inclusion in retrieval results.

        Transitions the entry from PENDING_APPROVAL to APPROVED.
        Triggers embedding generation and vector index upsert.

        Args:
            entry_id: The entry to approve.
            curator_id: The user ID of the approving curator.

        Returns:
            KnowledgeEntry: The approved entry.

        Raises:
            KnowledgeEntryNotFoundError: If the entry does not exist.
            KnowledgeWriteError: On storage write failure.
        """

    @abstractmethod
    async def deprecate_entry(
        self, entry_id: str, reason: str
    ) -> KnowledgeEntry:
        """
        Deprecate a knowledge entry, excluding it from future retrieval.

        The entry is retained for audit purposes. This is the only terminal
        operation permitted — entries are never deleted.

        Args:
            entry_id: The entry to deprecate.
            reason: Human-readable reason for deprecation (required).

        Returns:
            KnowledgeEntry: The deprecated entry.

        Raises:
            KnowledgeEntryNotFoundError: If the entry does not exist.
            KnowledgeWriteError: On storage write failure.
        """

    @abstractmethod
    async def list_pending_approval(
        self, offset: int = 0, limit: int = 50
    ) -> list[KnowledgeEntry]:
        """
        List knowledge entries awaiting curator approval.

        Args:
            offset: Number of entries to skip (for pagination).
            limit: Maximum number of entries to return.

        Returns:
            list[KnowledgeEntry]: Pending entries ordered by submission time.

        Raises:
            KnowledgeReadError: On storage backend failure.
        """

    @abstractmethod
    async def record_retrieval_usage(
        self, entry_id: str, engagement_id: str
    ) -> None:
        """
        Record that a knowledge entry was retrieved for a given engagement.

        Used for usage metrics and knowledge base quality management.

        Args:
            entry_id: The retrieved entry.
            engagement_id: The engagement that triggered the retrieval.
        """
