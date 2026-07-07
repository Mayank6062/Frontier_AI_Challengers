from __future__ import annotations

from typing import List
from pathlib import Path
import shutil

from .schemas import BundleManifest, ManifestFileEntry


class PersonaBundleResult:
    def __init__(self, persona: str, manifest: BundleManifest, output_path: str):
        self.persona = persona
        self.manifest = manifest
        self.output_path = output_path


class PersonaFilter:
    """Applies persona visibility matrix to produce persona-scoped bundle subsets."""

    def get_authorized_files(self, manifest: BundleManifest, persona: str) -> List[ManifestFileEntry]:
        """Returns all files whose persona_scope includes persona or is empty (all personas)."""
        authorized: List[ManifestFileEntry] = []
        for f in manifest.files:
            if not f.persona_scope or persona in f.persona_scope:
                authorized.append(f)
        return authorized

    def filter(self, master_manifest: BundleManifest, persona: str, source_path: str, output_path: str) -> PersonaBundleResult:
        """
        Copies authorized files to output_path.
        Generates persona-scoped manifest with only authorized files.
        Returns PersonaBundleResult.
        """
        src = Path(source_path)
        out = Path(output_path)
        out.mkdir(parents=True, exist_ok=True)

        authorized = self.get_authorized_files(master_manifest, persona)
        # Copy files
        for entry in authorized:
            src_file = src / entry.relative_path
            dest_file = out / entry.relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if src_file.exists():
                shutil.copy2(src_file, dest_file)

        # Build persona manifest (shallow copy)
        persona_manifest = master_manifest.copy()
        persona_manifest.files = authorized

        return PersonaBundleResult(persona=persona, manifest=persona_manifest, output_path=str(out))
