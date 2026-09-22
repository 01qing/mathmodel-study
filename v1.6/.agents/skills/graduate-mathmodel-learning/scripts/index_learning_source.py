#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, datetime, urllib.parse

p=argparse.ArgumentParser()
p.add_argument("--path-or-url", required=True)
p.add_argument("--source-type", required=True,
 choices=["problem","official_attachment","excellent_paper","expert_commentary","code","dataset","academic_literature","other"])
p.add_argument("--year", type=int)
p.add_argument("--problem-id")
p.add_argument("--title")
p.add_argument("--award-claim")
p.add_argument("--award-verified", action="store_true")
args=p.parse_args()

ROOT=Path.cwd()
idx=ROOT/"learning_sources"/"source_index.json"
if not idx.exists():
    raise SystemExit("run init_learning_workspace.py first")

data=json.loads(idx.read_text(encoding="utf-8"))
value=args.path_or_url
sha=None
local=Path(value)
if local.exists() and local.is_file():
    h=hashlib.sha256()
    with local.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    sha=h.hexdigest()

key=f"{value}|{sha or ''}"
for r in data.get("sources",[]):
    if r.get("_dedup_key")==key:
        print("[SKIP] source already indexed:",r["source_id"])
        raise SystemExit(0)

sid=f"src-{len(data.get('sources',[]))+1:05d}"
rec={
 "source_id":sid,
 "competition":"全国研究生数学建模竞赛",
 "year":args.year,
 "problem_id":args.problem_id,
 "source_type":args.source_type,
 "title":args.title,
 "path_or_url":value,
 "sha256":sha,
 "award_claim":args.award_claim,
 "award_verified":bool(args.award_verified),
 "retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verification_status":"not_verified",
 "notes":[],
 "_dedup_key":key
}
data.setdefault("sources",[]).append(rec)
idx.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print("[PASS] indexed",sid)
