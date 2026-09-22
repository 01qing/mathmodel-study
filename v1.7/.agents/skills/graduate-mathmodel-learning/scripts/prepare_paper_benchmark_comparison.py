#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

p=argparse.ArgumentParser()
p.add_argument("--benchmark-json", default="learning_output/model_benchmark/gmcm-2021-D/model_benchmark.json")
p.add_argument("--final-json", default="learning_output/final_fit/gmcm-2021-D/final_fit.json")
p.add_argument("--case-manifest", default=".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_case_manifest.json")
p.add_argument("--output-dir", default="learning_output/comparisons/gmcm-2021-D")
p.add_argument("--synthetic", action="store_true")
args=p.parse_args()

BENCH=Path(args.benchmark_json)
FINAL=Path(args.final_json)
CASE=Path(args.case_manifest)
OUT=Path(args.output_dir)
OUT.mkdir(parents=True,exist_ok=True)

if not BENCH.exists():
    raise SystemExit("benchmark missing")
if not CASE.exists():
    raise SystemExit("case manifest missing")

bench=json.loads(BENCH.read_text(encoding="utf-8"))
final=json.loads(FINAL.read_text(encoding="utf-8")) if FINAL.exists() else None
case=json.loads(CASE.read_text(encoding="utf-8"))

screening=case.get("paper_screening",{})
profiles=screening.get("profiles",{})
selected=screening.get("selected_primary_papers",[])
if len(selected)<2:
    raise SystemExit("need two selected primary papers")

paper_a,paper_b=selected[:2]

def our_q_route(q):
    if q=="Q1":
        q2=bench.get("recommendations",{}).get("q2")
        return f"Leakage-safe feature selector inside nested-CV Q1+Q2 pipeline: {q2}"
    if q=="Q2":
        return bench.get("recommendations",{}).get("q2")
    if q=="Q3":
        return json.dumps(bench.get("recommendations",{}).get("q3",{}),ensure_ascii=False)
    if q=="Q4":
        return "Not benchmarked in v1.0; use feasibility-first reference route and explicit ADMET semantics."
    return ""

comparison={
    "schema_version":"1.0",
    "case_id":"gmcm-2021-D",
    "status":"SYNTHETIC_EVIDENCE_BUNDLE" if args.synthetic else "REQUIRES_AGENT_REVIEW",
    "our_evidence":{
        "blind_status":case.get("blind_eval",{}).get("true_blind_status","NOT_RUN"),
        "data_audit_status":bench.get("data_audit_status"),
        "benchmark_profile":bench.get("profile"),
        "benchmark_status":"SYNTHETIC" if args.synthetic else "REAL_RUN",
        "final_fit_status":("SYNTHETIC" if args.synthetic else "REAL_RUN") if final else "NOT_RUN",
        "benchmark_recommendations":bench.get("recommendations",{}),
        "decision_explanations":bench.get("decision_explanations",{}),
    },
    "papers":{
        "A":{
            "file":paper_a,
            "team":profiles.get(paper_a,{}).get("team"),
            "route":profiles.get(paper_a,{}).get("route",{}),
            "strengths":profiles.get(paper_a,{}).get("strengths",[]),
            "risks":profiles.get(paper_a,{}).get("risks",[]),
            "evidence_status":profiles.get(paper_a,{}).get("readability","not_verified")
        },
        "B":{
            "file":paper_b,
            "team":profiles.get(paper_b,{}).get("team"),
            "route":profiles.get(paper_b,{}).get("route",{}),
            "strengths":profiles.get(paper_b,{}).get("strengths",[]),
            "risks":profiles.get(paper_b,{}).get("risks",[]),
            "evidence_status":profiles.get(paper_b,{}).get("readability","not_verified")
        }
    },
    "questions":{},
    "overall":{
        "more_worth_learning":None,
        "more_competition_efficient":None,
        "more_scientifically_cautious":None,
        "combine":[],
        "unresolved_without_reproduction":[
            "paper-specific numerical results have not all been independently reproduced",
            "real 2021 D benchmark remains separate from any synthetic smoke run" if args.synthetic else ""
        ]
    },
    "knowledge_candidates":{
        "methods":[],
        "problem_patterns":[],
        "error_patterns":[],
        "competition_lessons":[]
    }
}

for q in ["Q1","Q2","Q3","Q4"]:
    comparison["questions"][q]={
        "our_route":our_q_route(q),
        "paper_A_route":profiles.get(paper_a,{}).get("route",{}).get(q),
        "paper_B_route":profiles.get(paper_b,{}).get("route",{}).get(q),
        "paper_A_strengths":[],
        "paper_B_strengths":[],
        "our_strengths":[],
        "our_weaknesses":[],
        "adopt":[],
        "do_not_copy_blindly":[],
        "preferred_learning_source":None,
        "confidence":"not_verified",
        "agent_review_required":True
    }

(OUT/"paper_vs_benchmark.json").write_text(
    json.dumps(comparison,ensure_ascii=False,indent=2),encoding="utf-8"
)

instructions="""# Paper-vs-Benchmark Review

This file is an evidence bundle, not a completed verdict.

For Q1-Q4, fill:
- paper A strengths
- paper B strengths
- our strengths
- our weaknesses
- adopt
- do not copy blindly
- preferred learning source
- confidence

Then fill overall verdict and `knowledge_candidates`.

Do not:
- rank papers only by award;
- rank routes by algorithm complexity;
- call synthetic benchmark results evidence about the real 2021 D data;
- upgrade un-reproduced paper claims to verified.
"""
(OUT/"REVIEW_INSTRUCTIONS.md").write_text(instructions,encoding="utf-8")
print("[PASS] paper comparison evidence bundle written to",OUT)
