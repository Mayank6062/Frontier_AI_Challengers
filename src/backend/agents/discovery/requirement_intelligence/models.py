from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Requirement:
    text: str
    tags: List[str]


@dataclass(frozen=True)
class ExtractionResult:
    requirements: List[Requirement]
