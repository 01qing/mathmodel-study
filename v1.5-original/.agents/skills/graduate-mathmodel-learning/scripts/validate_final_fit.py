#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--final-json", default="learning_output/final_fit/gmcm-2021-D/final_fit.json")
args=p.parse_args()
path=Path(args.final_json)
errors=[]

if not path.exists():
    errors.append(f"missing final fit: {path}")
else:
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
        if obj.get("schema_version")!="1.0":
            errors.append("schema_version != 1.0")
        iso=obj.get("test_isolation",{})
        if iso.get("test_used_for_model_selection") is not False:
            errors.append("test used for model selection")
        if iso.get("test_used_for_hyperparameter_selection") is not False:
            errors.append("test used for hyperparameter selection")
        q2=obj.get("q2",{})
        if not q2.get("route"):
            errors.append("missing q2 route")
        if not q2.get("selected_features"):
            errors.append("missing final selected features")
        if not q2.get("test_predictions"):
            errors.append("missing q2 predictions")
        for lab,info in obj.get("q3",{}).items():
            if info.get("status")=="PASS" and not info.get("predictions"):
                errors.append(f"missing q3 predictions: {lab}")
    except Exception as e:
        errors.append(f"invalid final-fit json: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] final-fit contract valid")
