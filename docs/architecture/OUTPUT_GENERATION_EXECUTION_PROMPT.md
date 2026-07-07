# OUTPUT_GENERATION_EXECUTION_PROMPT.md
# Version: 1.0.0 | Classification: AI Agent Execution Playbook
# Authority: OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_V2.md (all chapters 0–20)
# Status: PRODUCTION — Follow exactly. No deviation permitted.

---

## 1. PURPOSE

This document is the ONLY execution guide an AI coding agent needs to implement
the ArchitectIQ Output Generation Layer. It does NOT contain architecture; it
contains execution workflow. All architecture lives in the Bible (Ch. 0–20).

When this document says "see Bible §X.Y", stop and read that section before
proceeding. Do not guess. Do not improvise. Do not infer from context.

---

## 2. SCOPE

Implement exactly: `src/backend/output_generation/` and its dependencies.
Do not touch any other layer. Do not modify Agent Layer. Do not modify Frontend.

---

## 3. AI AGENT ROLE

You are a senior backend engineer. You implement. You validate. You do not design.
Every architectural question is answered by the Bible. If you cannot find the answer
in the Bible, STOP and escalate (§26). Do not make architectural decisions.

---

## 4. ARCHITECTURE AUTHORITY RULES

| Rule | Authority | Location |
|------|-----------|----------|
| What to build | Bible | Ch. 0–20 |
| How to structure | Bible | Ch. 18 §18.3 |
| What interfaces to implement | Bible | Ch. 18 §18.5 |
| Layer boundaries | Bible | Ch. 2 §2.1, Ch. 18 §18.2 |
| Security constraints | Bible | Ch. 2 §2.5, Ch. 19 §19.8 |
| Performance budgets | Bible | Ch. 6, 8, 14, 16, 19 §19.9 |
| Acceptance criteria | Bible | Ch. 20 (338 criteria) |
| Anti-patterns (what NOT to do) | Bible | All chapters AP-* sections |

**You may not override any rule in the Bible. Ever.**

---

## 5. DOCUMENTS READ ORDER

Read in this exact order before writing a single line of code:

```
1. ARCHITECTURE_VISION.md                        (platform philosophy)
2. SYSTEM_ARCHITECTURE.md                        (system context)
3. BACKEND_MODULE_ARCHITECTURE.md                (module boundaries)
4. AI_AGENT_ARCHITECTURE.md                      (agent contracts)
5. FRONTEND_MODULE_ARCHITECTURE.md               (frontend contracts)
6. OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_V2.md  (YOUR SPECIFICATION)
   → Ch. 0  Document Governance
   → Ch. 1  Vision
   → Ch. 2  Architecture Principles
   → Ch. 3  Philosophy
   → Ch. 4  Personas
   → Ch. 5  UX Specification
   → Ch. 6  Portal Specification
   → Ch. 7  Diagram Engine
   → Ch. 8  Visualization Engine
   → Ch. 9  Architecture Story Engine
   → Ch. 10 AI Walkthrough Engine
   → Ch. 11 Documentation Engine
   → Ch. 12 Export Engine
   → Ch. 13 Presentation Engine
   → Ch. 14 Enterprise Quality Engine
   → Ch. 15 Architecture Score Engine
   → Ch. 16 Premium UI Specification
   → Ch. 17 Download Bundle Specification
   → Ch. 18 Complete Implementation Mapping
   → Ch. 19 Enterprise Testing Constitution
   → Ch. 20 Enterprise Acceptance Criteria (338)
```

Do not skip chapters. Each chapter is a prerequisite for implementation.

---

## 6. MANDATORY READING CHECKLIST

Before touching any file, confirm:

- [ ] Ch. 2 §2.1 — All 7 architecture principles (P-OG2-01..07) understood
- [ ] Ch. 18 §18.2 — Directory ownership matrix read
- [ ] Ch. 18 §18.3 — Complete repository tree memorized for current phase
- [ ] Ch. 18 §18.4 — Files to NEVER modify identified
- [ ] Ch. 18 §18.5 — All 4 interface contracts (ABCs) read
- [ ] Ch. 18 §18.6 — DI container wiring understood
- [ ] Ch. 18 §18.8 — Code generation rules CGR-01..15 memorized
- [ ] Ch. 18 §18.9 — Freeze rules memorized
- [ ] Ch. 19 §19.2 — Testing architecture understood
- [ ] Ch. 20 — Acceptance criteria for the phase being implemented identified

---

## 7. REPOSITORY FREEZE RULES

These files must NEVER be modified. Violation = immediate STOP + escalation.

| Frozen File | Freeze Rule | Consequence of Violation |
|------------|-------------|--------------------------|
| `config/schemas/output_manifest_v1.json` | FR-SCHEMA-01 | Breaks V1 bundle compatibility |
| `config/styles/diagram-tokens.yaml` | FR-TOKEN-01 | Auto-derived; edit tokens.yaml instead |
| `config/templates/presentation/v1.2/master_slides.xml` | FR-TEMPLATE-01 | Breaks all presentations |
| `tests/fixtures/baseline_images/*.png` | FR-BASELINE-01 | Breaks visual regression baseline |
| `tests/fixtures/canonical_snapshot_v2.json` | FR-FIXTURE-01 | Breaks all tests |
| Any ratified `ADR-OG2-*.md` file | FR-ADR-01 | Governance violation |
| Existing method signatures in `interfaces.py` | FR-IFACE-01 | Breaks all implementors |

If you need to change a frozen file: STOP. See §26 Escalation Rules.

---

## 8. IMPLEMENTATION PRINCIPLES

These are non-negotiable. Check every file you write against all 7:

**P-OG2-01 — Intelligence Upstream:** No LLM calls in `output_generation/`. Ever.
**P-OG2-02 — Determinism:** Same snapshot + template → byte-identical output.
**P-OG2-03 — Self-Containment:** Portal HTML zero external URLs.
**P-OG2-04 — Layer Ownership:** No imports from `agents/` or `frontend/`.
**P-OG2-05 — Persona-First:** Content filtered, never forked.
**P-OG2-06 — Provenance:** Every output file carries generation metadata.
**P-OG2-07 — Graceful Failure:** Per-format isolation; failures don't cascade.

Validate each principle after every file you create. Not at the end — after each file.

---

## 9. LAYER OWNERSHIP RULES

```
YOU OWN:        src/backend/output_generation/
YOU CONSUME:    ApprovedSnapshot (read-only input)
YOU CALL:       OutputStorageService (via DI)
YOU NEVER CALL: Any agent class, any LLM client, any frontend module
YOU NEVER WRITE TO: Database directly (use OutputManifestRepository interface)
```

Import boundary enforced by CI (`check_api_imports.py`). If CI blocks your import:
the import is wrong. Remove it. Find the Bible section that defines the correct pattern.

---

## 10. DEPENDENCY RULES

All dependencies flow in one direction. The dependency graph is acyclic:

```
ApprovedSnapshot → OutputGeneratorService → [Generators] → ManifestBuilder
                                                         → BundleAssembler
                                                         → QualityGateOrchestrator
                                                         → OutputStorageService
```

See Bible Ch. 18 §18.3 for the complete dependency tree.
**Rule:** If your new file imports something that imports your file = circular. Stop.
Run `python -c "from src.backend.output_generation import {your_module}"` to verify.

---

## 11. CODING STANDARDS

Apply before saving every file. No exceptions.

| Standard | Rule | Enforcement |
|----------|------|-------------|
| CGR-01 | Module docstring on every file | pydocstyle |
| CGR-02 | Class docstring on every class | pydocstyle |
| CGR-03 | Method docstring on every public method | pydocstyle |
| CGR-04 | All async methods use `async def` — no sync blocking I/O | pylint |
| CGR-05 | Pydantic v2: `model_validate_json()` not `parse_raw()` | manual |
| CGR-06 | Typed errors: `raise OutputGenerationError(...)` — not bare `Exception` | ruff |
| CGR-07 | All config values from `OutputSettings` — never hardcoded | grep |
| CGR-08 | Logging: `logger.info(msg, key=value)` — not f-strings in log calls | ruff |
| CGR-09 | Import order: stdlib → third-party → internal | isort |
| CGR-10 | Type hints on ALL signatures including return type | mypy |
| CGR-11 | Zero `print()` calls | grep |
| CGR-12 | Zero global mutable state | manual |
| CGR-13 | `subprocess.run()` always has explicit timeout | ruff |
| CGR-14 | All file paths validated before use | manual |
| CGR-15 | All secrets from environment variables only | truffleHog |

Run after every file: `ruff check {file} && mypy {file} --strict && black {file}`

---

## 12. REPOSITORY NAVIGATION RULES

**Before creating any file:**
1. Open Bible Ch. 18 §18.3 (Complete Repository Tree)
2. Find the exact path for your file in that tree
3. If the path is not in §18.3, STOP — the file may not be needed
4. If the path IS in §18.3, create it at that exact path

**Before modifying any file:**
1. Check §7 (Freeze Rules) — is this file frozen?
2. Check Bible Ch. 18 §18.4 — is this file in "never modify" list?
3. If yes to either: STOP. See §26 Escalation.

---

## 13. IMPLEMENTATION ORDER

Follow the phase sequence exactly. Do not reorder phases. Do not parallelize phases.

| Phase | Name | Bible Reference |
|-------|------|----------------|
| 0 | Read all authoritative documents | §5 Documents Read Order |
| 1 | Freeze architecture understanding | §6 Mandatory Reading Checklist |
| 2 | Repository analysis | Ch. 18 §18.3 |
| 3 | Implementation planning | Ch. 18 §18.7 |
| 4 | Implementation | Ch. 18 §18.7 Phase 1–7 |
| 5 | Technical validation | Ch. 19, Ch. 20 |
| 6 | Business validation | Ch. 20 AC-HACK-*, AC-GOV-* |
| 7 | Fix loop | §19 Fix Loop |
| 8 | Freeze implementation | Ch. 18 §18.9 |
| 9 | Final audit | §29 Output Validation Checklist |
| 10 | Ready for next layer | §30 Final Implementation Checklist |

---

## 14. FILE CREATION RULES

Before creating a file:
1. Confirm the path is in Bible Ch. 18 §18.3
2. Confirm the class/function name matches the checklist in Ch. 18 §18.4
3. Write the module docstring first (CGR-01)
4. Implement the ABC or interface contract exactly (Ch. 18 §18.5)
5. Run: `ruff check && mypy --strict && black`
6. Write the test file immediately (same session, same phase)

**File creation sequence for every module:**
```
1. Create implementation file
2. Run linters (must pass before continuing)
3. Create unit test file in tests/unit/test_{module}.py
4. Run unit tests (must pass before continuing)
5. Create golden/snapshot test if applicable
6. Commit both files together
```

Never create an implementation file without its test file.

---

## 15. FILE MODIFICATION RULES

Before modifying an existing file:
1. Run full test suite for that module: `pytest tests/unit/test_{module}.py -v`
2. Record the passing count
3. Make the modification
4. Re-run the same suite — passing count must not decrease
5. If passing count decreases: revert and debug before proceeding

When modifying `factory.py` or `service.py` (high-impact files):
- Run integration tests: `pytest tests/integration/ -v`
- Passing count must not decrease before committing

---

## 16. BUILD SEQUENCE

Execute in this exact order for each implementation phase:

```bash
# Step 1: Lint
ruff check src/backend/output_generation/{module}/

# Step 2: Type check
mypy src/backend/output_generation/{module}/ --strict

# Step 3: Format
black src/backend/output_generation/{module}/

# Step 4: Security scan
bandit -r src/backend/output_generation/{module}/ -ll

# Step 5: Import boundary check
python .tools/check_api_imports.py src/backend/output_generation/{module}/

# Step 6: Unit tests
pytest tests/unit/test_{module}.py -v --cov=src/backend/output_generation/{module}/

# Step 7: Coverage check
pytest tests/unit/test_{module}.py --cov={module} --cov-fail-under=80

# Step 8: Integration (after cross-module work)
pytest tests/integration/ -v

# Step 9: Snapshot tests (after any generator change)
pytest tests/snapshots/ -v
```

All 9 steps must pass before marking a phase complete.

---

## 17. VALIDATION SEQUENCE

After all implementation phases are complete, run the full validation suite:

```
Level 0:  ruff + mypy + black (must be zero violations)
Level 1:  pytest tests/unit/ (≥ 80% coverage)
Level 2:  pytest tests/snapshots/ (byte-identical determinism)
Level 3:  pytest tests/golden/ (reference output verification)
Level 4:  pytest tests/integration/ (cross-module)
Level 5:  pytest tests/security/ (XSS, secrets, CSP, path traversal)
Level 6:  pytest tests/accessibility/ (WCAG AA)
Level 7:  pytest tests/performance/ (all budgets: §19.9)
Level 8:  pytest tests/visual_regression/ (≤ 1% pixel diff)
Level 9:  pytest tests/e2e/ (full pipeline)
Level 10: pytest tests/cross_platform/ (PPTX, PDF)
Level 11: pytest tests/offline/ (portal with network disabled)
Level 12: pytest tests/cross_platform/test_browser_compat.py (Chromium, Firefox, WebKit)
```

Failure at any level blocks completion. Fix before proceeding to next level.

---

## 18. TESTING SEQUENCE

For each new module, create tests in this order:

**Mandatory (every module):**
- `tests/unit/test_{module}.py` — unit tests, mocked deps, ≥ 80% coverage
- `tests/snapshots/test_snapshot_{module}.py` — determinism test (generators only)

**Required (as applicable):**
- `tests/golden/test_golden_{module}.py` — reference output (generators)
- `tests/integration/test_{module}_integration.py` — cross-module (if cross-module)
- `tests/security/test_security_{module}.py` — security (HTML sanitizer, portal, bundle)
- `tests/performance/test_performance_{module}.py` — performance (service, diagrams, portal)
- `tests/offline/test_portal_offline.py` — offline (portal only)

Test naming: `test_{module}_{function}_{scenario}` (Bible §19.13)
Mock strategy: Bible §19.20 — mock only external dependencies
Fixture strategy: Bible §19.21 — all fixtures from `tests/fixtures/`

---

## 19. FIX LOOP

When a test fails:

```
Step 1: Read the failure message completely
Step 2: Identify the Bible chapter governing that behavior
Step 3: Re-read that chapter section
Step 4: Fix the implementation to match the Bible specification
Step 5: Re-run the failing test — must pass
Step 6: Re-run the entire test suite for that module — must not regress
Step 7: If still failing after 3 attempts: STOP → §26 Escalation
```

**Do NOT:**
- Modify tests to make them pass (unless the test is wrong — see §26)
- Comment out failing assertions
- Lower coverage thresholds
- Add `# noqa` without a specific documented justification

---

## 20. REVIEW LOOP

After every complete phase (Bible Ch. 18 §18.7):

```
1. Run full validation sequence (§17)
2. Verify all acceptance criteria for the phase (Bible Ch. 20)
3. Verify no anti-patterns introduced (Bible all AP-* sections)
4. Verify all 7 principles satisfied (§8)
5. Verify no freeze rules violated (§7)
6. Verify dependency graph still acyclic (§10)
7. Commit only when all 6 checks pass
```

---

## 21. FREEZE WORKFLOW

When a phase is complete and validated:

```
1. Run: python .tools/check_api_imports.py (must pass)
2. Run: python .tools/token_build.py --verify-only (if tokens changed)
3. Run full CI pipeline locally (§19.18)
4. Tag the commit: git tag phase/{N}-complete
5. Update implementation_status.md: phase N → COMPLETE
6. Do NOT modify phase N files after tagging
```

If you need to modify a completed-phase file: treat it as a freeze violation.
Unfreeze only by explicit approval from the Implementation Lead.

---

## 22. PRODUCTION QUALITY GATES

All must pass before the implementation is considered production-ready:

| Gate | Requirement | Bible Reference | Verification |
|------|-------------|----------------|-------------|
| QG-01 | Zero ruff violations | CGR-01..15 | CI: ruff |
| QG-02 | Zero mypy errors (--strict) | §11 | CI: mypy |
| QG-03 | Coverage ≥ 80% overall | Bible §19.19 | CI: pytest-cov |
| QG-04 | Coverage ≥ 95% critical paths (manifest, bundle, quality) | Bible §19.19 | CI: pytest-cov |
| QG-05 | All 22 diagram types render | Bible Ch. 7, AC-DIAG-01 | pytest tests/integration/ |
| QG-06 | Portal renders offline (network disabled) | AC-PORTAL-01 | pytest tests/offline/ |
| QG-07 | Portal TTI < 2s | AC-PERF-02 | pytest tests/performance/ |
| QG-08 | Full generation < 120s | AC-PERF-01 | pytest tests/performance/ |
| QG-09 | Zero XSS payloads escape sanitizer | AC-SEC-04 | pytest tests/security/ |
| QG-10 | Zero secrets in bundle | AC-SEC-01 | SecurityValidator + CI |
| QG-11 | WCAG 2.1 AA passes (axe-core) | AC-A11Y-01 | pytest tests/accessibility/ |
| QG-12 | Manifest v2 schema valid | AC-BUNDLE-01 | pytest tests/unit/ |
| QG-13 | Bundle integrity verified | AC-BUNDLE-03..06 | pytest tests/integration/ |
| QG-14 | All snapshots deterministic | AC-ARCH-07 | pytest tests/snapshots/ |
| QG-15 | Bandit: zero HIGH/CRITICAL findings | §22 | CI: bandit |
| QG-16 | Trivy: zero CRITICAL CVEs | AC-REPO-10 | CI: trivy |
| QG-17 | PPTX opens in PowerPoint + Google Slides + LibreOffice | AC-PRES-01 | pytest tests/cross_platform/ |
| QG-18 | No import from agents/ or frontend/ in output_generation/ | AC-ARCH-03 | CI: import-check |

---

## 23. CI GATES

CI pipeline defined in: Bible Ch. 19 §19.18 (`.github/workflows/output-generation.yml`)

CI blocks merge when any of the following fail:
- static-analysis job (ruff, mypy, black, import-check, token-build-verify)
- unit-tests job (including coverage threshold)
- snapshot-tests job
- golden-tests job
- integration-tests job
- security-tests job (bandit + test suite)
- accessibility-tests job
- performance-tests job
- visual-regression job
- e2e-tests job
- cross-platform job
- offline-tests job
- dependency-scan job (Trivy)

**Never push code that fails CI.** Run the full suite locally first.

---

## 24. DEFINITION OF DONE

A module is DONE when ALL of the following are true:

- [ ] Implementation file exists at path specified in Bible Ch. 18 §18.3
- [ ] File passes ruff, mypy --strict, black
- [ ] File has module docstring, class docstrings, method docstrings
- [ ] File has zero print() calls, zero hardcoded values
- [ ] Test file exists at `tests/unit/test_{module}.py`
- [ ] Test coverage ≥ 80% for this module
- [ ] Snapshot test exists and passes (generators only)
- [ ] Golden test exists and passes (if applicable)
- [ ] All applicable AC-* criteria from Bible Ch. 20 pass
- [ ] No applicable AP-* anti-patterns present
- [ ] All 7 principles (§8) satisfied
- [ ] No freeze rules (§7) violated
- [ ] Dependency graph still acyclic
- [ ] CI pipeline green

A phase is DONE when all its modules satisfy the above AND:
- [ ] Integration tests for the phase pass
- [ ] Phase tag committed: `git tag phase/{N}-complete`

---

## 25. STOP CONDITIONS

Immediately STOP all implementation activity when:

| Condition | Action |
|-----------|--------|
| You need to make an architectural decision | STOP → read Bible → if not found → §26 Escalation |
| A frozen file needs modification | STOP → §26 Escalation |
| A test has failed 3 times with different fixes | STOP → §26 Escalation |
| An import boundary violation is found | STOP → remove import → find correct pattern in Bible |
| A security test fails (XSS, secrets, path traversal) | STOP → fix immediately → no workarounds |
| Coverage drops below 80% on any module | STOP → write tests → do not lower threshold |
| A circular dependency is introduced | STOP → revert → restructure |
| CI pipeline is broken for > 30 minutes | STOP → §26 Escalation |
| You are unsure which Bible section governs behavior | STOP → read Bible → find the section |
| Any BLOCKER-severity acceptance criterion fails | STOP → fix → re-validate |

---

## 26. ESCALATION RULES

Escalate to the Implementation Lead when:
- An architectural decision is needed not covered by the Bible
- A frozen file must be modified (requires ADR amendment)
- A test fails after 3 fix attempts
- A CI gate cannot be satisfied without changing a frozen contract
- A performance budget cannot be met with current approach
- A Bible section contradicts another Bible section

**Escalation format:**
```
ESCALATION REQUEST
Phase: {N}
File: {path}
Issue: {exact description}
Bible sections consulted: {list}
Attempts made: {list of approaches tried}
Blocker: {what cannot proceed without resolution}
```

Do not guess. Do not work around. Do not skip. Escalate.

---

## 27. FORBIDDEN ACTIONS

These actions are absolutely prohibited. No exception, no justification.

```
❌ Calling any LLM API from within output_generation/
❌ Importing from src/backend/agents/ in output_generation/
❌ Importing from src/frontend/ in output_generation/
❌ Hardcoding hex colors, spacing, font sizes
❌ Hardcoding API keys, credentials, secrets
❌ Modifying any frozen file (§7)
❌ Lowering test coverage thresholds
❌ Commenting out failing assertions
❌ Adding # noqa without documented justification
❌ Using print() instead of logger
❌ Using global mutable state
❌ Making architectural decisions not in the Bible
❌ Fetching any external URL from portal HTML
❌ Using localStorage in portal
❌ Calling eval() in JavaScript
❌ Using CDN for Mermaid, fonts, or icons in portal
❌ Editing diagram-tokens.yaml directly (auto-derived)
❌ Making synchronous blocking I/O calls in async context
❌ Path traversal unvalidated input
❌ Accepting user input without validation
❌ Skipping a phase in the implementation order
❌ Committing untested code
❌ Ignoring a CI gate failure
```

---

## 28. AI DECISION RULES

When you face a decision, use this decision tree:

```
Is the answer in the Bible?
  YES → Follow the Bible exactly. No deviation.
  NO  → Is it a coding standard question?
    YES → Apply CGR-01..15 (§11)
    NO  → Is it an architecture question?
      YES → STOP. Read Bible Ch. 0–4 (principles). If still not found → §26.
      NO  → Is it a testing question?
        YES → Read Bible Ch. 19. Apply exactly.
        NO  → Is it a validation question?
          YES → Read Bible Ch. 20. Apply criteria.
          NO  → STOP. Escalate. Never guess.
```

**The Bible is the authority. You are the implementor. Do not swap roles.**

---

## 29. OUTPUT VALIDATION CHECKLIST

Run before marking any phase complete:

**Architecture Validation**
- [ ] P-OG2-01: No LLM calls in output_generation/
- [ ] P-OG2-02: Snapshot determinism test passes
- [ ] P-OG2-03: Portal offline test passes (network disabled)
- [ ] P-OG2-04: Import boundary check clean
- [ ] P-OG2-05: Persona filter tests pass
- [ ] P-OG2-06: Provenance fields present in all manifest entries
- [ ] P-OG2-07: Graceful failure test passes (optional generator failure = WARN only)

**Security Validation**
- [ ] XSS test suite (30+ payloads): all sanitized
- [ ] Secrets detection test: zero secrets in bundle
- [ ] CSP meta tag validation: present and correct
- [ ] Path traversal test: all rejected
- [ ] bandit -ll: zero HIGH/CRITICAL

**Performance Validation**
- [ ] Generation time: < 120s (canonical fixture)
- [ ] Portal TTI: < 2s (5MB bundle)
- [ ] Diagram render: < 10s per diagram
- [ ] Bundle size: ≤ 50MB uncompressed

**Quality Gate Validation**
- [ ] All 8 validators run in parallel
- [ ] Citation coverage: 100%
- [ ] BLOCKER verdict halts bundle persistence
- [ ] Quality report JSON validates against schema

**Bundle Validation**
- [ ] Manifest v2 JSON schema valid
- [ ] All BR-01..15 bundle rules pass (Bible §17.9)
- [ ] SHA-256 composite hash verified
- [ ] All persona bundles filter correctly

**Testing Validation**
- [ ] Coverage ≥ 80% overall
- [ ] Coverage ≥ 95% critical paths
- [ ] All snapshot tests pass
- [ ] All golden tests pass
- [ ] All security tests pass
- [ ] All accessibility tests pass (WCAG AA)

---

## 30. FINAL IMPLEMENTATION CHECKLIST

The implementation of the Output Generation Layer is complete when:

**Repository**
- [ ] All 70+ files in Bible Ch. 18 §18.3 created at exact paths
- [ ] Zero files modified outside `output_generation/`, `config/`, `tests/`
- [ ] All frozen files (§7) unchanged
- [ ] CODEOWNERS updated with correct team assignments

**Code Quality**
- [ ] ruff: zero violations
- [ ] mypy --strict: zero errors
- [ ] black: all files formatted
- [ ] bandit -ll: zero HIGH/CRITICAL
- [ ] Trivy: zero CRITICAL CVEs
- [ ] Zero print() calls
- [ ] Zero hardcoded values
- [ ] Zero global state

**Testing**
- [ ] All 14 test types implemented (Bible §19.2)
- [ ] Coverage ≥ 80% overall, ≥ 85% per module, ≥ 95% critical
- [ ] All snapshot tests pass (determinism verified)
- [ ] All golden tests pass
- [ ] All integration tests pass
- [ ] All security tests pass (30+ XSS payloads, secrets, CSP, path traversal)
- [ ] All accessibility tests pass (WCAG 2.1 AA)
- [ ] All performance tests pass (all budgets in Bible Ch. 19 §19.9)
- [ ] All visual regression tests pass (≤ 1% pixel variance)
- [ ] All E2E tests pass
- [ ] All cross-platform tests pass (Chromium, Firefox, WebKit)
- [ ] All offline tests pass (portal renders with network disabled)

**Validation**
- [ ] All 18 production quality gates pass (§22)
- [ ] All applicable AC-* criteria from Bible Ch. 20 pass
- [ ] No AP-* anti-patterns present in codebase
- [ ] All 7 P-OG2-* principles verified by tests
- [ ] CI pipeline fully green

**Delivery**
- [ ] All phase tags committed: `git tag phase/{0..7}-complete`
- [ ] `implementation_status.md` fully updated
- [ ] All 10 execution phases (§13) completed
- [ ] Output Generation Layer ready for next layer integration

---

## PHASE SPECIFICATIONS

### PHASE 0 — READ AUTHORITATIVE DOCUMENTS

**Objective:** Internalize all architecture, contracts, and constraints before coding.
**Inputs:** All documents listed in §5
**Outputs:** Completed §6 Mandatory Reading Checklist
**Files Allowed:** Read-only
**Files Forbidden:** No file creation in this phase
**Validation:** All 10 items in §6 checklist checked
**Completion Criteria:** Every checklist item checked; principles §8 memorized
**Failure Criteria:** Any checklist item skipped
**Rollback:** Re-read skipped sections; do not advance

---

### PHASE 1 — FREEZE ARCHITECTURE UNDERSTANDING

**Objective:** Confirm architecture is understood; identify all phase constraints.
**Inputs:** Completed Phase 0
**Outputs:** `implementation_plan.md` (not in src/ — working document only)
**Required Documents:** Bible Ch. 18 §18.7 (Phase-wise Roadmap)
**Files Allowed:** Working documents only
**Files Forbidden:** No src/ files in this phase
**Validation:** Implementation plan reviewed against Bible Ch. 18 §18.7
**Completion Criteria:** All 7 implementation phases mapped; dependencies identified
**Failure Criteria:** Any phase missing from plan; any dependency unknown
**Rollback:** Re-read Bible Ch. 18 §18.7; update plan

---

### PHASE 2 — REPOSITORY ANALYSIS

**Objective:** Map existing codebase; identify what exists vs. what must be created.
**Inputs:** Repository access, Bible Ch. 18 §18.3
**Outputs:** Gap analysis against Bible §18.3 tree
**Required Documents:** Bible Ch. 18 §18.3 (complete tree), §18.4 (freeze list)
**Files Allowed:** Read-only scan
**Files Forbidden:** No modifications
**Validation:** Every file in §18.3 is either existing or in creation queue
**Completion Criteria:** Full gap analysis complete; zero unknown files in src/backend/output_generation/
**Failure Criteria:** Files present that are not in §18.3 (unauthorized files)
**Rollback:** Document unauthorized files; escalate to §26

---

### PHASE 3 — IMPLEMENTATION PLANNING

**Objective:** Sequence all file creation; assign to Bible phases 1–7.
**Inputs:** Gap analysis from Phase 2, Bible Ch. 18 §18.7
**Outputs:** Ordered file creation list per Bible phase
**Required Documents:** Bible Ch. 18 §18.7 (all 7 phases and gate conditions)
**Files Allowed:** Working documents
**Files Forbidden:** No src/ files
**Validation:** Every file assigned to exactly one Bible phase
**Completion Criteria:** Creation order matches §18.7 exactly
**Failure Criteria:** Phase ordering violated; files assigned to wrong phase
**Rollback:** Re-sequence against §18.7

---

### PHASE 4 — IMPLEMENTATION (Bible Phases 1–7)

**Objective:** Create all files per Bible Ch. 18 §18.7 phases, in order.
**Inputs:** Gap analysis, implementation plan, Bible Ch. 0–20
**Outputs:** All 70+ implementation files + all test files
**Required Documents:** Bible chapter for the component being implemented
**Files Allowed:** Files in `src/backend/output_generation/` and `tests/`
**Files Forbidden:** Frozen files (§7); files outside `output_generation/`, `config/`, `tests/`
**Validation:** Build sequence §16 passes after every file
**Completion Criteria:** All 7 Bible phases complete; all phase gates passed
**Failure Criteria:** Any phase gate fails; any frozen file modified
**Rollback:** Revert to last passing phase tag; re-implement from that point

---

### PHASE 5 — TECHNICAL VALIDATION

**Objective:** Run full validation suite; verify all quality gates.
**Inputs:** Complete Phase 4 implementation
**Outputs:** Validation report; all gates green
**Required Documents:** Bible Ch. 19, Ch. 20
**Files Allowed:** Test files, configuration files
**Files Forbidden:** Implementation files (no changes in this phase)
**Validation:** All 12 levels in §17 must pass
**Completion Criteria:** All 18 production quality gates (§22) green
**Failure Criteria:** Any gate fails
**Rollback:** Return to Phase 4 fix loop (§19); fix and re-validate

---

### PHASE 6 — BUSINESS VALIDATION

**Objective:** Verify all 338 acceptance criteria from Bible Ch. 20.
**Inputs:** Validated Phase 5 implementation
**Outputs:** Acceptance criteria report
**Required Documents:** Bible Ch. 20 (all 20 AC categories)
**Files Allowed:** Test additions only
**Files Forbidden:** Implementation changes (any finding → Phase 7 fix loop)
**Validation:** All AC-* criteria verified; none marked FAIL
**Completion Criteria:** All CRITICAL and HIGH criteria pass; all MEDIUM criteria pass
**Failure Criteria:** Any CRITICAL AC fails; any HIGH AC fails
**Rollback:** Return to Phase 7 (Fix Loop)

---

### PHASE 7 — FIX LOOP

**Objective:** Resolve all failures from Phases 5–6.
**Inputs:** Failure list from Phase 5 or 6
**Outputs:** Fixed implementation; all tests passing
**Files Allowed:** Any non-frozen file
**Files Forbidden:** Frozen files (§7)
**Validation:** Re-run §17 from Level 0; all levels must pass
**Completion Criteria:** Zero failing tests; all gates green
**Failure Criteria:** Same fix required > 3 times → §26 Escalation
**Rollback:** Revert fix; escalate; do not apply workaround

---

### PHASE 8 — FREEZE IMPLEMENTATION

**Objective:** Tag the implementation as complete; enforce immutability.
**Inputs:** All phases 0–7 complete
**Outputs:** Phase tags; updated implementation_status.md
**Files Allowed:** implementation_status.md, git tags
**Files Forbidden:** All src/ implementation files (frozen after this phase)
**Validation:** All phase tags created; CI green on tagged commit
**Completion Criteria:** `phase/7-complete` tag on green commit
**Failure Criteria:** Any CI failure on tagged commit
**Rollback:** Delete tag; return to Phase 7

---

### PHASE 9 — FINAL AUDIT

**Objective:** Verify §29 Output Validation Checklist and §30 Final Implementation Checklist.
**Inputs:** Frozen Phase 8 implementation
**Outputs:** Signed-off checklists
**Files Allowed:** Documentation only
**Files Forbidden:** All src/ files
**Validation:** Every item in §29 and §30 checked
**Completion Criteria:** Both checklists 100% complete
**Failure Criteria:** Any unchecked item in either checklist
**Rollback:** Unfreeze (Phase 8 reversal); fix; re-freeze

---

### PHASE 10 — READY FOR NEXT LAYER

**Objective:** Hand off Output Generation Layer to next layer integration.
**Inputs:** Signed-off checklists from Phase 9
**Outputs:** Integration readiness declaration
**Validation:** Integration team confirms they can consume OutputGeneratorService API
**Completion Criteria:** Integration team accepts handoff
**Failure Criteria:** Integration team identifies missing contract
**Rollback:** Return to Phase 4; implement missing contract per Bible

---

*End of OUTPUT_GENERATION_EXECUTION_PROMPT.md*
*Version: 1.0.0 | Authority: OUTPUT_GENERATION_IMPLEMENTATION_BIBLE_V2.md*
*Total lines: see file | Maximum: 1000 lines*
