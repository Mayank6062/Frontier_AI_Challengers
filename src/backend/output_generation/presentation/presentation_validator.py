from __future__ import annotations

from typing import List, Any
import logging

from .models import Slide
from .validation import PresentationValidationSummary

logger = logging.getLogger(__name__)


class PresentationValidator:
    """Run syntactic and semantic checks on presentation slides.

    Returns a `PresentationValidationSummary` that indicates passed/failed counts.
    """

    def validate_presentation_definition(self, slides: List[Slide], snapshot: Any, persona: str) -> PresentationValidationSummary:
        checks: List[str] = []
        passed = 0
        failed = 0

        count = len(slides or [])
        # slide count rule
        if 1 <= count <= 100:
            passed += 1
            checks.append("SLIDE_COUNT_OK")
        else:
            failed += 1
            checks.append("SLIDE_COUNT_OUT_OF_RANGE")

        # accessibility: slides with media must have alt text (speaker notes used as proxy)
        missing_alt = 0
        for s in slides:
            media = getattr(s.content, "media", ()) or ()
            if media:
                notes = getattr(s, "notes", None)
                if not notes or not getattr(notes, "text", None):
                    missing_alt += 1

        if missing_alt == 0:
            passed += 1
            checks.append("ACCESSIBILITY_OK")
        else:
            failed += 1
            checks.append("MISSING_SPEAKER_NOTES_FOR_MEDIA")

        # basic layout presence
        layouts_present = all(getattr(s, "layout", None) is not None for s in slides)
        if layouts_present:
            passed += 1
            checks.append("LAYOUTS_OK")
        else:
            failed += 1
            checks.append("MISSING_LAYOUTS")

        summary = PresentationValidationSummary(checks=checks, passed=passed, failed=failed)
        logger.debug("Validation summary: %s", summary)
        return summary


__all__ = ["PresentationValidator"]
