from __future__ import annotations

from typing import Optional

from backend.core.interfaces.cache_interface import CacheInterface
from backend.core.interfaces.llm_interface import LLMInterface
from backend.core.interfaces.secrets_interface import SecretsInterface
from backend.core.interfaces.storage_interface import StorageInterface
from backend.core.interfaces.ledger_interface import LedgerInterface

# Infrastructure implementations live here — composition root owns them
from backend.infrastructure.cache.cache_service import CacheService
from backend.infrastructure.llm.llm_client import LLMClient
from backend.infrastructure.llm.anthropic_adapter import AnthropicAdapter
from backend.infrastructure.llm.openai_adapter import OpenAIAdapter
from backend.infrastructure.observability.logger import Logger
from backend.infrastructure.observability.metrics import Metrics
from backend.infrastructure.observability.tracer import start_trace, TraceHandle
from backend.infrastructure.secrets.secrets_manager import SecretsManager
from backend.infrastructure.storage.storage_service import StorageService
from backend.infrastructure.storage.session_store import SessionStore
from backend.infrastructure.storage.engagement_store import EngagementStore
from backend.infrastructure.decision_ledger.ledger_service import LedgerService


def create_cache_service() -> CacheInterface:
    return CacheService()


def create_storage_service() -> StorageService:
    return StorageService()


def create_session_store(storage: StorageService) -> SessionStore:
    return SessionStore(storage)


def create_engagement_store(storage: StorageService) -> EngagementStore:
    return EngagementStore(storage)


def create_secrets_manager(initial: dict[str, str] | None = None) -> SecretsInterface:
    return SecretsManager(initial)


def create_ledger_service() -> LedgerInterface:
    return LedgerService()


def create_llm_client() -> LLMInterface:
    return LLMClient()


def create_anthropic_adapter() -> LLMInterface:
    return AnthropicAdapter()


def create_openai_adapter() -> LLMInterface:
    return OpenAIAdapter()


def create_logger() -> Logger:
    return Logger()


def create_metrics() -> Metrics:
    return Metrics()


def create_trace_handle(
    name: str, metadata: dict[str, object] | None = None
) -> TraceHandle:
    return start_trace(name, metadata)


class DIContainer:
    def __init__(self, secrets_initial: Optional[dict[str, str]] = None) -> None:
        self._secrets_initial = secrets_initial

    def build(self) -> "DIContainer.Provided":
        # Instrumentation prints help locate blocking constructor during tests
        print("DI: create_cache_service")
        cache = create_cache_service()
        print("DI: create_storage_service")
        storage = create_storage_service()
        print("DI: create_session_store")
        session_store = create_session_store(storage)
        print("DI: create_engagement_store")
        engagement_store = create_engagement_store(storage)
        print("DI: create_secrets_manager")
        secrets = create_secrets_manager(self._secrets_initial)
        print("DI: create_ledger_service")
        ledger = create_ledger_service()
        print("DI: create_llm_client")
        llm = create_llm_client()
        print("DI: create_logger")
        logger = create_logger()
        print("DI: create_metrics")
        metrics = create_metrics()

        return DIContainer.Provided(
            cache=cache,
            storage=storage,
            session_store=session_store,
            engagement_store=engagement_store,
            secrets=secrets,
            ledger=ledger,
            llm=llm,
            logger=logger,
            metrics=metrics,
        )

    class Provided:
        def __init__(
            self,
            cache: CacheInterface,
            storage: StorageInterface,
            session_store: SessionStore,
            engagement_store: EngagementStore,
            secrets: SecretsInterface,
            ledger: LedgerInterface,
            llm: LLMInterface,
            logger: Logger,
            metrics: Metrics,
        ) -> None:
            self.cache = cache
            self.storage = storage
            self.session_store = session_store
            self.engagement_store = engagement_store
            self.secrets = secrets
            self.ledger = ledger
            self.llm = llm
            self.logger = logger
            self.metrics = metrics


__all__ = ["DIContainer"]
