from __future__ import annotations

import logging
import re
from typing import Optional


class MermaidSyntaxValidator:
    """Validate that Mermaid diagrams are structurally well-formed."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, content: str) -> bool:
        if not content.strip():
            return False
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            return False
        first = lines[0]
        return bool(re.match(r"^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|journey|gantt|pie|gitGraph|mindmap|timeline|quadrantChart|xychart-beta)", first))
