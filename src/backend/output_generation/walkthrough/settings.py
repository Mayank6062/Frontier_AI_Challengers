from __future__ import annotations

from pydantic import BaseModel


class WalkthroughLimits(BaseModel):
    max_steps: int = 200
    max_duration_seconds: int = 60 * 60

    model_config = {"extra": "forbid", "frozen": True}


class PlaybackDefaults(BaseModel):
    default_speed: str = "1x"
    allow_auto_advance: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughSettings(BaseModel):
    limits: WalkthroughLimits
    playback: PlaybackDefaults

    model_config = {"extra": "forbid", "frozen": True}
