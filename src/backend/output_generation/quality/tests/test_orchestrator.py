import asyncio

from src.backend.output_generation.quality.enums import ValidationSeverity
from src.backend.output_generation.quality.orchestrator import QualityGateOrchestrator


def test_validate_bundle_returns_report_and_verdict() -> None:
    orchestrator = QualityGateOrchestrator()
    bundle = {
        "artifacts": [
            {"path": "manifest.json"},
            {"path": "report.json"},
            {"path": "diagram.mmd"},
        ],
        "content": [
            "Executive Summary",
            "Architecture summary includes components and interfaces.",
            "Risk register describes deployment threats.",
        ],
    }

    report, verdict = asyncio.run(
        orchestrator.validate_bundle(bundle, engagement_id="eng-1", bundle_version=1)
    )

    assert report.engagement_id == "eng-1"
    assert report.completeness.required_files_present["diagram"] is True
    assert report.completeness.required_sections_present["executive_summary"] is True
    assert verdict in {
        ValidationSeverity.INFO,
        ValidationSeverity.WARN,
        ValidationSeverity.ERROR,
        ValidationSeverity.BLOCKER,
    }
