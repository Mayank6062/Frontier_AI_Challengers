from __future__ import annotations

import logging
import re
from typing import Optional


class HtmlSchemaValidator:
    """Validate a minimal structure for an HTML document."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, content: str) -> bool:
        if not content.strip():
            return False
        return bool(re.search(r"<html", content, re.IGNORECASE)) and bool(re.search(r"<body", content, re.IGNORECASE))
