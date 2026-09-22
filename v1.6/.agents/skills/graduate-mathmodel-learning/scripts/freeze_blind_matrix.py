#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, sys
from datetime import datetime, timezone

p=argparse.ArgumentParser()
p.add_argument("--gate", required=True)
p.add_argument("--matrix", required=True)
args=p.parse_args()

gpath=Path(args.gate); mpath=Path(args.matrix)
g=json.loads(gpath.read_text(encoding="utf-8"))
if not mpath.exists():
    print("[FAIL] matrix missing"); sys.exit(2)
data=mpath.read_bytes()
try:
    matrix=json.loads(data)
    if not isinstance(matrix,dict) or not matrix:
        raise ValueError("matrix must be a nonempty JSON object")
    if type(g.get("fresh_blind_eligible")) is not bool or type(g.get("solution_exposure_before_matrix")) is not bool:
        raise ValueError("incomplete gate")
except (ValueError,TypeError) as e:
    print(f"[FAIL] {e}"); sys.exit(2)
digest=hashlib.sha256(data).hexdigest()
if g.get("matrix_frozen"):
    if g.get("matrix_sha256") != digest:
        print("[FAIL] frozen matrix differs; preserve original and record a separate retrospective revision"); sys.exit(2)
    print("[PASS] existing freeze preserved"); sys.exit(0)
g["matrix_frozen"]=True
g["matrix_sha256"]=hashlib.sha256(data).hexdigest()
g["matrix_frozen_at"]=datetime.now(timezone.utc).isoformat()
if g.get("solution_exposure_before_matrix"):
    g["fresh_blind_eligible"]=False
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"[PASS] matrix frozen; fresh_blind_eligible={g['fresh_blind_eligible']}")
