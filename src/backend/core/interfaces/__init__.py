"""
Interface Layer — Public API.

Exports all interface contracts defined in the Application Core interfaces
module. Consuming layers import from this __init__.py to access the
normalized interface types.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module)
    REPOSITORY_MASTER_STRUCTURE.md Section 3 (core/interfaces/ file tree)

Dependency rule (REPOSITORY_MASTER_STRUCTURE.md Section 2.4):
    This module is consumed by:
        - src/backend/core/ (business logic depends on interfaces)
        - src/backend/infrastructure/ (implements these interfaces)
        - src/backend/agents/ (agents consume LLM and Knowledge interfaces)
        - src/backend/knowledge/ (consumes Storage, VectorStore, Embedding interfaces)
        - src/backend/output/ (consumes OutputStorage interface)

    This module must NOT import from:
        - src/backend/infrastructure/ (would invert the dependency direction)
        - src/backend/agents/ (would create circular dependency)
        - src/backend/api/ (would violate layer hierarchy)
"""

from .agent_interface import (
    AgentCitation,
    AgentContext,
    AgentInterface,
    AgentResult,
    AgentStatus,
)
from .cache_interface import CacheInterface
from .embedding_interface import EmbeddingInterface, EmbeddingResult
from .knowledge_interface import (
    KnowledgeCitation,
    KnowledgeEntry,
    KnowledgeEntryState,
    KnowledgeEntryType,
    KnowledgeInterface,
    KnowledgeRetrievalQuery,
    KnowledgeRetrievalResult,
)
from .ledger_interface import (
    LedgerEntry,
    LedgerEventType,
    LedgerIntegrityResult,
    LedgerInterface,
    LedgerWriteResult,
)
from .llm_interface import LLMInterface, LLMRequest, LLMResponse
from .oauth_interface import OAuthIdentity, OAuthProviderInterface, OAuthTokenResponse
from .observability_interface import (
    LogLevel,
    LogRecord,
    MetricDataPoint,
    ObservabilityInterface,
    TraceSpan,
)
from .output_storage_interface import (
    OutputArtifact,
    OutputBundle,
    OutputFormat,
    OutputStorageInterface,
)
from .secrets_interface import SecretsInterface, SecretValue
from .storage_interface import (
    StorageFilter,
    StorageInterface,
    StorageRecord,
    StorageWriteConfirmation,
)
from .vector_store_interface import (
    VectorQueryResult,
    VectorRecord,
    VectorStoreInterface,
)

__all__ = [
    # Agent interface
    "AgentInterface",
    "AgentContext",
    "AgentResult",
    "AgentCitation",
    "AgentStatus",
    # LLM interface
    "LLMInterface",
    "LLMRequest",
    "LLMResponse",
    # Storage interface
    "StorageInterface",
    "StorageRecord",
    "StorageFilter",
    "StorageWriteConfirmation",
    # Cache interface
    "CacheInterface",
    # Ledger interface
    "LedgerInterface",
    "LedgerEntry",
    "LedgerEventType",
    "LedgerWriteResult",
    "LedgerIntegrityResult",
    # Knowledge interface
    "KnowledgeInterface",
    "KnowledgeRetrievalQuery",
    "KnowledgeRetrievalResult",
    "KnowledgeCitation",
    "KnowledgeEntry",
    "KnowledgeEntryType",
    "KnowledgeEntryState",
    # Secrets interface
    "SecretsInterface",
    "SecretValue",
    # Observability interface
    "ObservabilityInterface",
    "LogRecord",
    "LogLevel",
    "TraceSpan",
    "MetricDataPoint",
    # Output storage interface
    "OutputStorageInterface",
    "OutputArtifact",
    "OutputBundle",
    "OutputFormat",
    # Vector store interface
    "VectorStoreInterface",
    "VectorRecord",
    "VectorQueryResult",
    # Embedding interface
    "EmbeddingInterface",
    "EmbeddingResult",
    # OAuth interface
    "OAuthProviderInterface",
    "OAuthIdentity",
    "OAuthTokenResponse",
]
