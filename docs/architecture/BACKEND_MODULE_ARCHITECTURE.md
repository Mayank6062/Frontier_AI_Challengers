# BACKEND_MODULE_ARCHITECTURE.md

> **Document Classification:** Backend Architecture — Source of Truth  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0 · SYSTEM_ARCHITECTURE.md v1.0.0  
> **Status:** Approved — Foundation Release  
> **Version:** 1.0.0  
> **Scope:** Complete internal architecture of the ArchitectIQ backend — all modules, all services, all managers, all patterns, all contracts  
> **Authority:** Every backend implementation document, every backend module specification, and every backend code file must be consistent with the architecture defined here. This document is the backend engineering constitution.

---

## Table of Contents

1. [Backend Philosophy](#1-backend-philosophy)
2. [Backend Layer Architecture](#2-backend-layer-architecture)
3. [Backend Module Hierarchy](#3-backend-module-hierarchy)
4. [Module Responsibilities](#4-module-responsibilities)
5. [Service Architecture](#5-service-architecture)
6. [Manager Architecture](#6-manager-architecture)
7. [Provider Architecture](#7-provider-architecture)
8. [Repository Pattern](#8-repository-pattern)
9. [Factory Pattern](#9-factory-pattern)
10. [Strategy Pattern](#10-strategy-pattern)
11. [Dependency Injection Strategy](#11-dependency-injection-strategy)
12. [Cross-Module Communication](#12-cross-module-communication)
13. [Event-Driven Components](#13-event-driven-components)
14. [Error Handling Architecture](#14-error-handling-architecture)
15. [Logging Architecture](#15-logging-architecture)
16. [Configuration Architecture](#16-configuration-architecture)
17. [Security Architecture](#17-security-architecture)
18. [Backend Extension Strategy](#18-backend-extension-strategy)
19. [Backend Validation Checklist](#19-backend-validation-checklist)
20. [Backend Freeze Rules](#20-backend-freeze-rules)

---

## 1. Backend Philosophy

### 1.1 Purpose

The ArchitectIQ backend is the intelligence and governance engine of the platform. It is responsible for everything that happens between a client request arriving at the API boundary and a governed, validated, architect-approved architecture artifact being returned. It orchestrates AI agents, enforces the engagement lifecycle state machine, manages knowledge retrieval and enrichment, produces structured outputs, and maintains the immutable audit trail.

The backend is not a traditional CRUD application with a thin service layer. It is a workflow engine, an agent coordination platform, and a governance framework — all unified behind a clean architecture boundary. This distinction shapes every design decision: modules are not organized around data entities but around capabilities and responsibilities.

### 1.2 Core Responsibilities

The backend owns exactly the following responsibilities — no more, no less:

- Authenticating and authorizing every request through the identity contract
- Managing architect sessions across the complete session lifecycle
- Governing the engagement state machine — the sole enforcer of what transitions are permitted
- Orchestrating the multi-agent pipeline for each engagement stage
- Executing all 12 AI agents through the structured agent lifecycle
- Querying and enriching the enterprise knowledge base
- Managing and versioning all prompt templates
- Recording every significant event to the immutable Decision Ledger
- Validating all AI agent outputs before they propagate downstream
- Generating all structured deliverable outputs from the approved design state
- Managing background knowledge enrichment from approved engagements
- Emitting complete structured observability for all operations

### 1.3 Design Goals

**Testability over convenience.** Every module must be independently testable with constructed inputs and mocked dependencies. A module that can only be tested through the full application stack is a module with a design defect — not a testing defect.

**Explicit over implicit.** Every dependency is declared. Every side effect is documented. Every assumption is validated at the module boundary. Nothing in the backend happens by convention or magic.

**The interface is the contract.** Business logic never depends on concrete implementations. It depends on interfaces. Implementations are interchangeable. This is the mechanism by which the backend remains cloud-agnostic, model-agnostic, and storage-agnostic at the architectural level.

**Configuration drives behavior, code drives capability.** The backend's behavior — which model an agent uses, what prompt version is active, which compliance frameworks apply to which domain — is controlled through configuration, not through code branches. New behaviors are added by updating configuration, not by modifying source.

**Failure is a first-class concern.** Every module is designed with its failure modes explicitly considered. Error types are defined, classified, and handled at the boundary where they are best understood. Errors do not travel as raw exceptions across module boundaries — they travel as typed error objects with recovery information.

### 1.4 Boundaries

**The backend starts at the API Gateway boundary and ends at the persistence boundary.** It does not own the client application, the deployment infrastructure, or the storage systems themselves (it owns the interfaces to those systems). It does not own the LLM providers (it owns the adapters that abstract them).

**The backend is the exclusive source of truth for business logic.** No business rule, no governance constraint, no validation logic exists anywhere except in the backend. The frontend renders state — it does not enforce business rules. Infrastructure stores state — it does not enforce business rules.

---

## 2. Backend Layer Architecture

The backend is organized into eight layers with a strict, unidirectional dependency hierarchy. Each layer has one clearly defined purpose. No layer imports from a layer above it. The dependency direction flows exclusively inward — from the outermost layer toward the domain core.

### 2.1 Layer Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1 — API LAYER                                                 │
│  FastAPI application: routers, middleware, schemas, DI configuration │
│  Depends on: Application Core (Layer 2)                              │
│  Never imports: Agents, Infrastructure implementations               │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 2 — APPLICATION CORE (Domain)                                 │
│  Business logic, state machine, service orchestration, interfaces    │
│  Depends on: Shared (Layer 8), Interfaces only (not implementations) │
│  Never imports: Infrastructure implementations, Agent internals       │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 3 — ORCHESTRATION LAYER                                       │
│  Agent pipeline coordination, scheduling, aggregation                │
│  Depends on: Application Core interfaces, Agent interfaces, Shared   │
│  Never imports: Infrastructure implementations, API layer            │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 4 — AGENT LAYER                                               │
│  12 specialized agents and their supporting logic                    │
│  Depends on: Core interfaces, Knowledge interfaces, LLM interface    │
│  Never imports: Other agents' internals, Orchestration layer         │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 5 — KNOWLEDGE LAYER                                           │
│  Knowledge base, RAG engine, ingestion pipeline                      │
│  Depends on: Core interfaces, Infrastructure interfaces, Shared      │
│  Never imports: Agent internals, Orchestration, API layer            │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 6 — OUTPUT LAYER                                              │
│  Document generators, diagram renderers, output packager             │
│  Depends on: Core interfaces, Infrastructure interfaces, Shared      │
│  Never imports: Agent internals, Orchestration, API layer            │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 7 — INFRASTRUCTURE LAYER                                      │
│  Implementations of all core interfaces: storage, cache, LLM, ledger│
│  Depends on: Core interfaces (implements them), Shared               │
│  Never imports: Business logic, Agent logic, Orchestration           │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 8 — SHARED LAYER                                              │
│  Common utilities, base models, exception hierarchy, constants       │
│  Depends on: Standard library and approved third-party utilities only │
│  Never imports: Any other backend layer (zero domain dependency)     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Layer Specifications

#### Layer 1 — API Layer

**Purpose:** The HTTP boundary of the backend. Translates HTTP requests into application commands and application results into HTTP responses. Owns nothing beyond the translation and gateway enforcement concerns.

**Responsibilities:**
- Route registration and HTTP method handling
- Request deserialization and schema validation (Pydantic)
- Response serialization and HTTP status code assignment
- Middleware execution (auth, rate limiting, correlation ID, logging)
- Dependency injection wiring for each request scope
- WebSocket connection management for streaming

**Allowed imports:** Application Core services (via DI), Shared schemas and exceptions, Middleware components.

**Forbidden imports:** Infrastructure implementations directly, Agent implementations, Orchestration internals. The API layer never knows how the application core implements anything — it only knows what the application core exposes.

---

#### Layer 2 — Application Core

**Purpose:** The domain heart of the backend. Contains all business logic, all business rules, and all interface definitions that the infrastructure layer implements. This layer is stable — it changes only when business requirements change, never when technology choices change.

**Responsibilities:**
- Engagement lifecycle management and state machine enforcement
- Session lifecycle management
- Authentication domain logic (token validation, identity model)
- Review workflow coordination (approval, refinement, rejection)
- Definition of all interface contracts that other layers implement
- Business rule validation that is not schema validation
- Cross-service orchestration commands (directing the Orchestration Layer to execute a pipeline stage)

**Allowed imports:** Shared utilities and models, Interface definitions (which live within this layer). The Application Core defines and consumes its own interfaces — it never imports from Layer 7 (Infrastructure implementations).

**Forbidden imports:** Infrastructure implementations, Agent implementations, Orchestration Layer internals. The domain must be completely decoupled from how things are stored, how agents execute, and how models are invoked.

---

#### Layer 3 — Orchestration Layer

**Purpose:** Coordinates the execution of agent pipelines. Determines which agents run, in which order, with what inputs, and assembles their outputs. Contains no business logic and no agent logic — it is pure coordination.

**Responsibilities:**
- Pipeline stage definition and execution sequencing
- Parallel agent dispatch for independent stages
- Sequential agent chaining for dependent stages
- Partial re-execution (targeted refinement) routing
- Progress event emission to the broadcast channel
- Result aggregation from multiple agent outputs
- Stage-level timeout and failure handling

**Allowed imports:** Core interfaces (AgentInterface, LedgerInterface via Core), Agent layer's base interface only (never specific agent implementations), Shared utilities.

**Forbidden imports:** Specific agent implementations (only the base interface), API layer, Infrastructure implementations directly, Knowledge layer internals.

---

#### Layer 4 — Agent Layer

**Purpose:** Contains the 12 specialized AI agents that perform the actual work of the pipeline. Each agent is a fully self-contained unit with its own logic, models, and tests. Agents are leaves in the dependency tree — they import from lower layers but nothing imports from their internals except through the agent interface.

**Responsibilities (per agent):**
- Input context validation against declared input schema
- Prompt construction from versioned templates and structured inputs
- LLM invocation through the LLM interface
- Output parsing and schema validation
- Citation attachment to every recommendation
- Confidence score calculation
- Structured result emission

**Allowed imports:** Base agent infrastructure (base class, context, result models), Core interfaces (LLMInterface, KnowledgeInterface, StorageInterface, LedgerInterface), Shared utilities, Configuration via the Config Loader.

**Forbidden imports:** Other agents' internal implementations, Orchestration Layer internals, API Layer, Infrastructure implementations directly (only interfaces).

---

#### Layer 5 — Knowledge Layer

**Purpose:** Manages the enterprise knowledge base and provides retrieval-augmented generation capability. Operates as a service that the Agent Layer (specifically the Knowledge Retrieval Agent) consumes.

**Responsibilities:**
- Vector index management and querying
- Semantic similarity search implementation
- Structured metadata filtering for domain and knowledge type
- Retrieved context assembly with source citations
- Knowledge entry validation (automated quality checks)
- Knowledge ingestion pipeline coordination
- Embedding generation for new knowledge entries
- Knowledge base curator approval gate management

**Allowed imports:** Core interfaces, Infrastructure interfaces (for vector store and structured store), Shared utilities.

**Forbidden imports:** Agent internals, Orchestration Layer, API Layer, Output Layer.

---

#### Layer 6 — Output Layer

**Purpose:** Transforms approved architecture state into deliverable artifacts in all configured formats. Operates exclusively on data produced by the Documentation Agent — it does not perform AI reasoning, knowledge retrieval, or business logic.

**Responsibilities:**
- Template loading and versioning
- Jinja2 template rendering for Markdown and HTML
- Mermaid diagram source generation
- Graphviz DOT source generation
- SVG and PNG rendering from Graphviz source
- PDF generation from HTML
- JSON serialization of architecture state
- Output file assembly and storage

**Allowed imports:** Core interfaces (for output storage), Shared utilities, Configuration for template loading.

**Forbidden imports:** Agent internals, Orchestration Layer, Knowledge Layer, API Layer.

---

#### Layer 7 — Infrastructure Layer

**Purpose:** Implements all interfaces defined by the Application Core. This is the only layer that communicates with external systems: databases, file stores, cache providers, LLM APIs, secrets managers. Everything in this layer is a concrete implementation of an abstract contract defined in Layer 2.

**Responsibilities:**
- Structured storage CRUD operations for sessions, engagements, users
- Decision Ledger append-only write implementation
- Vector store read/write for knowledge base
- Cache get/set/invalidate operations
- LLM provider API calls through provider-specific adapters
- Secrets retrieval from the secrets manager
- Observability emission (logs, traces, metrics)

**Allowed imports:** Core interfaces (implements them), Shared utilities, Third-party SDKs for external services.

**Forbidden imports:** Business logic, Agent logic, Orchestration logic. Infrastructure does not make business decisions.

---

#### Layer 8 — Shared Layer

**Purpose:** Provides common, domain-neutral utilities, base types, exception hierarchy, and constants used across all layers. Has zero domain dependencies — it is a pure utility layer.

**Responsibilities:**
- Pydantic base model with common fields (ID, timestamps)
- UUID generation standards
- UTC timestamp utilities
- Complete exception class hierarchy
- Text processing utilities
- Hashing utilities
- Input sanitization utilities
- Shared constants and enumerations
- Retry decorator utilities

**Allowed imports:** Python standard library and approved third-party utility packages (Pydantic, standard datetime, uuid) only.

**Forbidden imports:** Any other backend layer. If Shared needs something from another layer, the design is wrong — the dependency should flow in the other direction.

---

## 3. Backend Module Hierarchy

The backend is composed of the following modules. Each module is a cohesive unit with a single, clearly stated responsibility. The module hierarchy is organized by architectural layer.

### Layer 2 — Application Core Modules

| Module | Single Responsibility |
|--------|----------------------|
| `auth` | GitHub OAuth flow and identity token lifecycle |
| `session` | Session creation, persistence, restoration, and expiry |
| `engagement` | Engagement lifecycle and state machine enforcement |
| `review` | Human review workflow: approval, refinement, rejection, override recording |
| `workspace` | Workspace state assembly for client display |
| `interfaces` | All interface contracts that infrastructure implements (no logic — only contracts) |

### Layer 3 — Orchestration Modules

| Module | Single Responsibility |
|--------|----------------------|
| `master_orchestrator` | Top-level pipeline coordination and stage sequencing |
| `pipeline_manager` | Pipeline stage specification and stage-level state |
| `agent_scheduler` | Agent task queuing, dispatch, parallel execution, and result collection |
| `result_aggregator` | Assembly of multiple agent outputs into a coherent stage result |
| `message_bus` | Internal publish/subscribe for parallel agent coordination within stages |
| `progress_broadcaster` | Real-time pipeline progress event emission to connected clients |
| `refinement_router` | Targeted re-execution routing based on architect feedback analysis |

### Layer 4 — Agent Modules

| Module | Single Responsibility |
|--------|----------------------|
| `base` | Base agent class, execution lifecycle enforcement, agent registry |
| `requirement_intelligence` | Extract structured requirements from unstructured architect input |
| `knowledge_retrieval` | Query the knowledge base and assemble the retrieved context package |
| `architecture_design` | Generate candidate architecture options with trade-off rationale |
| `technology_recommendation` | Select component-level technologies against the catalog and scoring framework |
| `infrastructure_recommendation` | Design deployment topology and prepare IaC guidance |
| `security` | Threat modelling and security control mapping |
| `cost_optimization` | TCO modelling and cost optimization recommendations |
| `compliance` | Regulatory framework evaluation against candidate architectures |
| `risk_assessment` | Aggregate all validation findings into a prioritized risk register |
| `governance` | Policy compliance enforcement against enterprise standards |
| `human_collaboration` | Proposal consolidation and architect feedback routing |
| `documentation` | Structured deliverable generation from approved design state |

### Layer 5 — Knowledge Modules

| Module | Single Responsibility |
|--------|----------------------|
| `knowledge_base` | Knowledge entry CRUD, metadata management, and retrieval interface |
| `rag_engine` | Multi-signal retrieval query execution and context assembly |
| `ingestion_pipeline` | Processing of new knowledge entries: parse, validate, embed, gate |
| `embedding_service` | Vector embedding generation for text content |
| `curator_gateway` | Human approval gate for knowledge base entries |

### Layer 6 — Output Modules

| Module | Single Responsibility |
|--------|----------------------|
| `template_loader` | Versioned template loading and caching |
| `markdown_generator` | HLD, LLD, executive summary, risk register, assumptions log rendering |
| `html_generator` | Interactive HTML architecture report rendering |
| `pdf_generator` | PDF conversion from rendered HTML |
| `diagram_generator` | Mermaid and Graphviz DOT source generation |
| `diagram_renderer` | SVG and PNG rendering from DOT source |
| `json_serializer` | Machine-readable JSON architecture state serialization |
| `iac_generator` | Infrastructure-as-Code scaffolding generation (Phase 2) |
| `output_packager` | Assembly of all generated outputs into a versioned bundle |

### Layer 7 — Infrastructure Modules

| Module | Single Responsibility |
|--------|----------------------|
| `llm_gateway` | LLM provider request routing, sanitization, and response normalization |
| `anthropic_adapter` | Anthropic API client implementation of LLMInterface |
| `storage_service` | Structured storage read/write for sessions, engagements, users |
| `vector_store_service` | Vector index read/write for knowledge base |
| `cache_service` | Cache get/set/invalidate with TTL management |
| `decision_ledger_service` | Append-only Decision Ledger write and read implementation |
| `secrets_service` | Secrets retrieval and rotation-aware credential management |
| `observability_service` | Structured log emission, trace span management, metrics emission |
| `output_storage_service` | File-based storage for generated output artifacts |

### Layer 8 — Shared Modules

| Module | Single Responsibility |
|--------|----------------------|
| `base_model` | Pydantic base model with standard fields |
| `identifiers` | UUID v4 generation with typing |
| `timestamps` | UTC timestamp generation and formatting |
| `exceptions` | Complete exception class hierarchy |
| `text_utils` | Text cleaning, truncation, token estimation |
| `hash_utils` | Content hashing for cache keys and integrity |
| `sanitizer` | Input content sanitization for security |
| `retry_utils` | Retry decorator with exponential backoff |
| `constants` | Enumerated constants and platform-wide fixed values |

---

## 4. Module Responsibilities

### 4.1 `auth` Module

**Purpose:** Manages the GitHub OAuth authentication flow and the platform's identity token lifecycle. The single source of truth for all identity concerns.

**Responsibilities:**
- Initiate the GitHub OAuth authorization redirect
- Exchange the OAuth authorization code for an access token
- Validate the GitHub access token and extract the user identity
- Issue platform-internal session tokens (signed JWT)
- Validate platform session tokens on every authenticated request
- Manage token expiry and refresh logic
- Provide the authenticated identity object for downstream use

**Inputs:** OAuth code from the client redirect, platform token from the Authorization header.

**Outputs:** Authenticated identity object (user ID, email, display name, roles) attached to every authorized request context.

**Dependencies:** OAuthProvider (for GitHub OAuth communication), SecretsProvider (for signing key), StorageRepository (for token revocation list).

**Must never own:** Business logic beyond identity. The auth module does not know what an engagement is. It only knows who a user is.

---

### 4.2 `session` Module

**Purpose:** Manages the complete lifecycle of architect sessions — creation, persistence, restoration, and expiry.

**Responsibilities:**
- Create a new session record for a first-time login
- Restore a full session context for a returning login (conversation history, active engagement references, workspace state)
- Update the session's last-active timestamp on each interaction
- Expire sessions that have exceeded the inactivity threshold
- Provide the session context object for all downstream request processing
- Associate new engagements with their parent session

**Inputs:** Authenticated identity object from the auth module; session identifier from the client request.

**Outputs:** Session context object (session ID, identity, active engagement IDs, conversation history index, workspace state snapshot).

**Dependencies:** SessionRepository (for session persistence), CacheService (for session context caching).

**Must never own:** Authentication logic, engagement business logic, workspace rendering logic.

---

### 4.3 `engagement` Module

**Purpose:** The governance center of the platform. Owns the engagement lifecycle state machine and is the sole authority on what state transitions are permitted.

**Responsibilities:**
- Create new engagement records with INITIATED state
- Enforce state machine transitions — accept valid transitions, reject invalid ones with a typed error
- Persist every state transition durably before acknowledging it
- Coordinate pipeline execution triggers to the Orchestration Layer on valid transitions
- Coordinate human review gate transitions (accept approval, refinement, rejection inputs)
- Maintain the engagement's complete history: requirement inputs, agent outputs, human decisions
- Provide engagement context for pipeline invocation and workspace display
- Manage engagement versioning when a new approved version supersedes the prior

**Inputs:** User intent commands from the API Layer (routed via the EngagementService); pipeline completion signals from the Orchestration Layer.

**Outputs:** Engagement state transition confirmations; pipeline execution triggers; engagement context for orchestration and display.

**Dependencies:** EngagementRepository (for state persistence), LedgerService (for ledger writes on significant transitions), OrchestratorService (triggered on pipeline-initiating transitions).

**Must never own:** Agent logic, knowledge retrieval, output generation, direct storage implementation.

**Critical rule:** The state machine is implemented as a pure function within this module — given a current state and a transition trigger, it returns either a valid next state or a typed rejection. The persistence and side effects of the transition are managed by the EngagementService. The state machine itself has no side effects — it only validates and computes.

---

### 4.4 `review` Module

**Purpose:** Manages the human review workflow — the structured process by which an architect reviews a proposal, makes a decision, and provides feedback.

**Responsibilities:**
- Assemble the review context for the architect (proposal version, validation findings, citations)
- Accept and validate architect decisions (approve, refine, reject)
- Record architect overrides (direct component-level edits) as structured override records
- Route architect refinement feedback to the RefinementRouter for targeted re-execution determination
- Trigger Decision Ledger writes for every review action
- Manage the iteration tracking for multi-cycle reviews (version numbering)
- Provide the override authority enforcement — architect overrides are never superseded by agent re-execution

**Inputs:** Completed proposal package from the Human Collaboration Agent; architect decision input from the API Layer.

**Outputs:** Structured decision record (decision type, identity, timestamp, feedback or override payload); routing instruction to the EngagementService for state transition.

**Dependencies:** LedgerService (for all review action recording), RefinementRouter (for feedback analysis), EngagementRepository (for version management).

**Must never own:** Agent logic, proposal content generation, output rendering.

---

### 4.5 `workspace` Module

**Purpose:** Assembles and manages the workspace state — the structured representation of the current engagement's content as displayed in the architect's workspace panel.

**Responsibilities:**
- Assemble the workspace state from the current engagement record and agent outputs
- Track which workspace sections are complete, in-progress, or pending
- Provide workspace state to the API Layer for client synchronization
- Maintain the workspace display state separately from the engagement persistence state (workspace display state is ephemeral and reconstructed from engagement state on reconnect)
- Manage workspace section update events for streaming to the Progress Broadcaster

**Inputs:** Engagement state updates from the Engagement module; agent output events from the Orchestration Layer (via Progress Broadcaster).

**Outputs:** Workspace state snapshot for API response; workspace section update events for streaming.

**Dependencies:** EngagementRepository (read-only), CacheService (for workspace state caching during active sessions).

**Must never own:** Business logic, agent execution, direct storage writes.

---

### 4.6 `interfaces` Module

**Purpose:** The contract library of the Application Core. Defines every interface that a lower layer must implement. Contains no logic — only abstract method signatures and their documentation.

**Responsibilities:**
- Define `LLMInterface` — the contract for all LLM provider adapters
- Define `StorageInterface` — the contract for all persistent storage adapters
- Define `CacheInterface` — the contract for all cache adapters
- Define `LedgerInterface` — the contract for the Decision Ledger adapter
- Define `KnowledgeInterface` — the contract for the Knowledge Layer service
- Define `SecretsInterface` — the contract for secrets retrieval
- Define `ObservabilityInterface` — the contract for log, trace, and metric emission
- Define `AgentInterface` — the base execution contract for all 12 agents
- Define `OutputStorageInterface` — the contract for output artifact storage

**Inputs:** None — this module is a definition module, not a runtime module.

**Outputs:** Interface definitions imported by both the Application Core (consumers) and the Infrastructure Layer (implementors).

**Dependencies:** Shared base models for type definitions only.

**Must never own:** Implementation logic, business rules, runtime behavior. A module that implements an interface never returns the interface class — it returns a concrete implementation. The interface module never instantiates anything.

---

### 4.7 `base` Agent Module

**Purpose:** The foundation infrastructure for all 12 agents. Defines the base agent class that enforces the agent execution lifecycle, the agent registry for dynamic discovery, and the standardized context and result models.

**Responsibilities:**
- Define `BaseAgent` — the abstract class that all 12 agents inherit
- Enforce the agent execution lifecycle (validate → retrieve → construct → sanitize → invoke → parse → validate → cite → score → emit) as a template method
- Provide `AgentContext` — the standardized input context model shared by all agents
- Provide `AgentResult` — the standardized result model shared by all agents
- Maintain the `AgentRegistry` — a dynamic discovery mechanism that discovers registered agents by their `AGENT_ID`
- Provide `AgentValidator` — the output validation framework that checks schema conformance and citation presence before result emission

**Dependencies:** Core interfaces (LLMInterface, KnowledgeInterface), Shared base models, Configuration loader.

**Must never own:** Specific agent logic, infrastructure implementations, orchestration logic.

---

### 4.8 Twelve Individual Agent Modules

Each of the following agent modules has the same structural responsibility but completely different domain logic:

| Agent Module | Domain Logic Responsibility |
|-------------|---------------------------|
| `requirement_intelligence` | Extracts functional/NFRs, identifies ambiguities, flags compliance constraints from raw input |
| `knowledge_retrieval` | Formulates retrieval queries, executes RAG, assembles context with cited sources |
| `architecture_design` | Composes candidate architectures from requirements and retrieved patterns |
| `technology_recommendation` | Scores and selects technologies per component using catalog and scoring framework |
| `infrastructure_recommendation` | Maps logical design to deployment topology; generates IaC guidance structure |
| `security` | Applies threat modelling; maps security controls; classifies findings |
| `cost_optimization` | Calculates TCO from component selections; identifies optimization levers |
| `compliance` | Evaluates design elements against declared regulatory frameworks |
| `risk_assessment` | Aggregates security and compliance findings; scores and prioritizes risks |
| `governance` | Checks all outputs against enterprise policy catalog; flags guardrail violations |
| `human_collaboration` | Consolidates all pipeline outputs into a single navigable review package |
| `documentation` | Structures approved design state into all document section schemas |

**For every agent module, the following must never be owned within the module:**
- Orchestration logic (how agents are scheduled or sequenced)
- Infrastructure implementation (direct storage, direct LLM SDK calls — all through interfaces)
- Another agent's internal implementation (cross-agent imports are forbidden)
- Business state management (state machine logic, session management)

---

### 4.9 `knowledge_base` Module

**Purpose:** The primary service interface for the enterprise knowledge base. Manages knowledge entries, their metadata, and their retrieval state. The single owner of knowledge data integrity.

**Responsibilities:**
- Accept new knowledge entries from the ingestion pipeline (post-curator-approval)
- Maintain the knowledge entry lifecycle: pending, approved, deprecated
- Provide a typed query interface consumed by the RAG Engine
- Track retrieval and approval usage metrics per entry
- Enforce knowledge entry schema on all writes
- Manage knowledge catalog partitioning (by domain, by type, by recency)
- Provide the curator approval gate interface for human-governed ingestion

**Inputs:** Knowledge entries from the IngestionPipeline (curated); query specifications from the RAGEngine.

**Outputs:** Knowledge entry CRUD results; ranked retrieval results to the RAGEngine.

**Dependencies:** VectorStoreService (for embedding storage and semantic search), StorageService (for structured metadata), CacheService (for retrieval result caching).

**Must never own:** Agent logic, RAG retrieval logic (delegated to rag_engine module), engagement logic.

---

### 4.10 `rag_engine` Module

**Purpose:** Executes retrieval-augmented generation queries against the knowledge base. Owns the multi-signal retrieval strategy and the context assembly logic.

**Responsibilities:**
- Accept structured queries from the Knowledge Retrieval Agent
- Execute semantic similarity search against the vector index
- Apply structured filters (domain, knowledge type, date range, approval status)
- Apply deterministic lookups for exact-match standard references
- Combine multi-signal results with a composite relevance ranking
- Assemble the retrieved context package: items + citations + relevance scores
- Enforce retrieval count limits to respect agent context budgets
- Cache retrieval results keyed by query hash, invalidated on knowledge base updates

**Inputs:** Retrieval query from the Knowledge Retrieval Agent (requirement context + domain + filters + count limit).

**Outputs:** Ranked context package (items, citations, relevance scores, retrieval metadata).

**Dependencies:** KnowledgeBase module (query interface), VectorStoreService, CacheService.

**Must never own:** Agent logic, knowledge entry management (owned by knowledge_base module), prompt construction.

---

### 4.11 `output_packager` Module

**Purpose:** Assembles all generated output artifacts into a versioned, complete bundle associated with the approved architecture.

**Responsibilities:**
- Receive rendered output files from individual format generators
- Validate that all required output formats have been successfully generated
- Construct the output manifest (file paths, formats, generation timestamps, template versions)
- Store the output bundle in the OutputStorageService with engagement ID-scoped paths
- Provide the output bundle reference to the Engagement module for COMPLETED state recording
- Manage output versioning (each new approval creates a new output version)

**Inputs:** Individual output files from generators; approved architecture metadata.

**Outputs:** Output bundle manifest (file path references, format list, version number, integrity checksums).

**Dependencies:** OutputStorageService, EngagementRepository (read-only for metadata), Shared hash utilities.

**Must never own:** Document content logic, rendering logic, agent logic.

---

### 4.12 `llm_gateway` Module

**Purpose:** The abstraction layer for all LLM provider interactions. Every agent invocation that requires AI model execution passes through this module. No agent communicates directly with an LLM provider.

**Responsibilities:**
- Route LLM requests to the appropriate provider adapter based on the model identifier
- Enforce prompt content sanitization (PII detection, secret detection, injection detection)
- Apply per-agent token budget limits
- Implement per-model rate limiting with request queuing
- Normalize responses across different provider response formats
- Record every LLM invocation to the observability layer (model, tokens, latency, result)
- Implement retry logic for transient provider errors (429, 503)
- Manage provider adapter registry (which model ID maps to which adapter)

**Inputs:** Structured LLM request (model ID, system prompt, user prompt, parameters).

**Outputs:** Normalized LLM response (generated text, finish reason, token usage).

**Dependencies:** LLM provider adapters (AnthropicAdapter, future adapters), SecretsService (for API keys), CacheService (for deterministic response caching), ObservabilityService.

**Must never own:** Business logic, prompt construction (owned by agents), agent output validation.

---

### 4.13 `decision_ledger_service` Module

**Purpose:** The infrastructure implementation of the LedgerInterface. Provides the immutable, append-only write capability that the Decision Ledger requires.

**Responsibilities:**
- Accept structured ledger entries from the Application Core
- Validate the entry structure before writing
- Compute and attach the hash chain entry for tamper evidence
- Write to the append-only ledger store (durable write with confirmation before returning)
- Provide read capability for audit queries and Decision Ledger display
- Verify hash chain integrity on read (incremental verification)
- Support full chain integrity verification (scheduled verification trigger)

**Inputs:** LedgerEntry objects from the Application Core (via LedgerInterface).

**Outputs:** Write confirmation (with entry ID and chain hash); query results for read operations.

**Dependencies:** StorageService (underlying durable store), ObservabilityService (write audit logging).

**Must never own:** Business logic, engagement management, any mutable data operation. The ledger service only appends. It never updates or deletes.

---

### 4.14 `observability_service` Module

**Purpose:** Centralizes all observability concerns — structured logging, distributed tracing, and metrics emission. Every backend module emits observability through this service.

**Responsibilities:**
- Provide a structured logging interface (with mandatory field enforcement)
- Manage distributed trace spans (open, annotate, close)
- Propagate correlation IDs across all backend operations
- Emit metrics to the configured metrics backend (counters, histograms, gauges)
- Buffer and batch observability emissions to avoid blocking the critical path
- Provide the correlation ID assignment and propagation mechanism

**Inputs:** Log records, trace events, metric data points from any backend module.

**Outputs:** Structured log entries, trace spans, metric data points to the configured observability platform.

**Dependencies:** External observability platform SDKs only (no domain dependencies).

**Must never own:** Business logic, storage, authentication. The observability service is a passive recipient of information — it never makes decisions based on what it receives.

---

## 5. Service Architecture

Services in the ArchitectIQ backend are the orchestration units of the Application Core. A service owns the use-case coordination logic — it receives a command, invokes the appropriate modules and repositories, and returns a result. Services do not contain business rules (those live in domain modules) and do not contain persistence logic (that lives in repositories).

### 5.1 Service Definitions

#### `AuthService`

**Single Responsibility:** Coordinate the complete authentication flow — from OAuth initiation through platform token issuance.

**What it orchestrates:** OAuthProvider (code exchange), SecretsProvider (signing key retrieval), UserRepository (user record upsert), TokenManager (token issuance and validation).

**Key operations:** `initiate_oauth_flow()`, `complete_oauth_flow(code)`, `validate_token(token)`, `revoke_token(token)`.

**Lifecycle:** Stateless. Instantiated per-request via DI. No session state in the service itself.

---

#### `SessionService`

**Single Responsibility:** Coordinate session creation, restoration, and management across the session lifecycle.

**What it orchestrates:** SessionRepository (persistence), CacheService (session caching), ConversationHistoryManager (history index management).

**Key operations:** `create_session(identity)`, `restore_session(session_id, identity)`, `update_session_activity(session_id)`, `expire_session(session_id)`.

**Lifecycle:** Stateless. The session state is externalized in storage and cache.

---

#### `EngagementService`

**Single Responsibility:** Coordinate all engagement lifecycle operations — from creation through completion — via the engagement state machine.

**What it orchestrates:** EngagementStateMachine (transition validation), EngagementRepository (state persistence), LedgerService (significant event recording), OrchestratorService (pipeline triggering on valid transitions), ReviewManager (human review coordination).

**Key operations:** `create_engagement(session_id, requirement_input)`, `advance_state(engagement_id, trigger, actor)`, `get_engagement(engagement_id)`, `record_review_decision(engagement_id, decision)`.

**Lifecycle:** Stateless. All engagement state is externalized in the EngagementRepository.

**Critical invariant:** The EngagementService is the only component authorized to call `advance_state` on the EngagementStateMachine. No other component calls the state machine directly.

---

#### `OrchestratorService`

**Single Responsibility:** Coordinate the agent pipeline for a given engagement stage — sequencing, dispatching, and aggregating.

**What it orchestrates:** MasterOrchestrator, AgentScheduler, ResultAggregator, ProgressBroadcaster, RefinementRouter.

**Key operations:** `execute_stage(engagement_context, stage_spec)`, `execute_refinement(engagement_context, feedback, affected_agents)`, `get_pipeline_status(engagement_id)`.

**Lifecycle:** Stateless per invocation. The pipeline state for an in-progress execution is managed by the PipelineManager within the execution scope.

---

#### `KnowledgeService`

**Single Responsibility:** Provide the knowledge retrieval capability to the Agent Layer and the knowledge management capability to curators.

**What it orchestrates:** KnowledgeBase module, RAGEngine, IngestionPipeline, CuratorGateway, EmbeddingService.

**Key operations:** `query(retrieval_spec)`, `submit_entry(entry)`, `approve_entry(entry_id, curator_id)`, `deprecate_entry(entry_id, reason)`, `get_usage_metrics(entry_id)`.

**Lifecycle:** Stateless. Knowledge base state is externalized in storage.

---

#### `OutputService`

**Single Responsibility:** Coordinate the generation of all output artifacts from an approved architecture state.

**What it orchestrates:** TemplateLoader, all format-specific generators, DiagramRenderer, OutputPackager, OutputStorageService.

**Key operations:** `generate_outputs(engagement_id, approved_architecture, format_spec)`, `get_output_bundle(engagement_id, version)`.

**Lifecycle:** Stateless per generation invocation.

---

#### `WorkspaceService`

**Single Responsibility:** Assemble and maintain the workspace state representation for client display.

**What it orchestrates:** EngagementRepository (read-only), CacheService (workspace state caching).

**Key operations:** `get_workspace_state(engagement_id)`, `update_workspace_section(engagement_id, section, content)`, `reconstruct_workspace(engagement_id)` (for session restore).

**Lifecycle:** Stateless. Workspace state reconstructed from engagement state on demand.

---

## 6. Manager Architecture

Managers own long-running or complex stateful coordination that spans multiple service calls. They differ from services in that they maintain operational state within an execution scope (not persisted — ephemeral to the execution).

### 6.1 `EngagementStateMachine`

**Purpose:** Pure function implementation of the engagement lifecycle state machine.

**Why a manager, not a service:** The state machine is a domain object with its own identity — it has states, transitions, guards, and invariants. It is not a collection of unrelated operations; it is a single coherent model.

**Responsibilities:** Given a current state and a transition trigger, validate the transition and return the next valid state (or a typed rejection with the reason). Enforce all non-negotiable transition guards (including the PENDING_HUMAN_REVIEW requirement before APPROVED).

**Lifecycle:** Instantiated once (singleton within the application). It has no mutable state — it is a pure function of current state → new state.

---

### 6.2 `PipelineManager`

**Purpose:** Tracks the execution state of an active agent pipeline within a single orchestration invocation.

**Why a manager:** Pipeline execution involves many parallel and sequential steps. The pipeline manager maintains the per-execution state: which stages are complete, which are in-progress, which have failed, and what partial results have been collected.

**Responsibilities:** Track stage completion status, manage partial result collection, enforce stage dependencies (a later stage cannot start until its predecessor has completed), emit stage-level events to the ProgressBroadcaster.

**Lifecycle:** Instantiated per pipeline invocation. Discarded when the pipeline completes or fails. Pipeline execution state is not persisted — it is reconstructed from the durable engagement state if a retry is needed.

---

### 6.3 `PromptManager`

**Purpose:** Manages the loading, caching, and versioning of prompt templates.

**Why a manager:** Prompts are versioned, cached, and loaded dynamically based on agent configuration. Managing this with version-aware caching and change-detection requires a dedicated manager.

**Responsibilities:** Load the active prompt version for each agent from the configuration, cache loaded prompts to avoid repeated file reads, invalidate cache on configuration updates, provide the prompt assembly interface to agents (merge template + context).

**Lifecycle:** Application singleton. The prompt cache is maintained for the lifetime of the application.

---

### 6.4 `BackgroundJobManager`

**Purpose:** Manages the submission, tracking, and lifecycle of background tasks (primarily the knowledge enrichment pipeline).

**Why a manager:** Background tasks run outside the request lifecycle. They need submission tracking, failure alerting, and retry coordination that does not block the foreground path.

**Responsibilities:** Accept task submissions from the Application Core, queue tasks for background execution, track task completion and failure, retry failed tasks with backoff, alert on repeated failure.

**Lifecycle:** Application singleton. Maintains a task queue backed by a persistent queue (durable between restarts for critical tasks).

---

### 6.5 `RefinementRouter`

**Purpose:** Analyzes architect refinement feedback and determines which agents' outputs are affected by the requested change, producing a targeted re-execution plan.

**Why a manager:** Refinement routing requires understanding the dependency relationships between agents — which agents' outputs depend on the component being changed. This is a non-trivial coordination concern that warrants its own manager.

**Responsibilities:** Parse architect feedback (structured or free-text), identify the target component(s) of the feedback, determine the affected agent set using the agent dependency graph, produce a targeted re-execution specification for the Orchestrator.

**Lifecycle:** Stateless per refinement invocation.

---

### 6.6 `ConversationHistoryManager`

**Purpose:** Manages the ordered sequence of conversation messages within a session, providing history retrieval and pagination.

**Why a manager:** Conversation history grows unbounded within a session. Managing retrieval with efficient pagination, context window sizing for prompt construction, and persistence indexing requires dedicated coordination.

**Responsibilities:** Append new messages to the session's conversation history, retrieve history for client display (paginated), retrieve the last N messages for prompt context assembly, maintain the conversation history index in the session store.

**Lifecycle:** Instantiated per session. The history is persisted in the SessionRepository.

---

## 7. Provider Architecture

Providers abstract all external service communications. Every external system the platform depends on is represented by a provider interface in the `interfaces` module and a concrete implementation in the `infrastructure` layer. The rest of the backend never knows which concrete provider is in use.

### 7.1 `OAuthProvider`

**Interface contract:** `initiate_flow() → authorization_url`, `exchange_code(code) → token_response`, `validate_token(token) → identity`.

**Current implementation:** GitHub OAuth 2.0 adapter.

**Future extensions:** Corporate SSO adapter (SAML/OIDC), Google OAuth adapter. Adding a new OAuth provider requires a new implementation of `OAuthProvider` — zero changes to the auth module or any other module.

**Abstraction rationale:** Authentication provider is an organizational decision that changes independently of the platform's capabilities. Decoupling it means the platform can be deployed with any enterprise identity provider without a code change in the application layer.

---

### 7.2 `LLMProvider`

**Interface contract:** `invoke(request: LLMRequest) → LLMResponse` (normalized across providers).

**Current implementation:** `AnthropicAdapter` — communicates with the Anthropic Messages API using the claude-sonnet-4-6 model family.

**Future extensions:** `OpenAIAdapter`, `AzureOpenAIAdapter`, `GeminiAdapter`. Each implements the same interface. The LLMGateway routes to the correct adapter by model ID.

**Abstraction rationale:** Model selection is a frequently changing decision. New models are added, old models are deprecated. Wrapping every provider in a normalized interface means model changes never touch agent code.

---

### 7.3 `StorageProvider`

**Interface contract:** `read(key) → record`, `write(key, record) → confirmation`, `delete(key) → confirmation`, `query(filter_spec) → records`.

**Current implementation:** Configured relational database adapter (provider-agnostic at the application layer — PostgreSQL-compatible in practice).

**Future extensions:** Document store adapter, cloud-native managed database adapters.

**Abstraction rationale:** Storage technology changes as organizational infrastructure evolves. Application modules never see SQL — they see the storage interface. Migrating storage backends requires only a new adapter.

---

### 7.4 `VectorStoreProvider`

**Interface contract:** `upsert(id, vector, metadata)`, `query(vector, filter, top_k) → [(id, score, metadata)]`, `delete(id)`.

**Current implementation:** Adapter for the configured vector database (e.g., pgvector, Weaviate, Qdrant — selection in TECHNOLOGY_ARCHITECTURE.md).

**Future extensions:** Cloud-native vector store adapters (AWS OpenSearch, Azure AI Search).

**Abstraction rationale:** The vector store market is evolving rapidly. Isolating the implementation ensures the platform can adopt better vector stores as they mature.

---

### 7.5 `SecretsProvider`

**Interface contract:** `get_secret(name) → secret_value`, `refresh_secret(name) → secret_value`.

**Current implementation:** Adapter for the configured secrets manager (cloud-provider-specific, e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).

**Future extensions:** Any secrets manager that supports programmatic retrieval.

**Abstraction rationale:** Secrets management is infrastructure. The application never hardcodes credentials. The SecretsProvider is the single point of access.

---

### 7.6 `CacheProvider`

**Interface contract:** `get(key) → value | None`, `set(key, value, ttl)`, `delete(key)`, `invalidate_prefix(prefix)`.

**Current implementation:** Redis-compatible adapter.

**Future extensions:** In-memory adapter (for testing), cloud-native cache adapters.

**Abstraction rationale:** Cache implementation is an infrastructure concern. Application modules cache through the interface — they never manipulate the cache technology directly.

---

### 7.7 `NotificationProvider` (Future — Phase 2)

**Interface contract:** `send_notification(recipient, event_type, context)`.

**Planned implementation:** Email adapter, Slack webhook adapter, Microsoft Teams adapter.

**Abstraction rationale:** Notification delivery channel is a deployment configuration decision, not an application design decision.

---

## 8. Repository Pattern

Repositories provide the persistence abstraction for domain entities. Every piece of data that must survive a request boundary has a repository. Repositories encapsulate all storage access for their entity — no other module issues raw storage queries for an entity that has a repository.

### 8.1 Repository Philosophy

A repository looks like a collection from the perspective of the domain. The domain asks the repository for entities by their identifiers or by query predicates expressed in domain terms (not in SQL or storage terms). The repository translates those domain queries into storage operations — and translates storage results back into domain entities.

**What repositories own:** All storage access for their entity. Query translation. Domain entity hydration from storage records.

**What repositories never own:** Business rules, state machine logic, service coordination, cross-entity joins that express business logic.

### 8.2 Repository Definitions

#### `EngagementRepository`

**Owned entity:** `Engagement` (complete engagement record including state, all agent outputs, version history).

**Key operations:** `create(engagement)`, `get(engagement_id)`, `get_by_session(session_id)`, `save_state_transition(engagement_id, new_state, transition_metadata)`, `save_agent_output(engagement_id, stage, output)`, `save_approved_version(engagement_id, approved_snapshot)`.

**Critical contract:** `save_state_transition` is a write-ahead operation — it must complete and confirm before the state transition is communicated to the caller. This is the implementation of the Recovery Guarantee.

---

#### `SessionRepository`

**Owned entity:** `Session` (session record including conversation history index, workspace state, active engagement references).

**Key operations:** `create(session)`, `get(session_id)`, `get_by_identity(user_id)`, `update_activity(session_id, timestamp)`, `append_conversation_message(session_id, message)`, `get_conversation_history(session_id, offset, limit)`, `expire(session_id)`.

---

#### `UserRepository`

**Owned entity:** `User` (user record including identity, roles, preferences).

**Key operations:** `upsert(identity_from_oauth)`, `get(user_id)`, `get_by_external_id(github_user_id)`, `update_roles(user_id, roles)`.

---

#### `KnowledgeRepository`

**Owned entity:** `KnowledgeEntry` (knowledge base entry with metadata, embeddings, usage metrics).

**Key operations:** `create(entry)`, `approve(entry_id, curator_id)`, `deprecate(entry_id, reason)`, `get(entry_id)`, `list_pending_approval()`, `record_retrieval(entry_id)`, `record_approval_usage(entry_id, engagement_id)`.

Note: The KnowledgeRepository coordinates with the VectorStoreProvider for embedding operations and the StorageProvider for metadata — both through their respective interfaces.

---

#### `LedgerRepository`

**Owned entity:** `LedgerEntry` (immutable ledger records).

**Key operations:** `append(entry) → entry_with_chain_hash`, `get(entry_id)`, `get_by_engagement(engagement_id, offset, limit)`, `verify_chain_from(entry_id) → integrity_result`.

**Critical contract:** `append` is an atomic write that includes computing and storing the chain hash. It returns only after the write is durably confirmed. It never updates or deletes.

---

#### `OutputRepository`

**Owned entity:** `OutputBundle` (output manifest and file references for a completed engagement).

**Key operations:** `save_bundle(engagement_id, version, manifest)`, `get_bundle(engagement_id, version)`, `list_versions(engagement_id)`.

---

## 9. Factory Pattern

Factories are used where object creation is complex, conditional, or needs to be decoupled from the consuming code. The backend uses factories in three specific contexts.

### 9.1 `AgentFactory`

**Purpose:** Creates agent instances based on agent ID and configuration, without the consuming code (the Orchestrator) needing to know which concrete agent class to instantiate.

**Why a factory:** Agent instantiation requires injecting configuration (model ID, prompt version, parameters) that varies per agent type and per environment. The factory centralizes this complexity.

**Creation logic:** Given an `AGENT_ID`, the factory retrieves the agent's configuration from the ConfigurationService, instantiates the correct concrete agent class, injects all required dependencies (LLM interface, Knowledge interface, prompt templates), and returns a ready-to-execute agent instance.

**Consumer:** The AgentScheduler calls the AgentFactory to produce agent instances at dispatch time.

---

### 9.2 `OutputGeneratorFactory`

**Purpose:** Creates the appropriate output generator instance for each requested output format.

**Why a factory:** Output format is a configuration-driven choice. The factory maps format identifiers to generator implementations without the OutputService needing to enumerate all possible formats.

**Creation logic:** Given a format identifier (e.g., `"hld_markdown"`, `"architecture_html"`, `"mermaid_diagram"`), returns the appropriate generator instance configured with the correct versioned template.

**Consumer:** The OutputService calls the OutputGeneratorFactory for each format in the output specification.

---

### 9.3 `LLMAdapterFactory`

**Purpose:** Creates the appropriate LLM provider adapter instance based on the model identifier.

**Why a factory:** The model registry maps model identifiers to adapter classes. The factory performs this mapping without the LLMGateway needing to enumerate all available adapters.

**Creation logic:** Given a model ID (e.g., `"claude-sonnet-4-6"`), returns the appropriate adapter instance configured with the correct API endpoint and credentials.

**Consumer:** The LLMGateway calls the LLMAdapterFactory to resolve the adapter for each invocation.

---

## 10. Strategy Pattern

The strategy pattern is used where a behavior must be selectable at runtime or configurable without code changes. The backend applies it in five specific contexts.

### 10.1 Retrieval Strategy

**Context:** The RAG Engine applies different retrieval strategies based on the query type.

**Strategies defined:** `SemanticRetrievalStrategy` (embedding similarity search), `StructuredFilterStrategy` (exact metadata match), `HybridRetrievalStrategy` (semantic + structured combined), `DeterministicLookupStrategy` (exact-match for standards references).

**Selection:** The RAGEngine selects the retrieval strategy based on the query specification. The Knowledge Retrieval Agent declares the query type; the RAGEngine selects the appropriate strategy.

**Extensibility:** New retrieval strategies (e.g., graph-based retrieval, time-weighted retrieval) are added by implementing the `RetrievalStrategy` interface — zero changes to the RAGEngine's coordination logic.

---

### 10.2 Compliance Evaluation Strategy

**Context:** The Compliance Agent applies different evaluation strategies for different regulatory frameworks.

**Strategies defined:** One strategy per supported regulatory framework (e.g., `GDPRComplianceStrategy`, `HIPAAComplianceStrategy`, `SOC2ComplianceStrategy`, `ISO27001ComplianceStrategy`).

**Selection:** The Compliance Agent determines applicable frameworks from the engagement context and applies each framework's strategy independently.

**Extensibility:** New regulatory frameworks are added as new strategy implementations — no changes to the Compliance Agent's core logic.

---

### 10.3 Diagram Generation Strategy

**Context:** The diagram generator produces different diagram types from the same architecture state.

**Strategies defined:** `MermaidGenerationStrategy`, `GraphvizGenerationStrategy`, `PlantUMLGenerationStrategy` (future).

**Selection:** The OutputGeneratorFactory selects the strategy based on the requested output format.

**Extensibility:** New diagram formats are added as new strategies.

---

### 10.4 Cost Estimation Strategy

**Context:** The Cost Optimization Agent applies different cost models for different deployment targets.

**Strategies defined:** `CloudProviderCostStrategy` (parameterized per cloud provider), `HybridCostStrategy`, `OnPremiseCostStrategy` (future).

**Selection:** Strategy selected from the engagement context's declared deployment target.

**Extensibility:** New cost models per cloud provider or deployment type are added as strategies.

---

### 10.5 Notification Delivery Strategy (Future — Phase 2)

**Context:** Notifications are delivered through different channels based on user preferences and organizational configuration.

**Strategies defined:** `EmailNotificationStrategy`, `SlackNotificationStrategy`, `TeamsNotificationStrategy`.

**Selection:** User preferences from the UserRepository determine the notification strategy.

---

## 11. Dependency Injection Strategy

### 11.1 DI Philosophy

Dependency injection in the ArchitectIQ backend is constructor-based and interface-driven. Every class that requires a dependency declares it in its constructor as an interface type. No class creates its own dependencies using `new` or equivalent instantiation — all dependencies are provided from outside.

This enables three critical capabilities: independent testability (dependencies can be replaced with mocks in unit tests), configuration-driven behavior (different implementations can be injected in different environments), and lifetime management (the DI container controls whether a dependency is a singleton, scoped, or transient instance).

### 11.2 DI Container

The DI container is configured at application startup. It registers:
- All interface-to-implementation mappings
- All service instances and their lifetime
- All manager instances and their lifetime
- All factory instances (factories are registered as singletons)

The DI container is the only place in the backend where a concrete implementation class is referenced by name alongside its interface. The rest of the backend only knows the interface.

### 11.3 Lifetime Classifications

| Lifetime | Description | Applied To |
|----------|-------------|------------|
| **Singleton** | One instance for the application lifetime | PromptManager, AgentFactory, LLMAdapterFactory, LLMGateway, BackgroundJobManager, ObservabilityService, ConfigurationService |
| **Scoped** | One instance per request | AuthService, SessionService, EngagementService, WorkspaceService, all repositories (within a request unit of work) |
| **Transient** | New instance per injection | Individual agent instances (via AgentFactory), output generator instances (via OutputGeneratorFactory), retrieval strategy instances |

### 11.4 DI Registration Conventions

**Layer-by-layer registration:** Infrastructure implementations are registered as the interfaces they implement. The application layer and orchestration layer never register implementations — only interfaces.

**Environment-aware registration:** The DI container reads the environment configuration at startup and registers the appropriate implementations. In the test environment, in-memory implementations are registered. In production, external service implementations are registered.

**Validation on startup:** The DI container validates that every registered interface has exactly one implementation registered. Multiple implementations for the same interface (without a discriminator) are a startup error, not a runtime error.

---

## 12. Cross-Module Communication

### 12.1 Allowed Communication Patterns

| From | To | Method | Constraint |
|------|----|--------|------------|
| API Layer | Application Core Services | Direct service call (via DI) | Only to service interfaces, never to module internals |
| Application Core | Orchestration Layer | Service call via `OrchestratorService` interface | Only to invoke pipeline stages |
| Application Core | Infrastructure Layer | Through defined interface contracts (LedgerInterface, StorageInterface) | Never to concrete implementations directly |
| Orchestration Layer | Agent Layer | Through `AgentInterface.execute()` only | Never to agent internals; only through the base interface |
| Agent Layer | Knowledge Layer | Through `KnowledgeInterface.query()` | Only knowledge retrieval — no knowledge management |
| Agent Layer | Infrastructure Layer | Through `LLMInterface`, `StorageInterface` (read-only), `LedgerInterface` | Only through interfaces |
| Knowledge Layer | Infrastructure Layer | Through `VectorStoreInterface`, `StorageInterface` | Only through interfaces |
| Output Layer | Infrastructure Layer | Through `OutputStorageInterface`, `StorageInterface` (read-only) | Only through interfaces |

### 12.2 Forbidden Communication Patterns

| Forbidden Direction | Reason |
|--------------------|----|
| Agent A → Agent B (direct import) | Agent outputs flow through the Orchestrator. Direct agent-to-agent calls bypass the audit trail and coordination logic. |
| Infrastructure → Application Core | Infrastructure implements contracts — it never drives business logic. Inverting this dependency breaks the Clean Architecture invariant. |
| Infrastructure → Agents | Infrastructure is passive. Agents are active. Infrastructure never initiates calls to agents. |
| API Layer → Agents directly | Business logic must be invoked through the Application Core. The API layer does not know agents exist. |
| API Layer → Infrastructure directly | All infrastructure access is mediated by the Application Core. The API layer does not access storage, cache, or LLM directly. |
| Shared Layer → Any domain layer | Shared is a utility leaf. It has no domain knowledge and no domain dependencies. |
| Background jobs → API Layer | Background jobs operate asynchronously outside the request lifecycle. They cannot call the API layer. |

### 12.3 Communication Contracts

Every cross-module communication uses a typed contract model (Pydantic model). No raw dictionary, no untyped string payload, no `**kwargs` crosses a module boundary. The contract model is defined in the `interfaces` module (for cross-layer contracts) or in the consuming module's own model definitions (for intra-layer contracts with adjacent modules).

---

## 13. Event-Driven Components

### 13.1 Internal Event Bus

The backend maintains an internal event bus for decoupled communication between the Application Core and the Background Job Manager. The event bus is not a distributed message queue at this stage — it is an in-process publish/subscribe mechanism. External persistence-backed queuing is used only for background jobs that must survive process restarts.

**Events published on the internal bus:**

| Event | Publisher | Subscriber | Purpose |
|-------|-----------|------------|---------|
| `EngagementCompletedEvent` | Engagement module | BackgroundJobManager | Triggers knowledge enrichment pipeline |
| `KnowledgeEntrySubmittedEvent` | Ingestion Pipeline | CuratorGateway | Notifies curators of pending approval |
| `KnowledgeEntryApprovedEvent` | CuratorGateway | KnowledgeBase | Triggers indexing of approved entry |
| `AgentOutputAvailableEvent` | Agent Scheduler | ProgressBroadcaster | Triggers workspace section update |
| `PipelineStageCompletedEvent` | Pipeline Manager | ProgressBroadcaster, Engagement Manager | Progress notification + state advance |
| `PipelineFailedEvent` | Orchestrator | Engagement Manager, ObservabilityService | State set to FAILED + alert emission |

### 13.2 Background Execution Boundary

Background jobs execute outside the request lifecycle. The following operations are explicitly designated as background:

- Knowledge entry enrichment from approved engagements
- Embedding generation for new knowledge entries
- Knowledge base index optimization (periodic)
- Decision Ledger chain integrity verification (scheduled)
- Session expiry (scheduled sweep)
- Output artifact cleanup for expired engagements (scheduled)

Background jobs are submitted through the `BackgroundJobManager`, which maintains a durable queue for crash-safe execution. Background job failures generate observability alerts but do not affect the engagement processing path.

### 13.3 Async Boundaries

The backend is implemented with async/await throughout (Python asyncio). Async boundaries are explicit:

- All I/O operations (storage reads/writes, LLM calls, cache operations, vector store queries) are awaited.
- CPU-bound operations (embedding computation, diagram rendering) are dispatched to a thread pool to avoid blocking the event loop.
- Background jobs run in a separate execution context (background task queue) that does not share the request event loop.

---

## 14. Error Handling Architecture

### 14.1 Exception Hierarchy

All exceptions in the ArchitectIQ backend derive from a single `ArchitectIQException` base class. Every exception carries: a machine-readable error code, a human-readable message, a severity level, and a boolean indicating whether the error is recoverable.

```
ArchitectIQException (base)
├── DomainException (business rule violations)
│   ├── InvalidStateTransitionError (state machine rejection)
│   ├── EngagementNotFoundError
│   ├── SessionExpiredError
│   ├── UnauthorizedEngagementAccessError
│   └── ReviewDecisionConflictError
├── ValidationException (input and output validation failures)
│   ├── RequestSchemaValidationError (API layer input)
│   ├── AgentInputValidationError (agent context validation)
│   ├── AgentOutputValidationError (agent result validation — missing citations, schema failure)
│   └── KnowledgeEntryValidationError
├── InfrastructureException (external system failures)
│   ├── LLMProviderError (LLM API failure)
│   │   ├── LLMRateLimitError (429 — retryable)
│   │   ├── LLMUnavailableError (503 — retryable)
│   │   └── LLMInvalidResponseError (non-retryable)
│   ├── StorageWriteError
│   ├── StorageReadError
│   ├── LedgerWriteError (critical — triggers alert)
│   ├── VectorStoreError
│   └── CacheError (non-blocking — falls through to primary)
├── SecurityException (security policy violations)
│   ├── PromptPIIDetectionError (blocked prompt — logged as security event)
│   ├── PromptInjectionDetectionError
│   └── TokenValidationError
└── ConfigurationException (startup and configuration errors)
    ├── MissingConfigurationError
    ├── InvalidConfigurationError
    └── PromptVersionNotFoundError
```

### 14.2 Error Handling at Layer Boundaries

**API Layer boundary:** All exceptions are caught by the global exception handler middleware. Domain exceptions are translated to 4xx responses with typed error bodies. Infrastructure exceptions that are not recoverable are translated to 503 responses. Security exceptions are translated to 401 or 403 responses. All exceptions are logged with the correlation ID.

**Orchestration Layer boundary:** `InfrastructureException` from agent invocations is caught by the AgentScheduler. Recoverable exceptions trigger retry logic. Non-recoverable exceptions produce a typed failure record returned to the Orchestrator. The Orchestrator decides whether the failure is fatal to the stage (critical agent) or advisory (advisory agent).

**Agent Layer boundary:** `AgentOutputValidationError` is handled within the agent's execution lifecycle — the agent marks itself as failed and returns a typed failure result to the Scheduler. The agent does not propagate raw exceptions across its boundary.

**Infrastructure Layer boundary:** All external SDK exceptions are caught at the adapter boundary and translated to the platform's typed `InfrastructureException` hierarchy. No third-party exception type crosses the infrastructure boundary.

### 14.3 Error Recovery Strategy

| Error Type | Recovery Action |
|-----------|----------------|
| `LLMRateLimitError` | Exponential backoff retry (max 3 attempts) within the LLMGateway |
| `LLMUnavailableError` | Exponential backoff retry (max 3 attempts); if exhausted, advisory agent returns degraded result |
| `StorageWriteError` (non-ledger) | Exponential backoff retry (max 5 attempts); if exhausted, error propagated |
| `LedgerWriteError` | Exponential backoff retry (max 5 attempts); if exhausted, critical alert emitted and state transition blocked |
| `CacheError` | Silent fallthrough to primary store; logged as WARN; no user impact |
| `AgentOutputValidationError` | Agent marked as failed; Orchestrator applies degradation rules; architect notified via workspace |
| `InvalidStateTransitionError` | 409 Conflict returned to client; engagement state unchanged |
| `PromptPIIDetectionError` | Agent invocation blocked; security event logged; engagement flagged for review |

---

## 15. Logging Architecture

### 15.1 Structured Log Schema

Every log entry emitted by the backend is a structured JSON object. All log entries inherit the following mandatory fields from the `LogRecord` base model:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 UTC | Precise to milliseconds |
| `level` | Enum | DEBUG / INFO / WARN / ERROR / CRITICAL |
| `correlation_id` | UUID | Request-scoped trace identifier — propagated through all calls |
| `engagement_id` | UUID | Current engagement context (null for non-engagement operations) |
| `session_id` | UUID | Current session context |
| `user_id` | String | Authenticated identity (null for system operations) |
| `service_name` | String | Emitting service identifier |
| `service_version` | String | Deployed service version |
| `module_name` | String | Emitting module within the service |
| `event_type` | String | Machine-parseable event category (e.g., `agent.invocation.started`) |
| `message` | String | Human-readable event description |
| `error_code` | String | Present only on WARN and above; machine-parseable error code |
| `duration_ms` | Integer | Duration of the operation (where applicable) |

### 15.2 Correlation ID Propagation

A correlation ID is assigned at the API Gateway boundary (generated if not present in the request, validated if present — clients may pass a correlation ID for end-to-end tracing). The correlation ID is:

- Attached to the request context object passed through the dependency injection chain
- Included in every log entry emitted during the request lifecycle
- Propagated in the headers of every downstream service call
- Propagated in the context passed to background jobs spawned during the request

The correlation ID enables complete reconstruction of a request's journey through all services from a single identifier.

### 15.3 Audit Logging

Audit logging is distinct from operational logging. Audit events are written both to the operational log stream (for real-time monitoring) and to the Decision Ledger (for immutable record-keeping) for events that require the Decision Ledger's tamper-evidence guarantee.

Events logged to the Decision Ledger (via LedgerService) — not just the operational log:

- Proposal submitted for human review
- Architect approval with identity and approved architecture snapshot
- Architect refinement request with feedback
- Architect rejection with stated reason
- Architect override with component ID and before/after values
- Knowledge entry approval with curator identity
- Knowledge entry deprecation with reason

All other significant events are logged to the operational log stream only.

### 15.4 Sensitive Data in Logs

The following are never logged at any level:

- Authentication tokens or API keys (any secret value)
- Full prompt content (only token counts and model IDs are logged)
- LLM response content (only metadata: finish reason, token counts, latency)
- Personally identifiable information from requirement inputs
- Client-specific proprietary content

If a log entry would require including sensitive content to be useful for debugging, the content is replaced with a hash of the content. The hash is logged. The full content is stored separately (if required) in an access-controlled, encrypted debug store — never in the operational log stream.

---

## 16. Configuration Architecture

### 16.1 Configuration Ownership

Configuration is the exclusive property of the `config/` directory. No configuration value is hardcoded in the backend source. The backend reads configuration through the `ConfigurationService` — a single, centralized configuration access point.

No module reads environment variables directly. No module reads configuration files directly. All configuration access goes through the `ConfigurationService`, which provides:
- Type-safe configuration access (Pydantic models for all config sections)
- Environment-layer resolution (base → environment overlay → environment variables)
- Configuration validation on startup (all required values must be present and valid)
- Hot-reload capability for non-structural configuration changes (feature flags, prompt versions)

### 16.2 Settings Hierarchy

```
ConfigurationService
    ├── ApplicationSettings (server config, rate limits, CORS)
    ├── AuthSettings (OAuth client ID, token TTL, signing key reference)
    ├── AgentSettings (per-agent: model_id, prompt_version, parameters, timeout)
    ├── LLMSettings (per-model: endpoint, rate limits, token budget)
    ├── KnowledgeSettings (retrieval parameters, index partitioning, cache TTL)
    ├── StorageSettings (connection references — not credentials)
    ├── FeatureFlags (boolean and percentage rollout flags)
    ├── PromptSettings (active version per agent, template directory)
    ├── OutputSettings (active template versions per output type)
    ├── ObservabilitySettings (log level, trace sampling rate, metric emit interval)
    └── DomainSettings (active domains, domain-specific overrides)
```

### 16.3 Environment Isolation

No environment-specific value is in source code. The `ConfigurationService` resolves values through the following hierarchy (later sources override earlier):

1. `config/environments/base.yaml` — platform defaults
2. `config/environments/{environment}.yaml` — environment-specific overrides
3. Environment variables — deployment-specific values (endpoint URLs, feature flag overrides)
4. Secrets manager — credentials and sensitive values (injected at runtime, never in config files)

### 16.4 Feature Flags

Feature flags control capability availability at runtime without code deployment. All feature flags are registered in `config/features/feature-flags.yaml` with their default state. The `ConfigurationService` exposes feature flags through a typed `FeatureFlagService`:

- `is_enabled(flag_name) → bool` — for boolean flags
- `get_rollout_percentage(flag_name) → float` — for percentage rollout flags
- `evaluate_for_user(flag_name, user_id) → bool` — for user-cohort rollout flags

Feature flags are hot-reloaded by the ConfigurationService — a flag change does not require a service restart.

---

## 17. Security Architecture

### 17.1 Authentication Boundaries

Authentication is enforced at two boundaries within the backend:

**API Gateway boundary:** Every incoming request is validated for a valid platform session token before it reaches any backend service. The API Gateway middleware is the enforcer. A request without a valid token never reaches the Application Core.

**Service-to-service boundary:** Internal service calls are authenticated through the service mesh using mTLS with service identity certificates. No service accepts a request that originates outside the service mesh. An external caller cannot impersonate an internal service.

### 17.2 Authorization Boundaries

Authorization is enforced at two layers:

**Capability authorization (API Gateway):** The request's declared action (e.g., `engagement:create`, `knowledge:approve`) is evaluated against the authenticated identity's roles. Actions not permitted by the identity's roles are rejected at the gateway with 403.

**Resource authorization (Application Core):** Every operation on an engagement or session validates that the authenticated identity owns the resource. The EngagementService verifies the authenticated user ID matches the engagement's owner user ID on every operation. This check cannot be bypassed — it is embedded in the EngagementRepository query interface (the owner ID is a mandatory filter parameter).

### 17.3 Secrets Management at Runtime

**Startup secret retrieval:** Each service retrieves the secrets it requires from the SecretsService at startup using its service identity certificate. The SecretsService resolves secrets from the configured secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault — adaptor-configurable).

**In-memory secret handling:** Secrets are held in memory only for the duration of active use. They are not stored as class attributes accessible to arbitrary code. They are not logged. They are not included in exception messages or stack traces.

**Secret rotation:** The SecretsService monitors for secret rotation signals from the secrets manager. When a rotation occurs, the affected service re-fetches the updated secret on the next operation that requires it. No service restart is required for secret rotation.

### 17.4 Prompt Content Security

The LLMGateway enforces three content checks on every prompt before transmission:

**PII Detection:** Regular expression and structural pattern matching against known PII formats (email addresses, phone numbers, SSNs, passport numbers, financial account identifiers). A match blocks the invocation and emits a security event log entry.

**Secret Detection:** Pattern matching against known API key formats, connection string formats, and credential patterns. A match blocks the invocation and emits a critical security alert.

**Injection Detection:** Pattern matching against known prompt injection templates — attempts to override the system prompt, attempts to extract the system prompt, attempts to ignore prior instructions. A match triggers sanitization or rejection depending on pattern severity classification.

### 17.5 Trust Hierarchy

```
LEVEL 0 — External (internet): Untrusted; no assumptions about content
LEVEL 1 — Authenticated: Identity verified by API Gateway
LEVEL 2 — Authorized: Capability and resource ownership verified
LEVEL 3 — Service Mesh: Internal service-to-service; mTLS verified
LEVEL 4 — Infrastructure: Storage, cache, secrets; service identity verified
LEVEL 5 — LLM Provider: External; treated as untrusted output that requires parsing and validation
```

The LLM provider is deliberately placed at the same trust level as an external actor. Its outputs are parsed and validated by the agent framework — they are not trusted as-is and are never executed without an intervening validation step.

---

## 18. Backend Extension Strategy

### 18.1 Adding a New Agent

A new agent is self-contained. To add a new agent to the backend:

1. Create the agent module directory under the appropriate agent category.
2. Implement the `BaseAgent` class with the `execute()` method.
3. Declare `AGENT_ID`, `AGENT_VERSION`, and `AGENT_CATEGORY` as class constants.
4. Register the agent in the agent configuration file — the AgentRegistry discovers it automatically.
5. Add agent configuration to `config/agents/`.
6. Add prompt templates to `config/prompts/agents/`.
7. Write unit tests in the agent's `tests/` subdirectory.

**No changes required to:** Orchestration Layer, API Layer, Knowledge Layer, Infrastructure Layer, or any other existing agent.

### 18.2 Adding a New LLM Provider

1. Create a new adapter class in `infrastructure/llm/` that implements `LLMInterface`.
2. Register the new model IDs in `config/models/model-registry.yaml`.
3. The LLMAdapterFactory discovers the new adapter by model ID.
4. Assign the new model to specific agents in `config/agents/`.

**No changes required to:** Agents, Orchestration Layer, Application Core, API Layer.

### 18.3 Adding a New Output Format

1. Create a new generator class in `outputs/` that implements the generator interface.
2. Register the new format in the OutputGeneratorFactory.
3. Add the template to `config/templates/`.
4. The OutputService includes the new format in output generation when the format is declared in the engagement's output specification.

**No changes required to:** Agents, Documentation Agent, Application Core.

### 18.4 Adding a New Compliance Framework

1. Create a new compliance strategy class implementing `ComplianceEvaluationStrategy`.
2. Register the strategy with the `ComplianceStrategyRegistry`.
3. Add the framework's control checklist to the knowledge base via the ingestion pipeline.

**No changes required to:** The Compliance Agent's core logic, other agents, the Application Core.

### 18.5 Adding a New Background Job Type

1. Define a new job class implementing the `BackgroundJob` interface.
2. Define a new triggering event on the internal event bus.
3. Register the event-to-job mapping in the BackgroundJobManager configuration.

**No changes required to:** Existing job implementations, the Application Core's event publishing logic (new events are additive).

---

## 19. Backend Validation Checklist

Use this checklist to validate any new backend module, service, or implementation against the architecture.

### Module Design

- [ ] The module has exactly one stated responsibility, documented in its `README.md`.
- [ ] The module's inputs and outputs are typed Pydantic models — no raw dictionaries cross the module boundary.
- [ ] The module declares its dependencies in its constructor — no `import` of concrete implementations from other modules.
- [ ] The module can be instantiated and tested in isolation with mocked dependencies.
- [ ] No circular dependency exists between this module and any other module.

### Layer Compliance

- [ ] The module only imports from layers at the same level or below (never from layers above).
- [ ] The module uses the `interfaces` module for cross-layer communication — never the concrete implementation classes.
- [ ] The Shared Layer is imported only for utilities and base models — never for domain logic.
- [ ] Infrastructure modules implement interfaces; they do not define them.

### Agent Compliance (agent additions only)

- [ ] The agent inherits from `BaseAgent` and does not override the execution lifecycle template method — only implements the lifecycle step methods.
- [ ] The agent declares `AGENT_ID`, `AGENT_VERSION`, and `AGENT_CATEGORY`.
- [ ] The agent's `execute()` method returns `AgentResult` — never raw LLM output.
- [ ] Every recommendation in the agent output has a citation attached. The `AgentValidator` enforces this.
- [ ] The agent has a confidence score calculation in its output emission.

### Error Handling

- [ ] All exceptions raised by this module derive from `ArchitectIQException`.
- [ ] No raw third-party exception crosses this module's boundary — all external exceptions are caught and translated.
- [ ] Every error type has a machine-readable error code and a boolean `is_recoverable` flag.
- [ ] The module does not swallow exceptions silently — all caught exceptions are either handled, translated, or re-raised as typed platform exceptions.

### Observability

- [ ] Every significant operation emits a structured log entry through the `ObservabilityService`.
- [ ] Long-running operations open and close a trace span.
- [ ] The correlation ID from the request context is included in every log entry.
- [ ] No sensitive data (secrets, PII, full prompt content) appears in log entries.

### Security

- [ ] The module does not access secrets directly — only through the `SecretsService`.
- [ ] The module does not construct or validate authentication tokens — the `auth` module owns this.
- [ ] No user input reaches the LLM provider without passing through the LLMGateway's sanitization checks.
- [ ] The module does not perform authorization checks — this is the API Gateway's and EngagementService's responsibility.

### Testing

- [ ] Unit test coverage ≥ 85% for this module.
- [ ] Unit tests use mocked dependencies — no live external system calls in unit tests.
- [ ] Tests cover both the success path and the primary failure paths.
- [ ] For agent modules: golden output test added to `tests/agents/golden/`.

---

## 20. Backend Freeze Rules

The following rules are immutable. They define the non-negotiable structural properties of the backend. No implementation decision, performance optimization, or external requirement may violate them. Changes require an ARB-approved ADR.

| # | Backend Freeze Rule |
|---|---------------------|
| **BFR-01** | Every agent inherits from `BaseAgent` and is executed through the agent execution lifecycle enforced by the base class. Direct LLM calls outside the agent framework do not produce content that reaches the architect or any generated document. |
| **BFR-02** | No agent imports another agent's implementation. Agent A never calls Agent B. All inter-agent data flows through the Orchestration Layer. |
| **BFR-03** | All LLM API calls are made through the `LLMGateway`. No agent, service, or module holds a direct reference to an LLM provider SDK. |
| **BFR-04** | All storage reads and writes are made through the storage interface. No module holds a direct database connection or direct file system reference except the Infrastructure Layer implementations. |
| **BFR-05** | All secrets are retrieved through the `SecretsService`. No secret value is hardcoded, stored in configuration files, or injected as environment variables into application memory. |
| **BFR-06** | The `EngagementService` is the only component authorized to call `advance_state()` on the `EngagementStateMachine`. No other module, service, or agent transitions engagement states directly. |
| **BFR-07** | The `LedgerRepository.append()` method is write-only and append-only. No module in the backend holds a reference to a `delete()` or `update()` method on the ledger. The ledger adapter does not implement these methods. |
| **BFR-08** | The `Shared` layer imports nothing from any domain layer. Any utility that requires domain knowledge does not belong in `Shared` — it belongs in the domain module that needs it. |
| **BFR-09** | Every exception that crosses a layer boundary is a typed `ArchitectIQException` subclass. No raw third-party exception, no untyped `Exception`, and no string error message crosses a layer boundary. |
| **BFR-10** | No prompt is transmitted to the LLM Gateway without passing the PII, secret, and injection detection checks. A prompt that fails any check is blocked, logged as a security event, and never transmitted. This check is not bypassable by agent configuration. |

---

> **End of BACKEND_MODULE_ARCHITECTURE.md**  
> **Version 1.0.0 — Foundation Release**  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0 · SYSTEM_ARCHITECTURE.md v1.0.0  
> **Classification:** Backend Architecture — Source of Truth  
> **Next Document:** FRONTEND_MODULE_ARCHITECTURE.md
