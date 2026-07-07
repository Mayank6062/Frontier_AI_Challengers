from __future__ import annotations

import logging
import re
from typing import Optional


class DotSyntaxValidator:
    """Validate that DOT graph descriptions have a graph declaration and a closing brace."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, content: str) -> bool:
        if not content.strip():
            return False
        stripped = content.strip()
        if not re.search(r"^\s*(digraph|graph)\s+", stripped):
            return False
        return stripped.endswith("}")
