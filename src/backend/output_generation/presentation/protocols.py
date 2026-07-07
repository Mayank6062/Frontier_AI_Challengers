from __future__ import annotations

from typing import Protocol, Sequence, Dict
from uuid import UUID

from .contracts import (
    PresentationGenerationRequest,
    PresentationGenerationResponse,
)


class PresentationEngine(Protocol):
    def generate(
        self, request: PresentationGenerationRequest
    ) -> PresentationGenerationResponse: ...


class PresentationBuilder(Protocol):
    def build(self) -> UUID: ...


class PresentationValidator(Protocol):
    def validate(self, definition: object) -> bool: ...


class PresentationTemplateResolver(Protocol):
    def resolve(self, template_id: str) -> object: ...


class PresentationRegistry(Protocol):
    def register(self, name: str, entry: object) -> None: ...


class PresentationManifestBuilder(Protocol):
    def build(self) -> UUID: ...


class PresentationExporter(Protocol):
    def export(self, bundle: object, fmt: str) -> bytes: ...


class PresentationSerializer(Protocol):
    def serialize(self, bundle: object) -> bytes: ...


class PresentationThemeResolver(Protocol):
    def resolve(self, theme_name: str) -> object: ...


class PresentationAssetResolver(Protocol):
    def resolve(self, asset_ref: str) -> object: ...


class PresentationCitationResolver(Protocol):
    def resolve(self, citation_id: str) -> object: ...


class PresentationPersonaResolver(Protocol):
    def resolve(self, persona_id: str) -> object: ...


class PresentationLayoutResolver(Protocol):
    def resolve(self, layout_id: str) -> object: ...


class PresentationNotesGenerator(Protocol):
    def generate(self, slides: Sequence[object]) -> Sequence[str]: ...


class PresentationStatisticsProvider(Protocol):
    def collect(self) -> Dict[str, object]: ...


class PresentationIntegrityValidator(Protocol):
    def check(self, manifest: object) -> bool: ...


class PresentationAccessibilityValidator(Protocol):
    def check(self, manifest: object) -> bool: ...


class PresentationQualityValidator(Protocol):
    def check(self, manifest: object) -> bool: ...


class PresentationDefinitionProvider(Protocol):
    def provide(self) -> object: ...


class PresentationBundleBuilder(Protocol):
    def build(self) -> object: ...
