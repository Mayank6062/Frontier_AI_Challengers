from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class PresentationRegistryEntry(BaseModel):
    id: Optional[UUID]
    name: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationTemplateRegistry(BaseModel):
    templates: Dict[str, PresentationRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class PresentationAssetRegistry(BaseModel):
    assets: Dict[str, PresentationRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class PresentationThemeRegistry(BaseModel):
    themes: Dict[str, PresentationRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class PresentationPersonaRegistry(BaseModel):
    personas: Dict[str, PresentationRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}
