from __future__ import annotations

import json
import logging
from typing import Optional


class JsonSchemaValidator:
    """Validate that payloads parse as JSON and contain an object or array."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, content: str) -> bool:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return False
        return isinstance(payload, (dict, list))
