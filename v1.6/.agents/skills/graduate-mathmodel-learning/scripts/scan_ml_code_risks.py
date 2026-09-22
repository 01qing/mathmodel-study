#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re

p=argparse.ArgumentParser()
p.add_argument("--root",required=True)
p.add_argument("--output",default="learning_output/code_audit/static_scan.json")
args=p.parse_args()

ROOT=Path(args.root)
rules=[
    {
      "id":"fit-transform-test",
      "severity":"critical",
      "regex":r"\b\w+\s*=\s*\w+\.fit_transform\(\s*\w*(?:test|pred|val)\w*\s*\)",
      "message":"fit_transform appears on test/pred/validation-like data; verify that a train-fitted transform should be reused instead."
    },
    {
      "id":"pca-fit-test",
      "severity":"critical",
      "regex":r"\b(?:pca|pca_model)\.fit\(\s*\w*(?:test|pred|val)\w*\s*\)",
      "message":"PCA appears to be fitted on test/pred/validation data."
    },
    {
      "id":"metric-y-pred-first",
      "severity":"high",
      "regex":r"\b(?:precision_score|recall_score|f1_score|accuracy_score)\(\s*(?:y_pred|pred\w*)\s*,",
      "message":"Prediction-like variable is passed as the first metric argument; verify y_true/y_pred ordering."
    },
    {
      "id":"shuffle-false",
      "severity":"medium",
      "regex":r"train_test_split\([^\n]*shuffle\s*=\s*False",
      "message":"Order-dependent split; require an explicit temporal/group/order rationale."
    },
    {
      "id":"absolute-user-path",
      "severity":"low",
      "regex":r"['\"]/(?:Users|home)/[^'\"]+['\"]",
      "message":"Hard-coded absolute user path reduces reproducibility."
    }
]

files=[]
for f in ROOT.rglob("*.py"):
    text=f.read_text(encoding="utf-8",errors="ignore")
    findings=[]
    for rule in rules:
        for m in re.finditer(rule["regex"],text,flags=re.I):
            line=text.count("\n",0,m.start())+1
            findings.append({
                "rule_id":rule["id"],"severity":rule["severity"],
                "line":line,"match":m.group(0)[:240],
                "message":rule["message"]
            })
    # heuristic: fit_transform appears before first train_test_split
    ft=text.find("fit_transform(")
    sp=text.find("train_test_split(")
    if ft>=0 and sp>=0 and ft<sp:
        line=text.count("\n",0,ft)+1
        findings.append({
            "rule_id":"preprocess-before-split",
            "severity":"high","line":line,
            "match":"fit_transform before first train_test_split",
            "message":"A fitted preprocessing step occurs before the first holdout split; inspect for leakage."
        })
    # heuristic: accuracy used but no imbalance-aware metrics in file
    if "accuracy_score" in text and not any(k in text for k in ["balanced_accuracy","matthews_corrcoef","average_precision","roc_auc"]):
        findings.append({
            "rule_id":"accuracy-only-risk",
            "severity":"medium","line":None,
            "match":"accuracy_score without balanced/MCC/PR-AUC/ROC-AUC",
            "message":"Classification evaluation may be dominated by accuracy."
        })
    files.append({"path":str(f.relative_to(ROOT)),"findings":findings})

out={
    "schema_version":"1.1",
    "root":str(ROOT),
    "files":files,
    "counts":{}
}
for row in files:
    for x in row["findings"]:
        out["counts"][x["severity"]]=out["counts"].get(x["severity"],0)+1

op=Path(args.output)
op.parent.mkdir(parents=True,exist_ok=True)
op.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("[PASS] static code scan:",out["counts"])
