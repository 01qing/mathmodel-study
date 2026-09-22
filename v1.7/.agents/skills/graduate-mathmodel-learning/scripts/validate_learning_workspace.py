#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path.cwd()
required = [
    ROOT/".agents"/"skills"/"graduate-mathmodel-learning"/"SKILL.md",
    ROOT/"learning_sources"/"source_index.json",
    ROOT/"learning_output"/"context"/"learning_state.json",
    ROOT/"learning_output"/"context"/"next_learning.md",
    ROOT/"knowledge_base"/"methods",
    ROOT/"knowledge_base"/"problem_patterns",
    ROOT/"knowledge_base"/"paper_reviews",
]
errors=[]
for p in required:
    if not p.exists():
        errors.append(f"missing: {p}")

for p in [ROOT/"learning_sources"/"source_index.json",
          ROOT/"learning_output"/"context"/"learning_state.json"]:
    if p.exists():
        try:
            obj=json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(obj, dict):
                errors.append(f"not object: {p}")
        except Exception as e:
            errors.append(f"invalid json: {p}: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)

print("[PASS] learning workspace is valid")
