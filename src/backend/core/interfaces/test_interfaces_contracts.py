"""Smoke tests for interface contracts to ensure they are importable and expose expected symbols.

These tests contain no logic and exist only to exercise the interface modules
so coverage and import-time checks validate the contracts.
"""

from __future__ import annotations

from src.backend.core.interfaces import (
    agent_interface as agent_interface_mod,
    llm_interface as llm_interface_mod,
    knowledge_interface as knowledge_interface_mod,
    storage_interface as storage_interface_mod,
    cache_interface as cache_interface_mod,
    ledger_interface as ledger_interface_mod,
)


def test_agent_interface_exports() -> None:
    assert hasattr(agent_interface_mod, "AgentInterface")
    assert hasattr(agent_interface_mod, "AgentContext")
    assert hasattr(agent_interface_mod, "AgentResult")


def test_llm_interface_exports() -> None:
    assert hasattr(llm_interface_mod, "LLMInterface")
    assert hasattr(llm_interface_mod, "LLMResponse")


def test_knowledge_interface_exports() -> None:
    assert hasattr(knowledge_interface_mod, "KnowledgeInterface")
    assert hasattr(knowledge_interface_mod, "RetrievedContext")


def test_storage_cache_ledger_exports() -> None:
    assert hasattr(storage_interface_mod, "StorageInterface")
    assert hasattr(cache_interface_mod, "CacheInterface")
    assert hasattr(ledger_interface_mod, "LedgerInterface")


def test_observability_implementation_smoke() -> None:
    # Import the concrete components from the observability package
    from src.backend.infrastructure.observability import (
        Logger,
        Metrics,
        TraceHandle,
    )

    log = Logger()
    metrics = Metrics()

    # exercise logging paths
    log.emit_log("info", "test message", {"k": "v"})
    log.emit_log("error", "err message")

    # metrics should be recorded in the in-memory store
    metrics.emit_metric("test.metric", 3.14, {"env": "test"})
    assert metrics._metrics.get("test.metric") == 3.14

    # tracing returns a context manager via start_trace helper
    from src.backend.infrastructure.observability import start_trace

    handle = start_trace("unit-test-trace", {"x": 1})
    with handle:
        pass


def test_infrastructure_implementations_smoke() -> None:
    # Cache
    from src.backend.infrastructure.cache.cache_service import CacheService
    from src.backend.infrastructure.cache.retrieval_cache import RetrievalCache

    cache = CacheService()
    cache.set("k1", "v1", ttl_seconds=1)
    assert cache.get("k1") == "v1"
    cache.delete("k1")
    assert cache.get("k1") is None

    rc = RetrievalCache(cache)
    val = rc.get_or_set("k2", lambda: "computed", ttl_seconds=1)
    assert val == "computed"

    # Storage
    from src.backend.infrastructure.storage.storage_service import StorageService
    from src.backend.infrastructure.storage.session_store import SessionStore
    from src.backend.infrastructure.storage.engagement_store import EngagementStore

    storage = StorageService()
    storage.put("s:1", {"x": 1})
    assert storage.get("s:1") == {"x": 1}
    assert list(storage.query("s:"))
    storage.delete("s:1")

    ss = SessionStore(storage, prefix="s:")
    ss.put_session("1", {"y": 2})
    assert ss.get_session("1") == {"y": 2}
    ss.delete_session("1")

    es = EngagementStore(storage, prefix="e:")
    es.put_engagement("e1", {"name": "eng"})
    assert es.get_engagement("e1") == {"name": "eng"}
    assert list(es.list_engagements())

    # Secrets
    from src.backend.infrastructure.secrets.secrets_manager import SecretsManager

    sm = SecretsManager({"k": "secret"})
    assert sm.get_secret("k") == "secret"
    assert sm.get_secret("missing") is None

    # Decision ledger
    from src.backend.infrastructure.decision_ledger.ledger_service import (
        LedgerService,
    )

    ledger = LedgerService()
    ledger.append({"engagement_id": "e1", "payload": {"a": 1}})
    assert list(ledger.read_by_engagement("e1"))
    assert list(ledger.query())

    # Ledger schema dataclass instantiation
    from src.backend.infrastructure.decision_ledger.ledger_schema import LedgerRecord

    lr = LedgerRecord(engagement_id="e1", timestamp_iso="2020-01-01T00:00:00Z", payload={"a":1})
    assert lr.engagement_id == "e1"

    # LLM
    from src.backend.infrastructure.llm.llm_client import LLMClient
    from src.backend.infrastructure.llm.anthropic_adapter import AnthropicAdapter
    from src.backend.infrastructure.llm.openai_adapter import OpenAIAdapter
    from src.backend.infrastructure.llm.response_parser import parse_response

    client = LLMClient()
    resp = client.invoke("hello", "model")
    assert resp.text == "hello"

    aa = AnthropicAdapter()
    assert aa.invoke("hi", "m").text == "hi"

    oa = OpenAIAdapter()
    assert oa.invoke("yo", "m").text == "yo"

    assert parse_response(resp) == "hello"


def test_observability_correlation_and_logger_branches() -> None:
    # Correlation manager: new_id and validate
    from src.backend.infrastructure.observability.correlation import CorrelationManager

    cid = CorrelationManager.new_id()
    assert CorrelationManager.validate(cid) is True
    assert CorrelationManager.validate(None) is False
    assert CorrelationManager.validate("not-a-uuid") is False

    # Logger exercise other levels
    from src.backend.infrastructure.observability.logger import Logger

    l = Logger()
    l.emit_log("debug", "dbg")
    l.emit_log("warning", "warn")
    l.emit_log("critical", "crit")
