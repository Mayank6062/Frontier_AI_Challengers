"""
Interfaces Module — Core Layer Contract Library.

Defines every interface contract that the Infrastructure Layer implements
and the Application Core consumes. Contains no logic, no helper methods,
and no concrete implementations — only abstract method signatures and
their complete documentation.

Single Responsibility:
    Be the single source of truth for all interface contracts in the platform.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6
    REPOSITORY_MASTER_STRUCTURE.md Section 3 (core/interfaces/ file tree)

Module Contents:
    agent_interface.py        — Base execution contract for all 12 agents
    llm_interface.py          — LLM provider adapter contract
    storage_interface.py      — Persistent structured storage contract
    cache_interface.py        — Cache adapter contract
    ledger_interface.py       — Immutable Decision Ledger contract
    knowledge_interface.py    — Enterprise knowledge base service contract
    secrets_interface.py      — Secrets retrieval contract
    observability_interface.py — Logging, tracing, and metrics contract
    output_storage_interface.py — Output artifact storage contract
    vector_store_interface.py  — Vector index contract
    embedding_interface.py    — Embedding generation contract
    oauth_interface.py        — OAuth provider contract

Dependency Rules (REPOSITORY_MASTER_STRUCTURE.md Section 2.4):
    ALLOWED imports: Python stdlib, src/backend/shared/
    FORBIDDEN imports: src/backend/infrastructure/, src/backend/agents/,
                       src/backend/api/, src/backend/knowledge/,
                       src/backend/output/, src/backend/orchestration/

Consumers:
    src/backend/core/        — Business logic depends on these interfaces
    src/backend/infrastructure/ — Implements these interfaces
    src/backend/agents/      — Agents consume LLM and Knowledge interfaces
    src/backend/knowledge/   — Consumes Storage, VectorStore, Embedding
    src/backend/output/      — Consumes OutputStorage interface
    src/backend/orchestration/ — Consumes AgentInterface for dispatch
"""
