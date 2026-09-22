#!/usr/bin/env python3
from pathlib import Path
import json, sys

path=Path(".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_external_code_audit.json")
errors=[]
if not path.exists():
    errors.append("audit asset missing")
else:
    obj=json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema_version")!="1.1":
        errors.append("schema_version != 1.1")
    if len(obj.get("audited_files",[]))<5:
        errors.append("too few audited files")
    findings=obj.get("findings",[])
    if not any(x.get("severity")=="critical" for x in findings):
        errors.append("no critical finding")
    if not any(x.get("finding_type")=="strength" for x in findings):
        errors.append("audit should include strengths, not only faults")
    if not any(x.get("status")=="unresolved" for x in findings):
        errors.append("audit should preserve unresolved evidence gaps")
if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] external code audit contract valid")
