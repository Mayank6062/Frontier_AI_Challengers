"""Interfaces re-exports for the portal package.

This module intentionally re-exports Protocols from `protocols.py` so that
existing imports of `portal.interfaces` continue to work while the package
adopts the canonical contracts-only layout.
"""

from __future__ import annotations

from .protocols import (
    PortalBuilder,
    PortalRouter,
    PortalRegistry,
    PortalSearchEngine,
    PortalNavigationManager,
    PortalLayoutManager,
    PortalThemeEngine,
    PortalAccessibilityManager,
    PortalCommandPalette,
    PortalExplorerManager,
)

__all__ = [
    "PortalBuilder",
    "PortalRouter",
    "PortalRegistry",
    "PortalSearchEngine",
    "PortalNavigationManager",
    "PortalLayoutManager",
    "PortalThemeEngine",
    "PortalAccessibilityManager",
    "PortalCommandPalette",
    "PortalExplorerManager",
]
