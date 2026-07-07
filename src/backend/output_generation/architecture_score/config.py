from __future__ import annotations

from pydantic import BaseModel, Field


class ArchitectureScoreConfig(BaseModel):
    enabled: bool = Field(default=True)
    api_timeout_seconds: int = Field(default=30)

    model_config = {"extra": "forbid", "frozen": True}
