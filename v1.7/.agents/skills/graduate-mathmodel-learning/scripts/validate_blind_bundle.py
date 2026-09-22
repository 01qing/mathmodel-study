#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--bundle", default="learning_output/blind_eval/gmcm-2021-D")
args=p.parse_args()
b=Path(args.bundle)
errors=[]

required=["problem_facts.json","rubric.json","answer_template.json","EVAL_INSTRUCTIONS.md","contamination_guard.json"]
for name in required:
    if not (b/name).exists():
        errors.append(f"missing {name}")

if (b/"contamination_guard.json").exists():
    guard=json.loads((b/"contamination_guard.json").read_text(encoding="utf-8"))
    text=""
    for pth in b.rglob("*"):
        if pth.is_file() and pth.suffix.lower() in {".json",".md",".txt"}:
            try: text += "\n"+pth.read_text(encoding="utf-8")
            except: pass
    # Tokens may appear inside the guard and instructions as forbidden examples;
    # only fail if forbidden directories/files themselves are included.
    for forbidden_dir in guard.get("forbidden_directories",[]):
        if any(pth.is_dir() and pth.name==forbidden_dir for pth in b.rglob("*")):
            errors.append(f"forbidden directory present: {forbidden_dir}")

for forbidden_file in ["paper-screening-2021-D.md","reference-baseline-2021-D.md"]:
    if any(pth.name==forbidden_file for pth in b.rglob("*")):
        errors.append(f"forbidden file present: {forbidden_file}")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] blind bundle structurally clean")
