#!/usr/bin/env python3
from pathlib import Path
import json, shutil

ROOT = Path.cwd()
SKILL = ROOT / ".agents" / "skills" / "graduate-mathmodel-learning"
TEMPLATES = SKILL / "templates"

DIRS = [
    ROOT/"learning_sources"/"competitions",
    ROOT/"learning_output"/"context",
    ROOT/"learning_output"/"sessions",
    ROOT/"learning_output"/"analyses",
    ROOT/"learning_output"/"comparisons",
    ROOT/"learning_output"/"practice",
    ROOT/"knowledge_base"/"methods",
    ROOT/"knowledge_base"/"problem_patterns",
    ROOT/"knowledge_base"/"paper_reviews",
    ROOT/"knowledge_base"/"competition_lessons",
    ROOT/"knowledge_base"/"error_patterns",
]
for d in DIRS:
    d.mkdir(parents=True, exist_ok=True)

copies = [
    (TEMPLATES/"learning_state.json", ROOT/"learning_output"/"context"/"learning_state.json"),
    (TEMPLATES/"source_index.json", ROOT/"learning_sources"/"source_index.json"),
]
for src,dst in copies:
    if not dst.exists():
        shutil.copy2(src,dst)

next_file = ROOT/"learning_output"/"context"/"next_learning.md"
if not next_file.exists():
    next_file.write_text("# Next Learning\n\n- 尚未设置。\n", encoding="utf-8")

for year in range(2021, 2026):
    (ROOT/"learning_sources"/"competitions"/str(year)).mkdir(parents=True, exist_ok=True)

print("[PASS] learning workspace initialized")
