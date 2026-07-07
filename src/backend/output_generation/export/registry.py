from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class ExportFormatRegistration(BaseModel):
    format: str
    handler_name: str

    model_config = {"extra": "forbid", "frozen": True}


class ExportGeneratorRegistration(BaseModel):
    name: str
    version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportConverterRegistration(BaseModel):
    converter_type: str
    implementation: str

    model_config = {"extra": "forbid", "frozen": True}


class ExportTemplateRegistration(BaseModel):
    template_id: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportFeatureRegistration(BaseModel):
    feature_flag: str
    enabled: bool

    model_config = {"extra": "forbid", "frozen": True}


class RegistryMetadata(BaseModel):
    created_by: Optional[str]
    created_at: Optional[str]
    registry_id: Optional[UUID]

    model_config = {"extra": "forbid", "frozen": True}


class ExportRegistry(BaseModel):
    formats: Dict[str, ExportFormatRegistration] = {}
    generators: Dict[str, ExportGeneratorRegistration] = {}
    converters: Dict[str, ExportConverterRegistration] = {}
    templates: Dict[str, ExportTemplateRegistration] = {}
    features: Dict[str, ExportFeatureRegistration] = {}
    metadata: Optional[RegistryMetadata]

    model_config = {"extra": "forbid", "frozen": True}
