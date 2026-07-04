# INFRASTRUCTURE_IMPLEMENTATION_PLAN.md

Document Classification: Implementation Planning — Source of Truth (Planning Only)
Status: Draft (BLOCKED — missing authoritative evidence)
Version: 1.0.0

Scope
-----
This document is the authoritative, pre-implementation plan for the Backend Infrastructure Layer. It is a planning-only artifact created strictly from the frozen architecture documents listed in the Authoritative Documents section below. No code will be created from this plan. Implementation is explicitly blocked where any required evidence is missing or only inferred.

Authoritative Documents (read in full)
-------------------------------------
- docs/architecture/REPOSITORY_MASTER_STRUCTURE.md
- docs/architecture/BACKEND_MODULE_ARCHITECTURE.md
- docs/architecture/IMPLEMENTATION_SPECIFICATION.md
- docs/architecture/SYSTEM_ARCHITECTURE.md
- docs/architecture/SECURITY_ARCHITECTURE.md
- docs/architecture/API_ARCHITECTURE.md
- docs/architecture/ARCHITECTURE_VISION.md
- docs/architecture/WORKFLOW_ENGINE.md
- docs/architecture/KNOWLEDGE_ENGINE.md
- docs/architecture/DATABASE_ARCHITECTURE.md
- docs/architecture/OUTPUT_GENERATION_ARCHITECTURE.md
- docs/architecture/FRONTEND_MODULE_ARCHITECTURE.md
- docs/architecture/AI_AGENT_ARCHITECTURE.md
- docs/architecture/DATA_SOLUTION_ARCHITECTURE.md

Process and governance rules applied
-----------------------------------
- No implementation, modification, or file creation performed while producing this plan.
- Every factual statement below is classified as one of: DOCUMENTED, PARTIALLY DOCUMENTED, INFERRED, or ASSUMED.
- If any implementation requirement is classified as INFERRED or ASSUMED, implementation is blocked and this plan records the exact missing evidence and the document that must contain it.

Executive summary (short)
-------------------------
- The frozen architecture documents provide strong, unambiguous, DOCUMENTED guidance at the layer and module level for the Infrastructure Layer (Layer 7). See BACKEND_MODULE_ARCHITECTURE.md Layer 7 ("Infrastructure Modules"), Dependency/DI rules (Sections 11–12), and REPOSITORY_MASTER_STRUCTURE.md Layer ownership rules.
- However, critical implementation-level evidence required by governance is missing from the frozen documents: per-file canonical names and required file-level artifacts, per-file DI registration manifest and lifetimes, per-file owner (CODEOWNERS) mappings, secrets naming and retrieval adapter contract, retry/backoff numeric policies, and health-check probe definitions. These gaps are listed explicitly in the Blockers section and must be resolved before any implementation may proceed.
- Per the strict NO ASSUMPTIONS policy, implementation is BLOCKED. This plan documents what is provable and what is not, and enumerates exactly what authoritative evidence is missing.

Validation Phase — Repository verification (DOCUMENTED facts & findings)
------------------------------------------------------------------------
Source rule: REPOSITORY_MASTER_STRUCTURE.md is the authoritative "Complete Repository Tree" and governance source. (DOCUMENTED — REPOSITORY_MASTER_STRUCTURE.md)

Findings (high-level):
- The repository contains the top-level directories required by the master doc (docs/, src/, outputs/, config/, deploy/, scripts/, plugins/, tests/, .github/, .vscode/) — DOCUMENTED presence compared to the master tree (REPOSITORY_MASTER_STRUCTURE.md).
- The repository also contains runtime artefacts not enumerated in the master doc (.venv/, .mypy_cache/, .pytest_cache/, .ruff_cache/, .coverage, repo_file_list.txt). These are extras relative to the "Nothing extra" rule in REPOSITORY_MASTER_STRUCTURE.md (PARTIALLY DOCUMENTED policy; the presence of these files in the working tree is an operational deviation that must be reconciled). Evidence: REPOSITORY_MASTER_STRUCTURE.md ("Nothing generated into the source tree", Section 1.7 and "Repository Freeze Rules").
- The master doc lists specific example files in many places. The repository contains packages and many implementations; several explicit file names from the master-tree examples are not present. Because REPOSITORY_MASTER_STRUCTURE.md is authoritative and labeled "Complete Repository Tree", missing file-level artifacts are deviations that require reconciliation (MISSING EVIDENCE for per-file proof). (DOCUMENTED requirement that the repo match the master tree; however per-file presence is not fully aligned.)

Repository verification conclusion: BLOCKED for implementation until the master tree is reconciled with the actual repository (or the master doc is updated with an ADR). See Blockers.

Interface validation (DOCUMENTED facts)
--------------------------------------
- The Application Core defines interfaces in `src/backend/core/interfaces/` (DOCUMENTED — BACKEND_MODULE_ARCHITECTURE.md: "The interface is the contract" and Module list). Files present in the repository include `agent_interface.py`, `llm_interface.py`, `storage_interface.py`, `cache_interface.py`, `ledger_interface.py`, `knowledge_interface.py`, `secrets_interface.py`, `observability_interface.py`, and `output_storage_interface.py` (repository inspection). The existence of these interface contract modules is consistent with the architecture's requirement that Core defines interfaces. (DOCUMENTED — BACKEND_MODULE_ARCHITECTURE.md, Layer 2 and Layer 7 descriptions.)
- The DI Strategy (constructor-based, interface-driven, with registration at startup) is DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Section 11 "Dependency Injection Strategy").

Interface validation conclusion: Interfaces exist and are the frozen contracts the Infrastructure Layer must implement. That said, the architecture does not provide an exhaustive, authoritative mapping from each interface name to the exact implementation file path or the DI registration manifest required for implementation. This per-file mapping is MISSING EVIDENCE and therefore blocks implementation.

Per-module planning (only documented items are allowed)
---------------------------------------------------
Instructions applied: For every Infrastructure module named in BACKEND_MODULE_ARCHITECTURE.md Layer 7, the plan below lists only fields that are provably documented. Each field is annotated with its classification and the document citation. Where the authoritative document does not contain the required field, that field is marked MISSING EVIDENCE or PARTIALLY DOCUMENTED and the plan marks the module as BLOCKED.

Canonical Infrastructure modules (as listed in BACKEND_MODULE_ARCHITECTURE.md Layer 7 — DOCUMENTED)
- `llm_gateway`
- `anthropic_adapter`
- `storage_service`
- `vector_store_service`
- `cache_service`
- `decision_ledger_service`
- `secrets_service`
- `observability_service`
- `output_storage_service`

For each module below: every field is either DOCUMENTED (with citation) or flagged as MISSING EVIDENCE / PARTIALLY DOCUMENTED. No field is filled by inference.

1) Module: `llm_gateway`
- Module Name: `llm_gateway` — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md, Layer 7 — "llm_gateway").
- Purpose: LLM provider request routing, sanitization, and response normalization — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md, Layer 7 module list).
- Architecture Responsibility: Implement `LLMInterface` and route to provider adapters; DOCUMENTED in Layer 7 and Agent responsibilities referencing `LLMInterface` (BACKEND_MODULE_ARCHITECTURE.md, Layer 4 and Layer 7).
- Implemented Interface: `LLMInterface` — PARTIALLY DOCUMENTED (interface referenced across docs; the interface file `src/backend/core/interfaces/llm_interface.py` exists). Citation: BACKEND_MODULE_ARCHITECTURE.md (Layer 4 and Layer 7) and repo interface file listing.
- Expected Dependencies: Core Interfaces, Shared — DOCUMENTED (Layer rules: Infrastructure implements Core interfaces and may import Shared). Citation: BACKEND_MODULE_ARCHITECTURE.md (Layer 7 "Allowed imports").
- Allowed Imports: Core interfaces (interface types), Shared utilities, approved third-party SDKs — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 and Layer 8).
- Forbidden Imports: Business logic, Agent logic, Orchestration logic — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 "Forbidden imports" and Section 12.2 forbidden patterns).
- Consumers: Agents and Orchestration via `LLMInterface` — PARTIALLY DOCUMENTED (architecture says Agents use `LLMInterface`; does not list every consumer class/file). Citation: BACKEND_MODULE_ARCHITECTURE.md (Layer 4 and 12.1).
- External Systems: LLM provider APIs (documented conceptually) — DOCUMENTED (Layer 7 "LLM provider API calls through provider-specific adapters").
- Configuration Source: `config/` per REPOSITORY_MASTER_STRUCTURE.md (CONFIG floats to top) — DOCUMENTED (REPOSITORY_MASTER_STRUCTURE.md Section 1.5).
- Secret Source: `secrets_service` (module exists conceptually) — PARTIALLY DOCUMENTED (the need for a secrets service is documented, but exact secret naming and retrieval API are MISSING EVIDENCE). Citation: BACKEND_MODULE_ARCHITECTURE.md Layer 7.
- Logging Requirements: Structured logs and traces — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Section 15 / Layer 7 responsibilities).
- Observability Requirements: Emit metrics, traces, structured logs to `observability_service` — DOCUMENTED (Layer 7 responsibilities).
- Error Translation Rules: Errors must be translated to typed error objects before crossing boundaries — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md "Failure is a first-class concern").
- Retry Expectations: Shared `retry_utils` exist (DOCUMENTED) but per-call retry parameters are MISSING EVIDENCE (Section 11 and Shared list mention retry utilities but do not define thresholds). Classification: PARTIALLY DOCUMENTED.
- Health Check Requirements: Health checks are implied (observability/health) but specific probe definitions and thresholds are MISSING EVIDENCE. Classification: PARTIALLY DOCUMENTED.
- Testing Requirements: Infrastructure must be independently testable (DOCUMENTED high-level). Detailed test harness expectations per-service are MISSING EVIDENCE. Classification: PARTIALLY DOCUMENTED.
- Validation Requirements: Must implement interface contracts and pass type/contract checks — DOCUMENTED (Interface contract rules in BACKEND_MODULE_ARCHITECTURE.md).
- Freeze Requirements: Implementation requires explicit DI registration manifest, CODEOWNERS entries, and secrets/retry/health documentation to be present before file creation — MISSING EVIDENCE (these artifacts are not found in the authoritative docs).
- Module status: BLOCKED — reason: critical per-file implementation attributes (DI registration, secrets API, retry/health thresholds, owner mapping) are MISSING EVIDENCE in the frozen docs. (See Blockers below.)

2) Module: `anthropic_adapter`
- Module Name and Purpose: Anthropic API client implementation of `LLMInterface` — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 module list explicitly maps `anthropic_adapter` to `LLMInterface` implementation in narrative).
- Architecture Responsibility: Adapter that implements `LLMInterface` for Anthropic provider — PARTIALLY DOCUMENTED (mapping to `LLMInterface` is in the module list text; exact class names and file path are not specified). Citation: BACKEND_MODULE_ARCHITECTURE.md Layer 7.
- Implemented Interface: `LLMInterface` — PARTIALLY DOCUMENTED (interface exists in repo; mapping is documented at module list level).
- Expected Dependencies, Allowed/Forbidden Imports, Consumers, External Systems: follow the same documented/partially-documented pattern as `llm_gateway` above (DOCUMENTED at high level, per-file details MISSING EVIDENCE).
- Retry / Secrets / Health / Testing / Freeze Requirements: PARTIALLY DOCUMENTED or MISSING EVIDENCE as above.
- Module status: BLOCKED — missing file-level evidence (DI registration, secret key names, retry policy) prevents implementation.

3) Module: `storage_service`
- Purpose: Structured storage read/write for sessions, engagements, users — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 module list).
- Implemented Interface: `StorageInterface` — PARTIALLY DOCUMENTED (interface exists in `src/backend/core/interfaces/storage_interface.py`; mapping to concrete class is not specified in docs). Citation: BACKEND_MODULE_ARCHITECTURE.md Layer 7 and core interface listing.
- Configuration Source: `config/` (DOCUMENTED) but the exact configuration keys/connection strings and secrets are MISSING EVIDENCE (SECURITY_ARCHITECTURE.md and DATABASE_ARCHITECTURE.md do not specify exact config key names). Classification: PARTIALLY DOCUMENTED.
- Data durability, consistency, and schema expectations: DATABASE_ARCHITECTURE.md contains high-level DB architecture (DOCUMENTED) but does not mandate exact schema or retention policies for decision ledger or sessions (MISSING EVIDENCE at implementation granularity).
- Module status: BLOCKED — per-file DB adapter names, DI registration, credentials/secrets names are missing.

4) Module: `vector_store_service`
- Purpose: Vector index read/write for knowledge base — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 module list and KNOWLEDGE_ENGINE.md).
- Implemented Interface: implied `VectorStoreInterface` (documented as infrastructure interface in narrative but not always present as a named file across the documents) — PARTIALLY DOCUMENTED.
- External Systems: Vector DB or index provider (documented conceptually). Specific provider list and adapter mapping are MISSING EVIDENCE.
- Module status: BLOCKED — missing per-file mapping and config/secrets details.

5) Module: `cache_service`
- Purpose: Cache get/set/invalidate with TTL management — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 list).
- Implemented Interface: `CacheInterface` — PARTIALLY DOCUMENTED (interface exists; per-file mapping missing).
- Module status: BLOCKED for implementation until DI registration and runtime config keys are documented.

6) Module: `decision_ledger_service`
- Purpose: Append-only Decision Ledger implementation — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md, Core responsibilities include immutable Decision Ledger).
- Consistency/append-only guarantees: DOCUMENTED conceptually (decision ledger must be immutable), but the exact implementation durability SLAs, storage medium, and per-call semantics are MISSING EVIDENCE.
- Implemented Interface: `LedgerInterface` — PARTIALLY DOCUMENTED.
- Module status: BLOCKED until data-store and durability evidence are provided.

7) Module: `secrets_service`
- Purpose: Secrets retrieval and rotation-aware credential management — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 list).
- Required behaviour: rotation-aware retrieval and provider abstraction — DOCUMENTED conceptually.
- Missing evidence: concrete secrets API shape, secret key naming conventions, provider(s) supported, runtime wiring examples (MISSING EVIDENCE). Security/Secrets conventions should be present in SECURITY_ARCHITECTURE.md or IMPLEMENTATION_SPECIFICATION.md but are not. Classification: PARTIALLY DOCUMENTED / MISSING EVIDENCE.
- Module status: BLOCKED until secrets conventions and adapter contract are documented.

8) Module: `observability_service`
- Purpose: Structured log emission, trace span management, metrics emission — DOCUMENTED (Layer 7 list and Logging Architecture section).
- Implemented Interface: (observability interface file exists in core interfaces) — PARTIALLY DOCUMENTED.
- Observability naming conventions (metric names, span names, log schema): MISSING EVIDENCE (the architecture specifies observability is required but does not provide the canonical metric/log naming or required labels). Classification: PARTIALLY DOCUMENTED.
- Module status: BLOCKED until observability schema and metric/span naming docs are provided.

9) Module: `output_storage_service`
- Purpose: File-based storage for generated output artifacts — DOCUMENTED (BACKEND_MODULE_ARCHITECTURE.md Layer 7 list and OUTPUT_GENERATION_ARCHITECTURE.md responsibilities).
- Implemented Interface: `OutputStorageInterface` — PARTIALLY DOCUMENTED (interface file exists in repository; exact mapping to file is not present in the frozen docs).
- Module status: BLOCKED until per-file config for artifact storage, retention policies, and DI registration are documented.

Implementation Order (DOCUMENTED / INFERRED)
-----------------------------------------
- The frozen architecture does NOT provide a mandatory, prescriptive build or implementation sequence for infrastructure modules. The docs describe responsibilities and DI lifetimes but do not serialize module implementation steps. Therefore any proposed implementation order would be INFERRED. Classification: INFERRED.
- Implementation consequence: Per the NO ASSUMPTIONS policy, we MUST NOT proceed. Implementation order cannot be specified authoritatively from the frozen docs. The plan is BLOCKED pending an authoritative Implementation Sequence document or equivalent ADR.

Dependency Graph (DOCUMENTED facts)
---------------------------------
- Documented dependency direction (DOCUMENTED): Infrastructure implements Core interfaces and may import Shared; dependency direction is inward toward Domain Core (DOCUMENTED — BACKEND_MODULE_ARCHITECTURE.md Section 2, REPOSITORY_MASTER_STRUCTURE.md Section 1.4). No Infrastructure → Core inversion is allowed (DOCUMENTED — forbidden directions in Section 12.2).
- The docs require typed contracts (Pydantic) between modules (DOCUMENTED — BACKEND_MODULE_ARCHITECTURE.md 12.3). This establishes that Infrastructure is downstream of Interfaces and Shared.
- Verification: The architectural documents explicitly forbid circular dependencies and reverse dependency flows (DOCUMENTED). However the frozen docs do not provide an exhaustive import graph for the existing repository; a static analysis pass would be required to ensure the concrete codebase has no violations. That static analysis is an implementation-time gate (see Quality Gates). The dependency model itself in the architecture is DOCUMENTED.

Implementation Matrix (module-level, based only on documented evidence)
------------------------------------------------------------------
| Module | Interface | Status | Evidence |
|---|---|---:|---|
| llm_gateway | LLMInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; missing DI file mapping and secrets/ retry/health details |
| anthropic_adapter | LLMInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7 (module list); missing per-file evidence |
| storage_service | StorageInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; DATABASE_ARCHITECTURE.md (conceptual) — missing connection strings/credentials keys |
| vector_store_service | VectorStoreInterface (conceptual) | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; KNOWLEDGE_ENGINE.md — provider list missing |
| cache_service | CacheInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; missing DI registration evidence |
| decision_ledger_service | LedgerInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md; immutable ledger requirement documented but implementation medium missing |
| secrets_service | SecretsInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; SECURITY_ARCHITECTURE.md lacks secret key conventions |
| observability_service | ObservabilityInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; logging architecture documented but naming schema missing |
| output_storage_service | OutputStorageInterface | BLOCKED | BACKEND_MODULE_ARCHITECTURE.md Layer 7; OUTPUT_GENERATION_ARCHITECTURE.md references outputs storage but per-file config missing |

Quality gates (must be satisfied before any implementation PR is merged)
-----------------------------------------------------------------
For each gate below the plan records: Purpose, Success criteria, and Evidence source.

1. Repository Validation
- Purpose: Verify the repository exactly matches `REPOSITORY_MASTER_STRUCTURE.md` (no extra runtime artefacts, no missing files required by the master tree). 
- Success: A signed reconciliation (doc or ADR) showing either the repository has been updated to match the master tree, or the master tree has been updated via ADR to match the repo. No .venv or runtime caches tracked in repository. Evidence: REPOSITORY_MASTER_STRUCTURE.md. 

2. Architecture Validation
- Purpose: Confirm the implementation plan and DI registration manifest precisely match the frozen architecture documents (section and line references) and any new ADRs required.
- Success: A signed Architecture Review approval referencing exact doc sections used. Evidence: BACKEND_MODULE_ARCHITECTURE.md, REPOSITORY_MASTER_STRUCTURE.md, IMPLEMENTATION_SPECIFICATION.md.

3. Dependency Validation
- Purpose: Static verification that no implementation import violates the documented dependency direction and that infrastructure implements only interfaces from Core and Shared.
- Success: Static analysis report (import graph) demonstrating no illegal import edges. Evidence: BACKEND_MODULE_ARCHITECTURE.md Section 2, 12.

4. Import Validation
- Purpose: Lint and static checks for forbidden imports (no Infrastructure → Agents/Core logic), enforcement of interface-only consumption.
- Success: Lint report showing zero violations. Evidence: BACKEND_MODULE_ARCHITECTURE.md Section 12.2.

5. Unit Tests
- Purpose: Each implementation must be unit-testable via constructor-injected mocks. Tests exercise adapter behaviour against the interface contract.
- Success: Unit tests pass locally; test harness demonstrates injection and mocking. Evidence: BACKEND_MODULE_ARCHITECTURE.md (Testability principle) and IMPLEMENTATION_SPECIFICATION.md (testing guidance).

6. Coverage
- Purpose: Maintain code coverage ≥ 85% for the Infrastructure changeset (as enforced previously for Interface Layer).
- Success: Coverage report demonstrating ≥ 85% coverage for changed modules/tested code. Evidence: Project quality rules (previous gate results and CI configuration referenced in .github/workflows). NOTE: exact coverage target and enforcement point are documented in prior Interface work; treat as documented policy.

7. Type Checking (mypy)
- Purpose: `mypy --strict` must pass for implemented modules.
- Success: `mypy` report with no errors. Evidence: Project quality rules and prior runs.

8. Formatting & Linting (ruff/black)
- Purpose: Enforce code style and linting consistent with repo standards.
- Success: `ruff` and `black --check` pass. Evidence: REPOSITORY_MASTER_STRUCTURE.md (standards) and existing CI definitions.

9. Architecture Review / Freeze Review
- Purpose: Final architecture sign-off after implementation artifacts and DI registration manifest are proposed; ensure documentation and CODEOWNERS entries exist.
- Success: Formal Architecture Freeze approval recorded in repository (ADR or signed doc). Evidence: REPOSITORY_MASTER_STRUCTURE.md governance sections.

10. CI Validation
- Purpose: Full pipeline run (pytest, mypy, ruff, black, coverage) must pass in CI with implemented modules. 
- Success: CI run status green. Evidence: .github workflows and CI logs.

Blockers (required authoritative evidence missing — implementation STOP)
----------------------------------------------------------------
The following evidence items are missing from the frozen architecture documents and must exist before implementation may proceed. For each item I list the exact reason, the expected document that should contain it, and the consequence.

A. Per-file canonical names and DI registration manifest
- Missing evidence: Frozen docs list module names but do not mandate exact implementation file paths or the DI registration manifest (interface→implementation mapping and code-level class names). Without this, creating specific files would be an inference.
- Expected document: `IMPLEMENTATION_SPECIFICATION.md` extension or a new `DI_REGISTRATION_MANIFEST.md` that lists each interface, the authorized implementation file path(s), class names, and the required DI lifetime.
- Consequence: BLOCKED — cannot create implementation files or DI registrations.

B. Per-file Owner / CODEOWNERS mapping
- Missing evidence: No authoritative mapping of module → owner/team/person in the frozen docs. REPOSITORY_MASTER_STRUCTURE.md references CODEOWNERS but does not contain the mapping.
- Expected document: `.github/CODEOWNERS` populated and/or an `OWNERSHIP.md` table in docs that maps modules/files to owners and teams.
- Consequence: BLOCKED — cannot assign owner responsibilities or proceed to implementation without governance mapping.

C. Secrets naming conventions and secrets adapter contract
- Missing evidence: SECURITY_ARCHITECTURE.md and BACKEND_MODULE_ARCHITECTURE.md require a `secrets_service` but do not define secret key naming conventions, the retrieval API contract, or supported providers.
- Expected document: `SECURITY_SECRETS_POLICY.md` or an expanded `SECURITY_ARCHITECTURE.md` section with exact secret keys, example environment wiring, and adapter interface contract.
- Consequence: BLOCKED — cannot implement `secrets_service` or use secret values in other infra modules.

D. Retry / backoff / circuit-breaker operational policy
- Missing evidence: Shared.retry_utils exists conceptually, but numeric policies (retry counts, backoff base, jitter, idempotency classifications) and which operations are non-retriable are not documented.
- Expected document: `ERROR_HANDLING_POLICY.md` or augmentation of BACKEND_MODULE_ARCHITECTURE.md with per-service retry rules.
- Consequence: BLOCKED — cannot implement safe retry behaviour.

E. Health-check probe definitions and thresholds
- Missing evidence: The architecture requires health and observability but does not define per-service probes, endpoints, or acceptable thresholds.
- Expected document: `DEPLOYMENT_HEALTHCHECKS.md` or additions to `DEPLOYMENT_ARCHITECTURE.md` with explicit probes and semantics for each infra system.
- Consequence: BLOCKED — cannot implement health endpoints or monitors.

F. Observability schema (metric names, span conventions, log fields)
- Missing evidence: Observability is required but canonical metric and span naming conventions, required labels, and log schema are not present.
- Expected document: `OBSERVABILITY_SCHEMA.md` referenced by BACKEND_MODULE_ARCHITECTURE.md/IMPLEMENTATION_SPECIFICATION.md.
- Consequence: BLOCKED — cannot implement consistent observability output.

G. Implementation Sequence / Build Order
- Missing evidence: The frozen docs do not prescribe an authoritative implementation order for infrastructure modules. Any sequence would be an inference.
- Expected document: `IMPLEMENTATION_SPECIFICATION.md` (explicit implementation steps) or an ADR that prescribes the build sequence with prerequisites and validation gates.
- Consequence: BLOCKED — cannot start incremental implementation without a documented sequence.

Decision (final)
----------------
- Implementation is BLOCKED. This plan is the authoritative planning artifact created from the frozen architecture documents. It documents what is provable, what is partially documented, and what is missing.
- To proceed with implementation the missing evidence items (A–G above) must be produced and added to the frozen documents (or provided as ADRs and approved). After those documents exist, the plan will be updated to convert BLOCKED statuses to READY and to provide exact file-level implementation rows (module → file → owner → DI registration).

Next steps (recommended, minimal to unblock)
-------------------------------------------
1. Provide the DI registration manifest (minimal): for each interface name, authorized implementation file path and class name, and DI lifetime (Singleton/Scoped/Transient). Place this in `IMPLEMENTATION_SPECIFICATION.md` or `DI_REGISTRATION_MANIFEST.md` and reference the exact section in the master docs.
2. Publish `.github/CODEOWNERS` and an `OWNERSHIP.md` mapping modules to owners.
3. Publish `SECURITY_SECRETS_POLICY.md` describing secret key names and retrieval API.
4. Publish `ERROR_HANDLING_POLICY.md` with retry/backoff rules and idempotency classifications.
5. Publish `DEPLOYMENT_HEALTHCHECKS.md` with probe definitions.
6. Publish `OBSERVABILITY_SCHEMA.md` with required metrics/span/log fields.
7. Optionally publish an `IMPLEMENTATION_SEQUENCE.md` or update `IMPLEMENTATION_SPECIFICATION.md` with the required build order and prerequisites.

When those authoritative documents are available, I will: (a) re-run the Evidence Verification pass, (b) produce the per-file Infrastructure Implementation Matrix with section and line citations, and (c) produce a ready-to-implement plan with exact DI manifest, owners, and validation gates.

Appendix: primary citations
---------------------------
- REPOSITORY_MASTER_STRUCTURE.md — repository philosophy, folder responsibilities, configuration strategy, "Complete Repository Tree" (source of truth). (DOCUMENTED)
- BACKEND_MODULE_ARCHITECTURE.md — layer definitions, Layer 7 infrastructure module list, DI Strategy (Section 11), Cross-Module Communication (Section 12), Error Handling/Logging/Configuration sections. (DOCUMENTED)
- IMPLEMENTATION_SPECIFICATION.md — referenced for implementation conventions (read in full; where missing, noted in Blockers). (SOURCE READ — missing per-file registration evidence)
- SECURITY_ARCHITECTURE.md — referenced for secrets and security controls (read in full; missing per-secret naming conventions). (SOURCE READ)
- OUTPUT_GENERATION_ARCHITECTURE.md — referenced for output storage requirements. (SOURCE READ)
- DATABASE_ARCHITECTURE.md — referenced for storage/backing store durability semantics. (SOURCE READ)

End of plan (blocked).
