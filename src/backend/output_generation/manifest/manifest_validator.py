"""Manifest validator using JSON Schema and structural checks."""

from __future__ import annotations

from typing import List
from pathlib import Path
from .schemas import BundleManifest
import json


def validate_manifest_schema(manifest: BundleManifest, schema_path: Path) -> List[str]:
    errors: List[str] = []
    try:
        from jsonschema import validate, ValidationError  # type: ignore[import-untyped]

        schema = json.loads(schema_path.read_text())
        validate(instance=json.loads(manifest.model_dump_json()), schema=schema)
    except ImportError:
        errors.append("jsonschema not installed; cannot perform JSON Schema validation")
    except ValidationError as e:
        errors.append(f"schema validation error: {e.message}")
    return errors


def validate_manifest_structure(manifest: BundleManifest) -> List[str]:
    errs: List[str] = []
    # composite hash expected non-empty
    if not manifest.composite_hash:
        errs.append("empty_composite_hash")
    # ensure file ids unique
    ids = [f.file_id for f in manifest.files]
    if len(ids) != len(set(ids)):
        errs.append("duplicate_file_id")
    return errs


__all__ = ["validate_manifest_schema", "validate_manifest_structure"]
