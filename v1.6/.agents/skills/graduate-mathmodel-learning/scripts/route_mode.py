#!/usr/bin/env python3
import argparse, json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--mode", required=True, choices=["learn","competition","paper-review","review","practice"])
args=p.parse_args()

ROOT=Path.cwd()
base = ROOT/".agents"/"skills"/"paper-workflow-orchestrator"/"SKILL.md"

routes = {
 "learn": {
   "entry":"graduate-mathmodel-learning",
   "formal_orchestrator_required":False,
   "read":["learning_state","problem_analysis?","model_route?","learning_sources"],
   "write":["learning_output","knowledge_base"]
 },
 "competition": {
   "entry":"paper-workflow-orchestrator",
   "formal_orchestrator_required":True,
   "read":["workflow_guard","formal contracts","learning_state(optional)"],
   "write":["paper_output via original workflow","learning_output/session(optional)"]
 },
 "paper-review": {
   "entry":"graduate-mathmodel-learning",
   "formal_orchestrator_required":False,
   "read":["problem","paper","code?","learning_state","formal contracts?"],
   "write":["learning_output/comparisons","knowledge_base/paper_reviews"]
 },
 "review": {
   "entry":"graduate-mathmodel-learning",
   "formal_orchestrator_required":False,
   "read":["session","formal contracts?","learning_state"],
   "write":["competition_lessons","error_patterns","learning_state"]
 },
 "practice": {
   "entry":"graduate-mathmodel-learning",
   "formal_orchestrator_required":False,
   "read":["problem","learning_state"],
   "write":["learning_output/practice","session","learning_state"]
 }
}
out=routes[args.mode]
out["original_orchestrator_present"]=base.exists()
if args.mode=="competition" and not base.exists():
    out["status"]="BLOCKED"
    out["reason"]="paper-workflow-orchestrator not found"
else:
    out["status"]="READY"
print(json.dumps(out,ensure_ascii=False,indent=2))
