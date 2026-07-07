from __future__ import annotations

from pathlib import Path
import zipfile
import tarfile


class ArchiveBuilder:
    """Creates archives (zip or tar.gz) for a folder."""

    @staticmethod
    def create_zip(source_dir: str, dest_file: str, compress: bool = True) -> str:
        src = Path(source_dir)
        dest = Path(dest_file)
        compression = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
        with zipfile.ZipFile(dest, "w", compression=compression) as zf:
            for path in src.rglob("*"):
                arcname = path.relative_to(src)
                zf.write(path, arcname)
        return str(dest)

    @staticmethod
    def create_tar_gz(source_dir: str, dest_file: str) -> str:
        src = Path(source_dir)
        dest = Path(dest_file)
        with tarfile.open(dest, "w:gz") as tf:
            tf.add(str(src), arcname=".")
        return str(dest)
