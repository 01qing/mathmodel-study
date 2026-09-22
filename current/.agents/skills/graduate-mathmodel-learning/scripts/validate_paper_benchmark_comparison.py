#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--comparison-json", default="learning_output/comparisons/gmcm-2021-D/paper_vs_benchmark.json")
p.add_argument("--require-reviewed", action="store_true")
args=p.parse_args()

path=Path(args.comparison_json)
errors=[]
if not path.exists():
    errors.append(f"missing comparison: {path}")
else:
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
        if obj.get("schema_version")!="1.0":
            errors.append("schema_version != 1.0")
        if len(obj.get("papers",{}))<2:
            errors.append("need two papers")
        for q in ["Q1","Q2","Q3","Q4"]:
            row=obj.get("questions",{}).get(q)
            if not row:
                errors.append(f"missing {q}")
                continue
            if args.require_reviewed:
                if row.get("agent_review_required") is True:
                    errors.append(f"{q} still requires agent review")
                if not row.get("preferred_learning_source"):
                    errors.append(f"{q} missing preferred learning source")
        if args.require_reviewed:
            kc=obj.get("knowledge_candidates",{})
            if not any(kc.get(k) for k in ["methods","problem_patterns","error_patterns","competition_lessons"]):
                errors.append("reviewed comparison has no knowledge candidates")
    except Exception as e:
        errors.append(f"invalid comparison json: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] comparison contract valid")
