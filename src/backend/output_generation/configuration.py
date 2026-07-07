from __future__ import annotations

from pathlib import Path
from typing import Dict

DEFAULT_DIRS = {
    "templates": "templates/output_generation",
    "manifests": "manifests/output_generation",
    "themes": "themes/output_generation",
    "portals": "portals/output_generation",
    "diagrams": "diagrams/output_generation",
    "documentation": "documentation/output_generation",
    "exports": "exports/output_generation",
    "assets": "assets/output_generation",
}


def build_paths(base: Path) -> Dict[str, Path]:
    """Return mapping of configuration directories (not creating them).

    Callers can create them if desired. This keeps this module safe to import
    without side effects while providing the skeleton required by the
    implementation bible.
    """

    return {k: (base / v) for k, v in DEFAULT_DIRS.items()}


def create_skeleton(base: Path, create: bool = False) -> Dict[str, Path]:
    """Return mapping of paths and optionally create directories.

    Parameters
    - base: root path under which directories live
    - create: if True, actually create directories on disk
    """

    paths = build_paths(base)
    if create:
        for p in paths.values():
            p.mkdir(parents=True, exist_ok=True)
    return paths
