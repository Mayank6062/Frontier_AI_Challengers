from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel


class PresentationTemplateConfiguration(BaseModel):
    template_id: Optional[str]
    default_vars: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationPersonaConfiguration(BaseModel):
    persona_id: Optional[str]
    role: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationThemeConfiguration(BaseModel):
    theme_id: Optional[str]
    settings: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationLayoutConfiguration(BaseModel):
    layout_id: Optional[str]
    variants: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationBundleConfiguration(BaseModel):
    bundle_id: Optional[str]
    packaging: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationExportConfiguration(BaseModel):
    export_formats: Optional[Dict[str, object]]
    default_format: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationConfiguration(BaseModel):
    templates: Optional[Dict[str, PresentationTemplateConfiguration]]
    personas: Optional[Dict[str, PresentationPersonaConfiguration]]
    themes: Optional[Dict[str, PresentationThemeConfiguration]]
    layouts: Optional[Dict[str, PresentationLayoutConfiguration]]
    bundles: Optional[Dict[str, PresentationBundleConfiguration]]
    export: Optional[PresentationExportConfiguration]

    model_config = {"extra": "forbid", "frozen": True}
