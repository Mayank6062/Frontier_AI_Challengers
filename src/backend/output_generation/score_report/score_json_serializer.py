from __future__ import annotations

import json

from ..architecture_score.models import ArchitectureScore


class ScoreJsonSerializer:
    """Serialize the ArchitectureScore into deterministic JSON."""

    def serialize(self, score: ArchitectureScore) -> str:
        payload = score.model_dump(mode="json")
        return json.dumps(payload, indent=2, sort_keys=True, default=str)
