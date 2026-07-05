from __future__ import annotations

from typing import List


class DummyEmbedder:
    """Embedding abstraction that returns deterministic numeric vectors.

    No provider integrations. Suitable for unit tests and algorithm validation.
    """

    def __init__(self, dimension: int = 8) -> None:
        self._dim = dimension

    async def embed(self, text: str) -> List[float]:
        # deterministic pseudo-embedding: use character codes modulo dimension
        vec: List[float] = [0.0] * self._dim
        for i, ch in enumerate(text):
            vec[i % self._dim] += float(ord(ch) % 97) / 100.0
        return vec
