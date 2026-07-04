# SYSTEM_ARCHITECTURE.md

> **Document Classification:** Runtime Architecture — Source of Truth  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0  
> **Status:** Approved — Foundation Release  
> **Version:** 1.0.0  
> **Scope:** Complete runtime behavior of the ArchitectIQ platform — all components, all flows, all boundaries  
> **Authority:** This document is the definitive description of how the platform behaves as a running system. Every implementation document — backend modules, agent specifications, API contracts, infrastructure configuration — must be consistent with the runtime architecture defined here.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [High-Level Runtime Architecture](#2-high-level-runtime-architecture)
3. [Complete System Context](#3-complete-system-context)
4. [Runtime Components](#4-runtime-components)
5. [End-to-End Execution Flow](#5-end-to-end-execution-flow)
6. [Request Lifecycle](#6-request-lifecycle)
7. [Runtime State Management](#7-runtime-state-management)
8. [AI Execution Architecture](#8-ai-execution-architecture)
9. [Human in the Loop](#9-human-in-the-loop)
10. [Knowledge Flow](#10-knowledge-flow)
11. [Communication Architecture](#11-communication-architecture)
12. [Reliability Strategy](#12-reliability-strategy)
13. [Scalability Strategy](#13-scalability-strategy)
14. [Security Architecture](#14-security-architecture)
15. [Observability](#15-observability)
16. [Performance Strategy](#16-performance-strategy)
17. [Deployment View](#17-deployment-view)
18. [Future Evolution](#18-future-evolution)
19. [Architecture Principles](#19-architecture-principles)
20. [System Freeze Rules](#20-system-freeze-rules)

---

## 1. System Overview

### 1.1 What ArchitectIQ Is at Runtime

ArchitectIQ is a stateful, multi-agent AI platform that operates as a continuous, governed workflow engine. At runtime, it is not a simple request-response system — it is a long-running engagement processor that maintains context across multiple interactions, coordinates a pipeline of specialized AI agents, enforces a human approval gate through a state machine, and produces governed, versioned architecture artifacts.

Every architecture engagement the platform processes moves through a defined sequence of states. Each state transition is either triggered by the completion of an AI agent stage or by an explicit human decision. No state transition happens without being recorded. No architecture reaches its final state without passing through a mandatory human review checkpoint. The state machine is the control plane of the platform — it governs what is permitted to happen, and in what order.

### 1.2 The Three Fundamental Runtime Concerns

At runtime, ArchitectIQ manages three distinct concerns simultaneously:

**The Engagement Concern:** For each architecture engagement, the platform manages a long-lived, stateful workflow from requirement input through to final approved output. This workflow spans multiple user interactions, multiple agent executions, and one or more human review cycles. The engagement is the primary unit of work.

**The Session Concern:** The platform persists the complete interaction context of each architect session — conversation history, intermediate outputs, workspace state, pending approvals — so that any session can be fully restored across logins, devices, and time. A session is the persistent user context that wraps one or more engagements.

**The Knowledge Concern:** Every approved engagement enriches the platform's enterprise knowledge base, which in turn improves the quality of all future agent recommendations. This creates a compounding feedback loop: the platform becomes more valuable with every engagement it processes. The knowledge concern operates asynchronously — it does not block engagement processing.

### 1.3 The Four Runtime Guarantees

The platform provides four runtime guarantees that must hold under all operating conditions:

1. **The Human Approval Guarantee:** No architecture artifact reaches Final status without an explicit, identity-attributed human approval event recorded in the Decision Ledger. This guarantee is enforced by the engagement state machine — there is no code path from the VALIDATING state to the COMPLETED state that bypasses the PENDING_HUMAN_REVIEW state.

2. **The Traceability Guarantee:** Every recommendation produced by an AI agent is traceable to the retrieved knowledge item, enterprise standard, or prior approved precedent that grounded it. A recommendation without a traceable citation is not a valid agent output — the Agent Validator rejects it before it propagates to the next pipeline stage.

3. **The Immutability Guarantee:** Every entry written to the Decision Ledger is immutable and append-only. Approved architectures are versioned snapshots — they are never overwritten. A change to an approved architecture creates a new version with full lineage to its predecessor. The audit trail of the platform cannot be altered after the fact.

4. **The Recovery Guarantee:** No in-progress engagement is permanently lost due to a runtime failure. Engagement state is persisted durably after every state transition. A failed engagement worker can be restarted from the last durable state without requiring the architect to re-submit their requirements or re-execute completed pipeline stages.

---

## 2. High-Level Runtime Architecture

### 2.1 Runtime Component Map

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  EXTERNAL ACTORS                                         │
│              Data Solution Architect          LLM Provider          Identity Provider     │
└──────────────────────┬───────────────────────────┬──────────────────────┬───────────────┘
                       │                           │                      │
                       ▼                           │                      │
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION RUNTIME                                           │
│                                                                                          │
│    ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│    │   Three-Panel Client Application (Sessions | Chat | Workspace)                  │  │
│    │   Session Restoration · Real-time Progress Streaming · Output Display            │  │
│    └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                         │                                                │
└─────────────────────────────────────────┼────────────────────────────────────────────────┘
                                          │ HTTPS / WebSocket
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION RUNTIME                                            │
│                                                                                          │
│  ┌──────────────────┐    ┌─────────────────────┐    ┌──────────────────────────────┐   │
│  │   API Gateway    │───►│  Session Manager     │───►│   Engagement Manager         │   │
│  │ Auth · Rate Limit│    │  Context Restore     │    │   State Machine              │   │
│  └──────────────────┘    └─────────────────────┘    └──────────────┬───────────────┘   │
│                                                                      │                   │
└──────────────────────────────────────────────────────────────────────┼───────────────────┘
                                                                       │ Triggers
                                                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATION RUNTIME                                          │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Master Orchestrator                                         │ │
│  │   Pipeline Manager · Agent Scheduler · Result Aggregator · Progress Broadcaster     │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                         │                                                │
└─────────────────────────────────────────┼────────────────────────────────────────────────┘
                                          │ Dispatches
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              AGENT RUNTIME                                               │
│                                                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────────────────┐ │
│  │   DISCOVERY STAGE   │  │    DESIGN STAGE      │  │      VALIDATION STAGE           │ │
│  │                     │  │                      │  │                                  │ │
│  │ Requirement Intel.  │  │ Architecture Design  │  │ Security Agent                   │ │
│  │ Knowledge Retrieval │  │ Technology Rec.      │  │ Cost Optimization Agent          │ │
│  │                     │  │ Infrastructure Rec.  │  │ Compliance Agent                 │ │
│  └─────────────────────┘  └─────────────────────┘  │ Risk Assessment Agent            │ │
│                                                     └─────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          GOVERNANCE STAGE                                         │   │
│  │  Governance Agent · Human Collaboration Agent · Documentation Agent               │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
└──────────┬───────────────────────────────────────────────────────────────────────────────┘
           │ Reads from                                           │ Writes to
           ▼                                                      ▼
┌────────────────────────────┐              ┌────────────────────────────────────────────┐
│      KNOWLEDGE RUNTIME     │              │            INFRASTRUCTURE RUNTIME           │
│                            │              │                                             │
│  Enterprise Knowledge Base │              │  Decision Ledger · Session Store            │
│  RAG Engine                │              │  Cache Layer · Output Storage               │
│  Ingestion Pipeline        │              │  Observability Stack · Secrets Manager      │
└────────────────────────────┘              └────────────────────────────────────────────┘
```

### 2.2 Runtime Execution Topology

The platform operates in three concurrency modes simultaneously:

**Synchronous (interactive) path:** User interaction — sending a message, submitting requirements, triggering a review decision — requires a near-real-time response. The synchronous path handles authentication, session management, state machine transitions, and the initial acknowledgment of any long-running pipeline execution.

**Asynchronous (pipeline) path:** Agent pipeline execution is inherently long-running. Once triggered, the pipeline executes in the background while the client receives progress updates through a streaming channel. The architect does not wait for the pipeline to complete before they can see intermediate results — they receive progressive output as each pipeline stage completes.

**Background (learning) path:** Knowledge base enrichment from approved engagements, embedding generation for new knowledge entries, and index rebuilding operate asynchronously in the background, completely decoupled from the engagement processing path. A failure in the background path does not affect engagement processing.

---

## 3. Complete System Context

### 3.1 External Actors

| Actor | Type | Interaction | Trust Level |
|-------|------|-------------|-------------|
| **Data Solution Architect** | Primary human user | Three-panel workspace; submits requirements, reviews proposals, approves/refines/rejects architectures | Authenticated; role-based access |
| **Platform Administrator** | Human administrator | Configuration management, user management, knowledge base governance, audit log access | Authenticated; elevated privileges |
| **Knowledge Base Contributor** | Human (architect submitting a pattern) | Submits knowledge entries through the ingestion pipeline; entries require approval before becoming retrievable | Authenticated; limited to ingestion actions |

### 3.2 External Systems

| System | Role | Interaction Pattern | Failure Impact |
|--------|------|---------------------|----------------|
| **Identity Provider** (GitHub OAuth) | User authentication and identity | OAuth 2.0 / OIDC flow; token validation on every authenticated request | Authentication unavailable → login blocked; existing sessions served from token cache |
| **LLM Provider** (Anthropic and future providers) | AI reasoning for all 12 agents | HTTPS request per agent invocation; synchronous within agent execution | LLM unavailable → affected agent fails; pipeline stage fails gracefully; engagement blocked at current stage |
| **Vector Store** | Knowledge base semantic search | Synchronous query per knowledge retrieval call | Degraded retrieval quality → Knowledge Retrieval Agent flags reduced confidence; pipeline continues |
| **Structured Storage** | Session, engagement, ledger, output persistence | Synchronous read/write for critical paths; async for non-critical | Write failure on critical path → state transition fails; retried with backoff; engagement preserved |
| **Cache Provider** | Performance layer for retrieval and computation | Synchronous read; async write | Cache miss → request falls through to primary store; performance degraded, behavior unchanged |
| **Observability Platform** | Metrics, logs, traces | Asynchronous emission; fire-and-forget | Observability failure → silent degradation; core platform unaffected |

### 3.3 Trust Boundaries

```
UNTRUSTED (public internet)
    │
    ▼ TLS termination + identity verification
PARTIALLY TRUSTED (authenticated architect session)
    │
    ▼ Role validation + engagement ownership check
TRUSTED (authenticated + authorized for this engagement)
    │
    ▼ Internal service mesh — mTLS between services
FULLY TRUSTED (internal platform services)
    │
    ▼ Secrets manager — no credential in runtime memory beyond immediate use
INFRASTRUCTURE (secrets, keys, credentials — never in application memory at rest)
```

**The trust boundary between the LLM Provider and the platform is one-directional.** The platform sends sanitized context to the LLM. The LLM returns generated text. The LLM is an external system — it is not trusted to call back into the platform, access storage, or take any action beyond generating text.

---

## 4. Runtime Components

### 4.1 Client Application

**Purpose:** The runtime interface between the Data Solution Architect and the platform. A browser-based application that renders the three-panel workspace, maintains client-side session state, and communicates with the backend exclusively through the API Gateway.

**Responsibility at runtime:** Render the sessions panel (past and current engagement history), the chat panel (the conversational interaction surface with the AI pipeline), and the workspace panel (the evolving architecture artifact). Stream and display progressive pipeline output as it arrives from the backend. Surface the human review gate when the pipeline reaches the PENDING_HUMAN_REVIEW state. Maintain client-side state sufficient to restore the workspace display without requiring a full server round-trip.

**Inputs:** HTTP responses from the API Gateway; streaming events from the progress channel; user interactions (text input, review decisions, file uploads).

**Outputs:** HTTP requests to the API Gateway; user-initiated state transitions (approve, refine, reject); file upload payloads.

**Lifecycle:** Active for the duration of a browser session. Reconnects to in-progress engagement state on page refresh or re-login without requiring the architect to re-submit their inputs.

**Communication pattern:** Synchronous REST calls for state-changing operations. WebSocket or Server-Sent Events for progressive pipeline output streaming. No direct communication with any backend service other than the API Gateway.

---

### 4.2 API Gateway

**Purpose:** The single entry point for all client requests. Enforces authentication, authorization, and rate limiting before any request reaches backend services.

**Responsibility at runtime:** Validate the identity token on every incoming request. Evaluate the request against the authorization model (does this identity have the right to perform this action on this resource?). Apply per-identity rate limiting. Route authenticated, authorized requests to the appropriate backend service. Terminate TLS. Assign a correlation ID to every request for distributed tracing. Log every request and response at the gateway boundary.

**Inputs:** All HTTPS requests from the Client Application.

**Outputs:** Routed internal requests with validated identity context and correlation ID attached. Authentication failures (401), authorization failures (403), and rate limit rejections (429) returned to the client without reaching backend services.

**Lifecycle:** Stateless — horizontally scalable. Rate limit state is maintained in the shared cache layer, not in the gateway process itself.

**Critical invariant:** No request reaches any backend service without passing through the API Gateway. Backend services do not accept direct external connections.

---

### 4.3 Session Manager

**Purpose:** Manages the complete lifecycle of architect sessions — creation, persistence, restoration, and expiry.

**Responsibility at runtime:** On first login, creates a new session with a stable session identifier and persists the session record. On subsequent logins, restores the full session from persistent storage, including conversation history and workspace state. Maintains the association between a session and its active engagement(s). Handles session expiry according to configured policy. Provides session context to downstream components on every request.

**Inputs:** Validated identity from the API Gateway; session identifier from the client request.

**Outputs:** Session context (session ID, identity, active engagement ID, conversation history, workspace state) attached to every downstream request.

**Lifecycle:** Session records are persistent — they outlive individual HTTP connections and browser sessions. A session is only expired by explicit logout or by configured inactivity timeout.

**State owned:** Session record (session ID, identity, creation time, last active time, active engagement references, conversation history index).

---

### 4.4 Engagement Manager

**Purpose:** The control plane for architecture engagements. Implements and enforces the engagement lifecycle state machine.

**Responsibility at runtime:** Creates new engagement records when an architect initiates a new architecture request. Transitions engagement states according to the state machine — accepting only valid transitions and rejecting invalid ones. Persists every state transition durably before acknowledging it. Coordinates the initiation and resumption of agent pipeline execution. Enforces the human approval gate by requiring an explicit approval event before permitting the APPROVED → GENERATING_OUTPUTS transition. Provides engagement context to the Orchestration Layer on pipeline invocation.

**Inputs:** User intent signals from the API Gateway (new engagement, review decision, refinement request); pipeline completion signals from the Orchestration Layer.

**Outputs:** Engagement state transitions (persisted); pipeline execution triggers (to the Orchestration Layer); engagement context for state restoration.

**Lifecycle:** An engagement record persists from creation through to completion or explicit archival. An engagement's state is the single source of truth for where that engagement is in its lifecycle.

**State machine — complete state set:**

```
INITIATED
    ↓ (automatic on creation)
REQUIREMENTS_EXTRACTING
    ↓ (on Requirement Intelligence Agent completion)
KNOWLEDGE_RETRIEVING
    ↓ (on Knowledge Retrieval Agent completion)
DESIGNING
    ↓ (on Design Stage completion: Architecture + Technology + Infrastructure agents)
VALIDATING
    ↓ (on Validation Stage completion: Security + Cost + Compliance + Risk agents — parallel)
GOVERNANCE_CHECKING
    ↓ (on Governance Agent completion — hard policy violation → BLOCKED; pass → advance)
PENDING_HUMAN_REVIEW      ◄─────────────────────────────────────────┐
    ↓ (architect decision: approve / refine / reject)                │
    ├── APPROVED (architect selects approve)                         │
    │       ↓                                                        │
    │   GENERATING_OUTPUTS                                           │
    │       ↓                                                        │
    │   COMPLETED                                                    │
    │                                                                │
    ├── IN_REFINEMENT (architect selects refine + provides feedback)─┘
    │   (targeted re-execution of affected agents only)
    │
    └── REJECTED (architect selects reject → engagement closed)

BLOCKED (hard governance violation — not reviewable until resolved)
FAILED (unrecoverable pipeline failure — available for retry)
```

**Non-negotiable state machine rule:** There is no transition from any state to COMPLETED that does not pass through PENDING_HUMAN_REVIEW and APPROVED. This invariant is enforced in the state machine code — it is not a policy that can be disabled by configuration.

---

### 4.5 Master Orchestrator

**Purpose:** Coordinates the end-to-end agent pipeline for a given engagement stage. The Orchestrator is the intelligence of the pipeline — it knows which agents to run, in which order, with what inputs, and how to assemble their outputs.

**Responsibility at runtime:** Receives an execution trigger from the Engagement Manager with the current engagement context. Determines which pipeline stage to execute based on the current engagement state. Dispatches agent tasks to the Agent Scheduler — sequentially for dependent stages, in parallel for independent stages. Collects agent results as they complete. Passes each stage's output as the input for the next stage. Aggregates all stage outputs into a coherent proposal package. Emits progress events to the Progress Broadcaster for client-side display. Reports completion or failure back to the Engagement Manager.

**Inputs:** Engagement context (current state, structured requirements, prior agent outputs, retrieved knowledge, architect feedback for refinement). Pipeline stage specification from the current engagement state.

**Outputs:** Aggregated agent pipeline results; progress events; stage completion or failure signals to the Engagement Manager.

**Lifecycle:** Stateless across requests. A new orchestration execution is initiated for each pipeline trigger. The Orchestrator does not maintain state between pipeline triggers — all durable state lives in the Engagement Manager's engagement record.

**Critical invariant:** The Orchestrator never modifies agent outputs — it only routes and aggregates them. An agent's output is the agent's output. The Orchestrator's job is to ensure the right outputs reach the right inputs in the right order.

---

### 4.6 Agent Scheduler

**Purpose:** Manages the execution of agent tasks — queuing, dispatching, parallelization, and result collection.

**Responsibility at runtime:** Receives a set of agent task specifications from the Orchestrator. Determines which tasks can be executed in parallel (independent tasks within a stage) and which must be sequential (dependent on prior output). Dispatches tasks to available agent worker processes. Tracks task completion and failure. Returns results to the Orchestrator as they arrive. Enforces per-task timeouts. Handles task-level retry on transient failure without requiring the Orchestrator to manage retry logic.

**Inputs:** Agent task specifications (agent ID, input context, execution parameters, timeout).

**Outputs:** Agent results (or failure records) returned to the Orchestrator in completion order.

**Lifecycle:** Stateless across engagements. The execution context for each task is fully contained in the task specification.

---

### 4.7 Agent Workers (12 Agents)

Each of the platform's twelve agents is a discrete runtime component with a single responsibility. All agents share a common execution model — they differ only in their specific logic, their prompts, and their inputs and outputs.

**Common execution model for every agent:**

1. **Receive context** from the Agent Scheduler: engagement context, stage inputs, agent configuration (model selection, prompt version, parameters).
2. **Validate inputs** against the agent's declared input schema. Reject malformed inputs immediately.
3. **Retrieve relevant knowledge** from the Knowledge Layer (agents that require retrieval — not all agents query the knowledge base).
4. **Construct prompt** by merging the retrieved context with the versioned prompt template and the structured input. The prompt is constructed by the agent, not passed in from outside.
5. **Invoke LLM** through the LLM Gateway using the model assigned to this agent.
6. **Parse and validate output** from the LLM response against the agent's declared output schema. An output that fails schema validation is not passed downstream — the Agent Validator flags it as a failure.
7. **Attach citations** to every recommendation or finding in the output. A recommendation without a citation fails validation.
8. **Calculate confidence score** for the output based on retrieval relevance, schema completeness, and internal consistency checks.
9. **Emit structured result** to the Agent Scheduler with: output payload, citation list, confidence score, token usage, and latency.

**Agent execution groups and their pipeline position:**

| Stage | Agents | Execution Pattern |
|-------|--------|------------------|
| Discovery | Requirement Intelligence Agent | Sequential (first in pipeline) |
| Discovery | Knowledge Retrieval Agent | Sequential (depends on req. extraction output) |
| Design | Architecture Design Agent | Sequential (depends on knowledge retrieval) |
| Design | Technology Recommendation Agent | Sequential (depends on architecture candidates) |
| Design | Infrastructure Recommendation Agent | Sequential (depends on technology selection) |
| Validation | Security Agent | Parallel (all four run simultaneously on design output) |
| Validation | Cost Optimization Agent | Parallel |
| Validation | Compliance Agent | Parallel |
| Validation | Risk Assessment Agent | Parallel (also consumes security and compliance outputs after they complete) |
| Governance | Governance Agent | Sequential (runs after all validation outputs are available) |
| Governance | Human Collaboration Agent | Sequential (packages proposal for architect review; runs after governance check) |
| Governance | Documentation Agent | Sequential (runs after architect approval — generates final outputs) |

---

### 4.8 LLM Gateway

**Purpose:** Abstracts all LLM provider interactions behind a single runtime interface. Every agent interacts with the LLM through the LLM Gateway — no agent has a direct dependency on a specific LLM provider SDK.

**Responsibility at runtime:** Accepts a structured prompt request with a model identifier, prompt content, and execution parameters. Routes the request to the appropriate provider adapter based on the model identifier. Handles provider-specific request formatting. Enforces token budget constraints. Applies per-model rate limiting. Returns a normalized response regardless of which provider served the request. Records every LLM invocation — model, token counts, latency, success/failure — in the observability layer.

**Inputs:** Structured prompt request (model ID, system prompt, user prompt, parameters: temperature, max tokens, stop sequences).

**Outputs:** Normalized LLM response (generated text, finish reason, token usage statistics).

**Lifecycle:** Stateless. Each invocation is independent.

**Critical invariant:** No agent prompt passes personally identifiable information, client secrets, or internal infrastructure details. The LLM Gateway enforces a content sanitization check on every prompt before transmission. Prompts that contain patterns matching PII or secret formats are rejected and logged as security events.

---

### 4.9 Knowledge Base and RAG Engine

**Purpose:** The enterprise knowledge store and retrieval engine that grounds all agent reasoning in organizational knowledge rather than model-internal knowledge alone.

**Responsibility at runtime (Knowledge Base):** Stores enterprise architecture patterns, technology evaluations, approved precedents, regulatory frameworks, domain-specific knowledge, and technology catalog entries. Maintains a vector index for semantic similarity search and a structured index for exact-match and filtered retrieval. Provides read access to the Knowledge Retrieval Agent (primary consumer) and, through the Compliance Agent, to regulatory framework data.

**Responsibility at runtime (RAG Engine):** Executes retrieval queries from the Knowledge Retrieval Agent. Applies a multi-signal retrieval strategy: semantic similarity for broad relevance, structured filters for domain and recency, deterministic lookup for exact-match standards. Ranks results by composite relevance score. Constructs the retrieved context package — with source citations — that is passed to the Knowledge Retrieval Agent's output.

**Inputs to RAG Engine:** Query from the Knowledge Retrieval Agent (structured requirements, domain context, engagement type, explicit search terms).

**Outputs from RAG Engine:** Ranked set of relevant knowledge items with source citations, relevance scores, and recency metadata. Maximum item count is bounded by agent configuration to prevent context overflow.

**Lifecycle:** The knowledge base is a persistent, living store. The RAG Engine is stateless — it executes queries against the persistent store.

---

### 4.10 Decision Ledger

**Purpose:** The immutable, append-only record of every significant event in the platform's operation. The Decision Ledger is the platform's audit trail, accountability mechanism, and forensic record.

**Responsibility at runtime:** Accepts write requests from the Engagement Manager and the Human Collaboration Agent. Records: every proposal submitted for human review, every architect approval or rejection with identity attribution, every architect edit (override), every refinement request with feedback, every final architecture approval with timestamp, agent version, and prompt version. Provides read access for audit queries and for Decision Ledger review display in the workspace panel. Guarantees that every write is durable before acknowledging success — a state transition that depends on a ledger record being written does not advance until the write is confirmed.

**Inputs:** Structured ledger entries from the Engagement Manager and Human Collaboration Agent (event type, engagement ID, session ID, actor identity, payload, timestamp, hash of prior entry).

**Outputs:** Confirmation of successful write; ledger query results for read operations.

**Lifecycle:** Entries in the Decision Ledger are never deleted or modified. The ledger grows monotonically. Entries are retained according to the enterprise records retention policy.

**Integrity mechanism:** Each entry contains a cryptographic hash of the prior entry, forming a hash chain. Any attempt to modify or delete an entry breaks the chain, which is detected on integrity verification. Integrity verification is run on a scheduled basis.

---

### 4.11 Output Generator

**Purpose:** Produces all platform-generated deliverables from the approved design state.

**Responsibility at runtime:** Accepts the approved architecture state from the Documentation Agent and renders it into the configured output formats. Operates after architect approval — never before. Each output format has a dedicated renderer that applies the appropriate versioned template to the structured design data. Stores all generated outputs in the Output Storage component with engagement ID-scoped paths. Makes outputs available to the client through the Output Service.

**Inputs:** Approved architecture state (structured JSON from the Documentation Agent); output format specification; versioned templates from the configuration layer.

**Outputs:** Generated files in configured formats: Markdown documents, interactive HTML reports, PDF documents, Mermaid diagram source, Graphviz DOT source, rendered SVG/PNG diagrams, machine-readable JSON architecture state.

**Lifecycle:** Triggered once per approval event. If the architect makes changes after approval (creating a new version), the Output Generator runs again for the new version.

---

### 4.12 Progress Broadcaster

**Purpose:** Pushes real-time pipeline execution progress from the backend to the client application without requiring polling.

**Responsibility at runtime:** Maintains a persistent connection (WebSocket or Server-Sent Events) to each active client session. Subscribes to pipeline stage completion events emitted by the Orchestrator. Translates internal progress signals into client-facing progress messages with stage name, completion percentage, and stage-level summary. Pushes these messages to the connected client in real time. Handles client reconnection — a client that reconnects receives the current state plus a replay of progress events since its last connection.

**Inputs:** Pipeline progress events from the Orchestrator (stage name, status, partial output).

**Outputs:** Real-time push messages to connected client sessions.

**Lifecycle:** Connection-scoped. The broadcaster maintains a connection for the duration of the client session. No state is retained after session termination.

---

## 5. End-to-End Execution Flow

### 5.1 Complete Flow Diagram

```
ARCHITECT                     APPLICATION LAYER            ORCHESTRATION LAYER            AGENT LAYER
    │                               │                              │                           │
    │  1. Submit requirement         │                              │                           │
    │  (any format: text, doc, form) │                              │                           │
    ├──────────────────────────────►│                              │                           │
    │                               │                              │                           │
    │                               │ 2. Authenticate              │                           │
    │                               │    Authorize                 │                           │
    │                               │    Rate-limit                │                           │
    │                               │    Assign correlation ID     │                           │
    │                               │                              │                           │
    │                               │ 3. Restore/create session    │                           │
    │                               │    Create engagement         │                           │
    │                               │    State: INITIATED          │                           │
    │                               │                              │                           │
    │◄──────────────────────────────│ 4. ACK: Engagement created   │                           │
    │  (immediate response)         │    Pipeline starting          │                           │
    │                               │                              │                           │
    │                               │ 5. Trigger pipeline          │                           │
    │                               │    State: REQUIREMENTS_      │                           │
    │                               │    EXTRACTING                │                           │
    │                               ├─────────────────────────────►│                           │
    │                               │                              │ 6. Dispatch:               │
    │                               │                              │    Requirement Intel. Agent│
    │                               │                              ├──────────────────────────►│
    │◄·····························streaming progress events········│◄──────────────────────────│
    │   (workspace panel updates)   │                              │    Structured requirements │
    │                               │                              │    Ambiguity flags         │
    │                               │                              │    Confidence scores       │
    │                               │                              │                            │
    │                               │    State:                    │ 7. Dispatch:               │
    │                               │    KNOWLEDGE_RETRIEVING      │    Knowledge Retrieval Agent│
    │                               │                              ├──────────────────────────►│
    │◄·····························streaming progress events········│◄──────────────────────────│
    │                               │                              │    Ranked patterns         │
    │                               │                              │    With citations          │
    │                               │                              │                            │
    │                               │    State: DESIGNING          │ 8. Dispatch (sequential):  │
    │                               │                              │    Architecture Design →   │
    │                               │                              │    Technology Rec. →       │
    │                               │                              │    Infrastructure Rec.     │
    │◄·····························streaming progress events········│◄──────────────────────────│
    │                               │                              │    Candidate architectures │
    │                               │                              │    Tech. selections        │
    │                               │                              │    Topology design         │
    │                               │                              │                            │
    │                               │    State: VALIDATING         │ 9. Dispatch (parallel):    │
    │                               │                              │    Security Agent          │
    │                               │                              │    Cost Opt. Agent         │
    │                               │                              │    Compliance Agent        │
    │                               │                              │    Risk Assessment Agent   │
    │◄·····························streaming progress events········│◄──────────────────────────│
    │                               │                              │    Threat model            │
    │                               │                              │    TCO model               │
    │                               │                              │    Compliance checklist    │
    │                               │                              │    Risk register           │
    │                               │                              │                            │
    │                               │    State:                    │ 10. Dispatch:              │
    │                               │    GOVERNANCE_CHECKING       │    Governance Agent        │
    │                               │                              ├──────────────────────────►│
    │                               │                              │◄──────────────────────────│
    │                               │                              │    Policy check results    │
    │                               │                              │    Guardrail flags         │
    │                               │                              │                            │
    │                               │    State:                    │ 11. Dispatch:              │
    │                               │    PENDING_HUMAN_REVIEW      │    Human Collaboration     │
    │                               │                              │    Agent (packages         │
    │                               │                              │    complete proposal)      │
    │                               │                              ├──────────────────────────►│
    │◄──────────────────────────────│◄─────────────────────────────│◄──────────────────────────│
    │   12. REVIEW GATE             │    Decision Ledger: Proposal  │    Consolidated proposal  │
    │   Complete proposal displayed │    recorded                   │    package                │
    │   in workspace panel          │                              │                            │
    │   (requirements, candidates,  │                              │                            │
    │    validation findings,       │                              │                            │
    │    risk register, citations)  │                              │                            │
    │                               │                              │                            │
    │  13. ARCHITECT DECISION       │                              │                            │
    │  A) APPROVE                   │                              │                            │
    │  B) REFINE (with feedback)    │                              │                            │
    │  C) REJECT                    │                              │                            │
    │                               │                              │                            │
    │  ── PATH A: APPROVE ──────────┤                              │                            │
    │                               │ Decision Ledger: Approval    │                            │
    │                               │ with identity + timestamp    │                            │
    │                               │ State: GENERATING_OUTPUTS    │ 14. Dispatch:              │
    │                               │                              │    Documentation Agent     │
    │                               │                              │    (HLD, LLD, diagrams,    │
    │                               │                              │     executive summary)     │
    │                               │                              │                            │
    │                               │ 15. Output Generator         │                            │
    │                               │     renders all formats      │                            │
    │                               │     stores to Output Storage │                            │
    │                               │     State: COMPLETED         │                            │
    │                               │                              │                            │
    │                               │ 16. Knowledge Ingestion      │                            │
    │                               │     (background — async)     │                            │
    │◄──────────────────────────────│                              │                            │
    │   17. Outputs available       │                              │                            │
    │   in workspace panel          │                              │                            │
    │                               │                              │                            │
    │  ── PATH B: REFINE ───────────┤                              │                            │
    │  (Architect provides feedback)│ Decision Ledger: Refinement  │                            │
    │                               │ request recorded             │                            │
    │                               │ State: IN_REFINEMENT         │                            │
    │                               ├─────────────────────────────►│                            │
    │                               │ Targeted re-execution:       │ Only affected agents       │
    │                               │ Only agents impacted by      │ re-run. Unaffected         │
    │                               │ architect's feedback re-run  │ outputs preserved.         │
    │                               │ ─────────────────────────────┤                            │
    │                               │ Returns to PENDING_HUMAN_REVIEW (step 12)                 │
    │                               │                              │                            │
    │  ── PATH C: REJECT ───────────┤                              │                            │
    │                               │ Decision Ledger: Rejection   │                            │
    │                               │ with reason recorded         │                            │
    │                               │ State: REJECTED              │                            │
    │                               │ Engagement closed            │                            │
```

---

## 6. Request Lifecycle

### 6.1 Stage-by-Stage Lifecycle

Every request that initiates or advances an architecture engagement passes through the following stages. Each stage has a defined entry condition, a defined execution, and a defined exit condition.

**Stage 1 — Authentication and Authorization**

*Entry condition:* HTTP request received at the API Gateway.  
*Execution:* Identity token validated against the Identity Provider (or token cache). Request payload validated for schema conformance. Authorization evaluated: does this identity have rights to the requested action on the requested resource?  
*Exit condition (success):* Validated, authorized request forwarded with identity context and correlation ID.  
*Exit condition (failure):* 401 (unauthenticated), 403 (unauthorized), 400 (malformed request) returned to client. No backend service reached.

**Stage 2 — Session Resolution**

*Entry condition:* Authenticated, authorized request.  
*Execution:* Session identifier extracted from request. Session record retrieved from Session Store. If session record not found, new session created. Session context attached to request.  
*Exit condition:* Request enriched with session context forwarded to Engagement Manager.

**Stage 3 — Engagement State Transition**

*Entry condition:* Session context available; request intent identified (new engagement, review decision, refinement, output retrieval).  
*Execution:* State machine evaluates the requested transition against the current engagement state. Valid transitions are persisted before being acknowledged. Invalid transitions are rejected with a 409 (Conflict) response.  
*Exit condition (pipeline trigger):* Valid transition accepted, persisted, pipeline execution triggered.  
*Exit condition (review decision):* Valid approval/rejection persisted to engagement record and Decision Ledger. Next action determined by decision type.

**Stage 4 — Pipeline Execution (asynchronous)**

*Entry condition:* Engagement state transitioned to a pipeline-executing state (e.g., REQUIREMENTS_EXTRACTING).  
*Execution:* Orchestrator receives execution context. Agents are dispatched according to the stage specification. Progress events are emitted to the Progress Broadcaster throughout execution. Each agent's output is validated before propagating to the next stage. Pipeline failure at any stage is handled per the Reliability Strategy (Section 12).  
*Exit condition (success):* Final pipeline stage completes; Engagement Manager notified; state advanced.  
*Exit condition (failure):* Agent failure after exhausted retries; Engagement Manager notified; state set to FAILED; engagement preserved for retry.

**Stage 5 — Human Review (synchronous gate)**

*Entry condition:* Engagement state is PENDING_HUMAN_REVIEW.  
*Execution:* Architect receives consolidated proposal package in the workspace panel. Architect examines requirements interpretation, candidate architectures, trade-off rationale, validation findings, and decision citations. Architect takes one of three actions: approve, refine with feedback, or reject.  
*Exit condition:* Architect decision recorded in Decision Ledger. State machine advanced based on decision.

**Stage 6 — Output Generation (approval path)**

*Entry condition:* Engagement state is GENERATING_OUTPUTS (reached only via architect approval).  
*Execution:* Documentation Agent structures the approved architecture into all required document sections. Output Generator renders each configured format. Outputs stored in the Output Storage component.  
*Exit condition:* All configured outputs successfully generated and stored. State advanced to COMPLETED. Background knowledge ingestion triggered.

**Stage 7 — Knowledge Enrichment (background)**

*Entry condition:* Engagement state is COMPLETED.  
*Execution:* The ingestion pipeline processes the approved architecture as a new knowledge base entry. Document is chunked, embedded, and indexed in the vector store. Entry receives an approval status that makes it retrievable for future engagements.  
*Exit condition:* Knowledge base enriched with the new entry. This stage does not affect the engagement's COMPLETED state — it is fully asynchronous.

---

## 7. Runtime State Management

### 7.1 Session State

Session state represents the complete context of an architect's interaction with the platform, persisted across logins. Session state is owned and managed by the Session Manager.

**What session state contains:**
- Session identifier and architect identity
- Session creation timestamp and last active timestamp
- Ordered list of active and historical engagement references
- Conversation history index (message sequence with roles and timestamps)
- Client workspace display preferences
- Active streaming connection reference (non-persistent — reconstructed on reconnect)

**Session state persistence:** Session state is written to the structured storage layer on every meaningful change. Session state reads are served from a short-lived cache to minimize storage load on interactive requests.

**Session recovery:** If a client disconnects mid-session, the session state remains intact in storage. On reconnection, the Session Manager restores the session state from storage. The Progress Broadcaster replays any pipeline events that occurred during the disconnection. The architect resumes exactly where they left off.

### 7.2 Engagement State

Engagement state is the durable record of everything about a specific architecture engagement — its current phase in the lifecycle, the outputs of every completed pipeline stage, and the history of human decisions.

**What engagement state contains:**
- Engagement identifier and parent session reference
- Current state machine state
- Structured requirements output (from Requirement Intelligence Agent)
- Retrieved knowledge context (from Knowledge Retrieval Agent)
- Candidate architecture outputs (from Design Stage agents)
- Validation findings (from Validation Stage agents — security, cost, compliance, risk)
- Governance check result (from Governance Agent)
- Human review history (decisions, feedback, override records)
- Approved architecture snapshot (immutable after first approval)
- Version history (lineage of all prior approved versions)
- Output references (paths to generated output files)

**Engagement state persistence:** Every state transition is persisted before the transition is acknowledged. A state transition that fails before persistence is rolled back — the engagement remains in its prior state. This ensures the Recovery Guarantee: no engagement loses its state due to a transient failure.

### 7.3 Agent Execution Context

The agent execution context is the ephemeral runtime context assembled by the Orchestrator for each agent invocation. It is not persisted — it is reconstructed from durable engagement state when needed.

**What the context contains:** Engagement identifier; structured requirements; relevant prior agent outputs (stage-specific); retrieved knowledge items with citations; architect feedback (for refinement runs); agent configuration (model ID, prompt version, parameters); correlation ID for tracing.

### 7.4 Approval State

Approval state is a subset of engagement state that specifically tracks the human review and approval lifecycle.

**Approval state contents:** Review package version (corresponds to the pipeline output that triggered this review cycle); architect identity performing the review; decision (pending / approved / refined / rejected); override records (specific design elements modified by the architect); feedback provided for refinement; timestamp and digital signature of approval events.

**Approval state immutability:** Once an approval event is recorded in the Decision Ledger, it cannot be modified. If the architect subsequently changes the approved architecture, a new approval event is created for the new version. The original approval event remains in the ledger, and the new approval event references it as a predecessor.

### 7.5 Output State

Output state tracks the generated artifacts associated with a completed engagement.

**Output state contents:** Engagement identifier; output format list; file paths in Output Storage (one per format); generation timestamp; template version used for each format; output integrity checksum.

### 7.6 Recovery State

Recovery state enables the platform to resume an in-progress engagement pipeline from the point of failure, without requiring the architect to re-submit inputs or re-execute completed stages.

**Recovery mechanism:** Because every state transition is persisted before being acted upon, and because the Orchestrator reconstructs its execution context from persisted engagement state, a failed pipeline execution can be retried from the last completed state. The retry initiates from the pipeline stage that failed — it does not replay already-completed stages.

---

## 8. AI Execution Architecture

### 8.1 Agent Execution Lifecycle

Every agent follows an identical runtime execution lifecycle. The lifecycle is enforced by the Base Agent runtime — individual agents implement their specific logic within the lifecycle framework, not in place of it.

```
RECEIVE CONTEXT
    ↓
VALIDATE INPUTS (schema validation — immediate rejection on failure)
    ↓
RETRIEVE KNOWLEDGE (Knowledge Layer query — if required by this agent)
    ↓
CONSTRUCT PROMPT (merge: system prompt template + retrieved context + structured inputs)
    ↓
SANITIZE PROMPT (PII and secret pattern check — rejection on match)
    ↓
INVOKE LLM (via LLM Gateway — with configured model and parameters)
    ↓
PARSE RESPONSE (extract structured output from LLM response)
    ↓
VALIDATE OUTPUT (schema validation + citation presence check + confidence threshold)
    ↓
EMIT RESULT (structured output + citations + confidence score + token usage + latency)
    ↓
LOG EXECUTION (correlation ID + all execution metadata — to observability layer)
```

### 8.2 Parallel Execution — Validation Stage

The four Validation Stage agents (Security, Cost Optimization, Compliance, Risk Assessment) execute in parallel on the completed Design Stage output. Parallel execution reduces validation latency from the sum of individual agent latencies to approximately the maximum individual latency.

```
                         Design Stage Output
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼               ▼
           Security         Cost Opt.      Compliance       (Risk Assessment
            Agent            Agent           Agent          waits for Security
               │                │               │           and Compliance)
               │                │               │
               └────────────────┼───────────────┘
                                ▼
                        Risk Assessment Agent
                        (aggregates all findings
                         into unified risk register)
                                │
                                ▼
                         Governance Agent
```

The Risk Assessment Agent has a partial dependency: it can begin its analysis on the Design Stage output immediately, but it waits for Security Agent and Compliance Agent outputs before finalizing its risk register. This dependency is managed by the Agent Scheduler — the Risk Assessment Agent receives the Design Stage output immediately but receives the Security and Compliance findings as they complete.

### 8.3 Targeted Refinement — Partial Re-execution

When an architect selects the refine action, the Orchestrator does not re-run the entire pipeline. It analyzes the architect's feedback to determine which agents' outputs are affected by the requested change, and re-runs only those agents.

**Refinement dependency analysis:**

```
Refinement target:                   Agents that re-run:
─────────────────────────────────────────────────────────────────────
Requirements interpretation        → All agents (requirement change affects everything)
Architecture pattern selection     → Design Stage + Validation Stage + Governance
Technology selection               → Technology Rec. + Infrastructure Rec. + Cost Opt. + Risk
Security control design            → Security Agent + Governance Agent
Cost model parameters              → Cost Optimization Agent + Risk Assessment Agent
Compliance framework scope         → Compliance Agent + Risk Assessment Agent + Governance
Output only (documentation style)  → Documentation Agent only
```

Agents whose outputs are not affected by the refinement preserve their prior outputs unchanged. The Human Collaboration Agent re-packages the proposal with the updated agent outputs merged with the preserved outputs.

### 8.4 Confidence Calculation

Every agent output carries a confidence score — a value between 0 and 1 that represents the agent's self-assessed certainty in its output. Confidence is calculated from three signals:

1. **Retrieval relevance score** (for agents that query the knowledge base): the average relevance score of the knowledge items used to ground the recommendation. Higher relevance → higher confidence.

2. **Schema completeness score**: the proportion of required output fields that are populated versus left empty or flagged as uncertain. A fully populated output → higher confidence.

3. **Internal consistency score**: a heuristic check that validates whether the agent's recommendation is internally consistent — for example, whether the security controls recommended are appropriate for the data classification stated in the requirements.

The composite confidence score is reported alongside the agent output in the proposal package presented to the architect. Low confidence scores are highlighted in the workspace panel to direct the architect's attention.

### 8.5 Agent Memory and Context Isolation

Agents do not maintain persistent memory between invocations. Every agent invocation is stateless — the complete context required for the invocation is assembled by the Orchestrator and passed to the agent in the execution context. No agent reads from another agent's private state.

This design has three consequences:
- Agents are independently testable with constructed input contexts.
- A failed agent invocation has no side effects on other agents' state.
- Context size is bounded: the Orchestrator controls what context each agent receives, preventing unbounded context growth across pipeline stages.

---

## 9. Human in the Loop

### 9.1 The Review Gate — Design and Intent

The human review gate is not a UI feature — it is a structural property of the engagement state machine. The PENDING_HUMAN_REVIEW state is the only path between the AI-generated proposal and the approved architecture. The state machine has no bypass transition. No configuration, no feature flag, and no system setting removes this gate.

The Human Collaboration Agent manages the experience of this gate — packaging all agent outputs into a single, coherent, navigable review package so the architect has complete information at the moment of decision. The architect is not reviewing twelve separate agent reports — they are reviewing one consolidated proposal with contextual access to all underlying agent evidence.

### 9.2 Review Package Content

When the architect opens the review gate in the workspace panel, they see:

**Requirements interpretation:** The structured requirements extracted by the Requirement Intelligence Agent, with ambiguity flags and confidence scores. The architect can see exactly how the platform interpreted their input — and correct any misinterpretation before it propagates to an architecture decision.

**Candidate architectures:** One to three architecture options produced by the Architecture Design Agent, each with explicit trade-off rationale. For each candidate: the architecture pattern selected, the technology stack, the deployment topology, and the specific reasons it was chosen over alternatives.

**Technology evaluation:** The Technology Recommendation Agent's scoring matrix for each component-level technology decision, with the evaluation criteria applied and the source of each criterion (knowledge base citation).

**Validation findings (Security):** The Security Agent's threat model summary and control mapping. Findings are classified as blocking (must resolve before Final), advisory (should address), or informational (for architect awareness).

**Validation findings (Cost):** The TCO model with cost-driver breakdown and optimization recommendations.

**Validation findings (Compliance):** The compliance checklist results with pass/fail/needs-review status per applicable regulatory control.

**Validation findings (Risk):** The unified risk register with prioritized findings, probability-impact scoring, and suggested mitigations.

**Governance check results:** The Governance Agent's policy compliance summary. Any hard policy violations are displayed prominently — the architect must acknowledge them before proceeding.

**Citations panel:** Every recommendation in the proposal is hyperlinked to its source citation from the knowledge base. The architect can inspect the source material behind any recommendation.

### 9.3 Architect Decision Actions

**APPROVE:** The architect accepts the proposal as presented (or as modified through their review). This action is the trigger for the APPROVED state and GENERATING_OUTPUTS state. The approval is recorded in the Decision Ledger with the architect's authenticated identity, the timestamp, and the complete snapshot of the approved architecture state at that moment.

**REFINE (with feedback):** The architect provides structured or free-text feedback on specific aspects of the proposal that require modification. The feedback is routed by the Human Collaboration Agent to the relevant agents for targeted re-execution. The engagement enters IN_REFINEMENT state. On completion of the targeted re-execution, the engagement returns to PENDING_HUMAN_REVIEW with an updated proposal.

**REJECT:** The architect determines that the engagement's direction is fundamentally flawed — the requirements were misunderstood at a level that re-execution cannot fix, or the business context has changed. The rejection is recorded in the Decision Ledger with the architect's stated reason. The engagement is closed. A new engagement can be initiated.

### 9.4 Override Handling

When the architect directly edits a specific component of the proposed architecture — rather than providing free-text feedback — the edit is treated as an override.

**Override recording at runtime:**
1. The architect modifies a specific component in the workspace panel.
2. The modification is captured as a structured override record: component ID, original value, new value, architect identity, timestamp.
3. The override record is written to the Decision Ledger immediately.
4. The Orchestrator re-invokes all agents whose outputs depend on the modified component, using the architect's override as an authoritative constraint.
5. The Human Collaboration Agent re-packages the proposal with the overridden component locked and the dependent re-executed outputs updated.
6. The architect reviews the updated proposal, which preserves their override and shows how the AI-generated outputs have adapted to it.

**Override authority:** An architect override is the highest-authority input the platform can receive. It is never overridden by an agent output. If an agent's re-execution produces an output that conflicts with the architect's override, the conflict is surfaced to the architect as a finding — the agent does not silently ignore or replace the override.

### 9.5 Refinement Loop — Iteration Behavior

The refinement loop is unbounded — the architect can iterate as many times as necessary. Each iteration:
- Creates a new version of the proposal (version N+1)
- Preserves all prior proposal versions in the engagement record
- Records the refinement request and the architect's feedback in the Decision Ledger
- Re-executes only the agents whose outputs are affected by the feedback
- Returns to PENDING_HUMAN_REVIEW with the updated proposal

Each iteration is a separately numbered review cycle, not an overwrite of the prior cycle. The architect can compare the current proposal with any prior iteration through the engagement's version history.

---

## 10. Knowledge Flow

### 10.1 Knowledge Consumption (Read Path)

Knowledge is consumed primarily by the Knowledge Retrieval Agent during the Discovery Stage. The consumption flow:

```
Knowledge Retrieval Agent
    ↓ structured query (requirements + domain + engagement type)
RAG Engine
    ↓ semantic search + structured filter + ranked retrieval
Enterprise Knowledge Base (vector index + structured store)
    ↓ top-K relevant items with relevance scores and metadata
RAG Engine
    ↓ citation construction + context assembly
Knowledge Retrieval Agent
    ↓ retrieved context package (items + citations + relevance scores)
(becomes input to Design Stage agents via Orchestrator)
```

The Compliance Agent also queries the knowledge base directly for applicable regulatory frameworks, using a deterministic lookup (exact match on regulatory framework name) rather than semantic search.

### 10.2 Knowledge Validation (Quality Gate)

Before any knowledge item becomes retrievable by agents, it passes through a two-stage validation:

**Automated validation:** The ingestion pipeline validates the item against the knowledge entry schema — checks for required fields (pattern type, applicable domains, source reference, quality score), checks for completeness of content, and checks for embedding quality (the generated embedding must be within a defined similarity range of related existing entries — items that are too dissimilar from all existing entries, or too similar to existing entries, are flagged for human review).

**Human approval gate:** Every knowledge item — whether submitted directly by a contributor or generated by an approved engagement — requires an explicit approval by a designated Knowledge Base Curator before it is indexed and becomes retrievable. This approval is recorded in the Decision Ledger.

### 10.3 Knowledge Enrichment (Write Path — Background)

On engagement completion (COMPLETED state), the approved architecture enters the knowledge enrichment pipeline as a new knowledge base candidate. The enrichment process:

```
Approved architecture state
    ↓ (background process — does not block engagement completion)
Ingestion Pipeline
    ↓ document parsing + metadata extraction
Automated validation (schema + quality + similarity checks)
    ↓
Knowledge Base Curator approval gate
    ↓ (on approval)
Chunking + embedding generation
    ↓
Vector index update + structured store update
    ↓
New knowledge item retrievable by future engagements
```

This flow is entirely asynchronous with respect to the engagement that produced it. The engagement reaches COMPLETED state before the enrichment pipeline begins, and the enrichment pipeline's completion (or failure) has no effect on the engagement's state.

### 10.4 Knowledge Reuse Tracking

Every time a knowledge item is retrieved and included in a proposal that the architect approves, the item's retrieval count, approval association count, and last retrieval timestamp are updated in the knowledge base's structured store. These usage metrics serve three purposes:

- **Relevance decay correction:** Items that have been retrieved many times but have not contributed to approved proposals have their relevance weight reduced. Items that frequently appear in approved proposals have their relevance weight increased.
- **Staleness detection:** Items that have not been retrieved in a configured period are flagged for review — they may have become outdated.
- **Quality compounding:** High-quality items (frequently retrieved, frequently in approved proposals) rise to the top of retrieval results, compounding in value as the platform processes more engagements.

---

## 11. Communication Architecture

### 11.1 Synchronous Communication (Request-Response)

**Client to API Gateway:** All state-changing operations use synchronous HTTPS request-response. The API Gateway processes the request, validates identity, routes to the appropriate backend handler, and returns a response. Interactive operations (session creation, review decisions, output retrieval) use this pattern. Expected response time: < 500ms for synchronous endpoints.

**API Gateway to Application Services:** Internal synchronous calls within the Application Layer use direct service invocation. These calls carry the validated identity context and correlation ID forwarded from the gateway. Expected response time: < 200ms for operations that do not trigger agent pipelines.

**Agents to LLM Gateway:** Every agent invocation includes one or more synchronous LLM calls routed through the LLM Gateway. LLM calls are inherently latency-variable. Timeouts are configured per agent based on expected token volumes. The LLM Gateway handles per-provider rate limiting and retry on transient 429 responses.

**Agents to Knowledge Layer:** Knowledge retrieval is a synchronous call within the agent's execution lifecycle. The agent waits for the retrieval result before constructing its prompt. Expected retrieval time: < 2 seconds at p95.

**State transitions to Decision Ledger:** All Decision Ledger writes on the critical path (proposal recording, approval recording) are synchronous. The state machine does not advance until the ledger write is confirmed. This guarantees that every state transition is ledger-backed.

### 11.2 Asynchronous Communication (Streaming and Events)

**Pipeline progress to client:** Agent pipeline execution progresses asynchronously from the client's perspective. Progress events are emitted by the Orchestrator and broadcast to connected clients through the Progress Broadcaster over a persistent connection. The client receives incremental updates — stage completion, partial outputs, validation findings — without polling.

**Background knowledge enrichment:** The knowledge ingestion pipeline operates entirely asynchronously. It is triggered by a background event on engagement completion and runs without blocking any other platform operations.

**Observability emission:** All logging, tracing, and metrics are emitted asynchronously. The platform does not wait for observability writes to complete before processing continues. A failed observability write is retried in the background.

### 11.3 Message Bus (Inter-Agent Coordination)

The Orchestrator uses an internal message bus to coordinate the parallel execution of Validation Stage agents. When the Design Stage completes, the Orchestrator publishes the design output to the message bus. All four Validation Stage agents subscribe to this message and begin execution concurrently. When each agent completes, it publishes its result back to the bus. The Risk Assessment Agent subscribes to the results of the Security and Compliance agents in addition to the design output.

This message bus pattern is internal to the Orchestration Layer — it is not exposed to other platform components. From the perspective of the Application Layer and the Agent Layer, the Validation Stage is a single orchestrated step.

### 11.4 Interface Contracts

Every runtime communication boundary in the platform is governed by an explicit interface contract. Key contracts:

| Boundary | Contract Type | Key Guarantee |
|----------|--------------|---------------|
| Client → API Gateway | OpenAPI 3.0 specification | All fields typed and validated |
| API Gateway → Application Services | Internal typed interfaces | Identity context always present |
| Orchestrator → Agents | AgentInterface (execute method signature) | Standardized context in, standardized result out |
| Agents → Knowledge Layer | KnowledgeInterface (query method signature) | Cited results always returned |
| Agents → LLM Gateway | LLMInterface (invoke method signature) | Normalized response always returned |
| Any layer → Decision Ledger | LedgerInterface (record method signature) | Write confirmation before state advance |
| Orchestrator → Progress Broadcaster | Internal event schema | Progress events always carry engagement ID + stage + status |

---

## 12. Reliability Strategy

### 12.1 Retry Strategy

| Operation | Retry Policy | Max Attempts | Backoff |
|-----------|-------------|-------------|---------|
| LLM invocation (transient 429 / 503) | Exponential backoff | 3 | 2s, 4s, 8s |
| Knowledge base retrieval | Exponential backoff | 3 | 1s, 2s, 4s |
| Storage write (non-critical path) | Exponential backoff | 5 | 1s, 2s, 4s, 8s, 16s |
| Decision Ledger write (critical path) | Exponential backoff + alert | 5 | 500ms, 1s, 2s, 4s, 8s |
| External identity provider call | Exponential backoff | 3 | 1s, 2s, 4s |

Retries are agent-level for LLM failures — the Orchestrator is not aware of individual retry attempts within an agent invocation. If an agent exhausts its retries, the agent invocation fails and the Orchestrator handles the stage failure according to the graceful degradation rules below.

### 12.2 Timeout Strategy

| Operation | Timeout |
|-----------|---------|
| API Gateway request | 30 seconds (synchronous endpoints) |
| Agent invocation (total) | Configured per agent (range: 60–300 seconds based on expected token volume) |
| LLM call within agent | Agent timeout × 0.8 (leaves margin for agent-level processing) |
| Knowledge retrieval | 10 seconds |
| Storage write | 5 seconds |
| Decision Ledger write | 10 seconds (retried on timeout — critical path) |

### 12.3 Graceful Degradation

Not all agent failures cause engagement failure. The platform distinguishes between critical agents (whose failure blocks the pipeline) and advisory agents (whose failure produces a degraded but still usable proposal).

| Agent | Failure Treatment |
|-------|------------------|
| Requirement Intelligence Agent | Critical — pipeline fails; architect must re-submit |
| Knowledge Retrieval Agent | Degraded — pipeline continues with confidence flagged low; architect notified that retrieval unavailable |
| Architecture Design Agent | Critical — pipeline fails; cannot generate candidates without this agent |
| Technology Recommendation Agent | Degraded — architecture candidates presented without technology recommendations; architect completes technology selection manually |
| Infrastructure Recommendation Agent | Degraded — architecture candidates presented without topology; architect notified |
| Security Agent | Advisory only — proposal presented with security findings section marked unavailable; architect must acknowledge before approving |
| Cost Optimization Agent | Advisory only — same treatment as Security Agent |
| Compliance Agent | Advisory only — same treatment as Security Agent |
| Risk Assessment Agent | Advisory only — same treatment as Security Agent |
| Governance Agent | Critical — hard policy check cannot be bypassed; pipeline blocked |
| Human Collaboration Agent | Critical — review package cannot be assembled; pipeline blocked at review gate |
| Documentation Agent | Non-blocking — outputs marked unavailable; architect can re-trigger output generation |

### 12.4 Failure Isolation

Agent failures are isolated within the agent boundary. A failed agent does not affect the execution of other agents running in parallel. The Agent Scheduler collects failure records alongside success records. The Orchestrator handles the failure record according to the degradation rules above.

A failure in the background knowledge enrichment pipeline never affects engagement processing. The two pipelines share no runtime resources in the critical path.

### 12.5 Recovery Procedure

When an engagement enters the FAILED state:

1. The failure is logged with full context (agent ID, error type, input hash, execution trace) in the observability layer.
2. The architect is notified of the failure and the last successful pipeline stage.
3. The architect can initiate a retry — the Orchestrator resumes from the last successfully completed pipeline stage.
4. If the failure is systemic (same failure on retry), the engagement is flagged for platform administrator review and the architect is notified that manual intervention is required.

---

## 13. Scalability Strategy

### 13.1 Horizontal Scaling — All Stateless Components

Every component in the Application Layer, the Orchestration Layer, and the Agent Layer is stateless. State is externalized to the Storage Layer. Adding instances of any stateless component increases throughput proportionally without requiring coordination between instances.

**Independently scalable runtime units:**

| Component | Scaling Unit | Scaling Trigger |
|-----------|-------------|-----------------|
| API Gateway | Instances | Request rate |
| Session Manager | Instances | Active session count |
| Engagement Manager | Instances | Active engagement count |
| Master Orchestrator | Instances | Concurrent pipeline count |
| Agent Workers | Instances per agent type | Queue depth per agent type |
| LLM Gateway | Instances | LLM request rate |
| RAG Engine | Instances | Retrieval query rate |
| Progress Broadcaster | Instances | Connected client count |

Agent workers are independently scalable per agent type. The Security Agent can be scaled to four instances without scaling the Architecture Design Agent. This allows fine-grained capacity management based on actual pipeline bottlenecks.

### 13.2 Knowledge Base Scaling

Knowledge base scaling is a specialized concern due to the vector index's growth characteristics.

**Index partitioning strategy:** The knowledge base index is partitioned by domain and knowledge type. A retrieval query for a healthcare engagement queries the healthcare partition and the generic partition — not the financial services partition. This limits the effective index size for any given retrieval query, maintaining retrieval latency as the total knowledge base grows.

**Sharding by engagement volume:** As the knowledge base grows beyond a single index shard's optimal range, horizontal sharding is applied: shards by domain, shards by knowledge type (patterns, precedents, regulatory frameworks), and shards by date range (recent knowledge weighted higher in retrieval ranking).

### 13.3 Session and Engagement Store Scaling

Session and engagement records are keyed by stable identifiers (session ID, engagement ID). Partitioning by consistent hash of these identifiers distributes reads and writes evenly across storage nodes. Read scaling uses read replicas for session restoration operations (high read volume, low write frequency).

### 13.4 LLM Rate Limit Management

LLM provider rate limits are a primary scaling constraint. The LLM Gateway manages this constraint through:

- **Request queuing:** Requests that would exceed the rate limit are queued rather than rejected. Queue depth is bounded; requests beyond the queue bound are rejected with a 503 and an estimated retry-after time.
- **Per-agent token budget allocation:** Each agent has a configured token budget. The LLM Gateway enforces these budgets, preventing a single agent invocation from consuming disproportionate capacity.
- **Multi-model load distribution:** Future capability — requests can be distributed across multiple models (when multiple models are configured and approved) to increase effective throughput.

---

## 14. Security Architecture

### 14.1 Authentication Runtime Model

All user access to the platform is authenticated through GitHub OAuth 2.0. The authentication flow at runtime:

```
Client → Identity Provider (GitHub OAuth) → Authorization Code
    ↓
Client → API Gateway: Authorization Code
    ↓
API Gateway → Identity Provider: Code Exchange → Access Token + ID Token
    ↓
API Gateway: Validate ID Token (signature, expiry, issuer, audience)
    ↓
API Gateway: Extract identity claims (user ID, email, name)
    ↓
API Gateway: Issue platform session token (signed JWT)
    ↓
Client: Stores platform session token
    ↓ (all subsequent requests)
API Gateway: Validate platform session token (signature, expiry)
```

Service-to-service communication within the platform uses mutual TLS (mTLS) with service identity certificates — not user-issued tokens. A service cannot impersonate a user to call another service.

### 14.2 Authorization Runtime Model

Authorization is evaluated at two levels:

**Resource ownership authorization:** Every engagement and session is owned by the architect who created it. An architect cannot access another architect's engagement, even with valid authentication. This check is performed by the Engagement Manager on every operation, not only by the API Gateway.

**Role-based capability authorization:** Specific capabilities (knowledge base management, audit log access, user management, system configuration) are restricted to roles beyond the base architect role. Role assignments are managed through the platform's identity management and evaluated by the API Gateway on every request.

### 14.3 Data Isolation

**Engagement data isolation:** Engagement records are partitioned by architect identity at the storage level. A storage query for engagement data always includes the architect's identity as a mandatory partition key. A query that omits the identity filter is rejected by the storage service — there is no path by which engagement data from one architect is returned in response to a query from another architect's session.

**LLM context isolation:** Each agent invocation constructs its prompt from the engagement context of the specific engagement being processed. There is no shared prompt state or shared conversation history across engagements or across architects. The LLM sees only the context of the current invocation.

### 14.4 Secrets Management at Runtime

Secrets (LLM API keys, storage credentials, signing keys) are never stored in application code, configuration files, or environment variables. At runtime:

1. On service startup, each service retrieves the secrets it requires from the secrets manager using its service identity certificate.
2. Secrets are held in memory only for the duration of their immediate use.
3. Secrets are not logged, not included in error messages, and not passed between services.
4. Secret rotation by the secrets manager triggers a refresh signal to dependent services, which re-fetch the new secret on the next use.

### 14.5 Prompt Security at Runtime

The LLM Gateway enforces prompt content checks on every agent invocation before the prompt is transmitted to the LLM provider:

- **PII pattern detection:** The prompt is scanned for patterns matching common PII formats (email, phone, SSN, credit card). Detection triggers rejection of the invocation and a security event log.
- **Secret pattern detection:** The prompt is scanned for patterns matching API key formats, connection strings, and credential patterns. Detection triggers rejection and an alert.
- **Injection pattern detection:** The prompt is scanned for known prompt injection patterns — instructions embedded in user input that attempt to override the agent's system prompt. Detection triggers sanitization or rejection, depending on pattern severity.

### 14.6 Decision Ledger Integrity

The Decision Ledger's hash chain provides tamper evidence. At runtime, integrity verification is performed:
- On every read of a ledger entry (incremental verification of the chain up to the read entry).
- On a scheduled full-chain verification run (daily or configurable).
- Any chain break (indicating modification or deletion of an entry) raises a critical alert.

---

## 15. Observability

### 15.1 Structured Logging

Every log entry emitted by the platform is structured — a JSON document with standardized fields. No freeform log strings that require regex parsing.

**Mandatory fields on every log entry:**

| Field | Content |
|-------|---------|
| `timestamp` | UTC ISO 8601 with milliseconds |
| `correlation_id` | Request-scoped trace identifier |
| `engagement_id` | Engagement context (null for non-engagement requests) |
| `session_id` | Session context |
| `service_name` | Emitting service identifier |
| `service_version` | Service version |
| `level` | DEBUG / INFO / WARN / ERROR / CRITICAL |
| `message` | Human-readable event description |
| `event_type` | Machine-parseable event category |

**Log levels by event type:**

- `DEBUG`: Detailed execution trace (agent prompt construction, retrieval query details) — development and troubleshooting only.
- `INFO`: Normal operations (stage completions, state transitions, engagement creation).
- `WARN`: Degraded operations (cache miss, retrieval confidence below threshold, agent retry).
- `ERROR`: Recoverable failures (agent failure with retry exhausted, storage write failure).
- `CRITICAL`: Non-recoverable failures, security events, integrity violations.

### 15.2 Distributed Tracing

Every request that enters the API Gateway initiates a trace span. Trace spans propagate through every downstream service using the correlation ID as the trace context. Key span events:

- API Gateway request received and routed
- Session restoration (hit or miss)
- Engagement state transition (from → to)
- Agent invocation (agent ID, input token count, latency)
- LLM call (model ID, tokens in, tokens out, latency)
- Knowledge retrieval (query, result count, top result relevance, latency)
- Decision Ledger write (event type, latency)
- Output generation (format, file size, latency)

Trace data enables end-to-end latency analysis, per-agent performance profiling, and bottleneck identification without requiring manual log correlation.

### 15.3 Metrics

Key platform metrics emitted continuously:

| Metric | Type | Description |
|--------|------|-------------|
| `engagement_created_total` | Counter | Total engagements initiated |
| `engagement_completed_total` | Counter | Total engagements reaching COMPLETED state |
| `engagement_duration_seconds` | Histogram | Time from INITIATED to COMPLETED |
| `agent_execution_duration_seconds` | Histogram (by agent ID) | Per-agent execution latency |
| `agent_llm_tokens_consumed_total` | Counter (by agent ID, model ID) | Token consumption per agent |
| `knowledge_retrieval_duration_seconds` | Histogram | Retrieval operation latency |
| `knowledge_retrieval_relevance_score` | Histogram | Distribution of retrieval relevance scores |
| `human_review_cycle_count` | Histogram (by engagement) | Number of refinement iterations per engagement |
| `approval_rate` | Gauge | Proportion of proposals approved vs. refined vs. rejected |
| `pipeline_stage_failure_total` | Counter (by stage, by failure type) | Stage-level failure tracking |
| `decision_ledger_write_duration_seconds` | Histogram | Ledger write latency |
| `active_sessions_total` | Gauge | Currently active architect sessions |
| `concurrent_pipelines_total` | Gauge | Currently executing agent pipelines |

### 15.4 Audit Trail

The Decision Ledger is the platform's primary audit mechanism. The observability stack supplements it with execution-level audit detail.

**Decision Ledger audit capability:** Given any Final Architecture, the ledger provides: the complete sequence of proposal versions, the agent versions and prompt versions that produced each version, the architect identity and timestamp for every approval and override, and the refinement feedback that drove each iteration.

**Execution audit capability:** Given any agent invocation (via correlation ID from the ledger record), the observability stack provides: the complete input context, the prompt constructed (from the prompt version stored in config), the model invoked, the token counts, and the structured output. The combination of ledger and observability stack enables complete forensic reconstruction of any platform output.

---

## 16. Performance Strategy

### 16.1 Caching Strategy

**Knowledge retrieval cache:** Retrieval queries for identical requirement contexts (semantic hash match) return cached results without querying the vector store. Cache TTL is bounded by the last knowledge base update timestamp — a knowledge base update invalidates retrieval caches that may be affected.

**Session cache:** Frequently accessed session records are cached in the application-layer cache. Session cache TTL is short (minutes) — session records are small and the cache hit rate on active sessions is high.

**LLM response cache:** For specific, deterministic agent invocations (particularly the Compliance Agent, which applies identical prompts to identical regulatory frameworks), responses are cached by prompt hash. LLM response caches have a longer TTL (hours) and are invalidated by prompt version changes.

**Technology catalog cache:** The technology catalog (used by the Technology Recommendation Agent) changes infrequently. It is cached aggressively (hours to days) and invalidated only when the catalog configuration is updated.

### 16.2 Parallel Execution for Latency Reduction

Wherever agent outputs are independent, parallel execution is the default. The Validation Stage (four agents in parallel) is the primary application of this strategy. Parallel execution reduces the Validation Stage latency from the sum of individual agent times to approximately the time of the slowest agent.

### 16.3 Progressive Result Streaming

The client does not wait for pipeline completion before seeing results. Each pipeline stage's output is streamed to the workspace panel as it completes. This means:

- The structured requirements appear in the workspace panel within seconds of pipeline initiation.
- Retrieved knowledge items appear as the Knowledge Retrieval Agent completes.
- Architecture candidates appear as the Design Stage completes.
- Validation findings appear individually as each Validation Stage agent completes.
- The review gate opens automatically when all pipeline stages are complete.

From the architect's perspective, the engagement workspace is always populated with the most current available information — the pipeline is not a black box that eventually produces a completed output.

### 16.4 Request Prioritization

The platform distinguishes between interactive requests (architect-initiated, low latency expected) and background requests (knowledge enrichment, report generation). Interactive requests are served from a priority queue that is not shared with background work. A background process consuming high compute does not increase the latency of an architect's interactive request.

---

## 17. Deployment View

### 17.1 Logical Runtime Services

At runtime, the platform operates as a set of independently deployed, independently scalable logical services. The logical service boundary corresponds to the scaling unit — components that scale together are in the same service.

| Logical Service | Runtime Components | Scaling Characteristic |
|----------------|-------------------|-----------------------|
| **Client Service** | Three-panel web application | CDN-distributed; no server-side scaling required |
| **Gateway Service** | API Gateway, rate limiter | Horizontally scaled; stateless |
| **Application Service** | Session Manager, Engagement Manager, Engagement State Machine | Horizontally scaled; state externalized |
| **Orchestration Service** | Master Orchestrator, Agent Scheduler, Result Aggregator, Progress Broadcaster | Horizontally scaled; stateless per request |
| **Agent Service — Discovery** | Requirement Intelligence Agent, Knowledge Retrieval Agent workers | Independently scalable per agent type |
| **Agent Service — Design** | Architecture Design, Technology Recommendation, Infrastructure Recommendation workers | Independently scalable per agent type |
| **Agent Service — Validation** | Security, Cost Optimization, Compliance, Risk Assessment workers | Independently scalable per agent type; parallel within stage |
| **Agent Service — Governance** | Governance, Human Collaboration, Documentation workers | Independently scalable per agent type |
| **LLM Gateway Service** | LLM Gateway, provider adapters, rate limit controller | Horizontally scaled |
| **Knowledge Service** | Knowledge Base, RAG Engine | Read-scaled (multiple replicas); single-writer for index updates |
| **Ingestion Service** | Ingestion Pipeline (background) | Independently scaled; decoupled from engagement processing |
| **Output Service** | Output Generator, format renderers | Horizontally scaled; stateless |
| **Infrastructure Service** | Decision Ledger, Storage, Cache, Secrets Manager, Observability Stack | Each component scaled independently per its own characteristics |

### 17.2 Execution Environment Boundaries

**Internet boundary:** The Client Service and the API Gateway Service are the only components with internet exposure. All other services operate behind the platform's internal network boundary.

**Service mesh boundary:** All internal service-to-service communication occurs within the service mesh, where mTLS is enforced. Services outside the mesh cannot communicate with services inside it.

**LLM provider boundary:** LLM calls exit the service mesh through a controlled egress point — the LLM Gateway Service. LLM provider traffic passes through this single egress, which enforces prompt sanitization, rate limiting, and complete request/response logging.

**Storage boundary:** All persistent storage (session store, engagement store, knowledge base, decision ledger, output store) is accessed through storage service interfaces. Storage does not accept direct connections from agent services — all storage access passes through the appropriate service-level abstraction.

### 17.3 Multi-Zone Deployment

The platform is designed for multi-zone deployment within a single cloud region. Critical services (Gateway, Application, Orchestration, Knowledge) are deployed across a minimum of two availability zones. The Decision Ledger uses synchronous cross-zone replication — a write is not confirmed until it is durable in at least two zones.

The design is cloud-agnostic: multi-zone deployment is an infrastructure concern, not an application concern. The application services are not aware of which zone they are running in. Zone failover is handled at the infrastructure layer.

---

## 18. Future Evolution

### 18.1 Multi-Cloud Strategy

The platform's cloud-agnostic design (all infrastructure accessed through service interfaces, all cloud-specific implementations in adapter classes) enables multi-cloud deployment without application code changes. Future evolution:

- **Active-active multi-cloud:** Knowledge base replicated across cloud providers; client requests served from the closest cloud region regardless of provider.
- **Cloud-native service optimization:** Per-cloud adapter implementations that leverage cloud-specific managed services for performance and cost without changing the application contract.

### 18.2 Multiple LLM Strategy

The LLM Gateway's adapter pattern enables multi-model operation at runtime:

- **Per-agent model assignment:** Different agents use the model best suited to their task — a retrieval-focused agent uses a model optimized for RAG; a code generation agent uses a model optimized for structured output.
- **Fallback routing:** If the primary model for an agent is unavailable or over-limit, the LLM Gateway routes to a configured fallback model automatically.
- **A/B testing:** The LLM Gateway can route a configured percentage of agent invocations to a new model version for quality comparison, while the primary model serves the remainder.

### 18.3 Plugin Architecture

The plugin system (introduced in Phase 2) extends the platform's runtime capabilities without modifying core services. At runtime, plugins are loaded dynamically by the Plugin Registry at service startup. Plugins can provide:

- New agent types (registered with the Agent Registry, scheduled by the Agent Scheduler)
- New knowledge domain configurations (injected into the Knowledge Service at startup)
- New output format generators (registered with the Output Generator)
- New technology catalog entries (loaded into the Technology Recommendation Agent's catalog)

Plugin loading failures do not affect core platform operation — the Plugin Registry logs the failure and continues with the successfully loaded plugins.

### 18.4 New Agent Integration

New agents introduced in future platform releases integrate at runtime through the Agent Registry. A new agent is instantiated, registered by its `AGENT_ID`, and made available to the Orchestrator without changes to the orchestration logic. The pipeline stage that includes the new agent is updated through configuration — no orchestration code changes are required for standard agent additions.

### 18.5 New UI Clients

Additional client types (mobile application, embedded widget, CLI) consume the same API Gateway and Application Layer services as the primary web client. The backend services are client-type agnostic — they respond to authenticated, authorized requests regardless of the originating client type. New client types are added by implementing the API client contract for the target platform, without backend changes.

### 18.6 Enterprise System Integration

Future integrations with enterprise systems (JIRA for ticket creation, Confluence for document publishing, enterprise IAM for user provisioning, ITSM for change management) are implemented as outbound adapter services that consume approved engagement outputs. These adapters are external to the core platform — they listen for COMPLETED engagement events and produce integration-specific outputs. Core platform services are not modified to accommodate new integrations.

---

## 19. Architecture Principles

The following system-level principles govern every implementation decision. Every future implementation document must be consistent with these principles. Where a conflict exists between an implementation decision and a principle, the principle prevails.

**SP-01: State machine governs, services execute.**
The engagement state machine is the single authority on what is permitted to happen and when. No service may perform an action on an engagement that the state machine has not permitted. A service that performs an action without a valid state machine transition is a security defect.

**SP-02: Every state transition is persisted before it is acted upon.**
No system action is taken based on a state transition that has not been durably persisted. This is the basis of the Recovery Guarantee. Any implementation that performs actions on the assumption of a state transition that has not yet been confirmed violates this principle.

**SP-03: The Decision Ledger is the record of truth for all decisions.**
Any question about what was decided, by whom, when, and based on what information is answered by the Decision Ledger — not by application logs, not by storage records, not by human memory. If a decision is not in the Decision Ledger, it is not a platform decision.

**SP-04: Agents are the exclusive source of AI-generated architectural content.**
No AI-generated architectural content reaches the architect through any path other than an agent-produced, validator-checked, citation-attached output routed through the Orchestrator. Ad hoc LLM calls outside the agent framework are not permitted to produce content that appears in the workspace or in any generated document.

**SP-05: The human architect is the exclusive source of architectural approval.**
No system component — including the Governance Agent, the AI confidence scorer, or any automated pipeline — has the authority to approve an architecture. Approval is an explicit, identity-attributed human action. A system that marks an architecture as approved without a corresponding human approval event is not compliant with the platform architecture.

**SP-06: LLM provider isolation is absolute.**
The LLM provider is an external system. It receives sanitized prompts. It returns generated text. It has no access to platform storage, no ability to call platform services, and no knowledge of which engagement or architect it is serving. The LLM Gateway is the enforcement point for this isolation.

**SP-07: Failure isolation prevents cascade.**
A failure in any one agent or service must not cause failures in adjacent agents or services that are executing concurrently. Every agent invocation is isolated from every other. A failing Compliance Agent does not affect the Security Agent executing in parallel.

**SP-08: Progress is always visible.**
An architect who has submitted a requirement must always be able to see the current state of their engagement and the progress of any executing pipeline. A system state in which a pipeline is executing but the architect receives no progress signal is an unacceptable user experience, regardless of the pipeline's correctness.

**SP-09: Knowledge base changes are human-governed.**
No knowledge item becomes retrievable without human approval. An automated process — including the knowledge enrichment pipeline — can prepare and validate a knowledge entry, but a human Knowledge Base Curator must explicitly approve it before it influences agent recommendations. Automated approval of knowledge base entries is not permitted.

**SP-10: The platform never sacrifices audit integrity for performance.**
If a performance optimization requires reducing audit trail completeness — fewer ledger entries, less detailed logs, compressed trace data — the optimization is not made. Audit integrity is a non-negotiable constraint. Performance optimizations operate within the constraint of complete auditability.

---

## 20. System Freeze Rules

The following rules are runtime invariants. They represent behaviors that the platform guarantees under all operating conditions. No implementation decision, performance optimization, or feature request may violate these rules. Changing a rule requires an ARB-approved ADR and a revision to this document.

| # | System Freeze Rule |
|---|-------------------|
| **SFR-01** | The engagement state machine contains no transition from any state to COMPLETED that does not pass through PENDING_HUMAN_REVIEW and an explicit human APPROVED event. This is a code invariant — it is not configurable. |
| **SFR-02** | No agent may communicate directly with another agent. All inter-agent data flow passes through the Orchestrator. Direct agent-to-agent calls are not permitted and will not be introduced. |
| **SFR-03** | No prompt sent to the LLM Gateway may contain PII, credentials, or client secrets. The LLM Gateway enforces this at runtime. A prompt that fails this check is rejected and logged as a security event — it is not sanitized and sent. |
| **SFR-04** | Every Decision Ledger entry is immutable after write. No platform service has a DELETE or UPDATE operation on the Decision Ledger. The Ledger implements only APPEND and READ. |
| **SFR-05** | Every architect approval event in the Decision Ledger is signed with the architect's authenticated identity and the timestamp of the approval. An approval event without an attributed identity is not a valid approval event. |
| **SFR-06** | The LLM provider has no ability to initiate calls into the platform. All LLM interactions are outbound from the platform — request from platform, response from LLM. Webhook or callback patterns from LLM providers into the platform are not permitted. |
| **SFR-07** | No knowledge item produced by the automated enrichment pipeline becomes retrievable without a human approval event in the Decision Ledger. |
| **SFR-08** | Every API Gateway request that reaches a backend service carries a validated identity context and a correlation ID. Backend services do not process requests that arrive without these. |
| **SFR-09** | Engagement data from one architect session is never accessible from another architect's session. Storage queries always include the architect's identity as a mandatory filter. This filter cannot be bypassed by any service-level call. |
| **SFR-10** | The Recovery Guarantee is absolute: no in-progress engagement is permanently lost due to a runtime failure. Every state transition is persisted before being acted upon. A pipeline can always be retried from the last persisted state. |

---

> **End of SYSTEM_ARCHITECTURE.md**  
> **Version 1.0.0 — Foundation Release**  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0  
> **Classification:** Runtime Architecture — Source of Truth  
> **Next Document:** TECHNOLOGY_ARCHITECTURE.md
