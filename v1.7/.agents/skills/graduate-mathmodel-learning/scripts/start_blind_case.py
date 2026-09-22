#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, sys
from datetime import datetime, timezone

p=argparse.ArgumentParser()
p.add_argument("--case-id", required=True)
p.add_argument("--problem-fingerprint", required=True, help="hash or stable identifier for problem+attachments")
p.add_argument("--output", default=None)
p.add_argument("--solution-exposure", choices=["false","true"], default="false")
args=p.parse_args()

out = Path(args.output) if args.output else Path("learning_output/context") / f"{args.case_id}_blind_gate.json"
out.parent.mkdir(parents=True, exist_ok=True)

# Existing evidence is authoritative: initialization must not erase exposure/freeze.
if out.exists():
    try:
        previous=json.loads(out.read_text(encoding="utf-8"))
        if previous.get("case_id") != args.case_id or previous.get("problem_fingerprint") != args.problem_fingerprint:
            raise ValueError("case/fingerprint mismatch; use a separate record")
        if type(previous.get("fresh_blind_eligible")) is not bool or type(previous.get("solution_exposure_before_matrix")) is not bool:
            raise ValueError("invalid previous gate")
        if args.solution_exposure == "true":
            previous["solution_exposure_before_matrix"]=True
        previous["fresh_blind_eligible"] = previous["fresh_blind_eligible"] and not previous["solution_exposure_before_matrix"]
        out.write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding="utf-8")
        print(f"[PRESERVED] fresh_blind_eligible={previous['fresh_blind_eligible']}")
        sys.exit(0)
    except (ValueError,TypeError) as e:
        print(f"[FAIL] existing gate not overwritten: {e}"); sys.exit(2)

record={
    "schema_version":"1.5",
    "case_id":args.case_id,
    "created_at":datetime.now(timezone.utc).isoformat(),
    "problem_fingerprint":args.problem_fingerprint,
    "solution_exposure_before_matrix":args.solution_exposure=="true",
    "matrix_frozen":False,
    "fresh_blind_eligible":args.solution_exposure=="false",
    "rule":"If any paper/code/solution profile was read before matrix freeze, fresh_blind_eligible must remain false."
}
out.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"[{'ELIGIBLE' if record['fresh_blind_eligible'] else 'CONTAMINATED'}] {out}")
