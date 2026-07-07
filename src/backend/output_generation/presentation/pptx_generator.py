from __future__ import annotations

import io
import logging
from typing import List, Any

from .models import Slide

logger = logging.getLogger(__name__)


class PPTXGenerator:
    """Serialize a sequence of Slides to PPTX bytes using python-pptx.

    The generator creates simple, accessible slides (title + body). Images
    are attached when a media reference points to a valid file path.
    """

    async def serialize_to_pptx(self, slides: List[Slide], template_pack: Any, theme_artifact: Any) -> bytes:
        # Import locally via importlib to avoid static import-time errors
        import importlib

        pptx = importlib.import_module("pptx")
        util = importlib.import_module("pptx.util")
        Presentation = getattr(pptx, "Presentation")
        Inches = getattr(util, "Inches")

        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

        for s in slides:
            layout = prs.slide_layouts[6]
            slide = prs.slides.add_slide(layout)

            # Title
            if getattr(s.content, "heading", None):
                title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(1))
                title_frame = title_box.text_frame
                title_frame.text = str(s.content.heading)

            # Body paragraphs
            paragraphs = getattr(s.content, "paragraphs", ()) or ()
            if paragraphs:
                body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.6), Inches(9), Inches(4.5))
                body_frame = body_box.text_frame
                for p in paragraphs:
                    if not p:
                        continue
                    para = body_frame.add_paragraph()
                    para.text = str(p)

            # Speaker notes
            notes_obj = getattr(s, "notes", None)
            if notes_obj and getattr(notes_obj, "text", None):
                notes_slide = slide.notes_slide
                notes_text = notes_slide.notes_text_frame
                notes_text.text = notes_obj.text

            # Media: attempt to attach images if present
            media = getattr(s.content, "media", None) or ()
            for m in media:
                try:
                    asset = getattr(m, "asset", None)
                    uri = getattr(asset, "uri", None) if asset is not None else None
                    if uri:
                        slide.shapes.add_picture(uri, Inches(1), Inches(2), width=Inches(6))
                except Exception as e:
                    logger.warning("Failed to attach media to slide", exc_info=e)

        out = io.BytesIO()
        prs.save(out)
        return out.getvalue()

    def validate_pptx_integrity(self, pptx_bytes: bytes) -> bool:
        try:
            import importlib
            import io as _io

            pptx = importlib.import_module("pptx")
            Presentation = getattr(pptx, "Presentation")
            Presentation(_io.BytesIO(pptx_bytes))
            return True
        except Exception:
            logger.exception("PPTX integrity validation failed")
            return False


__all__ = ["PPTXGenerator"]
