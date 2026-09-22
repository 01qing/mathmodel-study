#!/usr/bin/env python3
from pathlib import Path
import argparse, json, datetime

p=argparse.ArgumentParser()
p.add_argument("--mode", choices=["learn","competition","paper-review","review","practice"])
p.add_argument("--year", type=int)
p.add_argument("--problem-id")
p.add_argument("--question-id")
p.add_argument("--session-id")
p.add_argument("--method")
p.add_argument("--method-level", choices=["unseen","introduced","can_explain","can_apply_with_help","can_apply_independently","can_compare_and_adapt"])
p.add_argument("--method-evidence")
p.add_argument("--weak-point")
p.add_argument("--error-pattern")
p.add_argument("--pending-replication")
p.add_argument("--completed-problem")
p.add_argument("--next-action")
args=p.parse_args()

ROOT=Path.cwd()
path=ROOT/"learning_output"/"context"/"learning_state.json"
if not path.exists(): raise SystemExit("run init_learning_workspace.py first")
data=json.loads(path.read_text(encoding="utf-8"))
focus=data.setdefault("current_focus",{})

for k,v in [("mode",args.mode),("year",args.year),("problem_id",args.problem_id),("question_id",args.question_id),("session_id",args.session_id)]:
    if v is not None: focus[k]=v

if args.method:
    m=data.setdefault("methods",{}).setdefault(args.method,{"level":"unseen","evidence":[],"last_updated":None})
    if args.method_level:
        # No automatic sophistication inference. User/Agent supplies level.
        m["level"]=args.method_level
    if args.method_evidence and args.method_evidence not in m["evidence"]:
        m["evidence"].append(args.method_evidence)
    m["last_updated"]=datetime.datetime.now(datetime.timezone.utc).isoformat()

def add(field,val):
    if val:
        arr=data.setdefault(field,[])
        if val not in arr: arr.append(val)

add("weak_points",args.weak_point)
add("error_patterns",args.error_pattern)
add("pending_replications",args.pending_replication)
add("completed_problems",args.completed_problem)
add("next_actions",args.next_action)

path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
next_md=ROOT/"learning_output"/"context"/"next_learning.md"
next_md.write_text("# Next Learning\n\n" + "".join(f"- {x}\n" for x in data.get("next_actions",[])[:10]),encoding="utf-8")
print("[PASS] learning state updated")
