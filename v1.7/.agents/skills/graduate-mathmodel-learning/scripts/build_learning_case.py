#!/usr/bin/env python3
from pathlib import Path
import argparse, json

p=argparse.ArgumentParser()
p.add_argument("--manifest", required=True)
p.add_argument("--root", default="learning_sources/competitions")
args=p.parse_args()

m=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
year=str(m["year"])
pid=str(m["problem_id"])
base=Path(args.root)/year/pid

for sub in [
    "problem","data","papers","code","expert_commentary",
    "literature","metadata","audit","reproduction"
]:
    (base/sub).mkdir(parents=True,exist_ok=True)

(base/"metadata"/"case_manifest.json").write_text(
    json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8"
)

readme=f"""# {m['case_id']}

Title: {m.get('title', m.get('canonical_working_title',''))}
Year: {year}
Problem: {pid}

## Workflow

1. materialize problem + attachments
2. verify source provenance
3. fresh blind problem-structure analysis
4. data/code audit
5. model competition
6. excellent-paper review
7. reproduction
8. knowledge extraction

Formal competition outputs remain under `paper_output/`; this learning workspace does not replace the original S0-S8 workflow.
"""
(base/"README.md").write_text(readme,encoding="utf-8")
print("[PASS] learning case workspace:",base)
