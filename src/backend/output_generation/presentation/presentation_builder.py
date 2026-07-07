from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Optional, Tuple
from uuid import uuid4

from .protocols import (
    PresentationTemplateResolver,
)
from .contracts import PresentationGenerationRequest, PresentationGenerationResponse
from .models import PresentationResult, PresentationArtifact

from .narrative_mapper import NarrativeMapper
from .slide_composer import SlideComposer
from .diagram_embedder import DiagramEmbedder
from .speaker_notes_hydrator import SpeakerNotesHydrator
from .theme_applier import ThemeApplier
from .pptx_generator import PPTXGenerator
from .presentation_validator import PresentationValidator

logger = logging.getLogger(__name__)


class PresentationBuilder:
    """Orchestrates presentation generation end-to-end.

    This implementation composes the canonical pipeline described in the
    Implementation Bible and uses the package's contracts and models.
    """

    def __init__(
        self,
        template_resolver: Optional[PresentationTemplateResolver] = None,
    ) -> None:
        self.template_resolver = template_resolver
        self.narrative_mapper = NarrativeMapper()
        self.slide_composer = SlideComposer()
        self.diagram_embedder = DiagramEmbedder()
        self.speaker_hydrator = SpeakerNotesHydrator()
        self.theme_applier = ThemeApplier()
        self.pptx_generator = PPTXGenerator()
        self.validator = PresentationValidator()

    async def build_presentation(
        self, request: PresentationGenerationRequest, approved_snapshot: object, persona: str, template_version: str, trace_id: Optional[str] = None
    ) -> Tuple[bytes, PresentationGenerationResponse]:
        start = datetime.utcnow()
        logger.info("Starting presentation build", extra={"trace_id": trace_id})

        # Resolve template pack
        template_pack = None
        if self.template_resolver:
            # run resolver in thread to avoid blocking; resolve by template version
            resolver = self.template_resolver
            template_pack = await asyncio.to_thread(lambda: resolver.resolve(template_version))

        # 1. Map narrative
        narrative = await self.narrative_mapper.map(approved_snapshot, persona)

        # 2. Compose slides
        slides = await self.slide_composer.compose(narrative, template_pack, persona)

        # 3. Embed diagrams
        slides = await self.diagram_embedder.embed(slides, approved_snapshot, template_pack)

        # 4. Hydrate speaker notes
        slides = await self.speaker_hydrator.hydrate(slides, approved_snapshot, template_pack)

        # 5. Validate pre-serialization
        validation = self.validator.validate_presentation_definition(slides, approved_snapshot, persona)
        if validation.failed > 0:
            # Blocker behavior: if failures exist, raise to signal caller
            raise RuntimeError(f"Presentation validation failed: {validation}")

        # 6. Apply theme
        theme_artifact = self.theme_applier.apply(template_pack, persona)

        # 7. Serialize to PPTX
        pptx_bytes = await self.pptx_generator.serialize_to_pptx(slides, template_pack, theme_artifact)

        # 8. Post-serialization validation
        integrity_ok = self.pptx_generator.validate_pptx_integrity(pptx_bytes)
        if not integrity_ok:
            raise RuntimeError("Generated PPTX failed integrity check")

        # 9. Build result + manifest artifact
        artifact = PresentationArtifact(path=f"presentations/{persona}_{uuid4().hex}.pptx", format=None)

        result = PresentationResult(artifacts=(artifact,), warnings=(), failures=())

        response = PresentationGenerationResponse(request_id=uuid4(), result=result, summary=None)

        duration = (datetime.utcnow() - start).total_seconds()
        logger.info("Presentation build complete", extra={"duration_seconds": duration, "size_bytes": len(pptx_bytes)})

        return pptx_bytes, response


__all__ = ["PresentationBuilder"]
