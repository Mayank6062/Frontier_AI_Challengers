import os

# Package path shim: make top-level `backend` package resolve to `src/backend`
# so tests and tools running from the repo root can import `backend.*` directly.
__path__.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "backend"))
)
