from __future__ import annotations

from typing import Protocol
from pathlib import Path
import shutil


class OutputStorageService(Protocol):
    async def write(self, src_path: str, dest_key: str) -> str:
        ...

    async def read(self, key: str) -> bytes:
        ...


class FilesystemOutputStorage:
    """Simple filesystem-backed OutputStorageService for tests and local runs."""

    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    async def write(self, src_path: str, dest_key: str) -> str:
        dest = self.root / dest_key
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest)
        return str(dest)

    async def read(self, key: str) -> bytes:
        p = self.root / key
        return p.read_bytes()
