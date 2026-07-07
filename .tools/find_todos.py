"""Scan source files for TODO/FIXME/PLACEHOLDER markers (focused on src/).
Excludes common build and storybook-static directories.
"""
import os
import re

ROOT = 'src'
EXCLUDE = {'node_modules', '.venv', 'venv', '.git', 'storybook-static', 'build', 'dist', '__pycache__'}
PATTERN = re.compile(r"\b(TODO|FIXME|TBD|PLACEHOLDER|TEMP|STUB|mock)\b", re.I)

def main():
    hits = []
    for root, dirs, files in os.walk(ROOT, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for f in files:
            if not f.endswith(('.py', '.tsx', '.ts', '.js', '.jsx', '.md')):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    for i, line in enumerate(fh, start=1):
                        if PATTERN.search(line):
                            hits.append((path, i, line.strip()))
            except Exception:
                continue
    if not hits:
        print('No TODO/FIXME/PLACEHOLDER markers found in src/')
        return 0
    for p, ln, text in hits:
        print(f"{p}:{ln}: {text}")
    print(f"Total markers: {len(hits)}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
