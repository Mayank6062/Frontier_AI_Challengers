# Repository Bootstrap

## Purpose

Define the exact, minimal implementation plan to create the repository skeleton exactly as frozen by the authoritative architecture documents. This document prescribes only folder and minimal-file creation; it does not change, extend, or implement any architecture, code, or ownership rules.

## Repository Creation Principles

- Follow the frozen architecture without deviation. 
- Create only folders and mandatory skeleton files. 
- Do not add code, placeholder logic, prompts, or implementation artifacts. 
- Do not rename, move, simplify, optimize, or otherwise alter any folder or ownership rule. 
- All changes are structural skeletons only; functional work begins in the implementation phase.

## Repository Source of Truth

The single authoritative source for repository structure is:

- `REPOSITORY_MASTER_STRUCTURE.md` (important/architecture/REPOSITORY_MASTER_STRUCTURE.md)

All folder names, locations, and ownerships are taken verbatim from that document. Do not consult any other source to alter structure.

## Bootstrap Rules

- Never invent folders, files, package names, or ownership entries not present in the source-of-truth. 
- Never rename, move, or merge any folder specified in the source-of-truth. 
- Never create implementation code, example code, TODOs, or placeholder logic. 
- Only create the minimal files listed in this document. 
- Preserve CI/ADR/ownership artifacts as declared in the source-of-truth; do not modify them.

## Folder Creation Strategy

- Create folders exactly as defined in `REPOSITORY_MASTER_STRUCTURE.md`. 
- For each folder create only mandatory skeleton files (see "Initial Files"). 
- Do not implement business logic, agent implementations, prompts, or configuration values. 
- Use `.gitkeep` for empty runtime or placeholder directories where a file is required to preserve the path. 
- Ensure each module directory has a `README.md` (text only) describing the module responsibility per the frozen documents; the content may be a single sentence referencing the authoritative document.

## Creation Order

Create folders in an order that respects dependency direction (outward → inward foundations):

1. Top-level infrastructure (config/, docs/, deploy/, .github/, scripts/, outputs/, plugins/, tests/) and tooling containers required to host the repository. 
2. `src/frontend/` skeleton (presentation layer) and frontend shell folders. 
3. `src/backend/api/` (API layer) skeleton. 
4. `src/backend/core/` including `interfaces/` (domain core and contract definitions). 
5. `src/backend/shared/` (shared utilities and base models). 
6. `src/backend/infrastructure/` skeleton (implementations placeholders). 
7. `src/backend/orchestration/` and workflow engine skeleton. 
8. `src/backend/agents/` base and category folders (agent implementation directories may remain empty). 
9. `src/backend/knowledge/` and `src/backend/outputs/` skeletons. 
10. `deploy/`, `tests/` and environment-specific configuration folders. 

This creation order is a mechanical sequence only; no file in a created folder shall contain implementation code.

## Initial Files

Only the following minimal files are permitted in newly created folders during bootstrap:

- `README.md` — one-line responsibility statement referencing the authoritative document.
- `__init__.py` — only for Python package folders where the real package will later exist.
- `.gitkeep` — to preserve otherwise-empty directories in version control where required.

No additional files are allowed during bootstrap. Do not create code files, configuration values, prompt templates, or build artifacts.

## Empty Modules Allowed

During bootstrap the following folders may remain intentionally empty (contain only `.gitkeep` and `README.md`):

- `outputs/` (runtime-generated content)
- `plugins/` (phase-2 placeholder)
- `src/backend/agents/{category}/{agent-name}/` (individual agent implementation directories)
- Any `tests/` subfolders reserved for golden fixtures or future artifacts

Folders not explicitly listed in the source-of-truth must not be created.

## Folder Validation Checklist

- Folder exists at the exact path declared in `REPOSITORY_MASTER_STRUCTURE.md`.
- Folder contains exactly one `README.md` with responsibility text (no implementation notes).
- Python package folders contain `__init__.py` and no other Python code.
- Intended-empty folders contain `.gitkeep` (and `README.md`) only.
- No source code files, prompt files, templates, or configuration values have been added.
- No changes to ownership, ADRs, or CI configuration were made during bootstrap.

## Bootstrap Completion Checklist

- All top-level folders from `REPOSITORY_MASTER_STRUCTURE.md` created. 
- All `src/` layer folders created in the prescribed creation order. 
- Every created folder contains only the permitted initial files. 
- All allowed-empty folders contain `.gitkeep` and `README.md`. 
- A single commit/PR contains only skeleton additions and points reviewers to the frozen authoritative documents. 

## Definition of Done

- A pull request (or commit) is accepted when it contains only the folder skeletons and permitted initial files as defined in this document and passes a structural review confirming: no implementation, no placeholders, exact path fidelity to `REPOSITORY_MASTER_STRUCTURE.md`, and `README.md` presence for each module. 
- After merge, the repository structure matches `REPOSITORY_MASTER_STRUCTURE.md` verbatim and is ready for implementation work under the frozen architecture and CI gates.

End of Repository Bootstrap
