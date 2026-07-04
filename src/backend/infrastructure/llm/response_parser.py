"""Simple response parser for LLM responses.

Parses `LLMResponse` into normalized text for the application core.
"""

from __future__ import annotations

from ...core.interfaces.llm_interface import LLMResponse


def parse_response(resp: LLMResponse) -> str:
    return resp.text


__all__ = ["parse_response"]
