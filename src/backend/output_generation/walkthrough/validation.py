from __future__ import annotations

from pydantic import BaseModel

from .contracts import (
    WV01_MetadataContract,
    WV02_ScriptContract,
    WV03_SummaryContract,
    WV04_GenerationRequestContract,
    WV05_ValidationContract,
    WV06_LightweightIndexContract,
    WV07_ManifestContract,
)


class WalkthroughValidationBundle(BaseModel):
    metadata_contract: WV01_MetadataContract
    script_contract: WV02_ScriptContract
    summary_contract: WV03_SummaryContract
    request_contract: WV04_GenerationRequestContract
    validation_contract: WV05_ValidationContract
    index_contract: WV06_LightweightIndexContract
    manifest_contract: WV07_ManifestContract

    model_config = {"extra": "forbid", "frozen": True}
