from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from .models import QualityReport


class QualityReportGenerator:
    """Generate a JSON report artifact for quality validation results."""

    def __init__(self, output_path: Optional[Path | str] = None, logger: Optional[logging.Logger] = None) -> None:
        self.output_path = Path(output_path) if output_path is not None else None
        self.logger = logger or logging.getLogger(__name__)

    def generate(self, report: QualityReport) -> dict[str, Any]:
        payload = report.model_dump(mode="json")
        if self.output_path is not None:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return payload
