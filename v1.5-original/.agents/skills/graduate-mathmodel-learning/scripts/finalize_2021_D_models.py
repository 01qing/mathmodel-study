#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, math, platform

import numpy as np
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression, mutual_info_classif, SelectFromModel
from sklearn.linear_model import ElasticNet, LogisticRegression
from sklearn.cross_decomposition import PLSRegression
from sklearn.svm import SVR, SVC
from sklearn.ensemble import (
    ExtraTreesRegressor, RandomForestRegressor, HistGradientBoostingRegressor,
    RandomForestClassifier, HistGradientBoostingClassifier
)
from sklearn.model_selection import KFold, StratifiedKFold, GridSearchCV

from xlsx_stream_reader import XlsxBook

p=argparse.ArgumentParser()
p.add_argument("--data-dir", required=True)
p.add_argument("--audit-json", default="learning_output/data_audit/gmcm-2021-D/data_audit.json")
p.add_argument("--benchmark-json", default="learning_output/model_benchmark/gmcm-2021-D/model_benchmark.json")
p.add_argument("--output-dir", default="learning_output/final_fit/gmcm-2021-D")
p.add_argument("--synthetic-json", default=None, help="Internal smoke-test only.")
p.add_argument("--seed", type=int, default=202109)
args=p.parse_args()

DATA=Path(args.data_dir)
AUDIT=Path(args.audit_json)
BENCH=Path(args.benchmark_json)
OUT=Path(args.output_dir)
OUT.mkdir(parents=True, exist_ok=True)
SEED=args.seed

if not AUDIT.exists():
    raise SystemExit("Missing data audit.")
if not BENCH.exists():
    raise SystemExit("Missing benchmark.")

audit=json.loads(AUDIT.read_text(encoding="utf-8"))
bench=json.loads(BENCH.read_text(encoding="utf-8"))
if audit.get("status") not in {"PASS","PASS_WITH_WARNINGS"}:
    raise SystemExit("Data audit must be PASS/PASS_WITH_WARNINGS.")
if bench.get("test_isolation",{}).get("used_in_benchmark") is not False:
    raise SystemExit("Benchmark violated test isolation.")
if bench.get("case_id")!="gmcm-2021-D":
    raise SystemExit("Wrong benchmark case.")

PROFILE=bench.get("profile","standard")
INNER={"smoke":2,"standard":5,"deep":5}.get(PROFILE,5)

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

def load_rows(path, kind):
    b=XlsxBook(path)
    s=choose_sheet(b,kind)
    it=b.iter_rows(s)
    header=next(it)
    headers=[str(x).strip() if x is not None else "" for x in header]
    rows=[]
    for row in it:
        if len(row)<len(headers):
            row=row+[None]*(len(headers)-len(row))
        rows.append({headers[i]:row[i] if i<len(row) else None for i in range(len(headers))})
    return headers,rows

def find_header(headers,candidates):
    for h in headers:
        for c in candidates:
            if norm(h)==norm(c): return h
    for h in headers:
        for c in candidates:
            if norm(c) in norm(h): return h
    return None

def by_smiles(rows,col):
    out={}
    for r in rows:
        key=str(r.get(col) or "")
        if key in out:
            raise ValueError(f"Duplicate SMILES requires explicit replicate policy: {key}")
        out[key]=r
    return out

labels=["Caco-2","CYP3A4","hERG","HOB","MN"]

if args.synthetic_json:
    syn=json.loads(Path(args.synthetic_json).read_text(encoding="utf-8"))
    X=np.asarray(syn["X"],dtype=float)
    Xtest=np.asarray(syn["X_test"],dtype=float)
    y_reg=np.asarray(syn["y_reg"],dtype=float)
    feature_names=np.asarray(syn["feature_names"],dtype=object)
    Y_cls={lab:[int(v) for v in syn["Y_cls"][lab]] for lab in labels}
    train_smiles=[f"S{i:04d}" for i in range(len(X))]
    test_smiles=syn.get("test_smiles",[f"T{i:04d}" for i in range(len(Xtest))])
else:
    hd,rd=load_rows(DATA/"Molecular_Descriptor.xlsx","train")
    hdt,rdt=load_rows(DATA/"Molecular_Descriptor.xlsx","test")
    ha,ra=load_rows(DATA/"ERα_activity.xlsx","train")
    hb,rb=load_rows(DATA/"ADMET.xlsx","train")

    dsm=find_header(hd,["SMILES"])
    dsmt=find_header(hdt,["SMILES"])
    asm=find_header(ha,["SMILES"])
    bsm=find_header(hb,["SMILES"])
    pcol=find_header(ha,["pIC50"])
    label_cols={lab:find_header(hb,[lab]) for lab in labels}
    desc_cols=[h for h in hd if h and h!=dsm]

    D=by_smiles(rd,dsm)
    A=by_smiles(ra,asm)
    B=by_smiles(rb,bsm)
    Dt=by_smiles(rdt,dsmt)

    if not (set(D)==set(A)==set(B)):
        raise SystemExit("Train SMILES mismatch.")
    train_smiles=sorted(D)
    test_smiles=[str(r.get(dsmt) or "") for r in rdt]

    X=[]; y_reg=[]; Y_cls={lab:[] for lab in labels}
    for key in train_smiles:
        row=[]
        for c in desc_cols:
            v=D[key].get(c)
            try: row.append(float(v) if v not in (None,"") else np.nan)
            except Exception: row.append(np.nan)
        X.append(row)
        y_reg.append(float(A[key][pcol]))
        for lab,col in label_cols.items():
            try: Y_cls[lab].append(int(float(B[key][col])))
            except Exception: Y_cls[lab].append(None)

    Xtest=[]
    for key in test_smiles:
        row=[]
        for c in desc_cols:
            v=Dt[key].get(c)
            try: row.append(float(v) if v not in (None,"") else np.nan)
            except Exception: row.append(np.nan)
        Xtest.append(row)

    X=np.asarray(X,dtype=float)
    Xtest=np.asarray(Xtest,dtype=float)
    y_reg=np.asarray(y_reg,dtype=float)
    feature_names=np.asarray(desc_cols,dtype=object)

keep=~np.all(np.isnan(X),axis=0)
X=X[:,keep]
Xtest=Xtest[:,keep]
feature_names=feature_names[keep]

def mi_reg(X_,y_):
    return mutual_info_regression(X_,y_,random_state=SEED)

def mi_cls(X_,y_):
    return mutual_info_classif(X_,y_,random_state=SEED)

def q2_selector(name):
    k=min(20,X.shape[1])
    if name=="mi":
        return SelectKBest(score_func=mi_reg,k=k)
    if name=="enet":
        return SelectFromModel(
            ElasticNet(alpha=0.01,l1_ratio=0.5,max_iter=20000,random_state=SEED),
            threshold=-np.inf,max_features=k
        )
    if name=="extra":
        return SelectFromModel(
            ExtraTreesRegressor(
                n_estimators=(12 if PROFILE=="smoke" else 300),
                min_samples_leaf=2,random_state=SEED,n_jobs=-1
            ),
            threshold=-np.inf,max_features=k
        )
    raise KeyError(name)

def q2_model(name):
    smoke=PROFILE=="smoke"
    if name=="elasticnet":
        return ElasticNet(max_iter=20000,random_state=SEED),{
            "model__alpha":[0.01] if smoke else [0.001,0.01,0.1,1.0],
            "model__l1_ratio":[0.5] if smoke else [0.2,0.5,0.8]}
    if name=="pls":
        return PLSRegression(scale=False),{
            "model__n_components":[2] if smoke else [2,5,10]}
    if name=="svr":
        return SVR(kernel="rbf"),{
            "model__C":[10] if smoke else [1,10,100],
            "model__gamma":["scale"] if smoke else ["scale",0.01],
            "model__epsilon":[0.1] if smoke else [0.05,0.1]}
    if name=="rf":
        return RandomForestRegressor(
            n_estimators=(12 if smoke else 300),random_state=SEED,n_jobs=-1
        ),{
            "model__max_depth":[None] if smoke else [None,10],
            "model__min_samples_leaf":[2] if smoke else [1,3]}
    if name=="hgb":
        return HistGradientBoostingRegressor(random_state=SEED),{
            "model__learning_rate":[0.1] if smoke else [0.05,0.1],
            "model__max_leaf_nodes":[31] if smoke else [15,31],
            "model__l2_regularization":[0.0] if smoke else [0.0,1.0]}
    raise KeyError(name)

def selected_names(est):
    sel=est.named_steps.get("selector")
    if sel is None:
        return list(feature_names)
    return list(feature_names[sel.get_support()])

# Q2
q2_id=bench["recommendations"]["q2"]
selector_name,model_name=q2_id.split("+",1)
q2m,q2grid=q2_model(model_name)
q2pipe=Pipeline([
    ("imputer",SimpleImputer(strategy="median")),
    ("scaler",StandardScaler()),
    ("selector",q2_selector(selector_name)),
    ("model",q2m)
])
q2cv=KFold(n_splits=INNER,shuffle=True,random_state=SEED)
q2search=GridSearchCV(
    q2pipe,q2grid,scoring="neg_root_mean_squared_error",
    cv=q2cv,n_jobs=(1 if PROFILE=="smoke" else -1),refit=True,error_score="raise"
)
q2search.fit(X,y_reg)
p_test=np.asarray(q2search.predict(Xtest)).reshape(-1)
ic50_test=np.power(10.0,9.0-p_test)
q2features=selected_names(q2search.best_estimator_)

# Q3
def q3_model(name):
    smoke=PROFILE=="smoke"
    if name=="logistic":
        return LogisticRegression(max_iter=10000,class_weight="balanced",solver="liblinear"),{
            "model__C":[1.0] if smoke else [0.1,1.0,10.0]}
    if name=="svc":
        return SVC(kernel="rbf",probability=True,class_weight="balanced",random_state=SEED),{
            "model__C":[2.0] if smoke else [0.5,2.0,10.0],
            "model__gamma":["scale"] if smoke else ["scale",0.01]}
    if name=="rf":
        return RandomForestClassifier(
            n_estimators=(12 if smoke else 300),class_weight="balanced",
            random_state=SEED,n_jobs=-1
        ),{
            "model__max_depth":[None] if smoke else [None,12],
            "model__min_samples_leaf":[2] if smoke else [1,3]}
    if name=="hgb":
        return HistGradientBoostingClassifier(class_weight="balanced",random_state=SEED),{
            "model__learning_rate":[0.1] if smoke else [0.05,0.1],
            "model__max_leaf_nodes":[31] if smoke else [15,31],
            "model__l2_regularization":[0.0] if smoke else [0.0,1.0]}
    raise KeyError(name)

q3out={}
for lab in labels:
    route=bench["recommendations"]["q3"].get(lab)
    if not route:
        q3out[lab]={"status":"BLOCKED","reason":"benchmark has no recommendation"}
        continue
    feature_mode,model_name=route.split("+",1)
    raw=Y_cls[lab]
    mask=np.asarray([v is not None for v in raw],dtype=bool)
    y=np.asarray([v for v in raw if v is not None],dtype=int)
    Xl=X[mask]
    counts=np.bincount(y,minlength=2)
    inner=min(INNER,int(counts.min()))
    if inner<2:
        q3out[lab]={"status":"BLOCKED","reason":"insufficient minority class for final CV"}
        continue

    model,grid=q3_model(model_name)
    steps=[
        ("imputer",SimpleImputer(strategy="median")),
        ("scaler",StandardScaler())
    ]
    if feature_mode=="mi":
        steps.append(("selector",SelectKBest(score_func=mi_cls,k=min(100,Xl.shape[1]))))
    steps.append(("model",model))
    pipe=Pipeline(steps)
    cv=StratifiedKFold(n_splits=inner,shuffle=True,random_state=SEED)
    search=GridSearchCV(
        pipe,grid,scoring="balanced_accuracy",cv=cv,n_jobs=(1 if PROFILE=="smoke" else -1),refit=True,error_score="raise"
    )
    search.fit(Xl,y)
    pred=search.predict(Xtest).astype(int)
    prob=None
    if hasattr(search.best_estimator_,"predict_proba"):
        try: prob=search.best_estimator_.predict_proba(Xtest)[:,1]
        except Exception: prob=None

    q3out[lab]={
        "status":"PASS",
        "route":route,
        "best_params":search.best_params_,
        "predictions":[int(v) for v in pred],
        "probability_1":[float(v) for v in prob] if prob is not None else None,
        "training_class_counts":{"0":int(counts[0]),"1":int(counts[1])}
    }

result={
    "schema_version":"1.0",
    "case_id":"gmcm-2021-D",
    "benchmark_source":str(BENCH),
    "benchmark_profile":PROFILE,
    "data_audit_status":audit["status"],
    "environment":{"python":platform.python_version(),"sklearn":sklearn.__version__},
    "q2":{
        "route":q2_id,
        "best_params":q2search.best_params_,
        "selected_features":q2features,
        "test_predictions":[
            {"SMILES":str(test_smiles[i]),"pIC50":float(p_test[i]),"IC50_nM":float(ic50_test[i])}
            for i in range(len(test_smiles))
        ]
    },
    "q3":q3out,
    "test_isolation":{
        "test_used_for_model_selection":False,
        "test_used_for_hyperparameter_selection":False,
        "test_use":"single final prediction after route freeze"
    }
}
(OUT/"final_fit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

with (OUT/"q2_test_predictions.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f)
    w.writerow(["SMILES","pIC50","IC50_nM"])
    for row in result["q2"]["test_predictions"]:
        w.writerow([row["SMILES"],row["pIC50"],row["IC50_nM"]])

with (OUT/"q3_test_predictions.csv").open("w",encoding="utf-8-sig",newline="") as f:
    cols=["SMILES"]
    for lab in labels:
        cols += [lab,lab+"_prob1"]
    w=csv.writer(f); w.writerow(cols)
    for i,s in enumerate(test_smiles):
        row=[s]
        for lab in labels:
            info=q3out[lab]
            if info.get("status")=="PASS":
                row += [info["predictions"][i],
                        info["probability_1"][i] if info["probability_1"] is not None else ""]
            else:
                row += ["",""]
        w.writerow(row)

lines=[
    "# 2021 D Final Fit","",
    f"- Benchmark route frozen from: `{BENCH}`",
    f"- Q2 route: `{q2_id}`",
    f"- Q2 final selected features: {len(q2features)}",
    f"- Test rows predicted: {len(test_smiles)}","",
    "## Test isolation",
    "- Test was not used for model-family selection.",
    "- Test was not used for hyperparameter selection.",
    "- Predictions were generated once after route freeze.","",
    "## Q3 routes"
]
for lab in labels:
    info=q3out[lab]
    lines.append(f"- {lab}: `{info.get('route')}` ({info.get('status')})")
(OUT/"final_fit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

print("[PASS] final fit written to",OUT)
