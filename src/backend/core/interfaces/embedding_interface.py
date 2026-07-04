"""
Embedding Interface Contract.

Defines the abstraction for vector embedding generation. All text content
that enters the vector store must first be converted to an embedding vector
through this interface. The embedding model is a deployment decision —
consuming modules never depend on a specific embedding model or provider.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 3 (Layer 5 Knowledge Modules:
        embedding_service module — single responsibility: vector embedding
        generation for text content)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.9 (knowledge_base dependencies)
    SYSTEM_ARCHITECTURE.md Section 4.9 (Knowledge Base and RAG Engine)

Implementors:
    src/backend/knowledge/embedding_service.py

Consumers:
    src/backend/knowledge/knowledge_base/ (embed approved entries)
    src/backend/knowledge/rag_engine/ (embed query text)
    src/backend/knowledge/ingestion_pipeline/ (embed ingested content)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Embedding models (interface-local DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EmbeddingResult:
    """
    The embedding vector produced from input text.

    Attributes:
        text_hash: SHA-256 hash of the source text for cache keying.
        vector: The embedding vector as a list of floats.
        dimensions: The number of dimensions in the vector.
        model_id: The embedding model that produced this vector.
        input_tokens: Number of tokens in the input text.
    """

    text_hash: str
    vector: list[float]
    dimensions: int
    model_id: str
    input_tokens: int


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class EmbeddingInterface(ABC):
    """
    Abstract contract for embedding generation adapters.

    Converts text content into dense vector embeddings for semantic
    similarity search. Implementations must be deterministic for the same
    model version and input text (i.e., the same input always produces
    the same output vector for a given model).

    Contract invariants:
        - generate() is deterministic for a fixed model version and input.
        - generate_batch() produces embeddings in the same order as the inputs.
        - The vector dimensionality is fixed per model — it never changes
          for a given implementation instance.
        - Implementations must never log the source text content.

    Raises:
        EmbeddingGenerationError: On embedding model failure.
        EmbeddingConnectionError: When the embedding service is unavailable.
    """

    @abstractmethod
    async def generate(self, text: str) -> EmbeddingResult:
        """
        Generate an embedding vector for the given text.

        Args:
            text: The source text to embed. Must be non-empty.

        Returns:
            EmbeddingResult: The generated embedding vector with metadata.

        Raises:
            EmbeddingGenerationError: On model or provider failure.
        """

    @abstractmethod
    async def generate_batch(
        self, texts: list[str]
    ) -> list[EmbeddingResult]:
        """
        Generate embedding vectors for a batch of texts.

        More efficient than calling generate() in a loop. Results are
        returned in the same order as the input texts.

        Args:
            texts: List of source texts to embed. Must be non-empty.

        Returns:
            list[EmbeddingResult]: Embeddings in input order.

        Raises:
            EmbeddingGenerationError: On model or provider failure.
        """

    @abstractmethod
    def get_model_id(self) -> str:
        """
        Return the embedding model identifier for this implementation.

        Used for observability attribution and compatibility checks.

        Returns:
            str: The model identifier (e.g., "text-embedding-3-small").
        """

    @abstractmethod
    def get_vector_dimensions(self) -> int:
        """
        Return the vector dimensionality produced by this model.

        All vectors from this implementation have exactly this many
        dimensions. Used to configure the vector store collection schema.

        Returns:
            int: The number of dimensions in each output vector.
        """
