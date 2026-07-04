"""Pytest configuration for shared layer tests."""

import sys
from pathlib import Path

# Ensure the src/backend module is in the path for imports
shared_dir = Path(__file__).parent
backend_dir = shared_dir.parent
src_dir = backend_dir.parent

sys.path.insert(0, str(src_dir))
