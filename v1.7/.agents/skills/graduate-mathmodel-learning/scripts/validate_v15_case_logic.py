#!/usr/bin/env python3
from pathlib import Path
import json, sys

base=Path(".agents/skills/graduate-mathmodel-learning/assets/cases")
errors=[]

def load(name):
    try: return json.loads((base/name).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{name}: {e}")
        return {}

c=load("2024_C_blind_contamination.json")
m=load("2024_C_independent_model_competition.json")
p=load("2024_C_paper_access_queue.json")

if c.get("fresh_blind_status")!="CONTAMINATED":
    errors.append("2024 C must be contaminated, not fresh blind")
if "NOT_FRESH_BLIND" not in m.get("analysis_status",""):
    errors.append("matrix status must preserve non-blind label")
if set(m.get("questions",{})) != {"Q1","Q2","Q3","Q4","Q5"}:
    errors.append("matrix must contain Q1-Q5")
q5=m.get("questions",{}).get("Q5",{})
obj=q5.get("objectives",{})
if "minimize" not in obj or "maximize" not in obj:
    errors.append("Q5 objective completeness failed")
count=p.get("full_paper_materialization",{}).get("materialized_count")
if type(count) is not int or count < 0:
    errors.append("materialized_count must be a nonnegative integer")
elif count:
    from validate_paper_inventory import validate
    papers=p.get("materialized_papers",[])
    if len(papers)!=count: errors.append("materialized papers need file evidence")
    errors.extend(validate(papers,base))
if not p.get("do_not_promote_profiles_to_papers"):
    errors.append("profile/paper boundary missing")

if errors:
    print("[FAIL]")
    for e in errors: print("-",e)
    sys.exit(1)
print("[PASS] v1.5 blind-order, model-competition and paper-access contracts valid")
