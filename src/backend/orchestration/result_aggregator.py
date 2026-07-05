from __future__ import annotations

from typing import List

from .models import StageResult, WorkflowContext


class ResultAggregator:
    """Aggregates stage results into the WorkflowContext.

    Strictly structural: it merges outputs under the stage_id key. It does not
    perform any business reasoning or interpretation.
    """

    def aggregate(self, ctx: WorkflowContext, results: List[StageResult]) -> None:
        """Merge outputs and aggregate metadata (confidence, citations, errors).

        Aggregation is structural only; it records per-stage outputs under
        their stage id and collects confidence/citation/error summaries under
        a reserved `_meta` key.
        """
        meta = ctx.accumulated.setdefault("_meta", {})
        confidences = meta.setdefault("confidences", {})
        citations = meta.setdefault("citations", {})
        errors = meta.setdefault("errors", {})

        for r in results:
            # merge stage output
            if r.output:
                ctx.accumulated.setdefault(r.stage_id, {})
                ctx.accumulated[r.stage_id].update(r.output)

            # collect confidence
            if r.confidence is not None:
                confidences[r.stage_id] = r.confidence

            # collect citations
            if r.citations:
                citations[r.stage_id] = list(r.citations)

            # collect errors
            if r.error or (r.errors and len(r.errors) > 0):
                errs: List[str] = []
                if r.error:
                    errs.append(r.error)
                errs.extend(r.errors or [])
                errors[r.stage_id] = errs
