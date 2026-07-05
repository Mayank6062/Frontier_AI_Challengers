"""Lightweight import validator for the API package.

Scans only `src/backend/api`, excludes common cache/build dirs, prints progress,
and detects forbidden imports such as `backend.infrastructure.*`.

Designed to be fast and safe: no subprocesses, no symlink following, and
will timeout after 30 seconds.
"""

import os
import re
import sys
import time

# Configuration
ROOT = os.path.join("src", "backend", "api")
EXCLUDE_DIRS = {
    ".venv",
    "venv",
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
    "htmlcov",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

# Forbidden import prefixes
FORBIDDEN_MODULES = (
    "infrastructure",
    "agents",
    "orchestrator",
    "workflow",
    "knowledge",
    "frontend",
)

# Debug flag: set DEBUG=1 in env to enable verbose per-file printing
DEBUG = os.environ.get("DEBUG", "0") in ("1", "true", "True")

# Timing / timeout
START = time.time()
TIMEOUT_SECONDS = 30.0

forbidden_re = re.compile(
    r"\b(from)\s+backend\.(%s)\b|\b(import)\s+backend\.(%s)\b"
    % ("|".join(FORBIDDEN_MODULES), "|".join(FORBIDDEN_MODULES))
)

files_scanned = 0
imports_checked = 0
violations = []


def is_in_tests(path: str) -> bool:
    return os.path.sep + "tests" + os.path.sep in path or path.endswith(
        os.path.sep + "tests"
    )


def safe_read(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return None


if not os.path.isdir(ROOT):
    print("Target directory not found:", ROOT)
    sys.exit(0)

checked_files_since_progress = 0

for root, dirs, files in os.walk(ROOT, topdown=True, followlinks=False):
    # prune excluded dirs
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

    for fname in files:
        if time.time() - START > TIMEOUT_SECONDS:
            print("TIMEOUT")
            # graceful termination summary
            break

        if not fname.endswith(".py"):
            continue

        fpath = os.path.join(root, fname)

        # Skip test modules and known non-production files
        if is_in_tests(fpath):
            continue
        if os.path.normpath(fpath).endswith(
            os.path.normpath(os.path.join("di", "composition.py"))
        ):
            continue

        files_scanned += 1
        checked_files_since_progress += 1

        if DEBUG:
            print(f"Scanning: {fpath}")

        content = safe_read(fpath)
        if content is None:
            # couldn't read file; skip but keep scanning
            continue

        # Count import-like lines and check them
        for line in content.splitlines():
            if "import" not in line and "from" not in line:
                continue
            imports_checked += 1
            if forbidden_re.search(line):
                violations.append((fpath, line.strip()))

        if checked_files_since_progress >= 25:
            print(f"Checked {files_scanned} files...")
            checked_files_since_progress = 0

    else:
        # continue outer loop if not broken by timeout
        continue
    # broken due to timeout
    break

elapsed = time.time() - START

print("\nSummary:")
print("Total files scanned:", files_scanned)
print("Total imports checked:", imports_checked)
print("Forbidden imports found:", len(violations))
print("Execution time: %.3fs" % elapsed)

if violations:
    print("\nViolations:")
    for p, line in violations:
        print(p)
        print("  ", line)

if elapsed > TIMEOUT_SECONDS:
    print("TIMEOUT")
    print("FAIL")
    sys.exit(2)

if violations:
    print("FAIL")
    sys.exit(2)

print("PASS")
sys.exit(0)
