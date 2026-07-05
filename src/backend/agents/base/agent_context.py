from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ...core.interfaces.observability_interface import ObservabilityInterface
from ...core.interfaces.storage_interface import StorageInterface
from ...core.interfaces.cache_interface import CacheInterface
from ...core.interfaces.secrets_interface import SecretsInterface
from ...core.interfaces.ledger_interface import LedgerInterface
from ...core.interfaces.llm_interface import LLMInterface


@dataclass(frozen=True)
class AgentContext:
    """Immutable execution context for agents.

    Contains only references to interfaces and lightweight metadata. Nothing
    in this object should perform I/O or instantiate other services.
    """

    session_id: Optional[str] = None
    engagement_id: Optional[str] = None
    observability: Optional[ObservabilityInterface] = None
    storage: Optional[StorageInterface] = None
    cache: Optional[CacheInterface] = None
    secrets: Optional[SecretsInterface] = None
    ledger: Optional[LedgerInterface] = None
    llm: Optional[LLMInterface] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    execution_id: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    runtime_vars: Dict[str, Any] = field(default_factory=dict)
