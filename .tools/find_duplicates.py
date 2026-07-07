"""Find duplicate filenames in the repository (excluding common build/vendor dirs)."""
from collections import defaultdict
import os

EXCLUDE = {"node_modules", ".venv", "venv", ".git", "storybook-static", "build", "dist", "__pycache__"}

def main():
    byname = defaultdict(list)
    for root, dirs, files in os.walk('.', topdown=True):
        # prune
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for f in files:
            byname[f].append(os.path.join(root, f))

    dups = {k: v for k, v in byname.items() if len(v) > 1}
    if not dups:
        print('No duplicate filenames found')
        return 0
    for name, paths in sorted(dups.items()):
        print('Duplicate:', name)
        for p in paths:
            print(' ', p)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
