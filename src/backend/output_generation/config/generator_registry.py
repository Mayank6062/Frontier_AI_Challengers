"""Register default generators into an OutputGeneratorFactory.

This helper wires the canonical generators required by the pipeline.
"""

from __future__ import annotations

from ..factory import OutputGeneratorFactory
from ..markdown.hld_generator import HLDGenerator
from ..markdown.lld_generator import LLDGenerator
from ..html.report_generator import ReportGenerator
from ..schemas import FormatGenerationResult
from typing import List


class CompositeMarkdownGenerator:
    """Runs HLD + LLD generators and merges results."""

    def __init__(self, hld: HLDGenerator, lld: LLDGenerator) -> None:
        self.hld = hld
        self.lld = lld

    async def generate(self, context):
        hres = await self.hld.generate(context)
        lres = await self.lld.generate(context)
        merged = FormatGenerationResult(
            artifacts=[*hres.artifacts, *lres.artifacts],
            generator_name="markdown",
            generator_version="0.1.0",
            warnings=[*hres.warnings, *lres.warnings],
            errors=[*hres.errors, *lres.errors],
        )
        return merged

    def get_output_file_type(self) -> str:
        return "text/markdown"

    def get_generator_version(self) -> str:
        return "0.1.0"

    def is_optional(self) -> bool:
        return False


def register_defaults(factory: OutputGeneratorFactory) -> None:
    """Register the canonical set of generators used by the pipeline."""
    hld = HLDGenerator()
    lld = LLDGenerator()
    report = ReportGenerator()

    factory.register("markdown", CompositeMarkdownGenerator(hld, lld))
    factory.register("html", report)


__all__ = ["register_defaults"]
