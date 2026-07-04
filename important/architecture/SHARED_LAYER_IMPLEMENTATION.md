# Shared Layer Implementation

## Purpose

Provide a concise, production-ready implementation plan for the Shared Layer (`src/backend/shared/`) that creates only skeleton artifacts required to start implementation while preserving the frozen architecture. This document mandates structure, responsibilities, validation, and test requirements for Shared. No design changes or implementation code are introduced.

## Responsibilities

- Provide cross-cutting, implementation-agnostic utilities, models, exceptions, and constants used by all other backend layers.  
- Contain zero business logic and zero dependencies on project modules.  
- Offer stable, minimal public APIs for consumption by Core, Orchestration, Agents, Infrastructure, API, Knowledge, and Outputs layers.

## Design Principles

- Single-responsibility per module within Shared.  
- No domain knowledge or business rules.  
- Explicit, minimal, and well-documented public APIs.  
- Immutable data model definitions for shared types.  
- Side-effect-free utilities where possible; IO limited to controlled helper functions (e.g., hashing) without external system access.

## Dependency Rules

- Shared MUST NOT import from or depend on any other project module.  
- Shared MAY import only from the Python standard library and approved third-party utility libraries (e.g., stable runtime utilities approved by Platform Engineering).  
- Any third-party dependency used in Shared requires prior approval and must be documented in the dependency manifest.  
- All other project layers (API, Core, Orchestration, Agents, Infrastructure, Knowledge, Outputs, Frontend) MAY depend on Shared.  

## Folder Structure

List of Shared Layer folders (exact names from the frozen repository):

- `src/backend/shared/`
  - `models/`
  - `exceptions/`
  - `utils/`
  - `constants/`

Do not create any additional folders under `src/backend/shared/` during bootstrap.

## Module Responsibilities

`models/`  
- Responsibility: Define framework-level, transport-agnostic data types used across layers (e.g., base model classes, identifier and timestamp primitives).  
- Inputs: primitive values from callers (strings, ints, dicts) for construction/validation.  
- Outputs: validated, serializable model instances and canonical serializers.  
- Dependencies: Python stdlib and approved third-party libs only.  
- Public API (high-level): `BaseModel` (serialization/validation contract), `Identifier` generator/validator, `Timestamp` utilities.

`exceptions/`  
- Responsibility: Define the canonical shared exception hierarchy for platform-wide error handling and policy translation.  
- Inputs: error contexts, messages, optional metadata.  
- Outputs: structured exception instances usable by logging and observability.  
- Dependencies: Python stdlib only.  
- Public API (high-level): `SharedError` base class, domain-agnostic derived exceptions (see Exception Hierarchy).

`utils/`  
- Responsibility: Provide general-purpose, side-effect-minimized helper functions (text sanitation, deterministic hashing, retry/backoff primitives, safe string utilities).  
- Inputs: primitive data (strings, bytes, callables for retry).  
- Outputs: pure values or lightweight wrappers (hash strings, sanitized text, retry-decorated callables).  
- Dependencies: Python stdlib and approved third-party utilities where necessary.  
- Public API (high-level): `sanitize_text()`, `compute_hash()`, `retry_policy()` factory, `parse_timestamp()` helpers.

`constants/`  
- Responsibility: Store platform-wide constant categories used by multiple layers (no environment-specific secrets or values).  
- Inputs: none at runtime (constants only).  
- Outputs: importable constant values.  
- Dependencies: none.  
- Public API (high-level): grouped constants packages (e.g., `AGENT_CONSTANTS`, `ENGAGEMENT_STATES`, `PLATFORM_CONSTANTS`).

## Data Models

Shared may contain only framework-level models; examples of allowed shared data models (names only):

- `BaseModel` — canonical serialization/validation base for shared types.  
- `Identifier` — canonical UUID/ID wrapper and validator.  
- `Timestamp` — UTC timestamp canonicalizer/serializer.  
- `Pagination` — generic pagination descriptor (offset/limit/cursor) — tooling-level only.  

No business/domain models (sessions, engagements, agents outputs, etc.) belong in Shared.

## Exception Hierarchy

Shared defines the canonical exception types consumed by upper layers. High-level hierarchy (names only):

- `SharedError` (base)  
  - `ValidationError`  
  - `SerializationError`  
  - `ConfigurationError`  
  - `DependencyError`  
  - `AgentSharedError` (adapter for agent-surface exceptions)  

Layer-specific exceptions (e.g., knowledge, ledger) may be defined under `exceptions/` as subclasses of `SharedError` but must remain domain-agnostic in behavior.

## Utility Modules

Allowed utility modules inside `utils/` (names only):

- `text_utils` — sanitization and safe formatting helpers.  
- `hash_utils` — deterministic hashing and stable keys.  
- `retry_utils` — retry/backoff primitives and factories (no external IO).  
- `time_utils` — timestamp parsing/formatting helpers.  
- `sanitizer` — input sanitizer for prompts and free text (NI: pure functions only).  

No IO-heavy utilities (database access, network clients, file-system state beyond safe temp helpers) belong in Shared.

## Constants

Categories of constants permitted in `constants/`:

- `Agent` constants (timeouts, default limits, non-secret operational thresholds).  
- `Engagement` lifecycle state identifiers (enumerations, stable strings).  
- `Platform` constants (correlation id header names, default time formats).  
- `Limits` (size limits for shared utilities).  

Constants must never contain secrets, environment-specific endpoints, or credentials.

## Validation Rules

Allowed:  
- Standard library and approved third-party utilities only.  
- Pure utility functions and stable data-model definitions.  
- Co-located unit tests and module `README.md`.  

Prohibited:  
- Imports from any other project module or layer.  
- Business logic, domain models, or agent-specific behavior.  
- Secrets, credentials, or environment-specific values.  
- Network, database, or external system clients (these belong in Infrastructure).

## Testing Requirements

- Unit tests co-located in each Shared module directory (e.g., `src/backend/shared/utils/tests/`).  
- Coverage: ≥ 85% for each Shared module; measured and enforced by CI.  
- Tests must validate API contracts, edge-case behavior, determinism, and error paths for utilities and model serializers.  
- No integration tests that require other project layers; all dependencies must be mocked.

## Freeze Rules

- The Shared Layer MUST have zero domain dependencies (REPOSITORY_MASTER_STRUCTURE FR-08).  
- The Shared Layer may import only Python standard library and approved third-party utilities.  
- Every module in Shared must include a `README.md` declaring its single responsibility.  
- Any change to Shared dependencies or the introduction of new third-party libraries requires an ADR and ARB approval before merge.

## Definition of Done

- All Shared folders created exactly as listed.  
- Each folder contains only permitted initial files (`README.md`, `__init__.py` where applicable, `.gitkeep` for empties).  
- Module `README.md` files are present and reference the frozen authoritative documents.  
- Unit tests present and passing; coverage gate satisfied.  
- No implementation/business logic or external system clients present.  
- Structural PR passes review for exact path fidelity to frozen architecture.

## Implementation Checklist

- [ ] Create `src/backend/shared/` and subfolders: `models/`, `exceptions/`, `utils/`, `constants/`.  
- [ ] Add `README.md` to each folder describing responsibility and pointing to authoritative docs.  
- [ ] Add `__init__.py` to Python package folders as required.  
- [ ] Add `.gitkeep` where an otherwise-empty folder must be preserved.  
- [ ] Add unit-test skeletons for each module and implement tests verifying boundary rules and utility behavior.  
- [ ] Open a single PR containing skeletons only; reference frozen authoritative documents in the PR description.  
- [ ] Obtain structural approval and merge; do not add implementation code in this PR.

End of Shared Layer Implementation
