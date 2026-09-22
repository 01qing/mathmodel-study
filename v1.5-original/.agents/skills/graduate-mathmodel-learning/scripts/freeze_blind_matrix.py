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
g["matrix_frozen"]=True
g["matrix_sha256"]=hashlib.sha256(data).hexdigest()
g["matrix_frozen_at"]=datetime.now(timezone.utc).isoformat()
if g.get("solution_exposure_before_matrix"):
    g["fresh_blind_eligible"]=False
gpath.write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"[PASS] matrix frozen; fresh_blind_eligible={g['fresh_blind_eligible']}")
