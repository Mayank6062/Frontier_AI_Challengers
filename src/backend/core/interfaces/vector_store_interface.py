"""
Vector Store Interface Contract.

Defines the abstraction for all vector index operations. The Knowledge Layer
stores and retrieves embedding vectors through this interface. No knowledge
module has a direct dependency on a specific vector database technology.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 7.4 (VectorStoreProvider contract)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.9 (knowledge_base module dependencies)
    SYSTEM_ARCHITECTURE.md Section 4.9 (Knowledge Base and RAG Engine)

Implementors:
    src/backend/infrastructure/vector_store_service.py
    (pgvector, Weaviate, Qdrant adapters)

Consumers:
    src/backend/knowledge/knowledge_base/ (embedding storage and retrieval)
    src/backend/knowledge/rag_engine/ (semantic similarity queries)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Vector store models (interface-local DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VectorRecord:
    """
    A vector embedding record for storage or update.

    Attributes:
        record_id: The unique identifier for this vector record.
            Must match the corresponding storage record's key for
            cross-reference integrity.
        vector: The embedding vector as a list of floats.
        metadata: Structured metadata for filtered queries.
            Required fields: "entry_type", "domain", "state".
        collection: The vector collection (namespace) to store in.
    """

    record_id: str
    vector: list[float]
    metadata: dict[str, Any]
    collection: str = "knowledge_base"


@dataclass(frozen=True)
class VectorQueryResult:
    """
    A single result from a vector similarity query.

    Attributes:
        record_id: The identifier of the matching record.
        score: The similarity score (0.0–1.0, higher is more similar).
        metadata: The metadata stored with this vector record.
    """

    record_id: str
    score: float
    metadata: dict[str, Any]


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class VectorStoreInterface(ABC):
    """
    Abstract contract for all vector index adapters.

    Manages embedding vector storage and semantic similarity retrieval.
    The interface is collection-aware — vectors are organized into named
    collections (namespaces) within the vector store.

    Contract invariants:
        - upsert() creates or overwrites the vector for the given record_id.
        - query() returns results ordered by descending similarity score.
        - delete() is idempotent — deleting a non-existent ID succeeds.
        - Metadata filters are AND-combined with the similarity search.
        - Results with a score below the min_score threshold are excluded.

    Raises:
        VectorStoreWriteError: On upsert or delete failure.
        VectorStoreQueryError: On query execution failure.
        VectorStoreConnectionError: When the vector store is unavailable.
    """

    @abstractmethod
    async def upsert(self, record: VectorRecord) -> None:
        """
        Create or overwrite a vector record in the store.

        Args:
            record: The vector record to store with its metadata.

        Raises:
            VectorStoreWriteError: On write failure.
        """

    @abstractmethod
    async def upsert_batch(self, records: list[VectorRecord]) -> None:
        """
        Create or overwrite multiple vector records in a single operation.

        Args:
            records: The vector records to store. All must belong to the
                same collection.

        Raises:
            VectorStoreWriteError: On write failure. Partial batch writes
                are retried from the last successful record.
        """

    @abstractmethod
    async def query(
        self,
        collection: str,
        query_vector: list[float],
        top_k: int,
        metadata_filter: dict[str, Any] | None = None,
        min_score: float = 0.0,
    ) -> list[VectorQueryResult]:
        """
        Execute a semantic similarity query against the vector index.

        Args:
            collection: The collection to query.
            query_vector: The query embedding vector.
            top_k: Maximum number of results to return.
            metadata_filter: Optional key-value metadata filter.
                All filter predicates are AND-combined with the similarity search.
            min_score: Minimum similarity score threshold. Results below
                this score are excluded.

        Returns:
            list[VectorQueryResult]: Results ordered by descending similarity score.

        Raises:
            VectorStoreQueryError: On query execution failure.
        """

    @abstractmethod
    async def delete(self, collection: str, record_id: str) -> None:
        """
        Remove a vector record from the store.

        Idempotent: succeeds if the record does not exist.

        Args:
            collection: The collection to delete from.
            record_id: The record identifier to delete.

        Raises:
            VectorStoreWriteError: On delete failure.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the vector store is currently operational.

        Returns:
            bool: True if the vector store is reachable and operational.
        """
