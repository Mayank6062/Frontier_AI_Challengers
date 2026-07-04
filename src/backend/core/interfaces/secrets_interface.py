from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class SecretsInterface(ABC):
    """Contract for secrets retrieval adapters.

    Implementations must securely retrieve secrets without exposing
    raw secret values in logs. The interface is intentionally minimal;
    concrete adapters may provide richer semantics.
    """

    @abstractmethod
    def get_secret(
        self, name: str
    ) -> Optional[str]:  # pragma: no cover - interface only
        """Return the secret string for `name` or `None` if not found."""

        raise NotImplementedError()
