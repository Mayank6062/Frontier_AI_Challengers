"""Minimal LLM client implementation that conforms to LLMInterface.

This implementation is a deterministic local adapter that echoes the prompt
into `LLMResponse.text` for testing purposes.
"""

from __future__ import annotations

from typing import Any, List, Optional

from ...core.interfaces.llm_interface import LLMInterface, LLMResponse


class LLMClient(LLMInterface):
    def __init__(self) -> None:
        # No global instantiation; constructor injection would be used in prod.
        pass

    def invoke(
        self,
        prompt: str,
        model_id: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        # Minimal normalization: echo prompt
        return LLMResponse(
            text=prompt,
            raw=None,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
        )


__all__ = ["LLMClient"]
