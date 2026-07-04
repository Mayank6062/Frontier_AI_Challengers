"""Secrets manager implementation (in-memory) for tests and local runs.

Implements `SecretsInterface` using a constructor-injected mapping.
"""

from __future__ import annotations

from typing import Dict, Optional

from ...core.interfaces.secrets_interface import SecretsInterface


class SecretsManager(SecretsInterface):
    def __init__(self, store: Optional[Dict[str, str]] = None) -> None:
        # Constructor injection: callers may provide a dict-like store.
        self._store: Dict[str, str] = store or {}

    def get_secret(self, name: str) -> Optional[str]:
        return self._store.get(name)


__all__ = ["SecretsManager"]
