#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil

p=argparse.ArgumentParser()
p.add_argument("--type", required=True, choices=["method","problem-pattern","paper-review","session"])
p.add_argument("--id", required=True)
args=p.parse_args()
ROOT=Path.cwd()
SKILL=ROOT/".agents"/"skills"/"graduate-mathmodel-learning"
mapping={
 "method":("method_card.json",ROOT/"knowledge_base"/"methods"),
 "problem-pattern":("problem_pattern.json",ROOT/"knowledge_base"/"problem_patterns"),
 "paper-review":("paper_review.json",ROOT/"knowledge_base"/"paper_reviews"),
 "session":("session_record.json",ROOT/"learning_output"/"sessions"),
}
tpl,folder=mapping[args.type]
folder.mkdir(parents=True,exist_ok=True)
obj=json.loads((SKILL/"templates"/tpl).read_text(encoding="utf-8"))
field={"method":"method_id","problem-pattern":"pattern_id","paper-review":"review_id","session":"session_id"}[args.type]
obj[field]=args.id
dst=folder/f"{args.id}.json"
if dst.exists():
    print("[SKIP] exists",dst)
else:
    dst.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    print("[PASS] created",dst)
