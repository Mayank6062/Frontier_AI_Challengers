from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .base import TimestampedModel


class ManifestHash(BaseModel):
    algorithm: str
    value: str

    model_config = {"extra": "forbid"}


class VersionMetadata(BaseModel):
    version: str
    semver: Optional[str] = None
    build: Optional[str] = None

    model_config = {"extra": "forbid"}


class TemplateMetadata(BaseModel):
    template_id: UUID = Field(default_factory=uuid4)
    name: str
    path: str
    engine: Optional[str] = None

    model_config = {"extra": "forbid"}


class GeneratorMetadata(BaseModel):
    generator_id: UUID = Field(default_factory=uuid4)
    name: str
    version: Optional[str] = None
    configuration: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}


class BundleManifest(TimestampedModel):
    bundle_id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    version: VersionMetadata
    templates: List[TemplateMetadata] = Field(default_factory=list)
    generators: List[GeneratorMetadata] = Field(default_factory=list)
    files: List[str] = Field(default_factory=list)
    hashes: List[ManifestHash] = Field(default_factory=list)
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid"}
