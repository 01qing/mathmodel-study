#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--manifest", default=".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_case_manifest.json")
args=p.parse_args()
path=Path(args.manifest)
errors=[]
if not path.exists():
    errors.append(f"missing manifest: {path}")
else:
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
        if len(obj.get("problem_assets",[])) < 2:
            errors.append("too few problem assets")
        minp=obj.get("first_pass_requirements",{}).get("minimum_papers_to_download",2)
        if len(obj.get("excellent_papers",[])) < minp:
            errors.append("not enough indexed excellent papers")
        if obj.get("title_status")=="conflicted" and not obj.get("conflicts"):
            errors.append("conflicted title without conflicts[]")
        if obj.get("title_status")=="resolved" and not obj.get("title_resolution"):
            errors.append("resolved title without title_resolution")
        screening=obj.get("paper_screening",{})
        selected=screening.get("selected_primary_papers",[])
        if screening.get("screening_status")=="PRIMARY_PAIR_SELECTED" and len(selected) < 2:
            errors.append("PRIMARY_PAIR_SELECTED requires at least two selected papers")
        profiles=screening.get("profiles",{})
        for f in selected:
            if f not in profiles:
                errors.append(f"selected paper missing profile: {f}")
    except Exception as e:
        errors.append(f"invalid manifest json: {e}")
if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] case manifest valid")
