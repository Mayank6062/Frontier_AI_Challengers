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
