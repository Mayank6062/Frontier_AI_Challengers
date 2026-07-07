CH18 REPOSITORY MIGRATION PLAN
=================================

This document maps the CURRENT repository (workspace) to the CHAPTER 18 canonical tree described in OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_v2 and prescribes migration actions. No code changes are performed by this plan — it only prescribes MOVE/RENAME/CREATE/KEEP/DELETE/MERGE operations and the implementation order.

Mapping table columns: Current Path | Target Path | Action | Reason | Reuse % | Risk

-- Major entries (canonical Chapter 18 tree items). For items present in repo the current path is listed; for missing items Current Path = MISSING.

1) Top-level output_generation package

Current Path: src/backend/output_generation/__init__.py
Target Path: src/backend/output_generation/__init__.py
Action: KEEP
Reason: Module exists; keep and export version.
Reuse %: 100%
Risk: Low

Current Path: MISSING
Target Path: src/backend/output_generation/exceptions.py
Action: CREATE
Reason: Chapter 18 requires OutputGenerationError hierarchy.
Reuse %: 0%
Risk: Low

Current Path: MISSING
Target Path: src/backend/output_generation/service.py
Action: CREATE
Reason: Chapter 18 requires OutputGeneratorService orchestrator.
Reuse %: 0%
Risk: Medium (orchestration integration)

Current Path: MISSING
Target Path: src/backend/output_generation/factory.py
Action: CREATE
Reason: DI factory required by Chapter 18.
Reuse %: 0%
Risk: Low

Current Path: MISSING
Target Path: src/backend/output_generation/schemas.py
Action: CREATE
Reason: Canonical shared DTOs expected at top-level.
Reuse %: 0%
Risk: Low

Current Path: src/backend/output_generation/interfaces.py
Target Path: src/backend/output_generation/interfaces.py
Action: REUSE AS-IS
Reason: Interfaces match Chapter 18 contracts; reuse.
Reuse %: 100%
Risk: Low

2) markdown/

Current Path: MISSING
Target Path: src/backend/output_generation/markdown/__init__.py
Action: CREATE
Reason: Chapter 18 mandates `markdown/` generators and templates.
Reuse %: 0%
Risk: Medium (templates + generators to author)

Current Path: MISSING
Target Path: src/backend/output_generation/markdown/hld_generator.py
Action: CREATE
Reason: Canonical generator required.
Reuse %: 0%
Risk: Medium

(all other markdown files listed in Chapter 18) -> CREATE

3) html/

Current Path: MISSING
Target Path: src/backend/output_generation/html/__init__.py
Action: CREATE
Reason: Chapter 18 requires HTML generator and templates.
Reuse %: 0%
Risk: Medium

4) portal/

Current Path: src/backend/output_generation/portal/__init__.py
Target Path: src/backend/output_generation/portal/__init__.py
Action: REUSE AS-IS
Reason: `portal/` folder exists with many files that match Chapter 18 responsibilities.
Reuse %: 85%
Risk: Low

5) diagrams/ (canonical plural)

Current Path: src/backend/output_generation/diagram/
Target Path: src/backend/output_generation/diagrams/
Action: RENAME
Reason: Chapter 18 uses `diagrams/` plural; current code in `diagram/` contains diagram implementations to be preserved but path must match spec.
Reuse %: 95%
Risk: Medium (import path changes across repository)

6) visualization/

Current Path: src/backend/output_generation/visualization/
Target Path: src/backend/output_generation/visualization/
Action: REUSE AS-IS
Reason: Directory exists and maps to Chapter 18; adapt imports if any.
Reuse %: 95%
Risk: Low

7) presentation/

Current Path: src/backend/output_generation/presentation/
Target Path: src/backend/output_generation/presentation/
Action: REUSE AS-IS
Reason: Exists; must ensure presence of `pptx_generator.py` and templates. If missing, create below.
Reuse %: 80%
Risk: Low-Medium

8) quality/

Current Path: src/backend/output_generation/quality/
Target Path: src/backend/output_generation/quality/
Action: REUSE AS-IS
Reason: Many validators exist; orchestrator may be missing.
Reuse %: 85%
Risk: Low

9) score_report/

Current Path: MISSING
Target Path: src/backend/output_generation/score_report/__init__.py
Action: CREATE
Reason: Chapter 18 defines `score_report/` for architecture scoring outputs.
Reuse %: 0%
Risk: Medium

10) export/

Current Path: src/backend/output_generation/export/
Target Path: src/backend/output_generation/export/
Action: REUSE AS-IS
Reason: `export/` exists but some exporters (pdf/docx/pptx) may be missing — create any missing files.
Reuse %: 70%
Risk: Low-Medium

11) manifest/

Current Path: MISSING (manifest functions scattered)
Target Path: src/backend/output_generation/manifest/
Action: CREATE + MOVE
Reason: Chapter 18 requires `manifest_builder.py`, `integrity_hasher.py`, `provenance_graph_builder.py`, `manifest_validator.py`, `schemas.py`. Existing code (bundle/integrity.py, bundle/validation.py) should be moved/adapted.
Reuse %: 70% (move integrity and some validation code)
Risk: Medium (imports and behavioral equivalence must be preserved)

12) bundle/

Current Path: src/backend/output_generation/bundle/
Target Path: src/backend/output_generation/bundle/
Action: REUSE AS-IS (with small renames)
Reason: Bundle layer exists and matches Chapter 18 responsibilities. Files present: `bundle_assembler.py`, `persona_filter.py`, `archive_builder.py`, `schemas.py`, `integrity.py`, `validation.py`, `storage.py`.
Reuse %: 95%
Risk: Low

Notes: Chapter 18 expects `bundle/naming_convention.py` and `bundle/bundle_validator.py` names; if logical equivalents exist, rename to canonical names (MOVE/RENAME) instead of creating duplicates.

13) storage/

Current Path: src/backend/output_generation/bundle/storage.py (single file)
Target Path: src/backend/output_generation/storage/local_storage.py
Action: MOVE + SPLIT
Reason: Chapter 18 defines a storage package with `local_storage.py`, `s3_storage.py`, `gcs_storage.py`. Existing storage implementation should be split into local + common interface.
Reuse %: 90%
Risk: Medium (requires careful split and DI updates)

14) orchestration/

Current Path: MISSING (orchestration exists elsewhere)
Target Path: src/backend/output_generation/orchestration/
Action: CREATE
Reason: Chapter 18 requires `generation_orchestrator.py`, `generation_event_handlers.py`, and `telemetry.py` under orchestration.
Reuse %: 0%
Risk: Medium

15) telemetry/

Current Path: src/backend/infrastructure/observability/metrics.py
Target Path: src/backend/output_generation/telemetry/metrics.py
Action: REUSE AS-IS (reference) + CREATE wrapper
Reason: Existing metrics implementation lives under infrastructure and can be reused; create `output_generation/telemetry/` package that imports/wraps infra implementation to meet Chapter 18 layout.
Reuse %: 90%
Risk: Low

16) config/

Current Path: config/schemas/output_manifest_v2.json
Target Path: config/schemas/output_manifest_v2.json
Action: KEEP
Reason: Canonical JSON schema present and correct.
Reuse %: 100%
Risk: Low

Current Path: MISSING
Target Path: src/backend/output_generation/config/di_container.py
Action: CREATE
Reason: Chapter 18 DI container required to wire storage/orchestrator/manifest/bundle.
Reuse %: 0%
Risk: Medium

17) tests/

Current Path: tests/test_bundle_phase2.py and other bundle tests
Target Path: tests/unit/test_bundle_assembler.py etc. (Chapter-18 test matrix)
Action: REUSE + CREATE
Reason: Existing tests for bundle layer can be reused; many canonical tests must be created (markdown, html, portal, performance, security, golden, visual regression).
Reuse %: 60%
Risk: Medium

18) presentation templates and config/templates

Current Path: MISSING or partial
Target Path: config/templates/{markdown,html,portal,presentation,pdf}/v*
Action: CREATE
Reason: Chapter 18 mandates templated packs.
Reuse %: 0%
Risk: Medium

19) score_report and quality orchestrator

Current Path: quality/ (validators exist)
Target Path: quality/orchestrator.py and score_report/
Action: CREATE + REUSE
Reason: Build orchestrator using existing validators; create score_report package.
Reuse %: 70%
Risk: Medium

20) README / docs / frozen files

Current Path: docs/architecture/OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_CREATION_PROMPT.md
Target Path: docs/architecture/OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_CREATION_PROMPT.md
Action: KEEP
Reason: Source-of-truth guidance present.
Reuse %: 100%
Risk: Low


SECTION 1 — Folders to Create
- src/backend/output_generation/exceptions.py (file)
- src/backend/output_generation/service.py (file)
- src/backend/output_generation/factory.py (file)
- src/backend/output_generation/schemas.py (file)
- src/backend/output_generation/markdown/
- src/backend/output_generation/html/
- src/backend/output_generation/diagrams/ (rename from `diagram`)
- src/backend/output_generation/manifest/
- src/backend/output_generation/storage/
- src/backend/output_generation/orchestration/
- src/backend/output_generation/telemetry/ (wrapper package)
- src/backend/output_generation/score_report/
- src/backend/output_generation/config/di_container.py
- config/templates/ (template packs)
- tests/unit/* (many missing unit tests), tests/integration/, tests/performance/, tests/security/, tests/golden/, tests/visual_regression/, tests/accessibility/

SECTION 2 — Folders to Rename
- src/backend/output_generation/diagram/ -> src/backend/output_generation/diagrams/ (RENAME)
  Reason: canonical plural name; content reused.
  Risk: Medium — update imports across repository.

SECTION 3 — Files to Move
- src/backend/output_generation/bundle/storage.py -> src/backend/output_generation/storage/local_storage.py (MOVE + SPLIT)
  Reason: consolidate storage backends.
  Risk: Medium

- src/backend/output_generation/bundle/integrity.py -> src/backend/output_generation/manifest/integrity_hasher.py (MOVE + RENAME)
  Reason: move manifest-related hashing to manifest package.
  Risk: Medium

- existing validators in bundle/validation.py -> src/backend/output_generation/manifest/manifest_validator.py (MOVE + SPLIT)
  Reason: move manifest-specific validations to manifest package.
  Risk: Medium

SECTION 4 — Files to Split
- bundle/storage.py -> split into `storage/local_storage.py` + `storage/common.py` for shared utilities.
  Reason: multi-backend support (local/s3/gcs).
  Risk: Medium

SECTION 5 — Files to Merge
- If `bundle/validation.py` and `quality/validation.py` contain duplicate validators, MERGE into canonical `quality/validators/` and `manifest/manifest_validator.py` as appropriate.
  Risk: Low-Medium

SECTION 6 — Files to Delete
- None recommended immediately. Prefer MOVE/RENAME/REUSE rather than delete. After refactor and tests, remove obsolete duplicates in a follow-up PR.

SECTION 7 — Files to Create
- src/backend/output_generation/exceptions.py
- src/backend/output_generation/service.py
- src/backend/output_generation/factory.py
- src/backend/output_generation/schemas.py
- src/backend/output_generation/markdown/hld_generator.py (and full markdown pack)
- src/backend/output_generation/html/report_generator.py (and templates)
- src/backend/output_generation/manifest/manifest_builder.py
- src/backend/output_generation/manifest/integrity_hasher.py
- src/backend/output_generation/manifest/provenance_graph_builder.py
- src/backend/output_generation/manifest/manifest_validator.py
- src/backend/output_generation/storage/s3_storage.py
- src/backend/output_generation/storage/gcs_storage.py
- src/backend/output_generation/storage/local_storage.py (from bundle/storage.py)
- src/backend/output_generation/config/di_container.py
- src/backend/output_generation/orchestration/generation_orchestrator.py
- src/backend/output_generation/telemetry/{metrics.py,tracing.py,structured_logging.py,health_check.py}
- Additional tests per Chapter 18 test matrix (see earlier section)

SECTION 8 — Files that MUST remain untouched (FROZEN)
- config/schemas/output_manifest_v1.json (if present) — frozen per Chapter 18 notes.
- config/templates/presentation/v1.2/master_slides.xml (if present)
- Visual baseline images in tests fixtures (do not alter).


Repository Tree Checklist (canonical Chapter 18 directories)

✅ src/backend/output_generation/
✅ src/backend/output_generation/bundle/
✅ src/backend/output_generation/portal/
✅ src/backend/output_generation/visualization/
✅ src/backend/output_generation/presentation/
✅ src/backend/output_generation/quality/
✅ src/backend/output_generation/export/
❌ src/backend/output_generation/markdown/  (missing)
❌ src/backend/output_generation/html/      (missing)
❌ src/backend/output_generation/diagrams/  (renamed `diagram/` present)
❌ src/backend/output_generation/manifest/  (missing)
❌ src/backend/output_generation/storage/   (missing as package)
❌ src/backend/output_generation/orchestration/ (missing)
❌ src/backend/output_generation/telemetry/ (missing)
❌ src/backend/output_generation/score_report/ (missing)
❌ src/backend/output_generation/config/di_container.py (missing)
❌ config/templates/* packs (partial/missing)
❌ tests/ canonical Chapter-18 test suites (many missing)


Migration Impact & Dependency Notes
- Renaming `diagram/` -> `diagrams/` will require updating all imports referencing `output_generation.diagram`. Use a project-wide rename (IDE) and run tests. Risk: Medium.
- Moving `bundle/integrity.py` into `manifest/` requires updating import paths used by `bundle_assembler` and other modules. Risk: Medium.
- Splitting `bundle/storage.py` into multiple storage backends will require updating DI wiring; create `config/di_container.py` early so DI can be used to wire new backends.
- Telemetry reuse: prefer to create `output_generation/telemetry` package that imports existing `src/backend/infrastructure/observability/metrics.py` to avoid duplication. Risk: Low.

Circular Dependencies Risk
- Creating `manifest/` and moving hashing/validation code may introduce cycles between `bundle` and `manifest` packages. Mitigation: keep `manifest` as a pure library (no bundle imports) and expose interfaces consumed by `bundle` only. Validate via static import graph analysis after moves.

Estimated Implementation Order (high-level phases)
1. Create `src/backend/output_generation/config/di_container.py` skeleton (no wiring yet). Run tests — should pass unchanged.
2. Create `src/backend/output_generation/telemetry/` wrapper that imports infra metrics (safe, low-risk). Update imports where needed.
3. Rename `diagram/` -> `diagrams/` (small scoped change). Run tests and fix import failures.
4. Create `manifest/` package and move `bundle/integrity.py` → `manifest/integrity_hasher.py`. Update imports in `bundle_assembler` to import from `manifest`.
5. Split `bundle/storage.py` into `storage/local_storage.py` and `storage/common.py`. Create DI config entries in `di_container.py` to reference local storage.
6. Create `service.py`, `factory.py`, `exceptions.py`, `schemas.py` stubs. Wire minimal DI. Run tests.
7. Create missing generators/templates incrementally: start with minimal markdown/html templates used by tests, then expand.
8. Create `orchestration/` package and wire `OutputGeneratorService` to orchestrator.
9. Implement missing test suites gradually (unit -> integration -> performance -> security -> golden -> visual). Run validation after each group.

Validation Order (per Chapter 18 rules)
- After each migration step run: `pytest -q`, `mypy`, `ruff`, `black --check`. Fix issues before continuing.
- Prioritize bundle-layer tests first (they exist and provide fast feedback). Then manifest tests, then orchestrator and telemetry.

Final Recommendation
- Do not create duplicate implementations. Prefer MOVE/RENAME/REUSE where possible.
- Implement the DI container early to reduce coupling risk and make subsequent moves simpler.
- Execute migration in small, testable commits, running the test/linters after each commit.
- After full migration, run the complete Chapter-18 validation matrix and generate CH18 freeze reports.

If you approve, I will now (only after explicit approval) produce a detailed per-file move/rename plan (concrete source → destination list) and a sequence of git-friendly patches to perform the renames/moves in small steps, running tests after each step.
