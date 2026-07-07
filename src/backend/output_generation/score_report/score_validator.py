from __future__ import annotations

from dataclasses import dataclass, field

from ..architecture_score.models import ArchitectureScore
from ..architecture_score.enums import ScoreSchemaVersion


@dataclass(slots=True)
class ValidationResult:
    severity: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ScoreValidator:
    """Validate an ArchitectureScore before rendering any score report artifacts."""

    def validate(self, score: ArchitectureScore) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if score.composite_score < 0 or score.composite_score > 100:
            errors.append("composite_score out of range [0, 100]")

        total_weight = sum(dim.weight for dim in score.all_dimensions)
        if abs(total_weight - 1.0) > 0.001:
            errors.append(f"Dimension weights sum to {total_weight:.3f}, expected 1.0")

        if not score.all_dimensions:
            errors.append("all_dimensions is empty — scoring is incomplete")

        if len(score.all_dimensions) < 16:
            warnings.append(
                f"Only {len(score.all_dimensions)} of 16 dimensions scored."
            )

        if score.metadata.score_schema_version not in {ScoreSchemaVersion.V2}:
            warnings.append("Unknown score_schema_version; fallback rendering will be used.")

        severity = "BLOCKER" if errors else ("WARN" if warnings else "PASS")
        return ValidationResult(severity=severity, errors=errors, warnings=warnings)
