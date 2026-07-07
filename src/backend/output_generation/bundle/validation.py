from __future__ import annotations

import json
from typing import List, Dict, Any
from pathlib import Path

from ..bundle.schemas import BundleManifest
from ..manifest.integrity_hasher import compute_composite_hash, compute_content_hash


def validate_manifest_schema(manifest_dict: Dict[str, Any], schema_path: Path) -> List[str]:
    errors: List[str] = []
    try:
        from jsonschema import validate, ValidationError  # type: ignore[import-untyped]

        schema = json.loads(schema_path.read_text())
        validate(instance=manifest_dict, schema=schema)
    except ImportError:
        errors.append("jsonschema not installed; cannot perform JSON Schema validation")
    except ValidationError as e:
        errors.append(f"schema validation error: {e.message}")
    return errors


def validate_provenance(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    p = manifest.provenance
    required = ["approved_by", "approved_at", "approval_ledger_hash", "snapshot_version", "trace_id"]
    for r in required:
        if not getattr(p, r, None):
            errs.append(f"missing provenance field: {r}")
    return errs


def validate_composite(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    table = [{"relative_path": e.relative_path, "content_hash": e.content_hash} for e in manifest.files]
    computed = compute_composite_hash(table)
    if computed != manifest.composite_hash:
        errs.append("composite_hash_mismatch")
    return errs


def validate_files_exist_and_hashes(bundle_root: Path, manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    file_ids = set()
    for e in manifest.files:
        file_ids.add(e.file_id)
        p = bundle_root / e.relative_path
        if not p.exists():
            errs.append(f"missing_artifact:{e.relative_path}")
            continue
        actual = compute_content_hash(p.read_bytes())
        if actual != e.content_hash:
            errs.append(f"hash_mismatch:{e.relative_path}")
    # relationships
    ids = {e.file_id for e in manifest.files}
    for e in manifest.files:
        for rel in e.relationships:
            if rel.target_file_id not in ids:
                errs.append(f"invalid_reference:{e.file_id}->{rel.target_file_id}")
    # duplicates
    rel_paths = [e.relative_path for e in manifest.files]
    dupes = set(x for x in rel_paths if rel_paths.count(x) > 1)
    for d in dupes:
        errs.append(f"duplicate_artifact:{d}")

    return errs


def validate_manifest_version(manifest: BundleManifest, expected: str = "2.0.0") -> List[str]:
    errs: List[str] = []
    if getattr(manifest, "manifest_version", None) != expected:
        errs.append(f"manifest_version_mismatch: expected {expected}")
    return errs


def validate_naming_conventions(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    import re

    # simple bundle_id naming rule: alnum, dash, underscore
    if not re.match(r"^[A-Za-z0-9_\-]+$", manifest.bundle_id):
        errs.append("invalid_bundle_id_name")
    return errs


def validate_bundle_state(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    # disallow ERROR states for finalization
    blocked = {"BUNDLE_BLOCKED", "GENERATION_FAILED"}
    if getattr(manifest, "status", None) in blocked:
        errs.append(f"invalid_bundle_state:{manifest.status}")
    return errs


def validate_persona_authorization(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    # For each persona declared, ensure at least one file is visible to it
    personas = getattr(manifest, "personas", []) or []
    for persona in personas:
        visible = [f for f in manifest.files if (not f.persona_scope) or (persona in f.persona_scope)]
        if not visible:
            errs.append(f"persona_has_no_visible_files:{persona}")
    return errs


def validate_archive(bundle_root: Path, manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    # ensure archive exists and contains manifest.json
    import zipfile

    archive_path = bundle_root.with_suffix('.zip')
    if not archive_path.exists():
        errs.append("archive_missing")
        return errs
    try:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            namelist = zf.namelist()
            if 'manifest.json' not in namelist:
                errs.append('archive_missing_manifest')
    except Exception as e:
        errs.append(f'archive_error:{e}')
    return errs


def run_all_validations(bundle_root: Path, manifest: BundleManifest, schema_path: Path) -> List[str]:
    errs: List[str] = []
    # manifest schema
    try:
        m_dict = json.loads(manifest.model_dump_json()) if hasattr(manifest, "model_dump_json") else json.loads(manifest.json())
    except Exception:
        m_dict = json.loads(manifest.json())

    errs += validate_manifest_schema(m_dict, schema_path)
    errs += validate_manifest_version(manifest)
    errs += validate_provenance(manifest)
    errs += validate_composite(manifest)
    errs += validate_files_exist_and_hashes(bundle_root, manifest)
    errs += validate_persona_authorization(manifest)
    errs += validate_naming_conventions(manifest)
    errs += validate_bundle_state(manifest)
    errs += validate_archive(bundle_root, manifest)
    return errs
