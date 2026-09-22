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
