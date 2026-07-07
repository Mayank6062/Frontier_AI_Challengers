from __future__ import annotations

from typing import List, Optional

from .models import Slide, SlideContent, SpeakerNotes
from .enums import SlideType, LayoutVariant
from .narrative_mapper import PresentationNarrative


class SlideComposer:
    """Compose Slides from a PresentationNarrative.

    Produces a list of `Slide` objects using the package models and enums.
    """

    async def compose(self, narrative: PresentationNarrative, template_pack: Optional[object], persona: str) -> List[Slide]:
        slides: List[Slide] = []

        # Title slide
        title_slide = Slide(
            type=SlideType.TITLE,
            layout=LayoutVariant.TITLE_AND_CONTENT,
            content=SlideContent(heading=narrative.title, paragraphs=(narrative.subtitle or "",)),
            notes=SpeakerNotes(text=None, time_hint_seconds=30),
            transition=None,
        )
        slides.append(title_slide)

        # Agenda/outline slide
        agenda_slide = Slide(
            type=SlideType.CONTENT,
            layout=LayoutVariant.ONE_COLUMN,
            content=SlideContent(heading="Agenda", paragraphs=tuple(narrative.outline_sections)),
            notes=SpeakerNotes(text="Review agenda", time_hint_seconds=60),
            transition=None,
        )
        slides.append(agenda_slide)

        # Body slides: one slide per outline item, with placeholder paragraphs
        for section in narrative.outline_sections:
            s = Slide(
                type=SlideType.CONTENT,
                layout=LayoutVariant.TWO_COLUMN,
                content=SlideContent(heading=section, paragraphs=(f"Summary of {section}",)),
                notes=SpeakerNotes(text=None, time_hint_seconds=90),
                transition=None,
            )
            slides.append(s)

        # Risk slide if present in call_to_action heuristic
        if "risk" in (narrative.call_to_action or "").lower() or any("risk" in s.lower() for s in narrative.outline_sections):
            risk_slide = Slide(
                type=SlideType.SUMMARY,
                layout=LayoutVariant.ONE_COLUMN,
                content=SlideContent(heading="Risk Landscape", paragraphs=("Top risks and mitigations",)),
                notes=SpeakerNotes(text="Discuss risks", time_hint_seconds=60),
                transition=None,
            )
            slides.append(risk_slide)

        # Finale
        finale = Slide(
            type=SlideType.SUMMARY,
            layout=LayoutVariant.ONE_COLUMN,
            content=SlideContent(heading="Next Steps", paragraphs=(narrative.call_to_action or "Questions?",)),
            notes=SpeakerNotes(text="Close and Q&A", time_hint_seconds=30),
            transition=None,
        )
        slides.append(finale)

        return slides


__all__ = ["SlideComposer"]
