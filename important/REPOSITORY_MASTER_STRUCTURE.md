# REPOSITORY_MASTER_STRUCTURE.md

> **Document Classification:** Repository Architecture — Source of Truth  
> **Parent Document:** ARCHITECTURE_VISION.md v1.0.0  
> **Status:** Approved — Foundation Release  
> **Version:** 1.0.0  
> **Authority:** This document defines the structure every implementation document must follow. No file, folder, or module may exist that is not accounted for here. Additions require an ADR and an architecture review.

---

## Table of Contents

1. [Repository Philosophy](#1-repository-philosophy)
2. [Repository Design Principles](#2-repository-design-principles)
3. [Complete Repository Tree](#3-complete-repository-tree)
4. [Folder Responsibilities](#4-folder-responsibilities)
5. [File Responsibilities](#5-file-responsibilities)
6. [Layer Ownership](#6-layer-ownership)
7. [Module Boundaries](#7-module-boundaries)
8. [Repository Dependency Rules](#8-repository-dependency-rules)
9. [Configuration Strategy](#9-configuration-strategy)
10. [Documentation Strategy](#10-documentation-strategy)
11. [Testing Strategy Structure](#11-testing-strategy-structure)
12. [AI Repository Structure](#12-ai-repository-structure)
13. [Generated Outputs Structure](#13-generated-outputs-structure)
14. [Deployment Structure](#14-deployment-structure)
15. [Future Scalability](#15-future-scalability)
16. [Repository Standards](#16-repository-standards)
17. [Repository Governance](#17-repository-governance)
18. [Future Expansion Strategy](#18-future-expansion-strategy)
19. [Architecture Validation Checklist](#19-architecture-validation-checklist)
20. [Repository Freeze Rules](#20-repository-freeze-rules)

---

## 1. Repository Philosophy

### 1.1 The Repository Is the System

The ArchitectIQ repository is not a collection of files that represents the system — it is the authoritative, versioned, living specification of the system itself. Every architectural boundary, every module responsibility, every agent contract, and every interface definition must be traceable to a file or folder in this repository. A decision that exists only in memory or conversation is not a decision for this platform.

### 1.2 Structure Communicates Architecture

An engineer who has never read a single line of ArchitectIQ's implementation code should be able to read the repository tree and correctly identify: the major components of the system, the layer each component belongs to, the responsibility of each module, and the boundary between frontend and backend, between agents and orchestration, between knowledge and infrastructure. If the repository tree requires explanation to be understood, the structure has failed.

This is not achieved through naming alone — it is achieved through the combination of naming, depth of nesting, and the deliberate assignment of exactly one responsibility per directory. Every directory is named with a noun that describes what it owns, not a verb that describes what it does, and not an adjective that describes how it behaves.

### 1.3 One Directory, One Owner, One Responsibility

Every directory in this repository has exactly one stated responsibility. That responsibility is documented in the directory's `README.md`. No directory owns two different things. No responsibility is shared across two directories without an explicit interface contract governing the communication. When a directory grows to encompass a second responsibility, the directory is refactored — not renamed.

### 1.4 The Dependency Direction Is Invariant

Dependencies in this repository flow in one direction: inward toward the domain core. The frontend depends on the application layer. The application layer depends on the domain core. The domain core defines interfaces that the infrastructure layer implements. The infrastructure layer does not depend on the domain core's business logic — it implements the interfaces the domain core defines. This is Clean Architecture, enforced by linting rules in the CI pipeline, not by convention.

### 1.5 Configuration Floats to the Top

Business logic does not contain configuration. Configuration does not contain business logic. Every value that may change between environments, between domains, or over time lives in the `config/` directory. The `src/` directory contains only code that is stable across configurations. This separation enables the platform to adapt to new domains, new models, and new deployment environments without touching source code.

### 1.6 Tests Are Co-Located with the Code They Test

Unit tests live in the same directory as the module they test. Integration tests live in a dedicated `tests/integration/` directory organized to mirror the source tree. End-to-end tests live in `tests/e2e/`. This co-location ensures that tests and code evolve together, that test files are discoverable by any engineer reading the source, and that deleting a module without deleting its tests is immediately visible.

### 1.7 Nothing Is Generated into the Source Tree

The `src/` directory contains only hand-authored source code. All generated outputs — architecture diagrams, HLD documents, IaC scaffolding, session workspaces — live in the `outputs/` directory. The `outputs/` directory is gitignored for runtime-generated content but version-controlled for golden test fixtures and template outputs.

---

## 2. Repository Design Principles

### 2.1 Folder Ownership Rules

| Rule | Description |
|------|-------------|
| **F-01** | Every top-level directory has a single clearly stated responsibility documented in its README. |
| **F-02** | No top-level directory may import from another top-level directory's internal implementation — only from its exported interfaces. |
| **F-03** | The `src/backend/agents/` directory owns all agent implementations. No agent logic lives anywhere else in the repository. |
| **F-04** | The `config/` directory owns all configuration. No environment-specific value, secret reference, or feature flag lives in `src/`. |
| **F-05** | The `docs/` directory owns all documentation. No documentation is authoritative if it exists only outside this directory. |
| **F-06** | The `tests/` directory at root level owns integration, E2E, performance, security, and golden tests. Unit tests are co-located with source. |
| **F-07** | The `deploy/` directory owns all deployment artifacts. No Dockerfile, Kubernetes manifest, or Terraform module lives in `src/`. |
| **F-08** | The `outputs/` directory owns all generated runtime outputs. No generated file lives in `src/` or `docs/`. |
| **F-09** | The `scripts/` directory owns all automation scripts. No automation script lives inline in source modules. |
| **F-10** | The `plugins/` directory owns the plugin registry and plugin interface. No plugin implementation lives in `src/backend/agents/`. |

### 2.2 Naming Standards

| Target | Convention | Example |
|--------|------------|---------|
| Directories | `kebab-case` | `requirement-intelligence/`, `decision-ledger/` |
| Python files | `snake_case.py` | `state_machine.py`, `base_agent.py` |
| TypeScript/React files | `PascalCase.tsx` for components, `camelCase.ts` for modules | `ChatPanel.tsx`, `sessionStore.ts` |
| Config files | `kebab-case.yaml` | `agent-config.yaml`, `model-config.yaml` |
| Prompt files | `kebab-case.md` or `kebab-case.txt` | `requirement-extraction-prompt.md` |
| Template files | `kebab-case.jinja2` | `hld-template.jinja2` |
| Test files | Mirror source file name + `_test` suffix (Python) or `.test` (TS) | `state_machine_test.py`, `ChatPanel.test.tsx` |
| Documentation files | `SCREAMING_SNAKE_CASE.md` for architecture documents | `ARCHITECTURE_VISION.md` |
| ADR files | `ADR-NNNN-short-description.md` | `ADR-0001-agent-interface-contract.md` |

### 2.3 Layer Separation Rules

| Rule | Description |
|------|-------------|
| **L-01** | The frontend (`src/frontend/`) may only call the backend through the API Gateway — never directly to internal backend services. |
| **L-02** | The API layer (`src/backend/api/`) may only interact with the Application Core (`src/backend/core/`) — never with agents, knowledge, or infrastructure directly. |
| **L-03** | The Application Core (`src/backend/core/`) defines interfaces. It does not implement infrastructure. It does not call agents directly — it calls the Orchestration Layer. |
| **L-04** | The Orchestration Layer (`src/backend/orchestration/`) calls agents. Agents do not call the Orchestration Layer. |
| **L-05** | Agents (`src/backend/agents/`) call the Knowledge Layer and the Infrastructure Layer through defined interfaces. Agents do not call other agents directly — only the Orchestrator mediates agent-to-agent data flow. |
| **L-06** | The Infrastructure Layer (`src/backend/infrastructure/`) implements interfaces defined by the Domain Core. It does not import from agents or orchestration. |

### 2.4 Dependency Direction (Visual Summary)

```
Frontend
    └──► API Gateway (Application Layer)
              └──► Application Core (Domain)
                        └──► Orchestration Layer
                                   └──► Agent Layer
                                             ├──► Knowledge Layer
                                             └──► Infrastructure Layer (via interfaces)
                        └──► Infrastructure Layer (via interfaces defined in Core)
```

**Forbidden directions:** Infrastructure → Core, Agents → Orchestration, API → Agents (bypassing Core), Frontend → Backend internal modules.

---

## 3. Complete Repository Tree

```
architectiq/
│
├── .github/                                   # GitHub platform configuration
│   ├── workflows/                             # CI/CD pipeline definitions
│   │   ├── ci.yaml                            # Main CI pipeline
│   │   ├── cd-staging.yaml                    # Staging deployment pipeline
│   │   ├── cd-production.yaml                 # Production deployment pipeline
│   │   ├── security-scan.yaml                 # Security scanning pipeline
│   │   ├── docs-publish.yaml                  # Documentation publishing
│   │   └── dependency-audit.yaml              # Dependency vulnerability audit
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.md
│   │   ├── feature-request.md
│   │   └── architecture-change.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS                             # Module ownership definitions
│
├── .vscode/                                   # Shared IDE settings
│   ├── settings.json
│   ├── extensions.json
│   └── launch.json
│
├── docs/                                      # Documentation Layer
│   ├── architecture/                          # Architecture documents
│   │   ├── ARCHITECTURE_VISION.md             # Constitutional document
│   │   ├── REPOSITORY_MASTER_STRUCTURE.md     # This document
│   │   ├── TECHNOLOGY_ARCHITECTURE.md
│   │   ├── BACKEND_MODULE_ARCHITECTURE.md
│   │   ├── FRONTEND_MODULE_ARCHITECTURE.md
│   │   ├── AGENT_ARCHITECTURE.md
│   │   ├── ORCHESTRATION_ARCHITECTURE.md
│   │   ├── KNOWLEDGE_BASE_ARCHITECTURE.md
│   │   ├── DATA_ARCHITECTURE.md
│   │   ├── SECURITY_ARCHITECTURE.md
│   │   └── DEPLOYMENT_ARCHITECTURE.md
│   ├── design/                                # Design documents
│   │   ├── ui-design-system.md
│   │   ├── chat-interaction-model.md
│   │   ├── session-persistence-design.md
│   │   ├── engagement-lifecycle-design.md
│   │   └── output-generation-design.md
│   ├── decisions/                             # Architecture Decision Records
│   │   ├── ADR-0001-agent-interface-contract.md
│   │   ├── ADR-0002-state-machine-enforcement.md
│   │   ├── ADR-0003-rag-retrieval-strategy.md
│   │   ├── ADR-0004-decision-ledger-schema.md
│   │   └── ADR-template.md
│   ├── api/                                   # API documentation
│   │   ├── openapi.yaml                       # OpenAPI specification
│   │   ├── websocket-protocol.md
│   │   └── error-codes.md
│   ├── standards/                             # Engineering standards
│   │   ├── CODING_STANDARDS.md
│   │   ├── TESTING_STANDARDS.md
│   │   ├── DOCUMENTATION_STANDARDS.md
│   │   ├── SECURITY_STANDARDS.md
│   │   └── AGENT_DEVELOPMENT_STANDARDS.md
│   ├── guides/                                # Developer guides
│   │   ├── getting-started.md
│   │   ├── local-development.md
│   │   ├── adding-a-new-agent.md
│   │   ├── adding-a-new-domain.md
│   │   ├── adding-a-knowledge-base-entry.md
│   │   ├── adding-an-output-template.md
│   │   └── contributing.md
│   ├── runbooks/                              # Operational runbooks
│   │   ├── incident-response.md
│   │   ├── agent-failure-recovery.md
│   │   ├── knowledge-base-maintenance.md
│   │   ├── decision-ledger-audit.md
│   │   └── deployment-rollback.md
│   └── diagrams/                             # Architecture diagrams (source)
│       ├── platform-overview.mermaid
│       ├── agent-interaction.mermaid
│       ├── data-flow.mermaid
│       ├── engagement-state-machine.mermaid
│       └── dependency-graph.mermaid
│
├── src/                                       # All source code
│   │
│   ├── frontend/                              # Presentation Layer
│   │   ├── src/
│   │   │   ├── components/                    # Reusable UI components
│   │   │   │   ├── sessions/                  # Sessions panel components
│   │   │   │   │   ├── SessionSidebar.tsx
│   │   │   │   │   ├── SessionCard.tsx
│   │   │   │   │   ├── SessionSearch.tsx
│   │   │   │   │   ├── SessionGroup.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── chat/                      # Chat panel components
│   │   │   │   │   ├── ChatPanel.tsx
│   │   │   │   │   ├── ChatMessage.tsx
│   │   │   │   │   ├── ChatInput.tsx
│   │   │   │   │   ├── ChatHistory.tsx
│   │   │   │   │   ├── TypingIndicator.tsx
│   │   │   │   │   ├── AgentStatusBadge.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── workspace/                 # Workspace panel components
│   │   │   │   │   ├── WorkspacePanel.tsx
│   │   │   │   │   ├── RequirementsView.tsx
│   │   │   │   │   ├── ArchitectureView.tsx
│   │   │   │   │   ├── ValidationView.tsx
│   │   │   │   │   ├── ReviewGate.tsx
│   │   │   │   │   ├── OutputView.tsx
│   │   │   │   │   ├── DiagramViewer.tsx
│   │   │   │   │   ├── DecisionLedgerView.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── shared/                    # Shared UI components
│   │   │   │   │   ├── Button.tsx
│   │   │   │   │   ├── Badge.tsx
│   │   │   │   │   ├── Card.tsx
│   │   │   │   │   ├── Modal.tsx
│   │   │   │   │   ├── Spinner.tsx
│   │   │   │   │   ├── Tooltip.tsx
│   │   │   │   │   ├── ProgressBar.tsx
│   │   │   │   │   ├── StatusIndicator.tsx
│   │   │   │   │   ├── ErrorBoundary.tsx
│   │   │   │   │   ├── EmptyState.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   └── layouts/                   # Layout wrappers
│   │   │   │       ├── ThreePanelLayout.tsx
│   │   │   │       ├── AuthLayout.tsx
│   │   │   │       └── index.ts
│   │   │   ├── pages/                         # Page-level components
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   ├── WorkspacePage.tsx
│   │   │   │   ├── HistoryPage.tsx
│   │   │   │   └── NotFoundPage.tsx
│   │   │   ├── hooks/                         # Custom React hooks
│   │   │   │   ├── useSession.ts
│   │   │   │   ├── useChat.ts
│   │   │   │   ├── useWorkspace.ts
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useEngagement.ts
│   │   │   │   └── useWebSocket.ts
│   │   │   ├── stores/                        # Client state management
│   │   │   │   ├── sessionStore.ts
│   │   │   │   ├── chatStore.ts
│   │   │   │   ├── workspaceStore.ts
│   │   │   │   ├── authStore.ts
│   │   │   │   └── engagementStore.ts
│   │   │   ├── services/                      # API client layer
│   │   │   │   ├── api-client.ts              # Base API client
│   │   │   │   ├── session-service.ts
│   │   │   │   ├── chat-service.ts
│   │   │   │   ├── engagement-service.ts
│   │   │   │   ├── output-service.ts
│   │   │   │   └── auth-service.ts
│   │   │   ├── types/                         # TypeScript type definitions
│   │   │   │   ├── session.types.ts
│   │   │   │   ├── chat.types.ts
│   │   │   │   ├── engagement.types.ts
│   │   │   │   ├── workspace.types.ts
│   │   │   │   ├── agent.types.ts
│   │   │   │   └── api.types.ts
│   │   │   ├── utils/                         # Frontend utility functions
│   │   │   │   ├── date-formatter.ts
│   │   │   │   ├── markdown-renderer.ts
│   │   │   │   ├── diagram-renderer.ts
│   │   │   │   └── error-handler.ts
│   │   │   ├── constants/                     # Frontend constants
│   │   │   │   ├── routes.ts
│   │   │   │   ├── api-endpoints.ts
│   │   │   │   └── ui-constants.ts
│   │   │   ├── router/                        # Client-side routing
│   │   │   │   └── AppRouter.tsx
│   │   │   └── App.tsx                        # Root application component
│   │   ├── public/                            # Static public assets
│   │   │   ├── favicon.ico
│   │   │   └── index.html
│   │   ├── tests/                             # Frontend tests
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── stores/
│   │   │   └── services/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   ├── .eslintrc.cjs
│   │   ├── .prettierrc
│   │   └── .env.example
│   │
│   └── backend/                               # Backend — all Python
│       │
│       ├── api/                               # Application Layer (API Gateway)
│       │   ├── v1/                            # API version 1
│       │   │   ├── routers/                   # Route modules
│       │   │   │   ├── auth_router.py
│       │   │   │   ├── session_router.py
│       │   │   │   ├── engagement_router.py
│       │   │   │   ├── chat_router.py
│       │   │   │   ├── workspace_router.py
│       │   │   │   └── output_router.py
│       │   │   └── __init__.py
│       │   ├── middleware/                    # Request middleware
│       │   │   ├── auth_middleware.py
│       │   │   ├── rate_limit_middleware.py
│       │   │   ├── correlation_id_middleware.py
│       │   │   ├── logging_middleware.py
│       │   │   └── error_handler_middleware.py
│       │   ├── schemas/                       # Pydantic request/response schemas
│       │   │   ├── auth_schemas.py
│       │   │   ├── session_schemas.py
│       │   │   ├── engagement_schemas.py
│       │   │   ├── chat_schemas.py
│       │   │   ├── workspace_schemas.py
│       │   │   └── output_schemas.py
│       │   ├── dependencies/                  # FastAPI dependency injection
│       │   │   ├── auth_deps.py
│       │   │   ├── session_deps.py
│       │   │   └── service_deps.py
│       │   └── main.py                        # FastAPI application entry point
│       │
│       ├── core/                              # Domain Core (Application Layer)
│       │   ├── engagement/                    # Engagement lifecycle management
│       │   │   ├── state_machine.py           # Engagement state machine
│       │   │   ├── engagement_manager.py      # Engagement lifecycle orchestration
│       │   │   ├── engagement_repository.py   # Engagement persistence interface
│       │   │   └── models.py                  # Engagement domain models
│       │   ├── session/                       # Session management
│       │   │   ├── session_manager.py
│       │   │   ├── session_repository.py      # Session persistence interface
│       │   │   └── models.py
│       │   ├── auth/                          # Authentication domain
│       │   │   ├── github_oauth.py
│       │   │   ├── token_manager.py
│       │   │   └── models.py
│       │   ├── review/                        # Human review workflow
│       │   │   ├── review_manager.py
│       │   │   ├── approval_workflow.py
│       │   │   └── models.py
│       │   └── interfaces/                    # Core interface contracts
│       │       ├── agent_interface.py         # Base agent interface
│       │       ├── storage_interface.py
│       │       ├── cache_interface.py
│       │       ├── ledger_interface.py
│       │       ├── knowledge_interface.py
│       │       └── llm_interface.py           # LLM abstraction interface
│       │
│       ├── orchestration/                     # Orchestration Layer
│       │   ├── master_orchestrator.py         # Top-level pipeline coordinator
│       │   ├── agent_scheduler.py             # Agent task scheduling
│       │   ├── pipeline_manager.py            # Pipeline stage management
│       │   ├── result_aggregator.py           # Agent output aggregation
│       │   ├── message_bus.py                 # Inter-agent message bus
│       │   ├── pipeline_stages/               # Pipeline stage definitions
│       │   │   ├── discovery_stage.py
│       │   │   ├── design_stage.py
│       │   │   ├── validation_stage.py
│       │   │   ├── review_stage.py
│       │   │   └── output_stage.py
│       │   └── models.py                      # Orchestration domain models
│       │
│       ├── agents/                            # Agent Layer — 12 agents
│       │   ├── base/                          # Base agent infrastructure
│       │   │   ├── base_agent.py              # Abstract base agent class
│       │   │   ├── agent_context.py           # Shared execution context
│       │   │   ├── agent_result.py            # Standardized result model
│       │   │   ├── agent_registry.py          # Agent discovery registry
│       │   │   └── agent_validator.py         # Output validation framework
│       │   │
│       │   ├── discovery/                     # Discovery Agents
│       │   │   ├── requirement_intelligence/
│       │   │   │   ├── agent.py               # Agent implementation
│       │   │   │   ├── extractor.py           # Requirement extraction logic
│       │   │   │   ├── classifier.py          # NFR / functional classifier
│       │   │   │   ├── ambiguity_detector.py  # Gap and ambiguity flagging
│       │   │   │   ├── models.py              # Agent-specific models
│       │   │   │   ├── tests/
│       │   │   │   │   ├── test_agent.py
│       │   │   │   │   ├── test_extractor.py
│       │   │   │   │   └── fixtures/
│       │   │   │   └── README.md
│       │   │   └── knowledge_retrieval/
│       │   │       ├── agent.py
│       │   │       ├── retriever.py           # RAG retrieval implementation
│       │   │       ├── ranker.py              # Result relevance ranking
│       │   │       ├── citation_builder.py    # Source citation construction
│       │   │       ├── models.py
│       │   │       ├── tests/
│       │   │       └── README.md
│       │   │
│       │   ├── design/                        # Design Agents
│       │   │   ├── architecture_design/
│       │   │   │   ├── agent.py
│       │   │   │   ├── candidate_generator.py
│       │   │   │   ├── tradeoff_analyzer.py
│       │   │   │   ├── pattern_composer.py
│       │   │   │   ├── models.py
│       │   │   │   ├── tests/
│       │   │   │   └── README.md
│       │   │   ├── technology_recommendation/
│       │   │   │   ├── agent.py
│       │   │   │   ├── scorer.py              # Technology scoring framework
│       │   │   │   ├── catalog_searcher.py    # Technology catalog queries
│       │   │   │   ├── build_vs_buy.py        # Build vs buy analysis
│       │   │   │   ├── models.py
│       │   │   │   ├── tests/
│       │   │   │   └── README.md
│       │   │   └── infrastructure_recommendation/
│       │   │       ├── agent.py
│       │   │       ├── topology_designer.py
│       │   │       ├── iac_scaffolder.py
│       │   │       ├── landing_zone_mapper.py
│       │   │       ├── models.py
│       │   │       ├── tests/
│       │   │       └── README.md
│       │   │
│       │   ├── validation/                    # Validation Agents
│       │   │   ├── security/
│       │   │   │   ├── agent.py
│       │   │   │   ├── threat_modeler.py
│       │   │   │   ├── control_mapper.py
│       │   │   │   ├── finding_classifier.py
│       │   │   │   ├── models.py
│       │   │   │   ├── tests/
│       │   │   │   └── README.md
│       │   │   ├── cost_optimization/
│       │   │   │   ├── agent.py
│       │   │   │   ├── tco_modeler.py
│       │   │   │   ├── cost_estimator.py
│       │   │   │   ├── optimization_advisor.py
│       │   │   │   ├── models.py
│       │   │   │   ├── tests/
│       │   │   │   └── README.md
│       │   │   ├── compliance/
│       │   │   │   ├── agent.py
│       │   │   │   ├── framework_evaluator.py
│       │   │   │   ├── control_checker.py
│       │   │   │   ├── residency_validator.py
│       │   │   │   ├── models.py
│       │   │   │   ├── tests/
│       │   │   │   └── README.md
│       │   │   └── risk_assessment/
│       │   │       ├── agent.py
│       │   │       ├── risk_aggregator.py
│       │   │       ├── risk_scorer.py
│       │   │       ├── mitigation_advisor.py
│       │   │       ├── models.py
│       │   │       ├── tests/
│       │   │       └── README.md
│       │   │
│       │   └── governance/                    # Governance Agents
│       │       ├── governance/
│       │       │   ├── agent.py
│       │       │   ├── policy_enforcer.py
│       │       │   ├── guardrail_checker.py
│       │       │   ├── catalog_validator.py
│       │       │   ├── models.py
│       │       │   ├── tests/
│       │       │   └── README.md
│       │       ├── human_collaboration/
│       │       │   ├── agent.py
│       │       │   ├── proposal_packager.py
│       │       │   ├── feedback_router.py
│       │       │   ├── override_recorder.py
│       │       │   ├── models.py
│       │       │   ├── tests/
│       │       │   └── README.md
│       │       └── documentation/
│       │           ├── agent.py
│       │           ├── hld_generator.py
│       │           ├── lld_generator.py
│       │           ├── executive_summary_generator.py
│       │           ├── risk_register_generator.py
│       │           ├── assumptions_log_generator.py
│       │           ├── diagram_generator.py
│       │           ├── models.py
│       │           ├── tests/
│       │           └── README.md
│       │
│       ├── knowledge/                         # Knowledge Layer
│       │   ├── knowledge_base/
│       │   │   ├── knowledge_base.py          # Knowledge base service
│       │   │   ├── entry_model.py             # Knowledge entry schema
│       │   │   ├── indexer.py                 # Vector index management
│       │   │   └── tests/
│       │   ├── rag_engine/
│       │   │   ├── rag_engine.py              # RAG orchestration
│       │   │   ├── semantic_searcher.py       # Semantic similarity search
│       │   │   ├── structured_filter.py       # Structured metadata filter
│       │   │   ├── result_ranker.py           # Multi-signal result ranking
│       │   │   ├── context_builder.py         # Retrieved context assembly
│       │   │   └── tests/
│       │   └── ingestion_pipeline/
│       │       ├── ingestion_pipeline.py      # Ingestion orchestration
│       │       ├── document_parser.py         # Document format parsing
│       │       ├── chunk_splitter.py          # Text chunking strategy
│       │       ├── embedder.py                # Embedding generation
│       │       ├── approval_gate.py           # Human approval for ingestion
│       │       └── tests/
│       │
│       ├── outputs/                           # Output Generation Layer
│       │   ├── generators/                    # Format-specific generators
│       │   │   ├── markdown_generator.py
│       │   │   ├── html_generator.py
│       │   │   ├── pdf_generator.py
│       │   │   ├── diagram_generator.py       # Mermaid / Graphviz
│       │   │   ├── json_generator.py
│       │   │   └── iac_generator.py
│       │   ├── renderers/                     # Rendering engines
│       │   │   ├── mermaid_renderer.py
│       │   │   ├── graphviz_renderer.py
│       │   │   └── html_renderer.py
│       │   ├── packager.py                    # Output bundle assembly
│       │   └── tests/
│       │
│       ├── infrastructure/                    # Infrastructure Layer (implementations)
│       │   ├── decision_ledger/
│       │   │   ├── ledger_service.py          # Implements ledger_interface.py
│       │   │   ├── ledger_schema.py           # Ledger record schemas
│       │   │   └── tests/
│       │   ├── storage/
│       │   │   ├── storage_service.py         # Implements storage_interface.py
│       │   │   ├── session_store.py
│       │   │   ├── engagement_store.py
│       │   │   └── tests/
│       │   ├── cache/
│       │   │   ├── cache_service.py           # Implements cache_interface.py
│       │   │   ├── retrieval_cache.py
│       │   │   └── tests/
│       │   ├── llm/
│       │   │   ├── llm_client.py              # Implements llm_interface.py
│       │   │   ├── anthropic_adapter.py       # Anthropic model adapter
│       │   │   ├── openai_adapter.py          # OpenAI model adapter (future)
│       │   │   ├── response_parser.py
│       │   │   └── tests/
│       │   ├── observability/
│       │   │   ├── logger.py                  # Structured logging
│       │   │   ├── tracer.py                  # Distributed tracing
│       │   │   ├── metrics.py                 # Metrics emission
│       │   │   └── correlation.py             # Correlation ID management
│       │   └── secrets/
│       │       ├── secrets_manager.py
│       │       └── tests/
│       │
│       ├── shared/                            # Shared Backend Utilities
│       │   ├── models/                        # Shared Pydantic models
│       │   │   ├── base_model.py
│       │   │   ├── identifiers.py             # UUID generation standards
│       │   │   └── timestamps.py              # UTC timestamp standards
│       │   ├── exceptions/                    # Custom exception hierarchy
│       │   │   ├── base_exception.py
│       │   │   ├── agent_exceptions.py
│       │   │   ├── knowledge_exceptions.py
│       │   │   ├── ledger_exceptions.py
│       │   │   └── validation_exceptions.py
│       │   ├── utils/                         # Shared utility functions
│       │   │   ├── text_utils.py
│       │   │   ├── hash_utils.py
│       │   │   ├── retry_utils.py
│       │   │   └── sanitizer.py              # Input sanitization
│       │   └── constants/                     # Shared constants
│       │       ├── agent_constants.py
│       │       ├── engagement_states.py
│       │       └── platform_constants.py
│       │
│       ├── tests/                             # Backend co-located unit tests
│       │   └── conftest.py                    # Shared test fixtures
│       │
│       ├── pyproject.toml                     # Python project configuration
│       ├── requirements.txt                   # Production dependencies
│       ├── requirements-dev.txt               # Development dependencies
│       └── .env.example                       # Environment variable template
│
├── config/                                    # Configuration Layer
│   ├── environments/                          # Per-environment configuration
│   │   ├── base.yaml                          # Base config (all envs inherit)
│   │   ├── development.yaml
│   │   ├── staging.yaml
│   │   └── production.yaml
│   ├── agents/                                # Per-agent configuration
│   │   ├── requirement-intelligence.yaml
│   │   ├── knowledge-retrieval.yaml
│   │   ├── architecture-design.yaml
│   │   ├── technology-recommendation.yaml
│   │   ├── infrastructure-recommendation.yaml
│   │   ├── security.yaml
│   │   ├── cost-optimization.yaml
│   │   ├── compliance.yaml
│   │   ├── risk-assessment.yaml
│   │   ├── governance.yaml
│   │   ├── human-collaboration.yaml
│   │   └── documentation.yaml
│   ├── models/                                # LLM model configurations
│   │   ├── anthropic.yaml
│   │   ├── model-registry.yaml                # All available model specs
│   │   └── model-selection-rules.yaml         # Per-agent model assignment rules
│   ├── prompts/                               # Prompt template library
│   │   ├── agents/                            # Per-agent prompt templates
│   │   │   ├── requirement-intelligence/
│   │   │   │   ├── v1.0/
│   │   │   │   │   ├── system-prompt.md
│   │   │   │   │   ├── extraction-prompt.md
│   │   │   │   │   └── clarification-prompt.md
│   │   │   │   └── CHANGELOG.md
│   │   │   ├── knowledge-retrieval/
│   │   │   │   └── v1.0/
│   │   │   ├── architecture-design/
│   │   │   │   └── v1.0/
│   │   │   ├── technology-recommendation/
│   │   │   │   └── v1.0/
│   │   │   ├── infrastructure-recommendation/
│   │   │   │   └── v1.0/
│   │   │   ├── security/
│   │   │   │   └── v1.0/
│   │   │   ├── cost-optimization/
│   │   │   │   └── v1.0/
│   │   │   ├── compliance/
│   │   │   │   └── v1.0/
│   │   │   ├── risk-assessment/
│   │   │   │   └── v1.0/
│   │   │   ├── governance/
│   │   │   │   └── v1.0/
│   │   │   ├── human-collaboration/
│   │   │   │   └── v1.0/
│   │   │   └── documentation/
│   │   │       └── v1.0/
│   │   └── shared/                            # Shared prompt fragments
│   │       ├── enterprise-context.md
│   │       ├── output-format-instructions.md
│   │       ├── citation-instructions.md
│   │       └── uncertainty-handling.md
│   ├── templates/                             # Output document templates
│   │   ├── hld/
│   │   │   ├── v1.0/
│   │   │   │   ├── hld-template.jinja2
│   │   │   │   └── sections/
│   │   │   └── CHANGELOG.md
│   │   ├── lld/
│   │   │   └── v1.0/
│   │   ├── executive-summary/
│   │   │   └── v1.0/
│   │   ├── risk-register/
│   │   │   └── v1.0/
│   │   ├── assumptions-log/
│   │   │   └── v1.0/
│   │   └── diagrams/
│   │       ├── mermaid-theme.yaml
│   │       └── graphviz-styles.yaml
│   ├── knowledge/                             # Knowledge base configuration
│   │   ├── domains/                           # Domain-specific settings
│   │   │   ├── generic.yaml                   # Default domain (always active)
│   │   │   ├── healthcare.yaml                # Healthcare domain config
│   │   │   ├── financial-services.yaml
│   │   │   ├── retail.yaml
│   │   │   └── manufacturing.yaml
│   │   ├── catalogs/                          # Technology catalogs
│   │   │   ├── cloud-services.yaml            # Cloud provider catalog
│   │   │   ├── data-platforms.yaml
│   │   │   ├── streaming-platforms.yaml
│   │   │   ├── storage-solutions.yaml
│   │   │   ├── analytics-tools.yaml
│   │   │   └── security-tools.yaml
│   │   └── retrieval-config.yaml              # RAG retrieval parameters
│   ├── features/                              # Feature flags
│   │   ├── feature-flags.yaml
│   │   └── rollout-strategy.yaml
│   └── constants.yaml                         # Global platform constants
│
├── tests/                                     # Top-Level Testing Layer
│   ├── integration/                           # Integration tests
│   │   ├── api/
│   │   │   ├── test_auth_endpoints.py
│   │   │   ├── test_session_endpoints.py
│   │   │   └── test_engagement_endpoints.py
│   │   ├── agents/
│   │   │   ├── test_pipeline_integration.py
│   │   │   └── test_agent_handoff.py
│   │   ├── knowledge/
│   │   │   └── test_rag_retrieval.py
│   │   └── conftest.py
│   ├── e2e/                                   # End-to-end tests
│   │   ├── flows/
│   │   │   ├── test_complete_engagement_flow.py
│   │   │   ├── test_human_review_flow.py
│   │   │   └── test_session_restore_flow.py
│   │   └── conftest.py
│   ├── agents/                                # Agent-specific tests
│   │   ├── golden/                            # Golden output fixtures
│   │   │   ├── requirement-intelligence/
│   │   │   ├── architecture-design/
│   │   │   └── documentation/
│   │   └── evaluation/                        # Agent quality evaluation
│   │       ├── test_recommendation_quality.py
│   │       └── test_citation_accuracy.py
│   ├── performance/                           # Performance tests
│   │   ├── test_pipeline_throughput.py
│   │   ├── test_rag_latency.py
│   │   └── test_concurrent_engagements.py
│   ├── security/                              # Security tests
│   │   ├── test_prompt_injection.py
│   │   ├── test_auth_bypass.py
│   │   └── test_data_isolation.py
│   ├── regression/                            # Regression tests
│   │   └── test_agent_output_regression.py
│   └── fixtures/                              # Shared test fixtures and data
│       ├── sample_requirements/
│       │   ├── simple-data-lake.txt
│       │   ├── oracle-to-cloud-migration.txt
│       │   └── analytics-platform.txt
│       ├── sample_architectures/
│       └── mock_knowledge_base/
│
├── deploy/                                    # Deployment Layer
│   ├── docker/
│   │   ├── backend/
│   │   │   ├── Dockerfile
│   │   │   └── .dockerignore
│   │   ├── frontend/
│   │   │   ├── Dockerfile
│   │   │   └── .dockerignore
│   │   └── nginx/
│   │       └── nginx.conf
│   ├── kubernetes/
│   │   ├── base/                              # Base Kubernetes manifests
│   │   │   ├── namespace.yaml
│   │   │   ├── backend-deployment.yaml
│   │   │   ├── frontend-deployment.yaml
│   │   │   ├── services.yaml
│   │   │   ├── ingress.yaml
│   │   │   └── configmaps.yaml
│   │   ├── overlays/                          # Kustomize overlays
│   │   │   ├── development/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── monitoring/
│   │       ├── prometheus-config.yaml
│   │       └── grafana-dashboards/
│   ├── terraform/
│   │   ├── modules/                           # Reusable Terraform modules
│   │   │   ├── networking/
│   │   │   ├── compute/
│   │   │   ├── storage/
│   │   │   ├── database/
│   │   │   └── observability/
│   │   ├── environments/
│   │   │   ├── development/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── README.md
│   └── scripts/
│       ├── deploy.sh
│       ├── rollback.sh
│       └── health-check.sh
│
├── scripts/                                   # Development and Utility Scripts
│   ├── setup/
│   │   ├── install-dependencies.sh
│   │   ├── setup-local-env.sh
│   │   └── seed-knowledge-base.sh
│   ├── database/
│   │   ├── migrate.py
│   │   ├── seed.py
│   │   └── reset-dev.py
│   ├── knowledge/
│   │   ├── ingest-pattern.py
│   │   ├── validate-entry.py
│   │   └── export-knowledge-base.py
│   └── utils/
│       ├── generate-correlation-id.py
│       └── validate-config.py
│
├── outputs/                                   # Generated Outputs (runtime)
│   ├── sessions/                              # Per-session workspaces
│   │   └── .gitkeep
│   ├── architectures/                         # Generated architecture artifacts
│   │   └── .gitkeep
│   ├── documents/                             # Generated documents
│   │   └── .gitkeep
│   ├── diagrams/                              # Generated diagrams
│   │   └── .gitkeep
│   ├── logs/                                  # Execution logs
│   │   └── .gitkeep
│   └── temp/                                  # Temporary workspace
│       └── .gitkeep
│
├── plugins/                                   # Plugin System (Phase 2+)
│   ├── interface/
│   │   ├── plugin_interface.py                # Plugin contract definition
│   │   └── README.md
│   ├── registry/
│   │   └── plugin_registry.yaml               # Registered plugins manifest
│   └── examples/
│       └── sample-domain-plugin/
│           ├── manifest.yaml
│           └── README.md
│
├── .gitignore
├── .env.example                               # Root environment template
├── README.md                                  # Repository entry point
├── CONTRIBUTING.md                            # Contribution guidelines
├── CHANGELOG.md                               # Version history
├── LICENSE
├── Makefile                                   # Development task automation
├── docker-compose.yml                         # Local development stack
└── docker-compose.test.yml                    # Test stack
```

---

## 4. Folder Responsibilities

### 4.1 Root Level

| Folder | Why It Exists | What It Owns | Must Never Own | Accessible By |
|--------|--------------|--------------|----------------|---------------|
| `.github/` | GitHub platform integration | Workflows, PR templates, issue templates, CODEOWNERS | Source code, configuration, documentation | CI/CD systems, GitHub platform |
| `docs/` | Documentation layer | All authoritative documentation | Source code, tests, config | All contributors (read); engineers with doc review approval (write) |
| `src/` | All application source code | Frontend and backend source | Deployment artifacts, configs, generated outputs | Engineers by layer (enforced by CODEOWNERS) |
| `config/` | Platform configuration | All environment configs, prompts, templates, feature flags | Business logic, source code | Backend services at runtime; engineers for authoring |
| `tests/` | Integration, E2E, performance, security, and golden tests | All non-unit tests | Unit tests (co-located with source), source code, config | QA engineers, CI/CD pipelines |
| `deploy/` | Deployment artifacts | Docker, Kubernetes, Terraform, deployment scripts | Source code, config, documentation | DevOps engineers, CI/CD pipelines |
| `scripts/` | Development and utility automation | Setup, database, knowledge, utility scripts | Production business logic | Engineers (local use); CI/CD pipelines (specific scripts) |
| `outputs/` | Runtime-generated content | All generated files from platform execution | Source code, config, tests | Platform at runtime; gitignored for dynamic content |
| `plugins/` | Plugin system infrastructure | Plugin interface, registry, examples | Core agent implementations, business logic | Plugin developers (future phase) |

### 4.2 `src/frontend/`

| Sub-folder | Why It Exists | What It Owns | Must Never Own |
|------------|--------------|--------------|----------------|
| `components/sessions/` | Sessions panel rendering | Session list, history, search, grouping components | Chat logic, workspace logic, API calls (uses hooks/services) |
| `components/chat/` | Chat interaction panel | Message rendering, input, typing indicators, agent status | Session management, workspace rendering |
| `components/workspace/` | Architecture workspace panel | Requirements view, architecture view, review gate, output display | Chat state, session state |
| `components/shared/` | Reusable UI primitives | Generic UI components (Button, Modal, Card, Spinner) | Domain-specific logic, API calls |
| `components/layouts/` | Page layout structure | Three-panel layout, auth layout | Page-specific content |
| `stores/` | Client state management | All client-side application state | API call implementation (delegated to services) |
| `services/` | API communication | All HTTP calls to the backend API | UI rendering logic, state management |
| `hooks/` | React hook abstractions | Reusable stateful logic connecting stores and services | Direct API calls, direct store mutations |
| `types/` | TypeScript definitions | All TypeScript types and interfaces | Logic, rendering |
| `constants/` | Frontend constants | Route paths, API endpoint constants, UI constants | Business logic, dynamic values |

### 4.3 `src/backend/`

| Sub-folder | Why It Exists | What It Owns | Must Never Own |
|------------|--------------|--------------|----------------|
| `api/` | HTTP interface layer | Route definitions, middleware, schemas, DI | Business logic, agent logic, infrastructure implementation |
| `core/` | Domain business logic | Engagement state machine, session management, auth, review workflow, interface definitions | Infrastructure implementation, agent logic, HTTP concerns |
| `orchestration/` | Agent pipeline coordination | Master orchestrator, scheduler, pipeline stages, result aggregator, message bus | Agent business logic, infrastructure implementation |
| `agents/` | AI agent implementations | All 12 agent implementations and their supporting logic | Orchestration logic, infrastructure implementation, other agents' internal logic |
| `knowledge/` | Knowledge management | Knowledge base service, RAG engine, ingestion pipeline | Agent business logic, output generation |
| `outputs/` | Output generation | Document generators, diagram renderers, packager | Knowledge retrieval, agent execution |
| `infrastructure/` | Technical infrastructure | Implementations of all core interfaces (storage, cache, LLM, ledger) | Business logic, agent logic |
| `shared/` | Common utilities | Shared models, exceptions, utilities, constants | Module-specific logic, infrastructure implementation |

### 4.4 `config/`

| Sub-folder | Why It Exists | What It Owns | Must Never Own |
|------------|--------------|--------------|----------------|
| `environments/` | Environment-specific values | Database URLs, service endpoints, logging levels per env | Secrets (secrets go to secrets manager) |
| `agents/` | Agent behavior configuration | Per-agent temperature, max tokens, retry settings, timeout | Prompt content (in `prompts/`) |
| `models/` | LLM model configuration | Model identifiers, API base URLs, capability declarations, per-agent model assignments | Credentials |
| `prompts/` | Prompt template library | All system and user prompt templates, versioned per agent | Rendered prompt outputs (runtime) |
| `templates/` | Output document templates | Jinja2 templates for HLD, LLD, summaries, risk registers | Source code, rendered outputs |
| `knowledge/` | Knowledge configuration | Domain configs, technology catalogs, retrieval parameters | Knowledge base content (in storage) |
| `features/` | Feature flag definitions | Feature flag names, rollout percentages, descriptions | Feature implementation |

---

## 5. File Responsibilities

### 5.1 Root Files

| File | Purpose | Responsibility | Future Growth |
|------|---------|---------------|---------------|
| `README.md` | Repository entry point | Describes the platform, how to get started, links to key documents | Updated on every major feature addition |
| `CONTRIBUTING.md` | Contribution guide | Defines the process for contributing: branching, PR, review, ADR | Expanded as governance matures |
| `CHANGELOG.md` | Version history | Records every release with changes, ADRs referenced | Append-only; one entry per release |
| `Makefile` | Task automation | `make setup`, `make test`, `make lint`, `make run`, `make build` | New targets added for new workflows |
| `docker-compose.yml` | Local dev stack | Defines all local services: backend, frontend, database, cache | New services added as platform grows |
| `.env.example` | Environment template | Documents all required environment variables with descriptions | One new line per new required variable |
| `CODEOWNERS` | Ownership mapping | Maps every directory to its owning engineer or team | Updated when ownership changes |

### 5.2 Critical Backend Files

| File | Purpose | Inputs | Outputs | Dependencies |
|------|---------|--------|---------|--------------|
| `src/backend/api/main.py` | FastAPI application entry point | Configuration, registered routers | Running ASGI application | All routers, middleware, DI containers |
| `src/backend/core/engagement/state_machine.py` | Engagement lifecycle state machine | Engagement state, transition trigger | New state, validation result | Engagement models, constants |
| `src/backend/core/interfaces/agent_interface.py` | Base agent contract | — | Abstract interface definition | No dependencies (defines contracts for others) |
| `src/backend/core/interfaces/llm_interface.py` | LLM abstraction contract | — | Abstract interface definition | No dependencies |
| `src/backend/orchestration/master_orchestrator.py` | Pipeline coordination | Engagement context, pipeline stage | Stage results, next stage trigger | Agent registry, pipeline manager, scheduler |
| `src/backend/agents/base/base_agent.py` | Agent abstract base class | Agent context, LLM interface | Agent result (standardized) | LLM interface, agent context, result model |
| `src/backend/infrastructure/decision_ledger/ledger_service.py` | Decision ledger implementation | Ledger entry | Persisted immutable record | Storage interface, ledger schema |
| `src/backend/infrastructure/llm/anthropic_adapter.py` | Anthropic model adapter | Prompt, model config | LLM response | LLM interface, Anthropic SDK |

### 5.3 Critical Configuration Files

| File | Purpose | Responsibility |
|------|---------|---------------|
| `config/environments/base.yaml` | Base configuration | All default values inherited by every environment |
| `config/models/model-registry.yaml` | Model registry | Canonical list of available models with capabilities and identifiers |
| `config/prompts/agents/requirement-intelligence/v1.0/system-prompt.md` | Agent system prompt | The versioned system prompt for the Requirement Intelligence Agent |
| `config/knowledge/catalogs/cloud-services.yaml` | Cloud technology catalog | Cloud service options available to the Technology Recommendation Agent |
| `config/features/feature-flags.yaml` | Feature flags | Runtime feature enablement without code deployment |

### 5.4 Critical Frontend Files

| File | Purpose | Responsibility |
|------|---------|---------------|
| `src/frontend/src/App.tsx` | Root component | Application initialization, router mounting, global providers |
| `src/frontend/src/components/layouts/ThreePanelLayout.tsx` | Primary layout | Renders the canonical three-panel workspace |
| `src/frontend/src/stores/engagementStore.ts` | Engagement state | Manages the lifecycle state of the current engagement on the client |
| `src/frontend/src/services/api-client.ts` | Base HTTP client | All API communication originates from this client |

---

## 6. Layer Ownership

### L1 — Presentation Layer

**Owner:** Frontend Engineering  
**Directory:** `src/frontend/`  
**Responsibility:** Renders the three-panel workspace interface. Manages client-side state. Communicates with the backend exclusively through the API Gateway. Manages GitHub OAuth flow and session persistence on the client.

**What It Owns:**
- All React component rendering
- Client-side state management (stores)
- API client service layer
- TypeScript type definitions for all frontend concerns
- Client-side routing

**What It Must Never Own:**
- Business logic
- Agent logic
- Knowledge retrieval
- Direct database access
- Secret values

**Interface Contract:** All communication with the backend is through versioned REST endpoints defined in `docs/api/openapi.yaml`. The frontend has no knowledge of the backend's internal structure.

---

### L2 — Application Layer

**Owner:** Backend Platform Engineering  
**Directory:** `src/backend/api/` and `src/backend/core/`  
**Responsibility:** Receives HTTP requests from the Presentation Layer. Validates input, enforces rate limiting and authentication. Manages the engagement lifecycle through the state machine. Routes requests to the Orchestration Layer. Defines all interface contracts used by the Infrastructure Layer.

**What It Owns:**
- API route definitions and HTTP concerns
- Request and response schema validation
- Engagement state machine definition
- Session management domain logic
- Authentication domain logic
- All interface definitions (`core/interfaces/`) that lower layers implement

**What It Must Never Own:**
- Agent implementation logic
- Infrastructure implementation (only interfaces)
- Knowledge base content
- Output rendering logic

---

### L3 — Orchestration Layer

**Owner:** Platform AI Engineering  
**Directory:** `src/backend/orchestration/`  
**Responsibility:** Coordinates the execution of agent pipelines. Sequences and parallelizes agent tasks. Routes outputs from one agent stage to the inputs of the next. Aggregates results into a coherent proposal for human review.

**What It Owns:**
- Master orchestrator logic
- Agent scheduling and parallelization
- Pipeline stage management
- Inter-agent data flow
- Result aggregation

**What It Must Never Own:**
- Agent business logic (only invokes agents by interface)
- Infrastructure implementation
- UI concerns
- Knowledge retrieval logic

---

### L4 — Agent Layer

**Owner:** AI Agent Engineering (each agent has a designated owner)  
**Directory:** `src/backend/agents/`  
**Responsibility:** Implements the 12 specialized AI agents. Each agent is independently owned, independently versioned, and independently testable.

**What It Owns:**
- All agent implementations
- Per-agent supporting logic (extractors, scorers, analyzers)
- Per-agent unit tests
- Per-agent domain models

**What It Must Never Own:**
- Orchestration logic
- Infrastructure implementation
- Direct database access (uses infrastructure interfaces)
- Cross-agent state (inter-agent data flows through the Orchestrator)

**Dependency Rule:** Agents depend on: (a) their own supporting logic, (b) the Knowledge Layer (via `knowledge_interface.py`), (c) the LLM (via `llm_interface.py`), (d) infrastructure services (via `storage_interface.py`, `ledger_interface.py`). Agents never depend on other agents or on the Orchestration Layer.

---

### L5 — Knowledge Layer

**Owner:** Data and Knowledge Engineering  
**Directory:** `src/backend/knowledge/`  
**Responsibility:** Manages the enterprise knowledge base. Provides retrieval-augmented generation capability. Runs the knowledge ingestion pipeline for new approved engagements.

**What It Owns:**
- Knowledge base service
- Vector index management
- RAG engine
- Knowledge ingestion pipeline
- Embedding generation

**What It Must Never Own:**
- Agent logic
- Business rule evaluation
- Output rendering

---

### L6 — Infrastructure Layer

**Owner:** Platform Engineering  
**Directory:** `src/backend/infrastructure/`  
**Responsibility:** Implements the interfaces defined in `src/backend/core/interfaces/`. Provides concrete implementations of storage, cache, LLM clients, the Decision Ledger, observability, and secrets management.

**What It Owns:**
- All interface implementations
- Database access code
- LLM client adapters
- Decision Ledger write logic
- Observability instrumentation

**What It Must Never Own:**
- Business logic
- Agent logic
- Interface definitions (only implementations)

---

### L7 — Configuration Layer

**Owner:** Platform Engineering (configuration governance); all teams (configuration content within their domain)  
**Directory:** `config/`  
**Responsibility:** Single location for all configuration — environment settings, agent parameters, model selection, prompt templates, output templates, technology catalogs, knowledge domain settings, feature flags.

---

### L8 — Shared Layer

**Owner:** Platform Engineering  
**Directory:** `src/backend/shared/`  
**Responsibility:** Shared utilities, models, exceptions, and constants used by multiple backend layers. This layer has no business logic — only utility functions and common data structures.

**Critical Rule:** The Shared Layer may be imported by any layer. No other layer may be imported by the Shared Layer. The Shared Layer has zero domain dependencies.

---

### L9 — Testing Layer

**Owner:** QA Engineering + each feature team for unit tests  
**Directory:** `tests/` (root) + co-located unit tests in `src/`  
**Responsibility:** All test code. Unit tests live next to the source they test. All other test types live in `tests/`.

---

### L10 — Deployment Layer

**Owner:** DevOps Engineering  
**Directory:** `deploy/`  
**Responsibility:** All deployment artifacts and infrastructure configuration.

---

### L11 — Documentation Layer

**Owner:** Platform Architecture (architecture docs); each team (module-level docs)  
**Directory:** `docs/`  
**Responsibility:** All authoritative documentation.

---

### L12 — Output Layer

**Owner:** Runtime (generated by platform execution)  
**Directory:** `outputs/`  
**Responsibility:** Stores all runtime-generated content. Gitignored for dynamic content. Version-controlled only for golden test fixtures.

---

## 7. Module Boundaries

### 7.1 Allowed Dependency Map

```
Module                           Can Depend On
─────────────────────────────────────────────────────────────────────
Frontend                         → Backend API (via HTTP only)
API Layer                        → Core (Domain)
API Layer                        → Shared
Core (Domain)                    → Shared
Core (Domain)                    → Interfaces (defines them; does not import implementations)
Orchestration                    → Core (via interfaces)
Orchestration                    → Agents (via agent_interface.py)
Orchestration                    → Shared
Agents (any)                     → agents/base/
Agents (any)                     → Knowledge (via knowledge_interface.py)
Agents (any)                     → Infrastructure (via core interfaces)
Agents (any)                     → Shared
Agents (any)                     → Config (read-only, via config loader in Shared)
Knowledge Layer                  → Infrastructure (via storage_interface.py)
Knowledge Layer                  → Shared
Infrastructure Layer             → core/interfaces/ (implements them)
Infrastructure Layer             → Shared
Outputs Layer                    → Agents (consumes outputs, does not call agents)
Outputs Layer                    → Shared
Outputs Layer                    → Config (templates)
```

### 7.2 Forbidden Dependencies

```
Module                           Must NEVER Depend On
──────────────────────────────────────────────────────────────────────
Infrastructure Layer             → Core (business logic)
Infrastructure Layer             → Agents
Infrastructure Layer             → Orchestration
Agent A                          → Agent B (direct import)
Agents                           → Orchestration Layer
Orchestration                    → Infrastructure (directly — only via Core interfaces)
API Layer                        → Agents (must go through Core)
API Layer                        → Infrastructure (must go through Core interfaces)
Frontend                         → Backend internal modules (only API)
Shared Layer                     → Any layer (zero dependencies)
Config Layer                     → Source code (Config is data, not code)
```

### 7.3 Agent-to-Agent Communication Rule

Agents do not communicate directly. All inter-agent data flow is mediated by the Orchestration Layer. Agent B receives the output of Agent A as an input delivered by the Orchestrator — it does not import Agent A or call Agent A's methods. This enforces the single-responsibility principle at the agent level and ensures that the Orchestrator maintains a complete record of all inter-agent data flow.

---

## 8. Repository Dependency Rules

### 8.1 Allowed Imports

```python
# ALLOWED: Agent importing base agent class
from src.backend.agents.base.base_agent import BaseAgent

# ALLOWED: Agent importing LLM interface (not implementation)
from src.backend.core.interfaces.llm_interface import LLMInterface

# ALLOWED: Agent importing shared utilities
from src.backend.shared.utils.text_utils import sanitize_input

# ALLOWED: Orchestrator importing agent via interface
from src.backend.agents.base.agent_interface import AgentInterface

# ALLOWED: Infrastructure importing interface to implement
from src.backend.core.interfaces.storage_interface import StorageInterface
```

### 8.2 Forbidden Imports

```python
# FORBIDDEN: Agent importing another agent's implementation
from src.backend.agents.design.architecture_design.agent import ArchitectureDesignAgent  # ❌

# FORBIDDEN: Agent importing orchestrator
from src.backend.orchestration.master_orchestrator import MasterOrchestrator  # ❌

# FORBIDDEN: Infrastructure importing agent
from src.backend.agents.validation.security.agent import SecurityAgent  # ❌

# FORBIDDEN: API layer importing infrastructure implementation
from src.backend.infrastructure.storage.storage_service import StorageService  # ❌

# FORBIDDEN: Any layer importing from another layer's private internals
from src.backend.agents.design.architecture_design.internal_logic import _private_fn  # ❌
```

### 8.3 Cross-Module Communication

Cross-module communication between non-adjacent layers is only permitted through:
1. **Defined interface classes** (`core/interfaces/`) for backend service communication.
2. **Versioned REST API contracts** for frontend-to-backend communication.
3. **The Orchestration message bus** for agent-to-agent data delivery.
4. **The Decision Ledger** for inter-session auditability.

### 8.4 Shared Library Usage

The `src/backend/shared/` layer is the only layer that may be imported by all other backend layers without restriction. Any utility that is used by two or more layers belongs in `shared/`. Any utility that is used by only one layer belongs inside that layer's directory.

---

## 9. Configuration Strategy

### 9.1 Where Everything Lives

| Configuration Type | Location | Format | Notes |
|-------------------|----------|--------|-------|
| Environment-specific values | `config/environments/{env}.yaml` | YAML | Inherits from `base.yaml`; no secrets |
| Secrets | Secrets manager (runtime injection) | N/A | Never stored in config files or source |
| Agent behavior parameters | `config/agents/{agent-name}.yaml` | YAML | Temperature, max tokens, retry, timeout |
| LLM model selection | `config/models/model-registry.yaml` | YAML | Model IDs, capabilities, pricing tier |
| Prompt templates | `config/prompts/agents/{agent}/v{N}/` | Markdown | Versioned; one directory per version |
| Output document templates | `config/templates/{type}/v{N}/` | Jinja2 | Versioned; one directory per version |
| Technology catalogs | `config/knowledge/catalogs/*.yaml` | YAML | Domain-specific technology options |
| Feature flags | `config/features/feature-flags.yaml` | YAML | Boolean and percentage rollout flags |
| Global constants | `config/constants.yaml` | YAML | Platform-wide constants |
| Domain configuration | `config/knowledge/domains/*.yaml` | YAML | Per-domain knowledge base settings |

### 9.2 Prompt Versioning Strategy

Every prompt template is versioned with its own directory. When a prompt is changed, a new version directory is created — the previous version directory is never modified. The active version for each agent is declared in `config/agents/{agent-name}.yaml`. This ensures that every output the platform produces can be reproduced: given the same engagement ID and the same agent version, the same prompt is resolvable from the repository history.

```
config/prompts/agents/requirement-intelligence/
├── v1.0/
│   ├── system-prompt.md       ← Never modified after release
│   ├── extraction-prompt.md
│   └── clarification-prompt.md
├── v1.1/
│   ├── system-prompt.md       ← New version for improvement
│   ├── extraction-prompt.md
│   └── clarification-prompt.md
└── CHANGELOG.md               ← Documents every version change and rationale
```

### 9.3 Environment Configuration Hierarchy

```
base.yaml (defaults for all environments)
    ↓ overridden by
development.yaml
    OR staging.yaml
    OR production.yaml
    ↓ further overridden by
Environment variables (for values that differ per deployment instance)
    ↓ secrets resolved by
Secrets manager at runtime
```

No environment-specific value that changes between deployment environments ever lives in source code. The `src/` directory is environment-neutral.

---

## 10. Documentation Strategy

### 10.1 Documentation Locations by Type

| Document Type | Location | Naming Convention | Audience |
|---------------|----------|-------------------|----------|
| Architecture Vision | `docs/architecture/ARCHITECTURE_VISION.md` | `SCREAMING_SNAKE_CASE.md` | All engineers, architects |
| Architecture per layer | `docs/architecture/{LAYER}_ARCHITECTURE.md` | `SCREAMING_SNAKE_CASE.md` | Engineers of that layer |
| Design documents | `docs/design/{topic}.md` | `kebab-case.md` | Engineers |
| Architecture Decision Records | `docs/decisions/ADR-NNNN-description.md` | `ADR-NNNN-kebab.md` | All contributors |
| API documentation | `docs/api/openapi.yaml` | OpenAPI 3.0 YAML | Frontend engineers, API consumers |
| Engineering standards | `docs/standards/*.md` | `SCREAMING_SNAKE_CASE.md` | All engineers |
| Developer guides | `docs/guides/*.md` | `kebab-case.md` | Engineers (onboarding) |
| Operational runbooks | `docs/runbooks/*.md` | `kebab-case.md` | SRE, DevOps |
| Module documentation | `src/backend/agents/{agent}/README.md` | `README.md` | Engineers of that module |
| Diagram source | `docs/diagrams/*.mermaid` | `kebab-case.mermaid` | Architects, engineers |

### 10.2 ADR Lifecycle

```
1. Trigger: Any decision affecting architecture, module boundaries, or Non-Negotiable Rules
2. Draft: Engineer creates ADR-NNNN using template at docs/decisions/ADR-template.md
3. Review: Architecture Review Board reviews the ADR in a pull request
4. Decision: ADR marked Approved or Rejected with reasoning
5. Implementation: Code changes implementing the ADR reference its number in commit message
6. Superseding: If a decision changes, new ADR is created with "Supersedes: ADR-NNNN" field
```

### 10.3 Documentation Currency Rules

- Every module directory must have a `README.md` describing its responsibility, inputs, and outputs.
- A pull request that changes a module's behavior without updating its `README.md` fails the review.
- Architecture documents are reviewed quarterly by the Architecture Review Board and updated for drift.

---

## 11. Testing Strategy Structure

### 11.1 Unit Tests (Co-located)

Unit tests live in a `tests/` subdirectory within the module they test.

```
src/backend/agents/discovery/requirement_intelligence/
├── agent.py
├── extractor.py
└── tests/
    ├── test_agent.py
    ├── test_extractor.py
    └── fixtures/
        ├── sample_input.txt
        └── expected_output.json
```

Coverage requirement: **≥ 85% per module**, enforced in CI.

### 11.2 Integration Tests (`tests/integration/`)

Integration tests verify the interaction between two or more modules. They test the contracts between modules — not the modules' internal implementations. Every integration test:
- Runs against a complete local stack (via `docker-compose.test.yml`)
- Tests one module boundary per test file
- Uses real service implementations (not mocks) unless testing against external systems

### 11.3 End-to-End Tests (`tests/e2e/`)

E2E tests verify complete platform workflows from UI interaction to output generation. Key flows that must have E2E test coverage:
- Complete engagement flow: requirement input → agent pipeline → human review → Final Architecture
- Session restore flow: session created → logout → login → session restored
- Human review flow: proposal generated → architect edits → refinement triggered → updated proposal

### 11.4 Agent Tests (`tests/agents/`)

Agent tests serve two purposes:
1. **Golden output tests:** Given a fixed input and a fixed prompt version, the agent produces an output that matches a known-good fixture within acceptable variance.
2. **Quality evaluation tests:** Measure the quality of agent outputs on a representative input set — measuring precision of requirement extraction, relevance of knowledge retrieval, completeness of architecture generation.

Golden output fixtures live in `tests/agents/golden/` and are version-controlled. Changing a prompt template must be accompanied by updated golden fixtures.

### 11.5 Performance Tests (`tests/performance/`)

| Test | Metric | Target |
|------|--------|--------|
| `test_pipeline_throughput.py` | Concurrent engagement capacity | 50 concurrent engagements |
| `test_rag_latency.py` | Knowledge retrieval p95 latency | < 2 seconds |
| `test_concurrent_engagements.py` | Engagement completion time under load | < 30 minutes p90 |

### 11.6 Security Tests (`tests/security/`)

| Test | What It Validates |
|------|------------------|
| `test_prompt_injection.py` | Malicious input in requirements cannot manipulate agent behavior |
| `test_auth_bypass.py` | Authentication cannot be bypassed for protected endpoints |
| `test_data_isolation.py` | One user's engagement data cannot be accessed by another user's session |

---

## 12. AI Repository Structure

### 12.1 Agent Structure (Canonical Pattern)

Every agent follows this identical directory pattern. No deviation is permitted.

```
src/backend/agents/{category}/{agent-name}/
├── agent.py              # Agent class — implements BaseAgent — single entry point
├── {supporting-logic}.py # Domain-specific supporting logic (multiple files allowed)
├── models.py             # Agent-specific Pydantic models (inputs, outputs)
├── tests/
│   ├── test_agent.py     # Tests for agent.py
│   ├── test_{support}.py # Tests for each supporting logic file
│   └── fixtures/         # Per-agent test fixtures
└── README.md             # Agent specification: responsibility, boundary, inputs, outputs
```

### 12.2 Agent Class Contract

Every agent must:
- Inherit from `BaseAgent` defined in `agents/base/base_agent.py`
- Implement the `execute(context: AgentContext) -> AgentResult` method
- Declare its `AGENT_ID`, `AGENT_VERSION`, and `AGENT_CATEGORY` as class constants
- Never call another agent directly
- Never access the database directly (use infrastructure interfaces)
- Never produce output without a citation or confidence declaration

### 12.3 Prompt Template Structure

```
config/prompts/agents/{agent-name}/v{major}.{minor}/
├── system-prompt.md          # The agent's system role definition
├── {task}-prompt.md          # Task-specific prompt(s)
└── CHANGELOG.md              # What changed in this version and why
```

Prompt files are Markdown for readability and are loaded by a config loader at runtime. Prompt files are versioned: the active version is declared in the agent config.

### 12.4 Knowledge Base Structure

```
Knowledge Base (vector store, managed at runtime)
├── Enterprise Patterns       # Architecture pattern library (generic)
├── Technology Evaluations    # Technology assessments with scoring
├── Approved Precedents       # Prior approved architecture decisions
├── Compliance Frameworks     # Regulatory and policy frameworks per domain
├── Domain Configurations     # Domain-specific pattern overrides
└── Technology Catalogs       # Approved technology catalog per domain
```

Ingestion into the knowledge base is governed by the `ingestion_pipeline/` module and requires human approval via the `approval_gate.py` component.

### 12.5 LLM Adapter Pattern

All agents interact with LLMs exclusively through the `LLMInterface` defined in `core/interfaces/llm_interface.py`. Concrete adapter implementations live in `infrastructure/llm/`. Adding a new LLM provider requires only a new adapter in `infrastructure/llm/` — no agent code changes.

```
infrastructure/llm/
├── llm_client.py             # Factory that returns the correct adapter
├── anthropic_adapter.py      # Implements LLMInterface using Anthropic SDK
├── openai_adapter.py         # Implements LLMInterface using OpenAI SDK (future)
└── response_parser.py        # Normalizes responses across providers
```

---

## 13. Generated Outputs Structure

All runtime-generated content is stored in `outputs/`. This directory is gitignored for dynamic content. The structure mirrors the types of outputs the platform generates.

```
outputs/
├── sessions/                          # Per-session workspaces (gitignored)
│   └── {session-id}/
│       ├── session-metadata.json
│       ├── conversation-history.json
│       └── workspace-state.json
├── architectures/                     # Generated architecture artifacts (gitignored)
│   └── {engagement-id}/
│       ├── candidate-architecture-1.json
│       ├── candidate-architecture-2.json
│       └── approved-architecture.json
├── documents/                         # Generated documents (gitignored)
│   └── {engagement-id}/
│       ├── hld.md
│       ├── hld.pdf
│       ├── lld.md
│       ├── executive-summary.md
│       ├── risk-register.md
│       └── assumptions-log.md
├── diagrams/                          # Generated diagrams (gitignored)
│   └── {engagement-id}/
│       ├── architecture-overview.mermaid
│       ├── architecture-overview.svg
│       ├── data-flow.mermaid
│       ├── architecture.dot            # Graphviz source
│       └── architecture.png
├── logs/                              # Agent execution logs (gitignored)
│   └── {engagement-id}/
│       ├── pipeline-execution.log
│       ├── agent-{agent-id}-execution.log
│       └── decision-ledger-export.json
└── temp/                              # Temporary workspace (gitignored, cleaned)
    └── {session-id}/
        └── .gitkeep
```

**Golden Test Fixtures** (version-controlled) live in `tests/agents/golden/` — not in `outputs/`. The `outputs/` directory is always `.gitignored` for dynamic content.

**Output Format Coverage:**

| Format | Generator | Use Case |
|--------|-----------|----------|
| Markdown (`.md`) | `markdown_generator.py` | HLD, LLD, summaries, risk registers |
| PDF (`.pdf`) | `pdf_generator.py` | Client-ready document delivery |
| Mermaid (`.mermaid`) | `diagram_generator.py` | Architecture diagrams for docs systems |
| Graphviz DOT (`.dot`) | `diagram_generator.py` | Architecture diagrams for advanced rendering |
| SVG (`.svg`) | `graphviz_renderer.py` | Scalable vector diagrams |
| PNG (`.png`) | `graphviz_renderer.py` | Raster diagrams for presentations |
| Interactive HTML (`.html`) | `html_generator.py` | Self-contained interactive architecture reports |
| JSON (`.json`) | `json_generator.py` | Machine-readable architecture state for API consumers |
| Agent execution log (`.log`) | Observability layer | Detailed agent thinking trail for audit |

---

## 14. Deployment Structure

```
deploy/
├── docker/
│   ├── backend/
│   │   ├── Dockerfile              # Multi-stage: build + runtime
│   │   └── .dockerignore
│   ├── frontend/
│   │   ├── Dockerfile              # Multi-stage: build (Vite) + serve (Nginx)
│   │   └── .dockerignore
│   └── nginx/
│       └── nginx.conf              # Reverse proxy + static file serving
├── kubernetes/
│   ├── base/                       # Environment-neutral Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── services.yaml
│   │   ├── ingress.yaml
│   │   ├── horizontal-pod-autoscaler.yaml
│   │   └── configmaps.yaml
│   ├── overlays/                   # Kustomize environment overlays
│   │   ├── development/
│   │   │   └── kustomization.yaml
│   │   ├── staging/
│   │   │   └── kustomization.yaml
│   │   └── production/
│   │       └── kustomization.yaml
│   └── monitoring/
│       ├── prometheus-config.yaml
│       ├── alerting-rules.yaml
│       └── grafana-dashboards/
│           ├── platform-overview.json
│           ├── agent-performance.json
│           └── engagement-analytics.json
├── terraform/
│   ├── modules/                    # Reusable, cloud-agnostic Terraform modules
│   │   ├── networking/             # VPC, subnets, security groups
│   │   ├── compute/                # Container orchestration platform
│   │   ├── storage/                # Object storage, blob storage
│   │   ├── database/               # Relational and vector databases
│   │   ├── cache/                  # Redis / cache infrastructure
│   │   └── observability/          # Metrics, logging, tracing infrastructure
│   └── environments/
│       ├── development/
│       │   └── main.tf
│       ├── staging/
│       │   └── main.tf
│       └── production/
│           └── main.tf
└── scripts/
    ├── deploy.sh                   # Production deployment script
    ├── rollback.sh                 # Rollback to previous version
    └── health-check.sh             # Post-deployment health validation
```

**CI/CD Pipeline Structure:**

| Pipeline | Trigger | Stages |
|----------|---------|--------|
| `ci.yaml` | Every PR, every push to main | Lint → Type Check → Unit Tests → Integration Tests → Security Scan → Build |
| `cd-staging.yaml` | Merge to main | Build → Push Image → Deploy to Staging → E2E Tests → Smoke Tests |
| `cd-production.yaml` | Tagged release | Pull Staging Image → Deploy to Production → Health Check → Rollback on failure |
| `security-scan.yaml` | Weekly + every PR | SAST → Dependency Audit → Secret Scan → Container Scan |
| `docs-publish.yaml` | Changes to `docs/` | Build documentation site → Publish |

---

## 15. Future Scalability

### 15.1 Supporting 100+ Modules

The repository is designed to scale to 100+ modules without structural changes:
- Modules are directories. Adding a module is adding a directory with a `README.md`.
- The `CODEOWNERS` file maps modules to teams — adding a module requires adding one line.
- The agent registry (`agents/base/agent_registry.py`) discovers agents dynamically — no central list requires updating when a new agent is added.
- Import linting rules are defined by pattern, not by explicit allowlist — new modules automatically inherit the correct boundary rules.

### 15.2 Supporting 50+ Agents

New agents are added by:
1. Creating a new directory under `src/backend/agents/{category}/{agent-name}/`
2. Implementing the `BaseAgent` interface
3. Adding an agent configuration file to `config/agents/`
4. Adding a prompt directory to `config/prompts/agents/`
5. Registering the agent in `config/agents/agent-registry.yaml`
6. Writing tests in `tests/agents/`

No change to the Orchestrator, the API layer, or any other agent is required.

### 15.3 Supporting Multiple UI Clients

Additional UI clients (mobile app, embedded widget, CLI) are added by:
- Creating a new directory under `src/` (e.g., `src/mobile/`, `src/cli/`)
- Implementing the API client for the target platform
- All clients consume the same backend API — the backend does not change

### 15.4 Supporting Multiple LLMs

New LLMs are added by:
1. Creating a new adapter in `infrastructure/llm/`
2. Implementing the `LLMInterface`
3. Registering the model in `config/models/model-registry.yaml`
4. Updating `config/agents/{agent}.yaml` to select the new model for specific agents

Zero agent code changes are required.

### 15.5 Supporting Multiple Clouds

The Terraform modules in `deploy/terraform/modules/` are cloud-agnostic abstractions. Cloud-specific implementations are created as separate module implementations (e.g., `modules/storage/aws/`, `modules/storage/azure/`). The application code does not know which cloud it is running on.

### 15.6 Plugin Architecture

The `plugins/` directory defines the extension point for future plugins. A plugin is an external module that implements `plugins/interface/plugin_interface.py` and registers in `plugins/registry/plugin_registry.yaml`. Plugins can add: new agent types, new output generators, new knowledge base domain configurations, new technology catalogs. Plugins do not modify core platform code.

---

## 16. Repository Standards

### 16.1 Naming Conventions (Canonical Reference)

| Target | Convention | Example |
|--------|------------|---------|
| Repository root | `architectiq` (lowercase, no prefix) | `architectiq/` |
| Top-level directories | `kebab-case` | `src/`, `deploy/`, `config/` |
| Python directories | `snake_case` | `requirement_intelligence/`, `state_machine/` |
| Python files | `snake_case.py` | `engagement_manager.py` |
| Python classes | `PascalCase` | `RequirementIntelligenceAgent` |
| Python functions | `snake_case` | `extract_requirements()` |
| Python constants | `SCREAMING_SNAKE_CASE` | `MAX_RETRY_COUNT = 3` |
| TypeScript directories | `kebab-case` | `session-sidebar/` |
| TypeScript/React component files | `PascalCase.tsx` | `SessionSidebar.tsx` |
| TypeScript module files | `camelCase.ts` | `sessionStore.ts` |
| TypeScript interfaces | `PascalCase` prefixed with `I` | `ISessionState` |
| Config files | `kebab-case.yaml` | `requirement-intelligence.yaml` |
| Prompt files | `kebab-case.md` | `system-prompt.md` |
| Template files | `kebab-case.jinja2` | `hld-template.jinja2` |
| Test files (Python) | `test_{source_file}.py` | `test_engagement_manager.py` |
| Test files (TypeScript) | `{SourceFile}.test.tsx` | `SessionSidebar.test.tsx` |
| Documentation files | `SCREAMING_SNAKE_CASE.md` | `ARCHITECTURE_VISION.md` |
| ADR files | `ADR-NNNN-short-description.md` | `ADR-0001-agent-interface-contract.md` |

### 16.2 File Length Standards

| File Type | Recommended Maximum | Hard Maximum |
|-----------|--------------------|----|
| Python agent implementation | 300 lines | 500 lines |
| Python supporting logic file | 200 lines | 350 lines |
| Python infrastructure adapter | 250 lines | 400 lines |
| React component file | 200 lines | 300 lines |
| Config YAML file | 100 lines | 200 lines |
| Prompt template file | 150 lines | 250 lines |

Files exceeding the recommended maximum must include a comment at the top explaining why splitting is not appropriate.

---

## 17. Repository Governance

### 17.1 Contribution Process

```
1. ENGINEER identifies a need for a new feature, module, or agent.
2. If the change is architectural: engineer creates ADR draft → Architecture Review Board reviews.
3. Engineer creates a feature branch: feature/{module-name}/{short-description}
4. Engineer implements the change, including tests and documentation.
5. Engineer creates a pull request using the PR template.
6. CI pipeline runs automatically: all gates must pass.
7. Required reviewers: (a) CODEOWNER of affected module, (b) one additional engineer.
8. For architectural changes: Platform Architect approval is also required.
9. PR is squash-merged to main with a conventional commit message.
10. CHANGELOG.md is updated in the same PR.
```

### 17.2 Branch Strategy

| Branch | Purpose | Merge Target | Protection |
|--------|---------|--------------|------------|
| `main` | Production state | — | Protected; requires CI pass + 2 approvals |
| `feature/{scope}/{name}` | Feature development | `main` | — |
| `fix/{scope}/{name}` | Bug fixes | `main` | — |
| `release/v{major}.{minor}` | Release preparation | `main` | Protected after release cut |
| `hotfix/{name}` | Production hotfixes | `main` | Requires expedited review |

### 17.3 Version Management

ArchitectIQ follows Semantic Versioning (`{MAJOR}.{MINOR}.{PATCH}`):
- `MAJOR`: Breaking change to a documented API contract or architecture boundary.
- `MINOR`: New capability added in a backward-compatible manner.
- `PATCH`: Bug fix or documentation update with no API or architecture change.

Prompt versions (`v{major}.{minor}`) are versioned independently from the platform version. A prompt version change does not require a platform release.

---

## 18. Future Expansion Strategy

### 18.1 Adding a New Agent

A new agent is self-contained within its directory. The process:
1. Copy the canonical agent directory structure.
2. Implement `BaseAgent` in `agent.py`.
3. Add supporting logic files as needed.
4. Add configuration to `config/agents/`.
5. Add prompts to `config/prompts/agents/`.
6. Register in `agents/base/agent_registry.py` (auto-discovered by pattern).
7. Write unit tests in `tests/` subdirectory.
8. Add golden test fixtures in `tests/agents/golden/`.
9. Update `AGENT_ARCHITECTURE.md`.

**Impact on existing code: Zero.**

### 18.2 Adding a New Domain

A new domain (e.g., manufacturing, gaming) requires:
1. Create `config/knowledge/domains/{domain}.yaml` with domain settings.
2. Populate the knowledge base with domain-specific patterns via the ingestion pipeline.
3. Create `config/knowledge/catalogs/{domain}-catalog.yaml` if domain needs specific technology options.
4. Update `config/models/model-selection-rules.yaml` if domain requires specific model assignments.

**Impact on existing code: Zero.**

### 18.3 Adding a New Output Format

A new output format requires:
1. Create a new generator in `src/backend/outputs/generators/`.
2. Implement the generator interface.
3. Add a template to `config/templates/{format}/v1.0/`.
4. Register the new format in the output packager.

**Impact on existing agents: Zero.**

### 18.4 Adding a New LLM Provider

1. Create a new adapter in `src/backend/infrastructure/llm/`.
2. Implement `LLMInterface`.
3. Register in `config/models/model-registry.yaml`.
4. Update `config/agents/` for agents that should use the new model.

**Impact on existing agents: Zero.**

---

## 19. Architecture Validation Checklist

Use this checklist to validate that any new module, agent, or feature addition conforms to the repository architecture.

### Structure Compliance

- [ ] New code lives inside an existing top-level directory or a new directory approved by an ADR.
- [ ] New directory has a `README.md` documenting its responsibility, what it owns, and what it must never own.
- [ ] New Python module has a `tests/` subdirectory with unit tests.
- [ ] No module spans two different architectural layers.

### Dependency Compliance

- [ ] No imports that violate the dependency direction rules in Section 8.
- [ ] No agent imports another agent's implementation directly.
- [ ] No infrastructure module imports business logic.
- [ ] Shared utilities used by a single module are in that module, not in `shared/`.
- [ ] All secrets accessed via secrets manager, not from environment variables in source.

### Configuration Compliance

- [ ] No environment-specific value is hardcoded in source.
- [ ] New agent has a corresponding config file in `config/agents/`.
- [ ] New agent has a versioned prompt directory in `config/prompts/agents/`.
- [ ] New prompt version creates a new versioned subdirectory; does not modify an existing version.

### Agent Compliance (agent additions only)

- [ ] Agent class inherits from `BaseAgent`.
- [ ] Agent declares `AGENT_ID`, `AGENT_VERSION`, and `AGENT_CATEGORY`.
- [ ] Agent implements only its stated single responsibility.
- [ ] Agent `README.md` documents responsibility, decision boundary, inputs, and outputs.
- [ ] Golden output tests added to `tests/agents/golden/`.

### Documentation Compliance

- [ ] If the change affects architecture: an ADR has been created.
- [ ] If a new module is added: `ARCHITECTURE_VISION.md` cross-reference verified.
- [ ] `CHANGELOG.md` entry added.
- [ ] API documentation updated if a new endpoint is introduced.

### Testing Compliance

- [ ] Unit tests written for all new code.
- [ ] Unit test coverage ≥ 85% for the new module.
- [ ] Integration tests written for new module boundary interactions.
- [ ] All CI gates pass.

---

## 20. Repository Freeze Rules

The following rules are immutable. No pull request, no business pressure, and no timeline constraint may override them. Any developer who believes a Freeze Rule should be changed must submit an ADR to the Architecture Review Board. Until the ADR is approved, the rule stands.

| # | Freeze Rule |
|---|-------------|
| **FR-01** | The directory structure at the top level (`src/`, `config/`, `docs/`, `tests/`, `deploy/`, `outputs/`, `scripts/`, `plugins/`) may not be changed without an ARB-approved ADR. Adding new top-level directories is a structural change requiring ARB approval. |
| **FR-02** | The dependency direction rules in Section 8 may not be violated. Any import that violates Section 8 is a build failure. The linting rule that enforces this may not be disabled. |
| **FR-03** | Every agent must implement `BaseAgent`. No agent may exist that bypasses the base agent interface. |
| **FR-04** | Agents may not communicate directly. All inter-agent data flow passes through the Orchestration Layer. |
| **FR-05** | Prompt templates are versioned. An existing prompt version directory may not be modified after it has been released. Changes create a new version directory. |
| **FR-06** | Secrets are never stored in source code, configuration files, or environment variable definitions in the repository. The CI pipeline scans for secrets and fails on detection. |
| **FR-07** | The `outputs/` directory is gitignored for dynamic content. Generated runtime files are never committed to the repository unless they serve as golden test fixtures in `tests/agents/golden/`. |
| **FR-08** | The `src/backend/shared/` layer has zero domain dependencies. It imports only from the Python standard library and approved third-party utility packages. It never imports from `src/backend/agents/`, `src/backend/orchestration/`, `src/backend/core/`, `src/backend/knowledge/`, or `src/backend/infrastructure/`. |
| **FR-09** | Every module directory must have a `README.md`. A module without a `README.md` fails the CI documentation check. |
| **FR-10** | The `ARCHITECTURE_VISION.md` is the supreme document. Any repository structure or documentation that contradicts it is incorrect. Resolving a contradiction means bringing this repository into compliance with the vision — not revising the vision to match the repository. |

---

> **End of REPOSITORY_MASTER_STRUCTURE.md**  
> **Version 1.0.0 — Foundation Release**  
> **Parent Document:** ARCHITECTURE_VISION.md v1.0.0  
> **Classification:** Repository Architecture — Source of Truth  
> **Next Document:** TECHNOLOGY_ARCHITECTURE.md
