"""Manifest builder constructs canonical manifests from generation artifacts."""

from __future__ import annotations

from typing import List
from .schemas import BundleManifest, BundleProvenance, ManifestFileEntry
from .integrity_hasher import compute_composite_hash


def build_manifest(
    bundle_id: str,
    engagement_id: str,
    engagement_version: int,
    bundle_version: int,
    files: List[ManifestFileEntry],
    provenance: BundleProvenance,
) -> BundleManifest:
    table = [{"relative_path": f.relative_path, "content_hash": f.content_hash} for f in files]
    composite = compute_composite_hash(table)
    manifest = BundleManifest(
        bundle_id=bundle_id,
        engagement_id=engagement_id,
        engagement_version=engagement_version,
        bundle_version=bundle_version,
        status="MANIFEST_CREATED",
        generated_at=__import__("datetime").datetime.utcnow(),
        generation_duration_seconds=0.0,
        generator_versions={},
        template_versions={},
        files=files,
        composite_hash=composite,
        provenance=provenance,
        personas=[],
    )
    return manifest


__all__ = ["build_manifest"]
