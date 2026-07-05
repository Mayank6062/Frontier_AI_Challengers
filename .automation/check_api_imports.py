import os
import re

found = False
for root, _, files in os.walk("src/backend/api"):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            s = open(p, encoding="utf8").read()
            for bad in ("infrastructure", "agents", "orchestration", "knowledge"):
                if re.search(
                    rf"\bfrom\s+backend\.{bad}\b|\bimport\s+backend\.{bad}\b", s
                ):
                    print(p + ": imports " + bad)
                    found = True
if not found:
    print("No forbidden imports found")
