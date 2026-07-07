from __future__ import annotations

from pydantic import BaseModel, Field


class NodeRank(BaseModel):
    node_id: str
    score: float

    model_config = {"extra": "forbid", "frozen": True}


class RankingWeights(BaseModel):
    degree: float = 0.4
    cluster_root: float = 0.2
    risk: float = 0.2
    cost: float = 0.1
    confidence: float = 0.1

    model_config = {"extra": "forbid", "frozen": True}


class RankingConfiguration(BaseModel):
    weights: RankingWeights = Field(default_factory=RankingWeights)

    model_config = {"extra": "forbid", "frozen": True}


class NodeImportance(BaseModel):
    node_id: str
    importance: float

    model_config = {"extra": "forbid", "frozen": True}


class RankingStatistics(BaseModel):
    computed: int = 0

    model_config = {"extra": "forbid", "frozen": True}
