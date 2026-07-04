"""Anthropic adapter placeholder implementing LLMInterface.

This adapter is intentionally minimal and mirrors the same API as other
adapters; in production this would wrap the Anthropic SDK.
"""

from __future__ import annotations

from typing import Any, List, Optional

from .llm_client import LLMClient
from ...core.interfaces.llm_interface import LLMResponse


class AnthropicAdapter(LLMClient):
    def invoke(
        self,
        prompt: str,
        model_id: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        # For now delegate to LLMClient behavior
        return super().invoke(prompt, model_id, max_tokens, temperature, stop, **kwargs)


__all__ = ["AnthropicAdapter"]
