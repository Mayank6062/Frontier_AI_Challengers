from __future__ import annotations

from typing import Protocol, Sequence, Optional, Dict
from uuid import UUID

from .models import (
    DocumentDefinition,
    DocumentGenerationRequest,
    DocumentGenerationResult,
    SectionOrderingRule,
)


class DocumentGenerator(Protocol):
    def generate(
        self, request: DocumentGenerationRequest
    ) -> DocumentGenerationResult: ...


class DocumentValidator(Protocol):
    def validate(self, definition: DocumentDefinition) -> Dict[str, object]: ...


class DocumentTemplateResolver(Protocol):
    def resolve(self, document_type: str, template_version: str) -> str: ...


class DocumentRegistry(Protocol):
    def list(self) -> Sequence[Dict[str, object]]: ...


class DocumentManifestBuilder(Protocol):
    def build(self, definition: DocumentDefinition) -> Dict[str, object]: ...


class DocumentRendererContract(Protocol):
    def render(self, definition: DocumentDefinition, format: str) -> bytes: ...


class DocumentFormatter(Protocol):
    def format(
        self, definition: DocumentDefinition, rules: Sequence[SectionOrderingRule]
    ) -> DocumentDefinition: ...


class DocumentBundleBuilder(Protocol):
    def assemble(
        self, documents: Sequence[DocumentDefinition]
    ) -> Dict[str, object]: ...


class DocumentReferenceResolver(Protocol):
    def resolve(self, ref: str) -> Optional[UUID]: ...


class DocumentCitationResolver(Protocol):
    def resolve(self, citation: str) -> Dict[str, object]: ...
