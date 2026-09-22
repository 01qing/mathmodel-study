#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path.cwd()
SKILL=ROOT/".agents"/"skills"/"graduate-mathmodel-learning"
catalog=SKILL/"assets"/"catalog"/"source_catalog_2021_2025.json"

errors=[]
if not catalog.exists():
    errors.append("source catalog missing")
else:
    try:
        obj=json.loads(catalog.read_text(encoding="utf-8"))
        years=obj.get("years",{})
        for y in ["2021","2022","2023","2024","2025"]:
            if y not in years:
                errors.append(f"missing year {y}")
        if years.get("2025",{}).get("excellent_papers",{}).get("status") not in [
            "gap_not_yet_indexed","confirmed","partially_verified"
        ]:
            errors.append("2025 excellent-paper status invalid")
    except Exception as e:
        errors.append(f"invalid source catalog json: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] source catalog valid")
