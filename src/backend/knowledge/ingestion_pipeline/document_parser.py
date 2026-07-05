from __future__ import annotations

from typing import List


def simple_document_parser(raw: str) -> List[str]:
    """Split raw text into documents by '---' delimiter."""
    parts = [p.strip() for p in raw.split("---") if p.strip()]
    return parts
