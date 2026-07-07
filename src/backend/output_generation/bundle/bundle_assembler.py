from __future__ import annotations

import json
from pathlib import Path
from typing import List
import shutil
from datetime import datetime

from .schemas import (
    BundleManifest,
    BundleAssemblyResult,
    BundleAssemblyRequest,
    BundleProvenance,
    BundleStatus,
)
from ..manifest.integrity_hasher import compute_content_hash, compute_composite_hash
from .archive_builder import ArchiveBuilder
from .storage import OutputStorageService, FilesystemOutputStorage
from .persona_filter import PersonaFilter
from .validation import run_all_validations


class IntegrityVerificationResult:
    def __init__(self, success: bool, mismatches: List[str] | None = None):
        self.success = success
        self.mismatches = mismatches or []


class BundleAssembler:
    """Orchestrates full bundle assembly per Chapter 17.

    Responsibilities:
      1. Create folder hierarchy
      2. Write artifact files
      3. Apply persona filtering (via PersonaFilter externally)
      4. Create archive
      5. Write to OutputStorageService
    """

    def __init__(self, storage: OutputStorageService | None = None):
        self.storage = storage or FilesystemOutputStorage(".output_storage")
        self.persona_filter = PersonaFilter()
        self.schema_path = Path("config/schemas/output_manifest_v2.json")

    async def assemble(self, generation_results: list, manifest: BundleManifest, request: BundleAssemblyRequest) -> BundleAssemblyResult:
        # Create folder (idempotent)
        bundle_root = Path(f"{manifest.engagement_id}-v{manifest.engagement_version}-b{manifest.bundle_version}")
        if bundle_root.exists():
            # verify existing manifest integrity; if passes, return stored archive if present
            iv = await self.verify_integrity(str(bundle_root))
            if iv.success:
                archive_candidate = bundle_root.with_suffix('.zip')
                if archive_candidate.exists():
                    stored = await self.storage.write(str(archive_candidate), archive_candidate.name)
                    return BundleAssemblyResult(
                        bundle_id=manifest.bundle_id,
                        status=BundleStatus(str(manifest.status)),
                        master_bundle_path=stored,
                        persona_bundle_paths={},
                        manifest=manifest,
                        generation_errors=[],
                        generation_warnings=[],
                        total_duration_seconds=0.0,
                    )
            # otherwise clean and rebuild
            shutil.rmtree(bundle_root)
        bundle_root.mkdir(parents=True, exist_ok=True)

        # write manifest.json and provenance
        manifest_path = bundle_root / "manifest.json"
        manifest_json = json.loads(manifest.model_dump_json()) if hasattr(manifest, "model_dump_json") else json.loads(manifest.json())
        # ensure provenance
        if not getattr(manifest, "provenance", None):
            manifest.provenance = BundleProvenance(
                approved_by="system",
                approved_at=getattr(manifest, "generated_at", datetime.utcnow()),
                approval_ledger_hash="",
                snapshot_version="",
                trace_id=request.trace_id,
            )

        manifest_path.write_text(json.dumps(manifest_json, indent=2))

        # write manifest sha256
        manifest_bytes = manifest_path.read_bytes()
        manifest_sha = compute_content_hash(manifest_bytes)
        (bundle_root / "manifest.json.sha256").write_text(f"sha256:{manifest_sha}  manifest.json")

        # write files (assuming generation_results provide file bytes and relative paths)
        for f in manifest.files:
            src_bytes = None
            # Try to find in generation_results by relative_path
            for gr in generation_results:
                if getattr(gr, "relative_path", None) == f.relative_path:
                    src_bytes = getattr(gr, "content_bytes", None)
                    break

            dest_path = bundle_root / f.relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if src_bytes is not None:
                dest_path.write_bytes(src_bytes)
            else:
                # Write empty placeholder if content not available
                dest_path.write_text("")

        # compute composite hash from manifest.files data and update manifest
        table = [{"relative_path": e.relative_path, "content_hash": e.content_hash} for e in manifest.files]
        composite = compute_composite_hash(table)
        manifest.composite_hash = composite
        manifest_path.write_text(json.dumps(json.loads(manifest.model_dump_json()) if hasattr(manifest, "model_dump_json") else json.loads(manifest.json()), indent=2))

        # Run validations before archiving
        validation_errors = run_all_validations(bundle_root, manifest, self.schema_path)
        if validation_errors:
            # surface as generation errors in result
            return BundleAssemblyResult(
                bundle_id=manifest.bundle_id,
                status=BundleStatus(str(manifest.status)),
                master_bundle_path="",
                persona_bundle_paths={},
                manifest=manifest,
                generation_errors=validation_errors,
                generation_warnings=[],
                total_duration_seconds=0.0,
            )

        # create master archive
        master_archive = str(bundle_root.with_suffix(".zip"))
        ArchiveBuilder.create_zip(str(bundle_root), master_archive, compress=request.compress_on_download)

        # persona-specific bundles
        persona_paths = {}
        for persona in manifest.personas:
            persona_out = bundle_root / f"persona_{persona}"
            # Apply persona filter to create persona-specific bundle
            # PersonaFilter.filter is synchronous; call directly and capture result
            _persona_result = self.persona_filter.filter(manifest, persona, str(bundle_root), str(persona_out))
            persona_archive = str(persona_out.with_suffix(".zip"))
            ArchiveBuilder.create_zip(str(persona_out), persona_archive, compress=request.compress_on_download)
            stored = await self.storage.write(persona_archive, Path(persona_archive).name)
            persona_paths[persona] = stored

        # store master archive
        stored_path = await self.storage.write(master_archive, Path(master_archive).name)

        result = BundleAssemblyResult(
            bundle_id=manifest.bundle_id,
            status=BundleStatus(str(manifest.status)),
            master_bundle_path=stored_path,
            persona_bundle_paths=persona_paths,
            manifest=manifest,
            generation_errors=[],
            generation_warnings=[],
            total_duration_seconds=0.0,
        )

        return result

    async def verify_integrity(self, bundle_path: str) -> IntegrityVerificationResult:
        bundle_root = Path(bundle_path)
        manifest_path = bundle_root / "manifest.json"
        if not manifest_path.exists():
            return IntegrityVerificationResult(False, ["manifest missing"])

        manifest = json.loads(manifest_path.read_text())
        mismatches = []
        for entry in manifest.get("files", []):
            rp = bundle_root / entry["relative_path"]
            if not rp.exists():
                mismatches.append(entry["relative_path"])
                continue
            actual_hash = compute_content_hash(rp.read_bytes())
            if actual_hash != entry["content_hash"]:
                mismatches.append(entry["relative_path"])

        composite_expected = manifest.get("composite_hash")
        composite_computed = compute_composite_hash([{"relative_path": e["relative_path"], "content_hash": e["content_hash"]} for e in manifest.get("files", [])])
        if composite_expected != composite_computed:
            mismatches.append("composite_hash_mismatch")

        return IntegrityVerificationResult(success=(len(mismatches) == 0), mismatches=mismatches)
