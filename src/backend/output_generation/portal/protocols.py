"""Protocol interfaces for the Portal package (contracts-only).

All Protocols are declaration-only (no implementation). Keep signatures
typed and generic where appropriate.
"""

from __future__ import annotations

from typing import Protocol, Sequence, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import (
        PortalState,
        PortalRoute,
        RouteMatch,
        SearchIndex,
        SearchEntry,
        LayoutModel,
    )


class PortalBuilder(Protocol):
    def build(self, config: Dict[str, object]) -> "PortalState": ...


class PortalRouter(Protocol):
    def resolve(self, path: str) -> "RouteMatch": ...


class PortalRegistry(Protocol):
    def register_route(self, route: "PortalRoute") -> str: ...


class PortalSearchEngine(Protocol):
    def index(self, index: "SearchIndex") -> None: ...

    def query(self, q: str, top_k: int = 10) -> Sequence["SearchEntry"]: ...


class PortalNavigationManager(Protocol):
    def go_to(self, path: str) -> None: ...


class PortalLayoutManager(Protocol):
    def get_layout(self) -> "LayoutModel": ...


class PortalThemeEngine(Protocol):
    def list_themes(self) -> Sequence[Any]: ...


class PortalAccessibilityManager(Protocol):
    def check(self, state: PortalState) -> Dict[str, object]: ...


class PortalCommandPalette(Protocol):
    def register(self, entry: Any) -> None: ...

    def query(self, q: str, top_k: int = 10) -> Sequence[Any]: ...


class PortalExplorerManager(Protocol):
    def get_explorer(self, name: str) -> Any: ...
