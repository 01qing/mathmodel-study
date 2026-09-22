#!/usr/bin/env python3
from pathlib import Path
import json, sys

base=Path(".agents/skills/graduate-mathmodel-learning/assets/cases")
audit_path=base/"2024_C_external_code_audit.json"
paper_path=base/"2024_C_paper_screening.json"
errors=[]

try:
    audit=json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("schema_version")!="1.4": errors.append("audit schema_version")
    if len(audit.get("audited_files",[]))<5: errors.append("too few audited files")
    if not any(x.get("severity")=="critical" for x in audit.get("findings",[])):
        errors.append("missing critical finding")
    if not any(x.get("finding_type")=="strength" for x in audit.get("findings",[])):
        errors.append("missing strengths")
    if not any(x.get("status")=="unresolved" for x in audit.get("findings",[])):
        errors.append("missing unresolved evidence gap")
    q5=[x for x in audit["findings"] if x["id"]=="Q5-second-objective-omitted"]
    if not q5 or q5[0]["severity"]!="critical":
        errors.append("Q5 omission not locked critical")
except Exception as e:
    errors.append(f"audit invalid: {e}")

try:
    paper=json.loads(paper_path.read_text(encoding="utf-8"))
    if paper.get("excellent_paper_pair_status")!="NOT_YET_SELECTED":
        errors.append("paper pair status must remain NOT_YET_SELECTED")
    profiles=paper.get("solution_profiles",[])
    if not any("champion" in x.get("profile_id","") for x in profiles):
        errors.append("champion solution profile missing")
except Exception as e:
    errors.append(f"paper screening invalid: {e}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] 2024 C code-audit and paper-screening contracts valid")
