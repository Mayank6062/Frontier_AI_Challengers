from __future__ import annotations

from ...core.interfaces.cache_interface import CacheInterface
from ...core.interfaces.llm_interface import LLMInterface
from ...core.interfaces.secrets_interface import SecretsInterface
from ...core.interfaces.storage_interface import StorageInterface
from ...core.interfaces.ledger_interface import LedgerInterface

from ...infrastructure.cache.cache_service import CacheService
from ...infrastructure.llm.llm_client import LLMClient
from ...infrastructure.llm.anthropic_adapter import AnthropicAdapter
from ...infrastructure.llm.openai_adapter import OpenAIAdapter
from ...infrastructure.observability.logger import Logger
from ...infrastructure.observability.metrics import Metrics
from ...infrastructure.observability.tracer import start_trace, TraceHandle

# CorrelationManager is available via observability package if consumers need it
from ...infrastructure.secrets.secrets_manager import SecretsManager
from ...infrastructure.storage.storage_service import StorageService
from ...infrastructure.storage.session_store import SessionStore
from ...infrastructure.storage.engagement_store import EngagementStore
from ...infrastructure.decision_ledger.ledger_service import LedgerService


def create_cache_service() -> CacheInterface:
	return CacheService()


def create_storage_service() -> StorageService:
	return StorageService()


def create_session_store(storage: StorageService) -> SessionStore:
	# storage is injected (constructor injection)
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
	# returns a TraceHandle (context manager) — factory mirrors interface expectations
	return start_trace(name, metadata)


class DIContainer:
	"""Lightweight container for wiring commonly-needed services.

	This is a simple assembly helper and does not create global singletons.
	Callers may instantiate the container at application bootstrap and pass
	the instance to components that require a pre-wired set of services.
	"""

	def __init__(self, secrets_initial: dict[str, str] | None = None) -> None:
		self._secrets_initial = secrets_initial

	def build(self) -> "DIContainer.Provided":
		cache = create_cache_service()
		storage = create_storage_service()
		session_store = create_session_store(storage)
		engagement_store = create_engagement_store(storage)
		secrets = create_secrets_manager(self._secrets_initial)
		ledger = create_ledger_service()
		llm = create_llm_client()
		logger = create_logger()
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


__all__ = [
	"create_cache_service",
	"create_storage_service",
	"create_session_store",
	"create_engagement_store",
	"create_secrets_manager",
	"create_ledger_service",
	"create_llm_client",
	"create_anthropic_adapter",
	"create_openai_adapter",
	"create_logger",
	"create_metrics",
	"create_trace_handle",
	"DIContainer",
]
