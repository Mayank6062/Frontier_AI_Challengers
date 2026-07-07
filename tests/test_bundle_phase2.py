import asyncio
import json
from pathlib import Path

from src.backend.output_generation.bundle.schemas import (
    BundleManifest,
    ManifestFileEntry,
    BundleAssemblyRequest,
)
from src.backend.output_generation.bundle.bundle_assembler import BundleAssembler
from src.backend.output_generation.bundle.integrity import compute_content_hash, compute_composite_hash


def make_sample_manifest(tmp_path: Path) -> BundleManifest:
    f1 = ManifestFileEntry(
        file_id="f1",
        relative_path="doc1.txt",
        file_type="text",
        media_type="text/plain",
        size_bytes=11,
        content_hash=compute_content_hash(b"hello world"),
        status="SUCCESS",
        generation_timestamp="2024-01-01T00:00:00Z",
        generator="gen",
        template_version="v1",
        persona_scope=["personaA"],
    )

    manifest = BundleManifest(
        bundle_id="b1",
        engagement_id="e1",
        engagement_version=1,
        bundle_version=1,
        status="PENDING",
        generated_at="2024-01-01T00:00:00Z",
        generation_duration_seconds=0.0,
        generator_versions={"gen":"1"},
        template_versions={"v1":"1"},
        files=[f1],
        composite_hash=compute_composite_hash([{"relative_path":"doc1.txt","content_hash":f1.content_hash}]),
        provenance={"approved_by":"x","approved_at":"2024-01-01T00:00:00Z","approval_ledger_hash":"abc","snapshot_version":"1","trace_id":"t1"},
        personas=["personaA"],
        archive_format="zip",
        compression_enabled=True,
    )
    return manifest


def test_assemble_and_verify(tmp_path: Path):
    manifest = make_sample_manifest(tmp_path)
    assembler = BundleAssembler()

    class GR:
        def __init__(self, relative_path, content_bytes):
            self.relative_path = relative_path
            self.content_bytes = content_bytes

    gr = GR("doc1.txt", b"hello world")

    req = BundleAssemblyRequest(engagement_id=manifest.engagement_id, engagement_version=1, approved_snapshot_id="s1", trace_id="t1", requested_personas=["personaA"], output_format="zip", compress_on_download=True)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res = loop.run_until_complete(assembler.assemble([gr], manifest, req))
    finally:
        loop.close()
    assert res.master_bundle_path is not None
