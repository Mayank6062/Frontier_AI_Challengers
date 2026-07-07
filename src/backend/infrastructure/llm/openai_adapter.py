"""Lightweight OpenAI adapter implementing LLMInterface.

This adapter mirrors the Anthropic adapter and provides a minimal implementation.
In production this would wrap the OpenAI SDK.
"""

from __future__ import annotations

from typing import Any, List, Optional

from .llm_client import LLMClient
from ...core.interfaces.llm_interface import LLMResponse


class OpenAIAdapter(LLMClient):
    def invoke(
        self,
        prompt: str,
        model_id: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        return super().invoke(prompt, model_id, max_tokens, temperature, stop, **kwargs)


__all__ = ["OpenAIAdapter"]
