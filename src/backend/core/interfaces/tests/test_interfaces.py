"""
Interface Layer — Unit Tests.

Tests verify abstract enforcement, inheritance compliance, method signatures,
typing correctness, and import boundary integrity for all interface contracts.

Test categories:
    1. Abstract Enforcement — ABC prevents direct instantiation
    2. Inheritance Compliance — concrete classes must implement all abstract methods
    3. Method Signatures — correct parameter names, types, and return annotations
    4. Model Integrity — frozen dataclasses, required fields, enum values
    5. Import Boundaries — interfaces depend only on stdlib and shared layer
    6. Export Completeness — __init__.py exports all public symbols

Authority:
    IMPLEMENTATION_SPECIFICATION.md Section 11 (Testing Strategy)
    IMPLEMENTATION_SPECIFICATION.md Section 12 (Validation Gates)
    BACKEND_MODULE_ARCHITECTURE.md Section 19 (Backend Validation Checklist)
"""

from __future__ import annotations

import inspect
from abc import ABC
from typing import Any

import pytest

from ..agent_interface import AgentContext, AgentInterface, AgentResult, AgentStatus
from ..cache_interface import CacheInterface
from ..embedding_interface import EmbeddingInterface, EmbeddingResult
from ..knowledge_interface import (
    KnowledgeEntry,
    KnowledgeEntryState,
    KnowledgeEntryType,
    KnowledgeInterface,
    KnowledgeRetrievalQuery,
    KnowledgeRetrievalResult,
)
from ..ledger_interface import (
    LedgerEntry,
    LedgerEventType,
    LedgerInterface,
    LedgerWriteResult,
)
from ..llm_interface import LLMInterface, LLMRequest, LLMResponse
from ..oauth_interface import OAuthIdentity, OAuthProviderInterface, OAuthTokenResponse
from ..observability_interface import (
    LogLevel,
    LogRecord,
    MetricDataPoint,
    ObservabilityInterface,
    TraceSpan,
)
from ..output_storage_interface import OutputFormat, OutputStorageInterface
from ..secrets_interface import SecretsInterface, SecretValue
from ..storage_interface import (
    StorageFilter,
    StorageInterface,
    StorageRecord,
    StorageWriteConfirmation,
)
from ..vector_store_interface import VectorRecord, VectorStoreInterface  # noqa: F401


# ===========================================================================
# 1. Abstract Enforcement Tests
# ===========================================================================


class TestAbstractEnforcement:
    """Verify all interfaces cannot be instantiated directly."""

    def test_agent_interface_is_abstract(self):
        """AgentInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AgentInterface()  # type: ignore[abstract]

    def test_llm_interface_is_abstract(self):
        """LLMInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            LLMInterface()  # type: ignore[abstract]

    def test_storage_interface_is_abstract(self):
        """StorageInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            StorageInterface()  # type: ignore[abstract]

    def test_cache_interface_is_abstract(self):
        """CacheInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            CacheInterface()  # type: ignore[abstract]

    def test_ledger_interface_is_abstract(self):
        """LedgerInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            LedgerInterface()  # type: ignore[abstract]

    def test_knowledge_interface_is_abstract(self):
        """KnowledgeInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            KnowledgeInterface()  # type: ignore[abstract]

    def test_secrets_interface_is_abstract(self):
        """SecretsInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            SecretsInterface()  # type: ignore[abstract]

    def test_observability_interface_is_abstract(self):
        """ObservabilityInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            ObservabilityInterface()  # type: ignore[abstract]

    def test_output_storage_interface_is_abstract(self):
        """OutputStorageInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            OutputStorageInterface()  # type: ignore[abstract]

    def test_vector_store_interface_is_abstract(self):
        """VectorStoreInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            VectorStoreInterface()  # type: ignore[abstract]

    def test_embedding_interface_is_abstract(self):
        """EmbeddingInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            EmbeddingInterface()  # type: ignore[abstract]

    def test_oauth_interface_is_abstract(self):
        """OAuthProviderInterface cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            OAuthProviderInterface()  # type: ignore[abstract]


# ===========================================================================
# 2. ABC Inheritance Tests
# ===========================================================================


class TestABCInheritance:
    """Verify all interfaces properly inherit from ABC."""

    def test_agent_interface_inherits_abc(self):
        assert issubclass(AgentInterface, ABC)

    def test_llm_interface_inherits_abc(self):
        assert issubclass(LLMInterface, ABC)

    def test_storage_interface_inherits_abc(self):
        assert issubclass(StorageInterface, ABC)

    def test_cache_interface_inherits_abc(self):
        assert issubclass(CacheInterface, ABC)

    def test_ledger_interface_inherits_abc(self):
        assert issubclass(LedgerInterface, ABC)

    def test_knowledge_interface_inherits_abc(self):
        assert issubclass(KnowledgeInterface, ABC)

    def test_secrets_interface_inherits_abc(self):
        assert issubclass(SecretsInterface, ABC)

    def test_observability_interface_inherits_abc(self):
        assert issubclass(ObservabilityInterface, ABC)

    def test_output_storage_interface_inherits_abc(self):
        assert issubclass(OutputStorageInterface, ABC)

    def test_vector_store_interface_inherits_abc(self):
        assert issubclass(VectorStoreInterface, ABC)

    def test_embedding_interface_inherits_abc(self):
        assert issubclass(EmbeddingInterface, ABC)

    def test_oauth_interface_inherits_abc(self):
        assert issubclass(OAuthProviderInterface, ABC)


# ===========================================================================
# 3. Concrete Implementation Compliance Tests
# ===========================================================================


class ConcreteAgentImpl(AgentInterface):
    """Minimal concrete agent for inheritance testing."""

    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id="test",
            agent_version="1.0.0",
            engagement_id="eng-1",
            correlation_id="corr-1",
            status=AgentStatus.COMPLETED,
            output_payload={},
            citations=[],
            confidence_score=0.9,
            token_usage={"input": 100, "output": 50},
            latency_ms=250.0,
        )

    def get_agent_id(self) -> str:
        return "test_agent"

    def get_agent_version(self) -> str:
        return "1.0.0"

    def get_agent_category(self) -> str:
        return "discovery"

    def get_input_schema(self) -> dict[str, Any]:
        return {}

    def get_output_schema(self) -> dict[str, Any]:
        return {}


class ConcreteLLMImpl(LLMInterface):
    """Minimal concrete LLM adapter for inheritance testing."""

    async def invoke(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            generated_text="test",
            finish_reason="stop",
            input_tokens=10,
            output_tokens=5,
            model_id="test-model",
            provider="test",
            latency_ms=100.0,
        )

    async def check_availability(self) -> bool:
        return True

    def get_model_id(self) -> str:
        return "test-model"

    def get_provider_name(self) -> str:
        return "test"

    def get_max_context_tokens(self) -> int:
        return 4096


class ConcreteStorageImpl(StorageInterface):
    """Minimal concrete storage adapter for inheritance testing."""

    async def read(self, collection: str, key: str) -> StorageRecord | None:
        return None

    async def write(self, collection: str, key: str, data: dict[str, Any]) -> StorageWriteConfirmation:
        return StorageWriteConfirmation(key=key, collection=collection, version=1, written_at_utc="2026-07-04T12:00:00Z", success=True)

    async def delete(self, collection: str, key: str) -> StorageWriteConfirmation:
        return StorageWriteConfirmation(key=key, collection=collection, version=1, written_at_utc="2026-07-04T12:00:00Z", success=True)

    async def query(self, filter_spec: StorageFilter) -> list[StorageRecord]:
        return []

    async def count(self, collection: str, predicates: dict[str, Any]) -> int:
        return 0

    async def check_health(self) -> bool:
        return True


class ConcreteCacheImpl(CacheInterface):
    """Minimal concrete cache adapter for inheritance testing."""

    async def get(self, key: str) -> Any | None:
        return None

    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        pass

    async def delete(self, key: str) -> None:
        pass

    async def invalidate_prefix(self, prefix: str) -> int:
        return 0

    async def exists(self, key: str) -> bool:
        return False

    async def check_health(self) -> bool:
        return True


class ConcreteLedgerImpl(LedgerInterface):
    """Minimal concrete ledger adapter for inheritance testing."""

    async def append(self, entry: LedgerEntry) -> LedgerWriteResult:
        return LedgerWriteResult(entry_id=entry.entry_id, entry_hash="abc", written_at_utc="2026-07-04T12:00:00Z", success=True)

    async def get(self, entry_id: str) -> LedgerEntry | None:
        return None

    async def list_by_engagement(self, engagement_id: str, offset: int = 0, limit: int = 50) -> list[LedgerEntry]:
        return []

    async def verify_chain(self, from_entry_id: str):
        from ..ledger_interface import LedgerIntegrityResult
        return LedgerIntegrityResult(valid=True, entries_verified=0, first_broken_entry_id=None, verification_completed_at_utc="2026-07-04T12:00:00Z")

    async def check_health(self) -> bool:
        return True


class ConcreteKnowledgeImpl(KnowledgeInterface):
    """Minimal concrete knowledge adapter for inheritance testing."""

    async def query(self, retrieval_query: KnowledgeRetrievalQuery) -> KnowledgeRetrievalResult:
        return KnowledgeRetrievalResult(items=[], citations=[], total_candidates=0, retrieval_strategy="semantic", retrieval_latency_ms=0.0, query_hash="")

    async def get_entry(self, entry_id: str) -> KnowledgeEntry | None:
        return None

    async def submit_entry(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        return entry

    async def approve_entry(self, entry_id: str, curator_id: str) -> KnowledgeEntry:
        return KnowledgeEntry(entry_id=entry_id, title="", content="", entry_type=KnowledgeEntryType.DOMAIN_KNOWLEDGE, domain="", state=KnowledgeEntryState.APPROVED, submitted_by="", approved_by=curator_id, embedding_id="", source_reference="", created_at_utc="", approved_at_utc="")

    async def deprecate_entry(self, entry_id: str, reason: str) -> KnowledgeEntry:
        return KnowledgeEntry(entry_id=entry_id, title="", content="", entry_type=KnowledgeEntryType.DOMAIN_KNOWLEDGE, domain="", state=KnowledgeEntryState.DEPRECATED, submitted_by="", approved_by="", embedding_id="", source_reference="", created_at_utc="", approved_at_utc="")

    async def list_pending_approval(self, offset: int = 0, limit: int = 50) -> list[KnowledgeEntry]:
        return []

    async def record_retrieval_usage(self, entry_id: str, engagement_id: str) -> None:
        pass


class ConcreteSecretsImpl(SecretsInterface):
    """Minimal concrete secrets adapter for inheritance testing."""

    async def get_secret(self, secret_name: str) -> SecretValue:
        return SecretValue(secret_name=secret_name, secret_value="test", version="1", expires_at_utc="", retrieved_at_utc="2026-07-04T12:00:00Z")

    async def refresh_secret(self, secret_name: str) -> SecretValue:
        return SecretValue(secret_name=secret_name, secret_value="refreshed", version="2", expires_at_utc="", retrieved_at_utc="2026-07-04T12:00:00Z")

    async def check_health(self) -> bool:
        return True


class ConcreteObservabilityImpl(ObservabilityInterface):
    """Minimal concrete observability adapter for inheritance testing."""

    def log(self, record: LogRecord) -> None:
        pass

    def start_span(self, span: TraceSpan) -> TraceSpan:
        return span

    def end_span(self, span: TraceSpan, status: str = "ok", error_message: str = "") -> None:
        pass

    def record_metric(self, data_point: MetricDataPoint) -> None:
        pass

    def assign_correlation_id(self) -> str:
        return "test-correlation-id"

    def get_correlation_id(self) -> str:
        return "test-correlation-id"


class ConcreteVectorStoreImpl(VectorStoreInterface):
    """Minimal concrete vector store for inheritance testing."""

    async def upsert(self, record: VectorRecord) -> None:
        pass

    async def upsert_batch(self, records: list[VectorRecord]) -> None:
        pass

    async def query(self, collection: str, query_vector: list[float], top_k: int, metadata_filter=None, min_score: float = 0.0):
        return []

    async def delete(self, collection: str, record_id: str) -> None:
        pass

    async def check_health(self) -> bool:
        return True


class ConcreteEmbeddingImpl(EmbeddingInterface):
    """Minimal concrete embedding adapter for inheritance testing."""

    async def generate(self, text: str) -> EmbeddingResult:
        return EmbeddingResult(text_hash="abc", vector=[0.1, 0.2], dimensions=2, model_id="test", input_tokens=5)

    async def generate_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        return [await self.generate(t) for t in texts]

    def get_model_id(self) -> str:
        return "test-embedding"

    def get_vector_dimensions(self) -> int:
        return 2


class ConcreteOAuthImpl(OAuthProviderInterface):
    """Minimal concrete OAuth adapter for inheritance testing."""

    async def initiate_flow(self, state: str) -> str:
        return "https://github.com/login/oauth/authorize?state=" + state

    async def exchange_code(self, authorization_code: str, state: str) -> OAuthTokenResponse:
        return OAuthTokenResponse(access_token="token", token_type="bearer", scope="read:user")

    async def validate_token(self, access_token: str) -> OAuthIdentity:
        return OAuthIdentity(provider_user_id="123", email="test@test.com", display_name="Test", username="testuser", avatar_url="", provider_name="github", provider_access_token=access_token, scopes=["read:user"])

    def get_provider_name(self) -> str:
        return "github"


class ConcreteOutputStorageImpl(OutputStorageInterface):
    """Minimal concrete output storage for inheritance testing."""

    async def save_artifact(self, engagement_id, output_version, output_format, content, template_version):
        from ..output_storage_interface import OutputArtifact
        return OutputArtifact(artifact_id="art-1", engagement_id=engagement_id, output_version=output_version, output_format=output_format, storage_path="path/to/artifact", content_hash="abc", size_bytes=len(content), template_version=template_version, generated_at_utc="2026-07-04T12:00:00Z")

    async def get_artifact(self, artifact_id: str) -> bytes | None:
        return None

    async def save_bundle(self, bundle):
        return bundle

    async def get_bundle(self, engagement_id, output_version):
        return None

    async def list_bundles(self, engagement_id):
        return []

    async def check_health(self) -> bool:
        return True


class TestConcreteImplementations:
    """Verify concrete implementations satisfy the interface contracts."""

    def test_concrete_agent_instantiates(self):
        impl = ConcreteAgentImpl()
        assert impl is not None

    def test_concrete_llm_instantiates(self):
        impl = ConcreteLLMImpl()
        assert impl is not None

    def test_concrete_storage_instantiates(self):
        impl = ConcreteStorageImpl()
        assert impl is not None

    def test_concrete_cache_instantiates(self):
        impl = ConcreteCacheImpl()
        assert impl is not None

    def test_concrete_ledger_instantiates(self):
        impl = ConcreteLedgerImpl()
        assert impl is not None

    def test_concrete_knowledge_instantiates(self):
        impl = ConcreteKnowledgeImpl()
        assert impl is not None

    def test_concrete_secrets_instantiates(self):
        impl = ConcreteSecretsImpl()
        assert impl is not None

    def test_concrete_observability_instantiates(self):
        impl = ConcreteObservabilityImpl()
        assert impl is not None

    def test_concrete_vector_store_instantiates(self):
        impl = ConcreteVectorStoreImpl()
        assert impl is not None

    def test_concrete_embedding_instantiates(self):
        impl = ConcreteEmbeddingImpl()
        assert impl is not None

    def test_concrete_oauth_instantiates(self):
        impl = ConcreteOAuthImpl()
        assert impl is not None

    def test_concrete_output_storage_instantiates(self):
        impl = ConcreteOutputStorageImpl()
        assert impl is not None

    def test_partial_implementation_raises(self):
        """A class that only partially implements an interface must raise on instantiation."""
        class PartialAgent(AgentInterface):
            async def execute(self, context: AgentContext) -> AgentResult:  # type: ignore[override]
                return None  # type: ignore

            def get_agent_id(self) -> str:
                return "partial"
            # Missing: get_agent_version, get_agent_category, get_input_schema, get_output_schema

        with pytest.raises(TypeError, match="abstract"):
            PartialAgent()  # type: ignore[abstract]


# ===========================================================================
# 4. Model Integrity Tests
# ===========================================================================


class TestModelIntegrity:
    """Verify interface-local DTO models are correctly structured."""

    def test_llm_request_is_frozen(self):
        """LLMRequest must be immutable."""
        req = LLMRequest(model_id="m", system_prompt="s", user_prompt="u", max_tokens=100)
        with pytest.raises(AttributeError):
            req.model_id = "other"  # type: ignore[misc]

    def test_llm_response_is_frozen(self):
        """LLMResponse must be immutable."""
        resp = LLMResponse(generated_text="t", finish_reason="stop", input_tokens=10, output_tokens=5, model_id="m", provider="p", latency_ms=100.0)
        with pytest.raises(AttributeError):
            resp.generated_text = "x"  # type: ignore[misc]

    def test_agent_context_is_frozen(self):
        """AgentContext must be immutable."""
        ctx = AgentContext(
            engagement_id="e", session_id="s", correlation_id="c",
            stage_name="discovery", structured_requirements={},
            prior_agent_outputs={}, retrieved_knowledge={},
            architect_feedback={}, model_id="m", prompt_version="1.0.0",
            agent_parameters={}, max_tokens=4000, temperature=0.0,
            engagement_domain="test",
        )
        with pytest.raises(AttributeError):
            ctx.engagement_id = "x"  # type: ignore[misc]

    def test_agent_result_is_frozen(self):
        """AgentResult must be immutable."""
        result = AgentResult(
            agent_id="a", agent_version="1.0.0", engagement_id="e",
            correlation_id="c", status=AgentStatus.COMPLETED,
            output_payload={}, citations=[], confidence_score=0.9,
            token_usage={}, latency_ms=100.0,
        )
        with pytest.raises(AttributeError):
            result.agent_id = "x"  # type: ignore[misc]

    def test_ledger_entry_is_frozen(self):
        """LedgerEntry must be immutable."""
        entry = LedgerEntry(
            entry_id="e1",
            event_type=LedgerEventType.ENGAGEMENT_CREATED,
            engagement_id="eng-1", session_id="sess-1",
            actor_id="user-1", actor_type="human",
            payload={}, occurred_at_utc="2026-07-04T12:00:00Z",
        )
        with pytest.raises(AttributeError):
            entry.entry_id = "x"  # type: ignore[misc]

    def test_storage_record_is_frozen(self):
        """StorageRecord must be immutable."""
        record = StorageRecord(key="k", collection="c", data={})
        with pytest.raises(AttributeError):
            record.key = "x"  # type: ignore[misc]

    def test_vector_record_is_frozen(self):
        """VectorRecord must be immutable."""
        record = VectorRecord(record_id="r", vector=[0.1, 0.2], metadata={})
        with pytest.raises(AttributeError):
            record.record_id = "x"  # type: ignore[misc]

    def test_secret_value_is_frozen(self):
        """SecretValue must be immutable."""
        sv = SecretValue(secret_name="n", secret_value="v", version="1", expires_at_utc="", retrieved_at_utc="")
        with pytest.raises(AttributeError):
            sv.secret_value = "x"  # type: ignore[misc]

    def test_log_record_is_frozen(self):
        """LogRecord must be immutable."""
        lr = LogRecord(level=LogLevel.INFO, message="m", module="mod", operation="op", correlation_id="c")
        with pytest.raises(AttributeError):
            lr.message = "x"  # type: ignore[misc]

    def test_agent_status_values(self):
        """AgentStatus enum contains all required values."""
        assert AgentStatus.PENDING == "pending"
        assert AgentStatus.RUNNING == "running"
        assert AgentStatus.COMPLETED == "completed"
        assert AgentStatus.FAILED == "failed"
        assert AgentStatus.DEGRADED == "degraded"

    def test_ledger_event_types_defined(self):
        """LedgerEventType contains all required event types."""
        assert LedgerEventType.ENGAGEMENT_CREATED == "engagement.created"
        assert LedgerEventType.REVIEW_DECISION_APPROVED == "review.decision_approved"
        assert LedgerEventType.ARCHITECTURE_APPROVED == "architecture.approved"

    def test_knowledge_entry_state_values(self):
        """KnowledgeEntryState enum contains all required values."""
        assert KnowledgeEntryState.PENDING_APPROVAL == "pending_approval"
        assert KnowledgeEntryState.APPROVED == "approved"
        assert KnowledgeEntryState.DEPRECATED == "deprecated"

    def test_output_format_enum_values(self):
        """OutputFormat contains all MVP output formats."""
        assert OutputFormat.MARKDOWN_HLD == "markdown_hld"
        assert OutputFormat.HTML_REPORT == "html_report"
        assert OutputFormat.MERMAID_DIAGRAM == "mermaid_diagram"
        assert OutputFormat.JSON_ARCHITECTURE_STATE == "json_architecture_state"

    def test_log_level_values(self):
        """LogLevel enum contains all required severity levels."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


# ===========================================================================
# 5. Abstract Method Signature Tests
# ===========================================================================


class TestMethodSignatures:
    """Verify all abstract methods have correct signatures."""

    def test_agent_execute_is_coroutine(self):
        """AgentInterface.execute must be async."""
        assert inspect.iscoroutinefunction(ConcreteAgentImpl.execute)

    def test_llm_invoke_is_coroutine(self):
        """LLMInterface.invoke must be async."""
        assert inspect.iscoroutinefunction(ConcreteLLMImpl.invoke)

    def test_llm_check_availability_is_coroutine(self):
        """LLMInterface.check_availability must be async."""
        assert inspect.iscoroutinefunction(ConcreteLLMImpl.check_availability)

    def test_storage_read_is_coroutine(self):
        """StorageInterface.read must be async."""
        assert inspect.iscoroutinefunction(ConcreteStorageImpl.read)

    def test_storage_write_is_coroutine(self):
        """StorageInterface.write must be async."""
        assert inspect.iscoroutinefunction(ConcreteStorageImpl.write)

    def test_cache_get_is_coroutine(self):
        """CacheInterface.get must be async."""
        assert inspect.iscoroutinefunction(ConcreteCacheImpl.get)

    def test_cache_set_is_coroutine(self):
        """CacheInterface.set must be async."""
        assert inspect.iscoroutinefunction(ConcreteCacheImpl.set)

    def test_ledger_append_is_coroutine(self):
        """LedgerInterface.append must be async."""
        assert inspect.iscoroutinefunction(ConcreteLedgerImpl.append)

    def test_knowledge_query_is_coroutine(self):
        """KnowledgeInterface.query must be async."""
        assert inspect.iscoroutinefunction(ConcreteKnowledgeImpl.query)

    def test_secrets_get_is_coroutine(self):
        """SecretsInterface.get_secret must be async."""
        assert inspect.iscoroutinefunction(ConcreteSecretsImpl.get_secret)

    def test_vector_store_upsert_is_coroutine(self):
        """VectorStoreInterface.upsert must be async."""
        assert inspect.iscoroutinefunction(ConcreteVectorStoreImpl.upsert)

    def test_embedding_generate_is_coroutine(self):
        """EmbeddingInterface.generate must be async."""
        assert inspect.iscoroutinefunction(ConcreteEmbeddingImpl.generate)

    def test_oauth_validate_token_is_coroutine(self):
        """OAuthProviderInterface.validate_token must be async."""
        assert inspect.iscoroutinefunction(ConcreteOAuthImpl.validate_token)

    def test_observability_log_is_sync(self):
        """ObservabilityInterface.log must be synchronous (not async)."""
        assert not inspect.iscoroutinefunction(ConcreteObservabilityImpl.log)

    def test_observability_record_metric_is_sync(self):
        """ObservabilityInterface.record_metric must be synchronous."""
        assert not inspect.iscoroutinefunction(ConcreteObservabilityImpl.record_metric)

    def test_agent_get_agent_id_is_sync(self):
        """AgentInterface.get_agent_id must be synchronous."""
        assert not inspect.iscoroutinefunction(ConcreteAgentImpl.get_agent_id)

    def test_llm_get_model_id_is_sync(self):
        """LLMInterface.get_model_id must be synchronous."""
        assert not inspect.iscoroutinefunction(ConcreteLLMImpl.get_model_id)


# ===========================================================================
# 6. Import Boundary Tests
# ===========================================================================


class TestImportBoundaries:
    """Verify interface modules import only from stdlib and shared layer."""

    def test_llm_interface_no_infra_imports(self):
        """llm_interface.py must not import from infrastructure."""
        import src.backend.core.interfaces.llm_interface as mod
        source = inspect.getsource(mod)
        assert "from src.backend.infrastructure" not in source
        assert "import infrastructure" not in source

    def test_agent_interface_no_infra_imports(self):
        """agent_interface.py must not import from infrastructure."""
        import src.backend.core.interfaces.agent_interface as mod
        source = inspect.getsource(mod)
        assert "from src.backend.infrastructure" not in source
        assert "import agents" not in source

    def test_storage_interface_no_infra_imports(self):
        """storage_interface.py must not import from infrastructure."""
        import src.backend.core.interfaces.storage_interface as mod
        source = inspect.getsource(mod)
        assert "from src.backend.infrastructure" not in source

    def test_knowledge_interface_no_agent_imports(self):
        """knowledge_interface.py must not import from agents."""
        import src.backend.core.interfaces.knowledge_interface as mod
        source = inspect.getsource(mod)
        assert "from src.backend.agents" not in source


# ===========================================================================
# 7. Export Completeness Tests
# ===========================================================================


class TestExportCompleteness:
    """Verify __init__.py exports all public symbols."""

    def test_all_interfaces_exported(self):
        """All interface classes must be in __init__.__all__."""
        from .. import __all__ as exports

        required_interfaces = [
            "AgentInterface",
            "LLMInterface",
            "StorageInterface",
            "CacheInterface",
            "LedgerInterface",
            "KnowledgeInterface",
            "SecretsInterface",
            "ObservabilityInterface",
            "OutputStorageInterface",
            "VectorStoreInterface",
            "EmbeddingInterface",
            "OAuthProviderInterface",
        ]
        for interface in required_interfaces:
            assert interface in exports, f"{interface} not in __init__.__all__"

    def test_all_models_exported(self):
        """Key model types must be in __init__.__all__."""
        from .. import __all__ as exports

        required_models = [
            "AgentContext",
            "AgentResult",
            "AgentStatus",
            "LLMRequest",
            "LLMResponse",
            "StorageRecord",
            "LedgerEntry",
            "LedgerEventType",
            "KnowledgeRetrievalQuery",
            "LogRecord",
            "LogLevel",
            "OutputFormat",
            "VectorRecord",
        ]
        for model in required_models:
            assert model in exports, f"{model} not in __init__.__all__"


# ===========================================================================
# 8. Concrete Agent Execution Tests
# ===========================================================================


class TestAgentExecution:
    """Verify agent execution flow through the interface."""

    @pytest.mark.asyncio
    async def test_agent_execute_returns_result(self):
        """Concrete agent execute() returns AgentResult."""
        impl = ConcreteAgentImpl()
        ctx = AgentContext(
            engagement_id="e1", session_id="s1", correlation_id="c1",
            stage_name="discovery", structured_requirements={},
            prior_agent_outputs={}, retrieved_knowledge={},
            architect_feedback={}, model_id="test-model",
            prompt_version="1.0.0", agent_parameters={},
            max_tokens=4000, temperature=0.0, engagement_domain="test",
        )
        result = await impl.execute(ctx)
        assert isinstance(result, AgentResult)
        assert result.status == AgentStatus.COMPLETED
        assert result.agent_id == "test"

    @pytest.mark.asyncio
    async def test_llm_check_availability(self):
        """Concrete LLM adapter check_availability returns bool."""
        impl = ConcreteLLMImpl()
        result = await impl.check_availability()
        assert isinstance(result, bool)
        assert result is True

    @pytest.mark.asyncio
    async def test_storage_read_returns_none_on_miss(self):
        """Concrete storage read returns None on cache miss."""
        impl = ConcreteStorageImpl()
        result = await impl.read("collection", "missing-key")
        assert result is None

    @pytest.mark.asyncio
    async def test_secrets_get_returns_value(self):
        """Concrete secrets adapter returns SecretValue."""
        impl = ConcreteSecretsImpl()
        result = await impl.get_secret("test-secret")
        assert isinstance(result, SecretValue)
        assert result.secret_name == "test-secret"

    @pytest.mark.asyncio
    async def test_embedding_generate_returns_result(self):
        """Concrete embedding adapter returns EmbeddingResult."""
        impl = ConcreteEmbeddingImpl()
        result = await impl.generate("test text")
        assert isinstance(result, EmbeddingResult)
        assert len(result.vector) == 2

    def test_observability_log_does_not_raise(self):
        """Observability log must not raise on any input."""
        impl = ConcreteObservabilityImpl()
        record = LogRecord(level=LogLevel.ERROR, message="test error", module="test", operation="test_op", correlation_id="c1")
        impl.log(record)  # Must not raise

    def test_agent_get_agent_id(self):
        """Concrete agent returns stable AGENT_ID."""
        impl = ConcreteAgentImpl()
        assert impl.get_agent_id() == "test_agent"

    def test_agent_get_category(self):
        """Concrete agent returns valid pipeline category."""
        impl = ConcreteAgentImpl()
        assert impl.get_agent_category() in ("discovery", "design", "validation", "governance")
