from datetime import datetime

from src.backend.output_generation.bundle import schemas, integrity


def test_compute_composite_hash_deterministic():
    files = [
        {"relative_path": "artifacts/hld.md", "content_hash": "a" * 64},
        {"relative_path": "artifacts/lld.md", "content_hash": "b" * 64},
    ]

    h1 = integrity.compute_composite_hash(files)
    h2 = integrity.compute_composite_hash(list(reversed(files)))
    assert isinstance(h1, str)
    assert len(h1) == 64
    assert h1 == h2


def test_bundle_manifest_pydantic_roundtrip():
    entry = schemas.ManifestFileEntry(
        file_id="11111111-1111-1111-1111-111111111111",
        relative_path="artifacts/hld.md",
        file_type="document",
        media_type="text/markdown",
        size_bytes=123,
        content_hash=("0" * 64),
        status=schemas.FileStatus.SUCCESS,
        generation_timestamp=datetime.utcnow(),
        generator="MarkdownHLDGenerator",
        template_version="1.0.0",
    )

    manifest = schemas.BundleManifest(
        bundle_id="22222222-2222-2222-2222-222222222222",
        engagement_id="ACME-2026-Q2",
        engagement_version=1,
        bundle_version=1,
        status="COMPLETE",
        generated_at=datetime.utcnow(),
        generation_duration_seconds=1.23,
        generator_versions={"MarkdownHLDGenerator": "1.0.0"},
        template_versions={"markdown": "1.0.0"},
        files=[entry],
        composite_hash=("0" * 64),
        provenance=schemas.BundleProvenance(
            approved_by="alice@acme.com",
            approved_at=datetime.utcnow(),
            approval_ledger_hash="ledgerhash",
            snapshot_version="3.2.1",
            trace_id="trace-uuid",
        ),
        personas=["architect"],
    )

    assert manifest.manifest_version == "2.0.0"
    assert manifest.files[0].relative_path == "artifacts/hld.md"
