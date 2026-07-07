from __future__ import annotations

from pydantic import BaseModel, Field


class ArchitectureScoreSettings(BaseModel):
    default_renderer: str = Field(default="json")
    max_dimensions: int = Field(default=50)
    min_confidence_for_publish: float = Field(default=0.5)

    model_config = {"extra": "forbid", "frozen": True}
