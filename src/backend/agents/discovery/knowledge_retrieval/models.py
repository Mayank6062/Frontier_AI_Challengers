from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Document:
    id: str
    content: str


@dataclass(frozen=True)
class RetrievalResult:
    documents: List[Document]
