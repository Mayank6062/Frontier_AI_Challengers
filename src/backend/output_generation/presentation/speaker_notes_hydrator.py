from __future__ import annotations

from typing import List, Any

from .models import Slide, SpeakerNotes


class SpeakerNotesHydrator:
    """Populate SpeakerNotes for slides using a simple templating approach.

    The implementation generates talking points from slide paragraphs and
    applies timing hints.
    """

    async def hydrate(self, slides: List[Slide], approved_snapshot: Any, template_pack: Any) -> List[Slide]:
        for slide in slides:
            if not slide.notes:
                slide.notes = SpeakerNotes(text=None, time_hint_seconds=60)

            # Build talking points from paragraphs
            paragraphs = getattr(slide.content, "paragraphs", ()) or ()
            talking = [p for p in paragraphs if isinstance(p, str) and p.strip()][:3]
            if not talking:
                talking = [slide.content.heading or "Discuss this slide"]

            slide.notes.text = "\n".join(talking)
            # Simple timing heuristic: 30s for title, 90s for content, 60s default
            if slide.type.name.lower() == "title":
                slide.notes.time_hint_seconds = 30
            elif slide.type.name.lower() == "content":
                slide.notes.time_hint_seconds = 90
            else:
                slide.notes.time_hint_seconds = 60

        return slides


__all__ = ["SpeakerNotesHydrator"]
