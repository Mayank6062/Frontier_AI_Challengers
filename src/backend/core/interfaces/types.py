"""Interface-layer type aliases and re-exports.

Per repository architecture, shared model types are owned by
`src/backend/shared/models`. This module re-exports those types so
interface modules can continue to import from `...interfaces.types`.
"""

from __future__ import annotations

from ...shared.models.types import Citation, TokenUsage, UUIDStr

__all__ = ["Citation", "TokenUsage", "UUIDStr"]
