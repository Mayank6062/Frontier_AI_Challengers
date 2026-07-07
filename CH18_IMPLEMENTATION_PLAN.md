CH18 IMPLEMENTATION PLAN
=================================

Purpose
- Refined, non-coding implementation roadmap to migrate the repository to match CHAPTER 18 of OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_v2. This document prescribes decisions (REUSE / MOVE / RENAME / SPLIT / WRAP / CREATE) for every missing/canonical item, an ordered phase plan, validations and rollback guidance.

Constraints
- Do NOT modify repository in this plan. Implementation will be executed only after approval of each phase.
- Chapter 18 is the single source of truth.

STEP 0: SOURCES CONSULTED
- docs/architecture/OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_CREATION_PROMPT.md (Chapter 18 sections)
- repo audit: CH18_REPOSITORY_MIGRATION_PLAN.md (existing audit)

-----------------------------------------------------------------
STEP 1 — Per-file Strategy (missing / canonical items)
For each canonical file/folder required by Chapter 18, decision and details follow.

Format: Current Path -> Target Path | Decision | Implementation Strategy | Reuse % | Dependencies | Validation Required | Independent?

1) `exceptions.py`
MISSING -> `src/backend/output_generation/exceptions.py` | CREATE
Strategy: Implement Chapter-18 OutputGenerationError hierarchy as a small module. No existing code to reuse. Keep typed exceptions and docstrings.
Reuse %: 0%
Deps: none
Validation: mypy, ruff, unit tests for error raising paths
Independent: YES

2) `service.py` (OutputGeneratorService)
MISSING -> `src/backend/output_generation/service.py` | CREATE (from Bible)
Strategy: Implement orchestrator class per Chapter 18 spec. Minimal stub first that accepts DI-provided components; fully implement in later phases. Start with async API, typed interfaces.
Reuse %: 0%
Deps: `interfaces.py`, DI container
Validation: unit tests for orchestrator plumbing (no business logic) + mypy
Independent: PARTIALLY (needs DI container setup to integrate)

3) `factory.py` (OutputGeneratorFactory)
MISSING -> `src/backend/output_generation/factory.py` | CREATE
Strategy: Small factory helpers to create generators; initially return existing generator instances from repo where applicable.
Reuse %: 0%
Deps: `interfaces.py`, `service.py`
Validation: unit tests for factory resolution
Independent: YES

4) `schemas.py` (top-level DTOs)
MISSING -> `src/backend/output_generation/schemas.py` | CREATE
Strategy: Consolidate commonly used DTOs used across modules; reuse models from existing module locations (e.g., `bundle/schemas.py`, `presentation/models.py`) by import references to avoid duplicate definitions. Implement schema adapters that re-export existing Pydantic models where possible (WRAP pattern).
Reuse %: 60% (wrap and re-export existing models)
Deps: `bundle/schemas.py`, other subpackages
Validation: tests for DTO serialization/deserialization; mypy
Independent: NO (depends on subpackages' models)

5) `markdown/` pack
MISSING -> `src/backend/output_generation/markdown/` | CREATE
Strategy: Create directory and canonical generators. Reuse text-processing utilities from `documentation/` and `story/` packages where applicable (REUSE + WRAP). Start with minimal `hld_generator.py` and `markdown_validator.py` implementations from Bible; expand templates in `config/templates` later.
Reuse %: 30%
Deps: `schemas.py`, `templates` in config
Validation: unit generator tests, snapshot markdown tests
Independent: PARTIALLY

6) `html/` pack
MISSING -> `src/backend/output_generation/html/` | CREATE
Strategy: Create HTML generator that wraps markdown -> HTML pipeline where repo already has markdown/html utilities. Implement `sanitizer.py` per Chapter 18 rules.
Reuse %: 30%
Deps: `markdown/`, `visualization` outputs
Validation: unit tests, HTML schema checks
Independent: PARTIALLY

7) `diagrams/` (rename)
Current: `src/backend/output_generation/diagram/` -> Target: `src/backend/output_generation/diagrams/` | RENAME
Strategy: Physical rename of package. Prefer project-wide IDE rename; keep code unchanged. After rename, update imports via automated refactor and run tests. This is RENAME rather than CREATE to avoid duplication.
Reuse %: 100% (code reused)
Deps: many modules import diagram.*; prepare import-change plan
Validation: run full test suite after rename, search for leftover imports
Independent: NO

8) `diagrams/*` files mandated by Bible (mermaid_generator, dot_generator etc.)
MISSING -> `src/backend/output_generation/diagrams/mermaid_generator.py` etc. | CREATE or REUSE if equivalents present
Strategy: For each diagram type, search current `diagram/` for equivalent; if present REUSE (move/rename); otherwise CREATE from Bible canonical code.
Reuse %: variable per file (0–90%)
Deps: `visualization`, `presentation`
Validation: renderer unit tests, image snapshot tests
Independent: NO

9) `manifest/` package
MISSING -> `src/backend/output_generation/manifest/` | CREATE + MOVE
Strategy: Consolidate manifest-related code. Move `bundle/integrity.py` -> `manifest/integrity_hasher.py` (MOVE+RENAME). Move manifest validation logic from `bundle/validation.py` -> `manifest/manifest_validator.py` (SPLIT). Reuse existing hashing and schema (config/schemas/output_manifest_v2.json). Implement provenance_graph_builder from Bible.
Reuse %: 70%
Deps: `bundle`, `storage`, `quality`
Validation: manifest unit tests, schema validation (jsonschema), composite hash tests
Independent: PARTIALLY (requires bundle consumer updates)

10) `storage/` package
Current: `src/backend/output_generation/bundle/storage.py` -> Target: `src/backend/output_generation/storage/local_storage.py` and others | MOVE + SPLIT
Strategy: Split single-storage file into `storage/local_storage.py` (from existing code) and create `storage/common.py` for shared interfaces; implement `s3_storage.py` and `gcs_storage.py` as adapters per Bible. Wrap existing filesystem adapter into canonical `OutputStorageService` interface (WRAP). Update DI to use Selector provider.
Reuse %: 85% (local adapter reuse)
Deps: DI container, bundle, manifest
Validation: storage unit tests (read/write/exists/list_prefix/make_immutable), integration tests with local FS
Independent: PARTIALLY

11) `orchestration/` package
MISSING -> `src/backend/output_generation/orchestration/` | CREATE
Strategy: Implement `generation_orchestrator.py` per Bible; reuse existing `orchestration` modules in repo only if they match contract. Provide event handlers that call `service.py` orchestrator. Minimal shim first, full logic later.
Reuse %: 10% (few existing orchestrations elsewhere)
Deps: `service`, `factory`, `telemetry`, `storage`
Validation: orchestration unit tests + end-to-end pipeline tests
Independent: NO

12) `telemetry/` package
Current: `src/backend/infrastructure/observability/metrics.py` -> Target: `src/backend/output_generation/telemetry/metrics.py` | WRAP
Strategy: Create wrapper package that re-exports and adapts infra observability primitives to Chapter 18 telemetry surface (metrics/tracing/structured_logging). Do not duplicate implementation; wrap and extend.
Reuse %: 90%
Deps: infra observability
Validation: telemetry unit tests, ensure logging/audit events are emitted during bundle assembly
Independent: NO (needs infra)

13) `config/di_container.py`
MISSING -> `src/backend/output_generation/config/di_container.py` | CREATE
Strategy: Implement DI container per Chapter 18 using dependency_injector or repo's DI pattern. Wire storage selector, manifest_builder, bundle_assembler, quality orchestrator. Initially provide minimal providers referencing existing implementations to avoid behavior changes.
Reuse %: 20% (use existing implementations)
Deps: storage, bundle, manifest, quality
Validation: container unit tests and application startup tests
Independent: PARTIALLY

14) `score_report/` package
MISSING -> `src/backend/output_generation/score_report/` | CREATE
Strategy: Implement score_report generator using existing architecture_score code; wrap existing logic into canonical package and add renderers.
Reuse %: 70%
Deps: `quality`, `visualization`
Validation: unit tests, score report structural validation
Independent: PARTIALLY

15) `export/*` missing exporters
Current: `src/backend/output_generation/export/` exists but lacks some canonical exporters -> Target: export/*.py | REUSE + CREATE
Strategy: Reuse present helpers; add missing `pdf_exporter.py`, `docx_exporter.py`, `pptx_exporter.py` if not present by implementing thin adapters invoking presentation/pptx generator and third-party libs.
Reuse %: 60%
Deps: `presentation`, external libs
Validation: exporter unit tests and basic render smoke tests
Independent: PARTIALLY

16) Tests (Chapter 18 test matrix)
MISSING tests -> Target: tests/* (unit/integration/perf/security/golden/visual/accessibility)
Decision: CREATE many tests but REUSE existing bundle tests. Implement in phases following feature completion.
Reuse %: 50%
Deps: all modules
Validation: run pytest, mypy, ruff, black
Independent: NO

-----------------------------------------------------------------
STEP 2 — Phase Breakdown (each phase independently compilable)
Rationale: sequence minimizes breaking changes and enables fast validation. Each phase produces a buildable state that passes unit tests for code touched.

Phase 1 — Core & DI skeleton
- Goal: create DI container skeleton, exceptions, schemas wrapper, service/factory stubs, telemetry wrapper.
- Files created (plan): `exceptions.py` (stub), `src/backend/output_generation/config/di_container.py` (skeleton), `schemas.py` (re-export wrappers), `service.py` (stub), `factory.py` (stub), `telemetry/__init__.py` (wrapper importing infra metrics)
- Files reused: `interfaces.py`, bundle package unchanged.
- Validation commands: pytest -q (bundle tests should continue passing), mypy, ruff, black --check
- Expected risks: minor import path adjustments; DI wiring mistakes
- Rollback plan: revert DI container and stubs commit; restore prior imports
- Acceptance criteria: repository imports resolve; unit tests for bundle pass; DI container importable

Phase 2 — Diagrams rename + adapters
- Goal: rename `diagram/` -> `diagrams/` and adapt imports. Add missing diagram generators where absent.
- Files modified: import paths across codebase
- Files reused: all diagram code
- Validation: pytest -q, search for `diagram.` occurrences
- Risks: import failures; mitigated by automated find/replace and running tests
- Rollback: revert rename commit
- Acceptance: full test suite passes; no import errors

Phase 3 — Manifest package
- Goal: create `manifest/` package and move hashing+manifest validation into it.
- Files created: `manifest/manifest_builder.py`, `manifest/integrity_hasher.py`, `manifest/manifest_validator.py`, `manifest/provenance_graph_builder.py`
- Files moved: `bundle/integrity.py` -> `manifest/integrity_hasher.py`; selected validators moved to manifest.
- Reused: hashing code and JSON schema
- Validation: run manifest unit tests (new) and existing bundle tests
- Risks: import cycles; mitigate by keeping manifest pure (no bundle imports)
- Rollback: revert move and re-run previous tests
- Acceptance: manifest unit tests pass and composite_hash matches

Phase 4 — Storage backends (local -> canonical package)
- Goal: split existing storage into `storage/local_storage.py` and create `storage/common.py`, `s3_storage.py`, `gcs_storage.py` stubs.
- Files moved: `bundle/storage.py` -> `storage/local_storage.py` (split)
- Reused: existing FS adapter logic
- Validation: storage unit tests: write/read/exists/list_prefix/make_immutable
- Risks: filesystem permission issues on CI; DI miswire
- Rollback: revert split commit
- Acceptance: storage adapter unit tests pass; bundle assembler can write/read to local storage

Phase 5 — Bundle finalization & naming
- Goal: ensure bundle layer uses manifest and storage canonical interfaces; rename files to canonical names where required (e.g., `naming_convention.py`).
- Files modified: `bundle_assembler.py` imports updated
- Validation: bundle assembly tests, verify_integrity tests
- Risks: mismatched manifest imports
- Rollback: revert changes
- Acceptance: bundle assembly end-to-end passes unit tests

Phase 6 — Orchestration + Service wiring
- Goal: implement `generation_orchestrator.py` and wire `OutputGeneratorService` end-to-end through DI.
- Files created: orchestrator module, event handlers
- Validation: integration pipeline unit tests (smoke)
- Risks: complexity; mitigate by incremental wiring and feature flags
- Rollback: revert orchestrator commit
- Acceptance: orchestration unit tests pass; API start-up stable

Phase 7 — Generators: markdown & html
- Goal: add `markdown/` and `html/` generators and minimal templates; provide snapshot tests.
- Files created: `markdown/hld_generator.py`, `markdown/markdown_validator.py`, `html/report_generator.py`, `html/sanitizer.py`
- Validation: generator unit tests, snapshot tests
- Risks: template quality, external deps
- Rollback: revert generators commit
- Acceptance: generator tests pass and snapshots match expected minimal baselines

Phase 8 — Presentation & Export
- Goal: implement `presentation/pptx_generator.py` and exporters (`export/pdf_exporter.py`, `docx_exporter.py`, `pptx_exporter.py`)
- Validation: export unit tests, compatibility smoke tests
- Risks: third-party libs; mitigate by stubbing heavy functionality first
- Rollback: revert exporters
- Acceptance: exporters render minimal documents and tests pass

Phase 9 — Quality & Score Report
- Goal: implement quality orchestrator, score_report package, and validators integration
- Validation: quality unit tests and score_report tests
- Risks: validator failures producing BLOCKERS; mitigate via config thresholds
- Rollback: revert orchestrator/quality commits
- Acceptance: quality gate runner produces expected outputs and tests pass

Phase 10 — Telemetry & Observability
- Goal: implement full telemetry package (wrap infra metrics, add structured logging and tracing), ensure audit logs for bundle generation
- Validation: telemetry unit tests, integration test verifying audit log emission
- Risks: integration with infra; mitigate by wrapper approach
- Rollback: revert telemetry wrapper
- Acceptance: telemetry emits metrics and audit logs during bundle assembly tests

Phase 11 — Tests expansion (performance/security/golden/visual/accessibility)
- Goal: implement remaining test suites per Chapter 18
- Validation: run entire test matrix
- Risks: flaky tests and infra dependencies; mitigate using CI resources and mocks
- Rollback: adjust or disable tests until infra available; keep implementation gated
- Acceptance: tests run green within acceptable thresholds

Phase 12 — Integration, Full Validation & Freeze
- Goal: run full validation: pytest, mypy, ruff, black, storybook (if required), snapshots, performance, accessibility, security, golden tests; produce CH18 freeze artifacts
- Validation commands: full CI pipeline
- Acceptance: all validations PASS; CH18 freeze reports generated

-----------------------------------------------------------------
STEP 3 — Per-phase Details (files created/modified/reused, validations, risks, rollback, acceptance)
Note: only phases 1–4 show full example; subsequent phases follow same pattern in execution.

Phase 1 details (Core & DI skeleton)
- Files Created: `src/backend/output_generation/exceptions.py` (stub), `src/backend/output_generation/config/di_container.py` (skeleton), `src/backend/output_generation/schemas.py` (wrappers), `src/backend/output_generation/service.py` (stub), `src/backend/output_generation/factory.py` (stub), `src/backend/output_generation/telemetry/__init__.py` (wrapper)
- Files Modified: none (initial implementation uses new files only)
- Files Reused: `src/backend/output_generation/interfaces.py`, `src/backend/output_generation/bundle/*`
- Validation commands:
  - pytest -q tests/test_bundle_phase2.py
  - mypy
  - ruff .
  - black --check .
- Expected Risks: incorrect import wiring, DI provider naming mismatches
- Rollback Plan: revert commit; DI not referenced by production code until Phase 6
- Acceptance Criteria: new modules importable, bundle tests unchanged and passing

Phase 2 details (Diagrams rename & adapters)
- Files Created: none (rename)
- Files Modified: import path changes across repository
- Files Reused: all existing diagram code
- Validation commands: pytest -q; grep for `diagram.` unresolved imports
- Expected Risks: module name collisions; hidden relative imports
- Rollback: revert rename
- Acceptance: full test suite passes; no import errors

Phase 3 details (Manifest package)
- Files Created: `manifest/*` files
- Files Modified: `bundle_assembler.py` (imports updated)
- Files Reused: existing hashing and manifest schema
- Validation commands: pytest -q tests/test_manifest_builder.py tests/test_bundle_phase2.py
- Expected Risks: import cycles; composite hash mismatch
- Rollback: revert move and re-run previous tests
- Acceptance: manifest unit tests pass and composite_hash matches

Phase 4 details (Storage backends)
- Files Created: `storage/local_storage.py`, `storage/common.py`, stubs for `s3_storage.py` and `gcs_storage.py`
- Files Modified: code that imports `bundle/storage.py` now imports `storage.local_storage`
- Files Reused: existing FS adapter logic
- Validation commands: pytest -q tests/test_storage.py
- Expected Risks: filesystem permission issues on CI; DI miswire
- Rollback: revert split commit
- Acceptance: storage adapter unit tests pass; make_immutable emulated

-- For Phases 5–12 follow the same template (listed previously).

STEP 4 — Dependency Graph (phase dependencies)
- Phase 1 (Core & DI) : base — no dependencies
- Phase 2 (Diagrams rename) : depends on Phase 1
- Phase 3 (Manifest) : depends on Phase 1
- Phase 4 (Storage) : depends on Phase 1 and Phase 3 (manifest hashing used by storage tests)
- Phase 5 (Bundle finalization) : depends on Phase 3 + Phase 4
- Phase 6 (Orchestration) : depends on Phases 1,3,4,5
- Phase 7 (Markdown/HTML generators) : depends on Phases 1 and 6 (service API)
- Phase 8 (Presentation & Export) : depends on Phase 7
- Phase 9 (Quality & Score) : depends on Phase 7 and Phase 3
- Phase 10 (Telemetry) : depends on Phase 1 and infra observability
- Phase 11 (Tests expansion) : depends on all feature phases
- Phase 12 (Integration & Freeze) : depends on all prior phases

No circular dependencies must be introduced — enforcement rules:
- `manifest` is library-only (no imports of `bundle`) to break potential cycles.
- `storage` exposes only interface; consumers depend on the interface not concrete adapters.

STEP 5 — Duplicate Implementations Check
- Goal: determine whether Chapter 18 can be implemented WITHOUT creating duplicate implementations.
- Verdict: YES — it is possible to avoid duplicate implementations by using the following approach:
  1. REUSE existing bundle code and diagram code in place where functionally equivalent.
  2. RENAME `diagram/` to `diagrams/` (move, not duplicate).
  3. MOVE `bundle/integrity.py` into `manifest/integrity_hasher.py` (single canonical file) and adapt imports.
  4. SPLIT `bundle/storage.py` into `storage/local_storage.py` (move content) + `storage/common.py` and create adapters for S3/GCS only (no duplicate FS logic).
  5. WRAP infra `metrics.py` into `output_generation/telemetry` rather than copy-paste.

If at any point a canonical file is missing and no equivalent exists, CREATE from Bible; always prefer the ordered choices: REUSE > MOVE > RENAME > WRAP > CREATE.

STEP 6 — Final validation checklist before implementation
- Confirm Chapter 18 canonical tree checklist (see CH18_REPOSITORY_MIGRATION_PLAN.md) — list all directories present/missing.
- Ensure infra observability package is stable and imported by telemetry wrapper.
- Create a small script that performs import graph analysis after each phase to detect cycles.

STEP 7 — Next actions (after your approval)
1. I will generate the concrete per-file move/rename list (explicit source -> destination entries) and an ordered sequence of small commits to implement Phase 1.
2. After you approve Phase 1 plan, I will perform Phase 1 changes (only after explicit approval). Each implementation step will be accompanied by running the validation commands and results reported.

-----------------------------------------------------------------
Document end. Approve to proceed with generating the concrete file-level move/rename patch plan for Phase 1.
