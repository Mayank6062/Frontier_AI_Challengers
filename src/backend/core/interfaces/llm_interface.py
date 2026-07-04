from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LLMResponse:
    text: str
    # Raw provider-specific payload if implementor needs it for diagnostics
    raw: Optional[Dict[str, Any]] = None
    # Token usage details (provider-normalized)
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class LLMInterface(ABC):
    """Abstract contract for LLM provider adapters.

    Implementations adapt provider SDKs to this normalized invoke() signature.
    """

    @abstractmethod
    def invoke(
        self,
        prompt: str,
        model_id: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResponse:  # pragma: no cover - interface only
        """Synchronously invoke the configured LLM and return a normalized response.

        Adapter implementations may raise provider-specific exceptions; callers
        should catch and translate to domain errors as appropriate.
        """

        raise NotImplementedError()
