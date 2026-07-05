import ast, os, sys
from collections import defaultdict

ROOT = 'src/backend/api'
modules = {}

for root, _, files in os.walk(ROOT):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            mod = os.path.relpath(path, 'src').replace(os.path.sep, '.')[:-3]  # backend.api....
            modules[mod] = path

edges = defaultdict(set)

for mod, path in modules.items():
    try:
        src = open(path, encoding='utf8').read()
    except Exception:
        continue
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                name = n.name
                if name.startswith('backend.api'):
                    edges[mod].add(name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith('backend.api'):
                edges[mod].add(node.module)

# detect cycles
visited = {}
stack = []
cycles = []


def dfs(n):
    visited[n] = 1
    stack.append(n)
    for m in edges.get(n,[]):
        if m not in modules:
            continue
        if m not in visited:
            dfs(m)
        elif visited[m] == 1:
            # cycle found from m to n
            idx = stack.index(m)
            cycles.append(stack[idx:]+[m])
    visited[n] = 2
    stack.pop()

for n in modules:
    if n not in visited:
        dfs(n)

if cycles:
    print('FOUND', len(cycles), 'cycles')
    for c in cycles:
        print(' -> '.join(c))
    sys.exit(2)
print('NO_CYCLES')
