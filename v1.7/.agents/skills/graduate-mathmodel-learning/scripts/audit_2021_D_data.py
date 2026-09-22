#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import argparse, json, math, sys
from xlsx_stream_reader import XlsxBook

p=argparse.ArgumentParser()
p.add_argument("--data-dir", required=True)
p.add_argument("--output-dir", default="learning_output/data_audit/gmcm-2021-D")
p.add_argument("--tolerance", type=float, default=1e-6)
args=p.parse_args()

DATA=Path(args.data_dir)
OUT=Path(args.output_dir)
OUT.mkdir(parents=True, exist_ok=True)

FILES={
 "activity":"ERα_activity.xlsx",
 "descriptor":"Molecular_Descriptor.xlsx",
 "admet":"ADMET.xlsx",
 "meaning":"分子描述符含义解释.xlsx",
}
FAVORABLE={"Caco-2":1,"CYP3A4":None,"hERG":0,"HOB":1,"MN":0}

def norm(x):
    return str(x or "").strip().lower().replace(" ","").replace("_","").replace("-","")

def choose_sheet(book, kind):
    names=book.sheet_names()
    for n in names:
        if kind in norm(n):
            return n
    if kind=="train" and names: return names[0]
    if kind=="test" and len(names)>1: return names[1]
    return None

def dict_rows(book, sheet):
    it=book.iter_rows(sheet)
    try: header=next(it)
    except StopIteration: return [], iter(())
    headers=[str(x).strip() if x is not None else "" for x in header]
    def gen():
        for row in it:
            if len(row)<len(headers): row=row+[None]*(len(headers)-len(row))
            yield {headers[i]:row[i] if i<len(row) else None for i in range(len(headers))}
    return headers,gen()

def find_header(headers, candidates):
    for h in headers:
        for c in candidates:
            if norm(h)==norm(c): return h
    for h in headers:
        for c in candidates:
            if norm(c) in norm(h): return h
    return None

def compare(a,b):
    return {
      "same_length":len(a)==len(b),
      "same_order":a==b,
      "same_set":set(a)==set(b),
      "left_count":len(a),"right_count":len(b),
      "left_duplicates":len(a)-len(set(a)),
      "right_duplicates":len(b)-len(set(b)),
      "left_only_count":len(set(a)-set(b)),
      "right_only_count":len(set(b)-set(a)),
    }

def sheet_structure(path):
    b=XlsxBook(path); out=[]
    for s in b.sheet_names():
        it=b.iter_rows(s)
        try: header=next(it)
        except StopIteration:
            out.append({"name":s,"data_rows":0,"columns":0,"headers":[]}); continue
        n=0; mc=len(header)
        for r in it:
            n+=1; mc=max(mc,len(r))
        out.append({"name":s,"data_rows":n,"columns":mc,
                    "headers":[str(x) if x is not None else "" for x in header]})
    return out

report={"schema_version":"0.8","case_id":"gmcm-2021-D","status":"PENDING",
        "files":{},"checks":{},"warnings":[],"blockers":[]}

for key,name in FILES.items():
    path=DATA/name
    report["files"][key]={"name":name,"present":path.exists()}
    if path.exists():
        report["files"][key]["structure"]=sheet_structure(path)
    else:
        report["blockers"].append(f"missing file: {name}")

if report["blockers"]:
    report["status"]="BLOCKED"
    (OUT/"data_audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("[BLOCKED] missing required files")
    sys.exit(2)

# Activity
ab=XlsxBook(DATA/FILES["activity"])
ats=choose_sheet(ab,"train"); aes=choose_sheet(ab,"test")
h,rows=dict_rows(ab,ats)
scol=find_header(h,["SMILES"]); icol=find_header(h,["IC50_nM","IC50"]); pcol=find_header(h,["pIC50"])
asm=[]; errs=[]; missing=0; nonpos=0; n=0
for r in rows:
    n+=1; asm.append(str(r.get(scol) or ""))
    try:
        ic=float(r.get(icol)); pc=float(r.get(pcol))
        if ic<=0: nonpos+=1
        else: errs.append(abs((9-math.log10(ic))-pc))
    except Exception: missing+=1
ht,rt=dict_rows(ab,aes); tscol=find_header(ht,["SMILES"])
asm_t=[str(r.get(tscol) or "") for r in rt]
report["checks"]["activity"]={
 "train_sheet":ats,"test_sheet":aes,"train_rows":n,
 "smiles_column":scol,"ic50_column":icol,"pic50_column":pcol,
 "nonpositive_ic50":nonpos,"missing_or_non_numeric_pairs":missing,
 "formula_max_abs_error":max(errs) if errs else None,
 "formula_mean_abs_error":sum(errs)/len(errs) if errs else None,
 "formula_over_tolerance":sum(e>args.tolerance for e in errs)
}

# Descriptors
db=XlsxBook(DATA/FILES["descriptor"])
dts=choose_sheet(db,"train"); des=choose_sheet(db,"test")
h,rows=dict_rows(db,dts); dscol=find_header(h,["SMILES"])
desc=[x for x in h if x and x!=dscol]
stats={x:{"count":0,"missing":0,"numeric":0,"nonnumeric":0,"min":None,"max":None} for x in desc}
dsm=[]; dn=0
for r in rows:
    dn+=1; dsm.append(str(r.get(dscol) or ""))
    for x in desc:
        v=r.get(x)
        if v is None or v=="":
            stats[x]["missing"]+=1; continue
        stats[x]["count"]+=1
        try:
            z=float(v); stats[x]["numeric"]+=1
            stats[x]["min"]=z if stats[x]["min"] is None else min(stats[x]["min"],z)
            stats[x]["max"]=z if stats[x]["max"] is None else max(stats[x]["max"],z)
        except Exception: stats[x]["nonnumeric"]+=1

constants=[x for x,s in stats.items() if s["numeric"] and s["min"]==s["max"] and not s["nonnumeric"]]
allmissing=[x for x,s in stats.items() if s["count"]==0]
anymissing=[x for x,s in stats.items() if s["missing"]>0]
nonnumeric=[x for x,s in stats.items() if s["nonnumeric"]>0]
ht,rt=dict_rows(db,des); dtscol=find_header(ht,["SMILES"])
dsm_t=[str(r.get(dtscol) or "") for r in rt]
report["checks"]["descriptors"]={
 "train_sheet":dts,"test_sheet":des,"train_rows":dn,
 "descriptor_count":len(desc),"smiles_column":dscol,
 "constant_columns_count":len(constants),"constant_columns":constants[:100],
 "all_missing_columns_count":len(allmissing),"all_missing_columns":allmissing[:100],
 "columns_with_any_missing_count":len(anymissing),
 "nonnumeric_columns_count":len(nonnumeric),"nonnumeric_columns":nonnumeric[:100]
}

# ADMET
bb=XlsxBook(DATA/FILES["admet"])
bts=choose_sheet(bb,"train"); bes=choose_sheet(bb,"test")
h,rows=dict_rows(bb,bts); bscol=find_header(h,["SMILES"])
lcols={k:find_header(h,[k]) for k in FAVORABLE}
counts={k:Counter() for k in FAVORABLE}
bsm=[]; bn=0
for r in rows:
    bn+=1; bsm.append(str(r.get(bscol) or ""))
    for label,col in lcols.items():
        v=r.get(col)
        if v in (None,""): counts[label]["missing"]+=1
        else:
            try: counts[label][str(int(float(v)))]+=1
            except Exception: counts[label]["other"]+=1

dist={}
for label,c in counts.items():
    n0,n1=c.get("0",0),c.get("1",0); valid=n0+n1
    dist[label]={"0":n0,"1":n1,"missing":c.get("missing",0),"other":c.get("other",0),
                 "minority_ratio":min(n0,n1)/valid if valid else None,
                 "favorable_class":FAVORABLE[label],
                 "semantic_ambiguity":label=="CYP3A4"}
ht,rt=dict_rows(bb,bes); btscol=find_header(ht,["SMILES"])
bsm_t=[str(r.get(btscol) or "") for r in rt]
report["checks"]["admet"]={"train_sheet":bts,"test_sheet":bes,"train_rows":bn,
 "smiles_column":bscol,"label_columns":lcols,"distributions":dist}

# Meaning file
report["checks"]["descriptor_meaning"]=sheet_structure(DATA/FILES["meaning"])

# Cross-file alignment
alignment={
 "train_activity_vs_descriptor":compare(asm,dsm),
 "train_activity_vs_admet":compare(asm,bsm),
 "train_descriptor_vs_admet":compare(dsm,bsm),
 "test_activity_vs_descriptor":compare(asm_t,dsm_t),
 "test_activity_vs_admet":compare(asm_t,bsm_t),
}
report["checks"]["smiles_alignment"]=alignment
for name,c in alignment.items():
    if not c["same_set"]: report["blockers"].append(f"SMILES set mismatch: {name}")
    elif not c["same_order"]: report["warnings"].append(f"SMILES order differs: {name}; reindex by SMILES")

# Expected facts
for label,actual,expected in [
 ("activity train rows",n,1974),("descriptor train rows",dn,1974),("ADMET train rows",bn,1974),
 ("descriptor count",len(desc),729),("activity test rows",len(asm_t),50),
 ("descriptor test rows",len(dsm_t),50),("ADMET test rows",len(bsm_t),50)]:
    if actual!=expected: report["warnings"].append(f"{label}={actual}, problem statement expected {expected}")

if report["checks"]["activity"]["formula_over_tolerance"]>0:
    report["warnings"].append("IC50/pIC50 relation exceeds tolerance; inspect unit/rounding")
if constants:
    report["warnings"].append("constant descriptor columns exist; remove inside training pipeline")
if allmissing:
    report["warnings"].append("all-missing descriptor columns exist")

report["test_isolation_policy"]={
 "allowed":["final prediction after model/hyperparameters are frozen"],
 "forbidden":["feature selection","hyperparameter tuning","threshold selection","model selection"]
}
report["status"]="BLOCKED" if report["blockers"] else ("PASS_WITH_WARNINGS" if report["warnings"] else "PASS")

(OUT/"data_audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

lines=["# 2021 D Data Audit","",f"Status: **{report['status']}**","",
       "## Core facts",f"- Activity train rows: {n}",f"- Descriptor train rows: {dn}",
       f"- ADMET train rows: {bn}",f"- Descriptor count: {len(desc)}",
       f"- Activity test rows: {len(asm_t)}",f"- Descriptor test rows: {len(dsm_t)}",
       f"- ADMET test rows: {len(bsm_t)}","","## IC50 ↔ pIC50",
       f"- max abs error: {report['checks']['activity']['formula_max_abs_error']}",
       f"- mean abs error: {report['checks']['activity']['formula_mean_abs_error']}",
       f"- over tolerance: {report['checks']['activity']['formula_over_tolerance']}",
       "","## Descriptor quality",f"- constant columns: {len(constants)}",
       f"- all-missing columns: {len(allmissing)}",f"- columns with any missing: {len(anymissing)}",
       f"- nonnumeric descriptor columns: {len(nonnumeric)}","","## ADMET distributions"]
for label,d in dist.items():
    lines.append(f"- {label}: 0={d['0']}, 1={d['1']}, missing={d['missing']}, minority_ratio={d['minority_ratio']}, favorable={d['favorable_class']}")
lines += ["","## Warnings"] + ([f"- {x}" for x in report["warnings"]] or ["- none"])
lines += ["","## Blockers"] + ([f"- {x}" for x in report["blockers"]] or ["- none"])
(OUT/"data_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"[{report['status']}] audit written to {OUT}")
