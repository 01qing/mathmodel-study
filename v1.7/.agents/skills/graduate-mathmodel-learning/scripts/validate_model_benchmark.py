#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--benchmark-json", default="learning_output/model_benchmark/gmcm-2021-D/model_benchmark.json")
args=p.parse_args()
path=Path(args.benchmark_json)
errors=[]

if not path.exists():
    errors.append(f"missing benchmark: {path}")
else:
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
        if obj.get("schema_version")!="0.9":
            errors.append("schema_version != 0.9")
        if obj.get("test_isolation",{}).get("used_in_benchmark") is not False:
            errors.append("test set isolation violated")
        q2=obj.get("q1_q2",{})
        if not q2.get("recommended_pipeline"):
            errors.append("missing q2 recommendation")
        if len(q2.get("candidates",[]))<2:
            errors.append("too few q2 candidates")
        for lab,info in obj.get("q3",{}).items():
            if info.get("status")=="PASS" and not info.get("recommended_pipeline"):
                errors.append(f"missing recommendation for {lab}")
    except Exception as e:
        errors.append(f"invalid benchmark json: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] benchmark contract valid")
