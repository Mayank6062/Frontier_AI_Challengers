from __future__ import annotations

from typing import Protocol, Sequence, Optional, Dict
from uuid import UUID

from .models import (
    WalkthroughScript,
    WalkthroughGenerationRequest,
    WalkthroughGenerationResult,
    WalkthroughValidationSummary,
    WalkthroughReference,
    WalkthroughPlaybackMetadata,
)
from .manifest import WalkthroughManifest


class WalkthroughGenerator(Protocol):
    def generate(
        self, request: WalkthroughGenerationRequest
    ) -> WalkthroughGenerationResult: ...


class WalkthroughValidator(Protocol):
    def validate(self, script: WalkthroughScript) -> WalkthroughValidationSummary: ...


class WalkthroughRegistry(Protocol):
    def list(self) -> Sequence[WalkthroughReference]: ...

    def get(self, id: UUID) -> Optional[WalkthroughReference]: ...


class WalkthroughManifestBuilder(Protocol):
    def build(self, script: WalkthroughScript) -> WalkthroughManifest: ...


class WalkthroughPlayerContract(Protocol):
    def play(self, walkthrough_id: UUID) -> WalkthroughPlaybackMetadata: ...


class WalkthroughNavigator(Protocol):
    def next(self, current_step_id: UUID) -> Optional[UUID]: ...

    def prev(self, current_step_id: UUID) -> Optional[UUID]: ...


class WalkthroughFocusResolver(Protocol):
    def resolve(self, target_id: UUID) -> object: ...


class WalkthroughRendererContract(Protocol):
    def render_step(self, step_id: UUID) -> str: ...


class WalkthroughExportContract(Protocol):
    def export(self, walkthrough_id: UUID, format: str) -> bytes: ...


class WalkthroughSettingsProvider(Protocol):
    def get_settings(self) -> Dict[str, object]: ...
