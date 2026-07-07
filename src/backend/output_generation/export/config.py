from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel

from .enums import ExportFeatureFlag


class ExportTimeoutConfiguration(BaseModel):
    default_seconds: Optional[int]
    hard_limit_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportTemplateConfiguration(BaseModel):
    template_id: Optional[str]
    default_vars: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportLimits(BaseModel):
    max_artifacts: Optional[int]
    max_total_bytes: Optional[int]
    max_rows_csv: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class ExportDefaults(BaseModel):
    timeout: Optional[ExportTimeoutConfiguration]
    template: Optional[ExportTemplateConfiguration]
    limits: Optional[ExportLimits]

    model_config = {"extra": "forbid", "frozen": True}


class ExportPolicies(BaseModel):
    retry_on_transient: bool = False
    retry_mode: Optional[str]
    timeout_policy: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportFeatureFlags(BaseModel):
    flags: Optional[Dict[ExportFeatureFlag, bool]]

    model_config = {"extra": "forbid", "frozen": True}


class ExportConfiguration(BaseModel):
    id: Optional[str]
    defaults: Optional[ExportDefaults]
    policies: Optional[ExportPolicies]
    features: Optional[ExportFeatureFlags]

    model_config = {"extra": "forbid", "frozen": True}
