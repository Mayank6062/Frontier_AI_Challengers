from __future__ import annotations

import logging
from typing import List, Any
from pathlib import Path

from .models import Slide, MediaReference, PresentationAsset

logger = logging.getLogger(__name__)


class DiagramEmbedder:
    """Resolve and attach diagram asset paths to slide media references.

    This implementation is non-failing: missing diagrams are replaced with
    a packaged placeholder reference and a warning is logged.
    """

    PLACEHOLDER = "templates/presentation/v1.2/placeholder.svg"

    async def embed(self, slides: List[Slide], approved_snapshot: Any, template_pack: Any) -> List[Slide]:
        for slide in slides:
            if not slide.content or not slide.content.media:
                continue
            resolved_media: List[MediaReference] = []
            for m in slide.content.media:
                # If asset has uri, check file exists
                uri = getattr(m, "asset", None)
                path = None
                try:
                    if isinstance(uri, PresentationAsset):
                        path = uri.uri
                    else:
                        path = getattr(m, "asset", None) or getattr(m, "uri", None)
                except Exception:
                    path = None

                if path:
                    p = Path(path)
                    if p.exists():
                        # attach as-is
                        resolved_media.append(m)
                        continue
                # fallback
                logger.warning("Diagram not found, using placeholder", extra={"slide": getattr(slide, "id", None)})
                placeholder_asset = PresentationAsset(uri=self.PLACEHOLDER, description="placeholder")
                placeholder_ref = MediaReference(asset=placeholder_asset, caption=(getattr(m, "caption", None) or "placeholder"))
                resolved_media.append(placeholder_ref)

            slide.content.media = tuple(resolved_media)

        return slides


__all__ = ["DiagramEmbedder"]
