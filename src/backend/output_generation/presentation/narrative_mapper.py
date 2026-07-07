from __future__ import annotations

from typing import Any, List
from dataclasses import dataclass


@dataclass
class PresentationNarrative:
    title: str
    subtitle: str
    duration_minutes: int
    persona_target: str
    outline_sections: List[str]
    call_to_action: str | None
    key_messages: List[str]


class NarrativeMapper:
    """Maps an ApprovedSnapshot-like object into a PresentationNarrative.

    This implementation is defensive: it accepts either dict-like snapshots
    or objects with attributes. It produces a stable, simple narrative used
    by the slide composer.
    """

    async def map(self, approved_snapshot: Any, persona: str) -> PresentationNarrative:
        # accept dict-like or object
        if isinstance(approved_snapshot, dict):
            snap = approved_snapshot
        else:
            # try to extract attributes
            snap = {k: getattr(approved_snapshot, k, None) for k in ("title", "subtitle", "duration_minutes", "outline_sections", "call_to_action", "key_messages")}

        title = snap.get("title") or snap.get("engagement_name") or "Presentation"
        subtitle = snap.get("subtitle") or snap.get("summary") or ""
        duration = int(snap.get("duration_minutes") or snap.get("duration") or 15)
        outline = snap.get("outline_sections") or snap.get("sections") or ["Overview", "Solution", "Risks", "Next Steps"]
        call_to_action = snap.get("call_to_action") or None
        key_messages = snap.get("key_messages") or []

        # Persona-targeting can refine sections; keep simple mapping for now
        persona_target = persona

        return PresentationNarrative(
            title=title,
            subtitle=subtitle,
            duration_minutes=duration,
            persona_target=persona_target,
            outline_sections=list(outline),
            call_to_action=call_to_action,
            key_messages=list(key_messages),
        )


__all__ = ["NarrativeMapper", "PresentationNarrative"]
