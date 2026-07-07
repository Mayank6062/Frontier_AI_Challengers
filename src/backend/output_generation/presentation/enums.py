from __future__ import annotations

import enum

from ..enums import FailureSeverity


class PresentationFormat(enum.StrEnum):
    PPTX = "pptx"
    PDF = "pdf"


class SlideType(enum.StrEnum):
    TITLE = "title"
    SECTION = "section"
    CONTENT = "content"
    MEDIA = "media"
    SUMMARY = "summary"


class LayoutVariant(enum.StrEnum):
    ONE_COLUMN = "one_column"
    TWO_COLUMN = "two_column"
    TITLE_AND_CONTENT = "title_and_content"


class TransitionType(enum.StrEnum):
    NONE = "none"
    FADE = "fade"
    SLIDE = "slide"


class PersonaRole(enum.StrEnum):
    PRESENTER = "presenter"
    AUDIENCE = "audience"


# Reuse `FailureSeverity` from the package-wide enums where severity is needed.
# Do not subclass enum to avoid duplicate-member issues.
PresentationSeverity = FailureSeverity
