import os
import re
import sys

ROOT = "src/backend/api"
patterns = [
    r"CacheService\s*\(",
    r"StorageService\s*\(",
    r"SessionStore\s*\(",
    r"EngagementStore\s*\(",
    r"SecretsManager\s*\(",
    r"LedgerService\s*\(",
    r"LLMClient\s*\(",
    r"Logger\s*\(",
    r"Metrics\s*\(",
]
violations = []
for root, dirs, files in os.walk(ROOT):
    # skip test dirs under api
    if "tests" in dirs:
        dirs.remove("tests")
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            s = open(p, encoding="utf8").read()
            for pat in patterns:
                if re.search(pat, s):
                    violations.append((p, pat))

print("FOUND", len(violations), "instantiations")
for v in violations:
    print(v[0])
if violations:
    sys.exit(2)
print("NO_DIRECT_INSTANTIATIONS")
