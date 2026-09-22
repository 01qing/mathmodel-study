#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations
import argparse, json, math, platform, time

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
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    balanced_accuracy_score, accuracy_score, matthews_corrcoef,
    f1_score, precision_score, recall_score, roc_auc_score,
    average_precision_score, brier_score_loss
)

from xlsx_stream_reader import XlsxBook

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--data-dir", required=True)
PARSER.add_argument("--audit-json", default="learning_output/data_audit/gmcm-2021-D/data_audit.json")
PARSER.add_argument("--output-dir", default="learning_output/model_benchmark/gmcm-2021-D")
PARSER.add_argument("--profile", choices=["smoke","standard","deep"], default="standard")
PARSER.add_argument("--seed", type=int, default=202109)
PARSER.add_argument("--synthetic-json", default=None, help="Internal smoke-test input; real runs must use XLSX data-dir.")
ARGS = PARSER.parse_args()

DATA = Path(ARGS.data_dir)
AUDIT = Path(ARGS.audit_json)
OUT = Path(ARGS.output_dir)
OUT.mkdir(parents=True, exist_ok=True)

if not AUDIT.exists():
    raise SystemExit("Run audit_2021_D_data.py first.")
audit = json.loads(AUDIT.read_text(encoding="utf-8"))
if audit.get("status") == "BLOCKED":
    raise SystemExit("Data audit BLOCKED; benchmark forbidden.")
if audit.get("status") not in {"PASS","PASS_WITH_WARNINGS"}:
    raise SystemExit("Data audit must be PASS/PASS_WITH_WARNINGS.")

PROFILE = {
    "smoke": {
        "outer": 2, "inner": 2,
        "q2_selectors": ["mi"],
        "q2_models": ["elasticnet","rf"],
        "q3_feature_modes": ["all"],
        "q3_models": ["logistic","rf"],
    },
    "standard": {
        "outer": 5, "inner": 3,
        "q2_selectors": ["mi","enet","extra"],
        "q2_models": ["elasticnet","pls","svr","rf","hgb"],
        "q3_feature_modes": ["all","mi"],
        "q3_models": ["logistic","svc","rf","hgb"],
    },
    "deep": {
        "outer": 5, "inner": 5,
        "q2_selectors": ["mi","enet","extra"],
        "q2_models": ["elasticnet","pls","svr","rf","hgb"],
        "q3_feature_modes": ["all","mi"],
        "q3_models": ["logistic","svc","rf","hgb"],
    },
}[ARGS.profile]

SEED = ARGS.seed

def norm(x):
    return str(x or "").strip().lower().replace(" ","").replace("_","").replace("-","")

def choose_sheet(book, kind):
    names = book.sheet_names()
    for n in names:
        if kind in norm(n):
            return n
    if kind == "train" and names:
        return names[0]
    if kind == "test" and len(names) > 1:
        return names[1]
    return None

def load_rows(path, kind="train"):
    book = XlsxBook(path)
    sheet = choose_sheet(book, kind)
    it = book.iter_rows(sheet)
    header = next(it)
    headers = [str(x).strip() if x is not None else "" for x in header]
    rows = []
    for row in it:
        if len(row) < len(headers):
            row = row + [None] * (len(headers)-len(row))
        rows.append({headers[i]: row[i] if i < len(row) else None for i in range(len(headers))})
    return headers, rows

def find_header(headers, candidates):
    for h in headers:
        for c in candidates:
            if norm(h) == norm(c):
                return h
    for h in headers:
        for c in candidates:
            if norm(c) in norm(h):
                return h
    return None

def by_smiles(rows, col):
    out = {}
    for r in rows:
        key = str(r.get(col) or "")
        if key in out:
            raise ValueError(f"Duplicate SMILES requires an explicit replicate policy: {key}")
        out[key] = r
    return out

# ---------- Load aligned training data or isolated synthetic smoke data ----------
if ARGS.synthetic_json:
    syn = json.loads(Path(ARGS.synthetic_json).read_text(encoding="utf-8"))
    X = np.asarray(syn["X"], dtype=float)
    y_reg = np.asarray(syn["y_reg"], dtype=float)
    feature_names = np.asarray(syn["feature_names"], dtype=object)
    labels = ["Caco-2","CYP3A4","hERG","HOB","MN"]
    Y_cls = {lab:[int(v) for v in syn["Y_cls"][lab]] for lab in labels}
else:
    hd, rd = load_rows(DATA/"Molecular_Descriptor.xlsx", "train")
    ha, ra = load_rows(DATA/"ERα_activity.xlsx", "train")
    hb, rb = load_rows(DATA/"ADMET.xlsx", "train")

    dsm = find_header(hd, ["SMILES"])
    asm = find_header(ha, ["SMILES"])
    bsm = find_header(hb, ["SMILES"])
    pcol = find_header(ha, ["pIC50"])
    labels = ["Caco-2","CYP3A4","hERG","HOB","MN"]
    label_cols = {lab: find_header(hb, [lab]) for lab in labels}
    desc_cols = [h for h in hd if h and h != dsm]

    D = by_smiles(rd, dsm)
    A = by_smiles(ra, asm)
    B = by_smiles(rb, bsm)

    if not (set(D) == set(A) == set(B)):
        raise SystemExit("Training SMILES sets differ; benchmark blocked.")

    keys = sorted(D)
    X = []
    y_reg = []
    Y_cls = {lab: [] for lab in labels}
    for key in keys:
        row = []
        for col in desc_cols:
            v = D[key].get(col)
            try:
                row.append(float(v) if v not in (None,"") else np.nan)
            except Exception:
                row.append(np.nan)
        X.append(row)
        y_reg.append(float(A[key][pcol]))
        for lab, col in label_cols.items():
            try:
                Y_cls[lab].append(int(float(B[key][col])))
            except Exception:
                Y_cls[lab].append(None)

    X = np.asarray(X, dtype=float)
    y_reg = np.asarray(y_reg, dtype=float)
    feature_names = np.asarray(desc_cols, dtype=object)

# all-missing columns are schema defects, not supervised selection.
keep = ~np.all(np.isnan(X), axis=0)
X = X[:, keep]
feature_names = feature_names[keep]

def mean_std(vals):
    arr = np.asarray(vals, dtype=float)
    if len(arr) == 0:
        return None, None
    return float(np.mean(arr)), float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0

def jaccard(a,b):
    a,b = set(a),set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

def selection_stability(selected):
    if len(selected) < 2:
        return None
    vals = [jaccard(a,b) for a,b in combinations(selected,2)]
    return float(np.mean(vals))

def selection_frequency(selected):
    counts = {}
    for arr in selected:
        for f in arr:
            counts[f] = counts.get(f,0) + 1
    n = max(1,len(selected))
    return [
        {"feature":k, "count":v, "frequency":v/n}
        for k,v in sorted(counts.items(), key=lambda kv:(-kv[1],kv[0]))
    ]

def mi_reg(X_, y_):
    return mutual_info_regression(X_, y_, random_state=SEED)

def mi_cls(X_, y_):
    return mutual_info_classif(X_, y_, random_state=SEED)

SELECTOR_COMPLEXITY = {"mi":1,"enet":1,"extra":2}

def q2_selector(name):
    k = min(20, X.shape[1])
    if name == "mi":
        return SelectKBest(score_func=mi_reg, k=k)
    if name == "enet":
        return SelectFromModel(
            ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=20000, random_state=SEED),
            threshold=-np.inf, max_features=k
        )
    if name == "extra":
        return SelectFromModel(
            ExtraTreesRegressor(
                n_estimators=250, min_samples_leaf=2,
                random_state=SEED, n_jobs=-1
            ),
            threshold=-np.inf, max_features=k
        )
    raise KeyError(name)

def q2_model(name):
    smoke = ARGS.profile == "smoke"
    if name == "elasticnet":
        return (
            ElasticNet(max_iter=20000, random_state=SEED),
            {
                "model__alpha":[0.01] if smoke else [0.001,0.01,0.1,1.0],
                "model__l1_ratio":[0.5] if smoke else [0.2,0.5,0.8],
            }, 1
        )
    if name == "pls":
        return (
            PLSRegression(scale=False),
            {"model__n_components":[2] if smoke else [2,5,10]},
            1
        )
    if name == "svr":
        return (
            SVR(kernel="rbf"),
            {
                "model__C":[10] if smoke else [1,10,100],
                "model__gamma":["scale"] if smoke else ["scale",0.01],
                "model__epsilon":[0.1] if smoke else [0.05,0.1],
            }, 2
        )
    if name == "rf":
        return (
            RandomForestRegressor(n_estimators=(10 if ARGS.profile=="smoke" else 250), random_state=SEED, n_jobs=-1),
            {
                "model__max_depth":[None] if smoke else [None,10],
                "model__min_samples_leaf":[2] if smoke else [1,3],
            }, 3
        )
    if name == "hgb":
        return (
            HistGradientBoostingRegressor(random_state=SEED),
            {
                "model__learning_rate":[0.1] if smoke else [0.05,0.1],
                "model__max_leaf_nodes":[31] if smoke else [15,31],
                "model__l2_regularization":[0.0] if smoke else [0.0,1.0],
            }, 3
        )
    raise KeyError(name)

def selected_names(estimator):
    sel = estimator.named_steps.get("selector")
    if sel is None or sel == "passthrough":
        return list(feature_names)
    mask = sel.get_support()
    return list(feature_names[mask])

def paired_tie(lower_better, winner, runner, metric):
    a = np.asarray([x[metric] for x in winner["fold_metrics"]], dtype=float)
    b = np.asarray([x[metric] for x in runner["fold_metrics"]], dtype=float)
    diff = (b-a) if lower_better else (a-b)
    if len(diff) < 2:
        return {"practical_tie":False,"mean_difference":float(np.mean(diff)),"ci95_halfwidth":None}
    se = float(np.std(diff,ddof=1) / math.sqrt(len(diff)))
    half = 1.96 * se
    md = float(np.mean(diff))
    return {
        "practical_tie": abs(md) <= half,
        "mean_difference": md,
        "ci95_halfwidth": half,
    }

# ---------- Q1 + Q2 nested CV ----------
outer_reg = KFold(n_splits=PROFILE["outer"], shuffle=True, random_state=SEED)
outer_reg_splits = list(outer_reg.split(X, y_reg))
q2_candidates = []

for selector_name in PROFILE["q2_selectors"]:
    for model_name in PROFILE["q2_models"]:
        model, grid, model_complexity = q2_model(model_name)
        fold_metrics = []
        fold_features = []
        best_params = []
        fit_seconds = 0.0

        for fold, (tr, va) in enumerate(outer_reg_splits, 1):
            inner = KFold(n_splits=PROFILE["inner"], shuffle=True, random_state=SEED+fold)
            pipe = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("selector", q2_selector(selector_name)),
                ("model", model),
            ])
            search = GridSearchCV(
                pipe, grid, scoring="neg_root_mean_squared_error",
                cv=inner, n_jobs=(1 if ARGS.profile=="smoke" else -1), refit=True, error_score="raise"
            )
            t0 = time.time()
            search.fit(X[tr], y_reg[tr])
            fit_seconds += time.time()-t0
            pred = np.asarray(search.predict(X[va])).reshape(-1)
            fold_metrics.append({
                "fold":fold,
                "rmse":float(math.sqrt(mean_squared_error(y_reg[va],pred))),
                "mae":float(mean_absolute_error(y_reg[va],pred)),
                "r2":float(r2_score(y_reg[va],pred)),
            })
            fold_features.append(selected_names(search.best_estimator_))
            best_params.append(search.best_params_)

        rmse_m, rmse_s = mean_std([x["rmse"] for x in fold_metrics])
        mae_m, mae_s = mean_std([x["mae"] for x in fold_metrics])
        r2_m, r2_s = mean_std([x["r2"] for x in fold_metrics])

        q2_candidates.append({
            "pipeline_id":f"{selector_name}+{model_name}",
            "selector":selector_name,
            "model":model_name,
            "complexity":SELECTOR_COMPLEXITY[selector_name]+model_complexity,
            "outer_metrics":{
                "rmse_mean":rmse_m,"rmse_std":rmse_s,
                "mae_mean":mae_m,"mae_std":mae_s,
                "r2_mean":r2_m,"r2_std":r2_s,
            },
            "fold_metrics":fold_metrics,
            "selector_stability_jaccard":selection_stability(fold_features),
            "selection_frequency":selection_frequency(fold_features),
            "best_params_per_fold":best_params,
            "fit_seconds_total":fit_seconds,
        })

q2_candidates.sort(key=lambda r:(
    r["outer_metrics"]["rmse_mean"],
    r["outer_metrics"]["mae_mean"],
    r["outer_metrics"]["rmse_std"],
    r["complexity"],
))
q2_metric_winner = q2_candidates[0]
q2_recommended = q2_metric_winner
q2_tie = None
if len(q2_candidates) > 1:
    q2_tie = paired_tie(True, q2_candidates[0], q2_candidates[1], "rmse")
    if q2_tie["practical_tie"]:
        q2_recommended = sorted(
            q2_candidates[:2],
            key=lambda r:(r["complexity"],r["outer_metrics"]["rmse_mean"])
        )[0]

# ---------- Q3 nested CV ----------
def q3_model(name):
    smoke = ARGS.profile == "smoke"
    if name == "logistic":
        return (
            LogisticRegression(max_iter=10000, class_weight="balanced", solver="liblinear"),
            {"model__C":[1.0] if smoke else [0.1,1.0,10.0]}, 1
        )
    if name == "svc":
        return (
            SVC(kernel="rbf", probability=True, class_weight="balanced", random_state=SEED),
            {
                "model__C":[2.0] if smoke else [0.5,2.0,10.0],
                "model__gamma":["scale"] if smoke else ["scale",0.01],
            }, 2
        )
    if name == "rf":
        return (
            RandomForestClassifier(
                n_estimators=(12 if ARGS.profile=="smoke" else 300), class_weight="balanced",
                random_state=SEED, n_jobs=-1
            ),
            {
                "model__max_depth":[None] if smoke else [None,12],
                "model__min_samples_leaf":[2] if smoke else [1,3],
            }, 2
        )
    if name == "hgb":
        return (
            HistGradientBoostingClassifier(class_weight="balanced", random_state=SEED),
            {
                "model__learning_rate":[0.1] if smoke else [0.05,0.1],
                "model__max_leaf_nodes":[31] if smoke else [15,31],
                "model__l2_regularization":[0.0] if smoke else [0.0,1.0],
            }, 3
        )
    raise KeyError(name)

def q3_selector(mode, n_features):
    if mode == "all":
        return None
    return SelectKBest(score_func=mi_cls, k=min(100,n_features))

def cls_metrics(y, pred, prob):
    out = {
        "balanced_accuracy":float(balanced_accuracy_score(y,pred)),
        "accuracy":float(accuracy_score(y,pred)),
        "mcc":float(matthews_corrcoef(y,pred)),
        "f1":float(f1_score(y,pred,zero_division=0)),
        "precision":float(precision_score(y,pred,zero_division=0)),
        "recall":float(recall_score(y,pred,zero_division=0)),
        "roc_auc":None,"pr_auc":None,"brier":None,
    }
    if prob is not None:
        try: out["roc_auc"] = float(roc_auc_score(y,prob))
        except Exception: pass
        try: out["pr_auc"] = float(average_precision_score(y,prob))
        except Exception: pass
        try: out["brier"] = float(brier_score_loss(y,prob))
        except Exception: pass
    return out

q3 = {}
q3_recommendations = {}

for lab in labels:
    raw = Y_cls[lab]
    mask = np.asarray([v is not None for v in raw], dtype=bool)
    y = np.asarray([v for v in raw if v is not None], dtype=int)
    Xl = X[mask]
    counts = np.bincount(y, minlength=2)
    min_class = int(counts.min())

    if min_class < 2:
        q3[lab] = {
            "status":"BLOCKED",
            "reason":f"minority class count {min_class} < 2; stratified CV impossible"
        }
        continue

    outer_n = min(PROFILE["outer"], min_class)
    outer = StratifiedKFold(
        n_splits=outer_n, shuffle=True, random_state=SEED
    )
    splits = list(outer.split(Xl,y))
    candidates = []

    for feature_mode in PROFILE["q3_feature_modes"]:
        for model_name in PROFILE["q3_models"]:
            model, grid, complexity = q3_model(model_name)
            fold_metrics = []
            best_params = []
            fit_seconds = 0.0

            for fold,(tr,va) in enumerate(splits,1):
                train_counts = np.bincount(y[tr], minlength=2)
                inner_n = min(PROFILE["inner"], int(train_counts.min()))
                if inner_n < 2:
                    raise RuntimeError(f"{lab}: not enough minority samples for inner CV")

                inner = StratifiedKFold(
                    n_splits=inner_n, shuffle=True, random_state=SEED+fold
                )
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler()),
                ]
                sel = q3_selector(feature_mode, Xl.shape[1])
                if sel is not None:
                    steps.append(("selector",sel))
                steps.append(("model",model))
                pipe = Pipeline(steps)

                search = GridSearchCV(
                    pipe, grid, scoring="balanced_accuracy",
                    cv=inner, n_jobs=(1 if ARGS.profile=="smoke" else -1), refit=True, error_score="raise"
                )
                t0 = time.time()
                search.fit(Xl[tr],y[tr])
                fit_seconds += time.time()-t0
                pred = search.predict(Xl[va])

                prob = None
                if hasattr(search.best_estimator_,"predict_proba"):
                    try: prob = search.best_estimator_.predict_proba(Xl[va])[:,1]
                    except Exception: pass

                fm = cls_metrics(y[va],pred,prob)
                fm["fold"] = fold
                fold_metrics.append(fm)
                best_params.append(search.best_params_)

            summary = {}
            for metric in [
                "balanced_accuracy","accuracy","mcc","f1","precision","recall",
                "roc_auc","pr_auc","brier"
            ]:
                vals = [x[metric] for x in fold_metrics if x.get(metric) is not None]
                m,s = mean_std(vals)
                summary[metric+"_mean"] = m
                summary[metric+"_std"] = s

            candidates.append({
                "pipeline_id":f"{feature_mode}+{model_name}",
                "feature_mode":feature_mode,
                "model":model_name,
                "complexity":complexity + (0 if feature_mode=="all" else 1),
                "outer_metrics":summary,
                "fold_metrics":fold_metrics,
                "best_params_per_fold":best_params,
                "fit_seconds_total":fit_seconds,
            })

    candidates.sort(key=lambda r:(
        -r["outer_metrics"]["balanced_accuracy_mean"],
        -r["outer_metrics"]["mcc_mean"],
        -(r["outer_metrics"]["pr_auc_mean"] if r["outer_metrics"]["pr_auc_mean"] is not None else -1),
        r["outer_metrics"]["balanced_accuracy_std"],
        r["complexity"],
    ))

    metric_winner = candidates[0]
    recommended = metric_winner
    tie = None
    if len(candidates) > 1:
        tie = paired_tie(False,candidates[0],candidates[1],"balanced_accuracy")
        if tie["practical_tie"]:
            recommended = sorted(
                candidates[:2],
                key=lambda r:(r["complexity"],-r["outer_metrics"]["balanced_accuracy_mean"])
            )[0]

    q3[lab] = {
        "status":"PASS",
        "class_counts":{"0":int(counts[0]),"1":int(counts[1])},
        "candidates":candidates,
        "metric_winner":metric_winner["pipeline_id"],
        "top2_tie_analysis":tie,
        "recommended_pipeline":recommended["pipeline_id"],
    }
    q3_recommendations[lab] = recommended["pipeline_id"]

q2_runner = q2_candidates[1] if len(q2_candidates) > 1 else None
if q2_tie is not None and q2_tie.get("practical_tie"):
    q2_reason = (
        f"Top pipelines are a practical tie on outer-fold RMSE; "
        f"recommend {q2_recommended['pipeline_id']} because it has lower declared complexity/risk."
    )
else:
    q2_reason = (
        f"Recommend {q2_recommended['pipeline_id']} because it wins the declared lexicographic rule: "
        f"RMSE first, then MAE and variability."
    )

q2_decision = {
    "recommended": q2_recommended["pipeline_id"],
    "metric_winner": q2_metric_winner["pipeline_id"],
    "runner_up": q2_runner["pipeline_id"] if q2_runner else None,
    "reason": q2_reason,
    "runner_up_rmse_gap": (
        q2_runner["outer_metrics"]["rmse_mean"] - q2_recommended["outer_metrics"]["rmse_mean"]
        if q2_runner else None
    ),
    "switch_condition": (
        "Switch if repeated/independent validation shows the alternative has a stable RMSE advantage "
        "outside the current fold-wise uncertainty band, or if the recommended selector is materially less stable."
    )
}

q3_decisions = {}
for lab, info in q3.items():
    if info.get("status") != "PASS":
        q3_decisions[lab] = {"recommended": None, "reason": info.get("reason")}
        continue
    rec_id = info["recommended_pipeline"]
    winner_id = info["metric_winner"]
    runner = info["candidates"][1] if len(info["candidates"]) > 1 else None
    tie = info.get("top2_tie_analysis")
    if tie is not None and tie.get("practical_tie"):
        reason = (
            f"Top pipelines are a practical tie on balanced accuracy; recommend {rec_id} "
            f"because it has lower declared complexity/risk."
        )
    else:
        reason = (
            f"Recommend {rec_id} by the declared rule: balanced accuracy, then MCC, PR-AUC and variability."
        )
    rec_row = next(x for x in info["candidates"] if x["pipeline_id"] == rec_id)
    q3_decisions[lab] = {
        "recommended": rec_id,
        "metric_winner": winner_id,
        "runner_up": runner["pipeline_id"] if runner else None,
        "reason": reason,
        "runner_up_balanced_accuracy_gap": (
            rec_row["outer_metrics"]["balanced_accuracy_mean"] -
            runner["outer_metrics"]["balanced_accuracy_mean"]
            if runner else None
        ),
        "switch_condition": (
            "Switch if repeated/independent validation shows another pipeline has a stable advantage "
            "in balanced accuracy/MCC/PR-AUC, or if probability calibration requirements change the ranking."
        )
    }

result = {
    "schema_version":"0.9",
    "case_id":"gmcm-2021-D",
    "profile":ARGS.profile,
    "seed":SEED,
    "environment":{
        "python":platform.python_version(),
        "sklearn":sklearn.__version__,
    },
    "data_audit_status":audit["status"],
    "q1_q2":{
        "outer_folds":PROFILE["outer"],
        "inner_folds":PROFILE["inner"],
        "candidates":q2_candidates,
        "metric_winner":q2_metric_winner["pipeline_id"],
        "top2_tie_analysis":q2_tie,
        "recommended_pipeline":q2_recommended["pipeline_id"],
        "recommended_selector_stability_jaccard":q2_recommended["selector_stability_jaccard"],
        "recommended_selection_frequency":q2_recommended["selection_frequency"],
    },
    "q3":q3,
    "recommendations":{
        "q2":q2_recommended["pipeline_id"],
        "q3":q3_recommendations,
        "rule":"lexicographic metrics; practical ties prefer lower complexity",
    },
    "decision_explanations":{
        "q2":q2_decision,
        "q3":q3_decisions,
    },
    "test_isolation":{
        "used_in_benchmark":False,
        "allowed_next_use":"final prediction only after route is frozen",
    }
}

(OUT/"model_benchmark.json").write_text(
    json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8"
)

lines = [
    "# 2021 D Leakage-Safe Model Benchmark","",
    f"Profile: `{ARGS.profile}`",
    f"Data audit: `{audit['status']}`","",
    "## Q1/Q2",
    f"- Metric winner: `{q2_metric_winner['pipeline_id']}`",
    f"- Recommended: `{q2_recommended['pipeline_id']}`",
    f"- RMSE: {q2_recommended['outer_metrics']['rmse_mean']:.6f} ± {q2_recommended['outer_metrics']['rmse_std']:.6f}",
    f"- MAE: {q2_recommended['outer_metrics']['mae_mean']:.6f} ± {q2_recommended['outer_metrics']['mae_std']:.6f}",
    f"- R²: {q2_recommended['outer_metrics']['r2_mean']:.6f} ± {q2_recommended['outer_metrics']['r2_std']:.6f}",
    f"- Selector stability Jaccard: {q2_recommended['selector_stability_jaccard']}",
    f"- Why: {q2_decision['reason']}",
    f"- Switch condition: {q2_decision['switch_condition']}",
]
if q2_tie is not None:
    lines.append(f"- Top2 practical tie: {q2_tie['practical_tie']}")
lines += ["","### Top20 by selection frequency"]
for x in q2_recommended["selection_frequency"][:20]:
    lines.append(f"- {x['feature']}: {x['frequency']:.3f}")

lines += ["","## Q3"]
for lab in labels:
    info = q3[lab]
    if info["status"] != "PASS":
        lines.append(f"- {lab}: BLOCKED — {info['reason']}")
        continue
    rec = info["recommended_pipeline"]
    row = next(c for c in info["candidates"] if c["pipeline_id"] == rec)
    m = row["outer_metrics"]
    lines.append(
        f"- {lab}: `{rec}` | balanced_accuracy={m['balanced_accuracy_mean']:.4f} "
        f"| MCC={m['mcc_mean']:.4f} | PR-AUC={m['pr_auc_mean'] if m['pr_auc_mean'] is not None else 'NA'}"
    )
    lines.append(f"  - Why: {q3_decisions[lab]['reason']}")
    lines.append(f"  - Switch: {q3_decisions[lab]['switch_condition']}")

lines += [
    "","## Decision rule",
    "- Q2: RMSE → MAE → RMSE std → lower complexity on practical tie.",
    "- Q3: balanced accuracy → MCC → PR-AUC → lower variability → lower complexity on practical tie.",
    "- Official test set was not used.",
]
(OUT/"model_benchmark.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("[PASS] benchmark written to",OUT)
