from __future__ import annotations

from typing import List, Optional, Dict, Set
from pydantic import BaseModel, Field
from ..enums import (
    ArchitectureFilterCategory,
    ArchitectureSortBy,
    DependencyLayoutAlgorithm,
    DependencyDirection,
    RiskSortBy,
    SortDirection,
    RiskCategory,
    RiskStatus,
    CitationGroupBy,
    TimelineEventType,
    TimelineZoomLevel,
)


class ArchitectureExplorerState(BaseModel):
    tree: List[Dict[str, object]] = Field(default_factory=list)
    selected_node: Optional[str] = None
    expanded_nodes: List[str] = Field(default_factory=list)
    filter_text: str = ""
    filter_category: ArchitectureFilterCategory = ArchitectureFilterCategory.ALL
    sort_by: ArchitectureSortBy = ArchitectureSortBy.NAME
    loading: bool = False
    error: Optional[str] = None
    empty_reason: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class DependencyExplorerState(BaseModel):
    graph: Dict[str, List[str]] = Field(default_factory=dict)
    selected_node: Optional[str] = None
    highlighted_path: Optional[List[str]] = None
    layout_algorithm: DependencyLayoutAlgorithm = DependencyLayoutAlgorithm.FORCE
    filter_technology: List[str] = Field(default_factory=list)
    filter_direction: DependencyDirection = DependencyDirection.BOTH
    loading: bool = False
    error: Optional[str] = None
    empty_reason: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class RiskExplorerState(BaseModel):
    risks: List[Dict[str, object]] = Field(default_factory=list)
    selected_risk: Optional[str] = None
    sort_by: RiskSortBy = RiskSortBy.SCORE
    sort_direction: SortDirection = SortDirection.DESC
    filter_severity: Set[RiskCategory] = Field(default_factory=set)
    filter_category: Set[RiskCategory] = Field(default_factory=set)
    filter_status: Set[RiskStatus] = Field(default_factory=set)
    heatmap_view: bool = False
    loading: bool = False
    error: Optional[str] = None
    empty_reason: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class CitationExplorerState(BaseModel):
    citations: List[Dict[str, object]] = Field(default_factory=list)
    selected_citation: Optional[str] = None
    group_by: CitationGroupBy = CitationGroupBy.CATEGORY
    filter_category: Set[str] = Field(default_factory=set)
    filter_agent: Set[str] = Field(default_factory=set)
    search_text: str = ""
    sort_by: Optional[str] = None
    loading: bool = False
    error: Optional[str] = None
    empty_reason: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class TimelineExplorerState(BaseModel):
    events: List[Dict[str, object]] = Field(default_factory=list)
    selected_event: Optional[str] = None
    filter_event_type: Set[TimelineEventType] = Field(default_factory=set)
    zoom_level: TimelineZoomLevel = TimelineZoomLevel.OVERVIEW
    loading: bool = False
    error: Optional[str] = None
    empty_reason: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class ExplorerRegistry(BaseModel):
    architecture: ArchitectureExplorerState = Field(
        default_factory=ArchitectureExplorerState
    )
    dependency: DependencyExplorerState = Field(default_factory=DependencyExplorerState)
    risk: RiskExplorerState = Field(default_factory=RiskExplorerState)
    citation: CitationExplorerState = Field(default_factory=CitationExplorerState)
    timeline: TimelineExplorerState = Field(default_factory=TimelineExplorerState)

    model_config = {"extra": "forbid", "frozen": True}
