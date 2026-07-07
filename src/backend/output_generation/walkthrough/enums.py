from __future__ import annotations

import enum


class WalkthroughMode(enum.StrEnum):
    GUIDED = "guided"
    AUTOPLAY = "autoplay"
    SELF_PACED = "self_paced"


class WalkthroughStatus(enum.StrEnum):
    DRAFT = "draft"
    READY = "ready"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class WalkthroughPlayerMode(enum.StrEnum):
    PRESENT = "present"
    REVIEW = "review"
    PRACTICE = "practice"


class WalkthroughTargetType(enum.StrEnum):
    NODE = "node"
    EDGE = "edge"
    SECTION = "section"
    PANEL = "panel"
    ANCHOR = "anchor"


class WalkthroughPanel(enum.StrEnum):
    SIDEBAR = "sidebar"
    MAIN = "main"
    OVERLAY = "overlay"


class PlaybackState(enum.StrEnum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    ENDED = "ended"


class PlaybackSpeed(enum.StrEnum):
    X0_5 = "0.5x"
    X1 = "1x"
    X1_5 = "1.5x"
    X2 = "2x"


class TransitionType(enum.StrEnum):
    CUT = "cut"
    FADE = "fade"
    SLIDE = "slide"


class NavigationDirection(enum.StrEnum):
    FORWARD = "forward"
    BACKWARD = "backward"
    JUMP = "jump"


class AutoAdvanceMode(enum.StrEnum):
    OFF = "off"
    TIMED = "timed"
    EVENT = "event"


class FocusMode(enum.StrEnum):
    HIGHLIGHT = "highlight"
    ZOOM = "zoom"
    PAN = "pan"


class NarrationStyle(enum.StrEnum):
    NONE = "none"
    VOICE_OVER = "voice_over"
    SUBTITLES = "subtitles"


class ValidationStatus(enum.StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
