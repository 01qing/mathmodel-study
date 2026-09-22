#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--comparison-json", default="learning_output/comparisons/gmcm-2021-D/paper_vs_benchmark.json")
args=p.parse_args()

ROOT=Path.cwd()
path=Path(args.comparison_json)
if not path.exists():
    raise SystemExit("comparison missing")
obj=json.loads(path.read_text(encoding="utf-8"))

for q,row in obj.get("questions",{}).items():
    if row.get("agent_review_required") is True:
        raise SystemExit(f"{q} still requires agent review; do not extract knowledge yet")

kc=obj.get("knowledge_candidates",{})

targets={
    "methods":ROOT/"knowledge_base"/"methods",
    "problem_patterns":ROOT/"knowledge_base"/"problem_patterns",
    "error_patterns":ROOT/"knowledge_base"/"error_patterns",
    "competition_lessons":ROOT/"knowledge_base"/"competition_lessons",
}
written=[]

for kind,folder in targets.items():
    folder.mkdir(parents=True,exist_ok=True)
    for item in kc.get(kind,[]):
        if not isinstance(item,dict):
            continue
        item_id=item.get("id")
        if not item_id:
            continue
        payload={
            "schema_version":"1.0",
            "knowledge_type":kind,
            "id":item_id,
            "title":item.get("title",item_id),
            "claim":item.get("claim",""),
            "evidence_status":item.get("evidence_status","our_inference"),
            "source_case":"gmcm-2021-D",
            "source_refs":item.get("source_refs",[]),
            "applicability":item.get("applicability",[]),
            "failure_conditions":item.get("failure_conditions",[]),
            "notes":item.get("notes",[])
        }
        out=folder/f"{item_id}.json"
        out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
        written.append(str(out))

manifest={
    "schema_version":"1.0",
    "case_id":"gmcm-2021-D",
    "written":written,
    "count":len(written)
}
outdir=ROOT/"learning_output"/"knowledge_extraction"/"gmcm-2021-D"
outdir.mkdir(parents=True,exist_ok=True)
(outdir/"knowledge_extraction_manifest.json").write_text(
    json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8"
)
print(f"[PASS] knowledge cards written: {len(written)}")
