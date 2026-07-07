from __future__ import annotations

from typing import Sequence, Dict
from pydantic import BaseModel

from .models import (
    WalkthroughMetadata,
    WalkthroughScript,
    WalkthroughSummary,
    WalkthroughGenerationRequest,
    WalkthroughValidationSummary,
)


class WV01_MetadataContract(BaseModel):
    metadata: WalkthroughMetadata

    model_config = {"extra": "forbid", "frozen": True}


class WV02_ScriptContract(BaseModel):
    script: WalkthroughScript

    model_config = {"extra": "forbid", "frozen": True}


class WV03_SummaryContract(BaseModel):
    summary: WalkthroughSummary

    model_config = {"extra": "forbid", "frozen": True}


class WV04_GenerationRequestContract(BaseModel):
    request: WalkthroughGenerationRequest

    model_config = {"extra": "forbid", "frozen": True}


class WV05_ValidationContract(BaseModel):
    validation: WalkthroughValidationSummary

    model_config = {"extra": "forbid", "frozen": True}


class WV06_LightweightIndexContract(BaseModel):
    index: Sequence[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class WV07_ManifestContract(BaseModel):
    manifest_id: str
    title: str

    model_config = {"extra": "forbid", "frozen": True}
