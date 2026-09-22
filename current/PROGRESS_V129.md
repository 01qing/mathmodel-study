# MathModel-Core v1.29 Progress

## 1. Version role

v1.29 is the first **Dev-validation** version after the 2025-A Train case group and its Mini Transfer Test were sealed in v1.28.

The paper used here is **S029 / 2025-B / Dev**. It is not imported as Train evidence.

## 2. Leakage-safe Dev protocol

Before opening S029, MathModel-Core independently read only public problem-only material and froze a candidate solution/baseline:

- file: `learning_output/dev_validation/2025-B-S029/pre_solution_baseline.md`
- SHA256: `f0c9a3e4878c8b16272b8e9c1634e08008aa4c712b3cf1fe3fe9090cafc8341e`
- state at freeze: `solution_opened=false`, `dev_or_test_solution_exposure=false`

Only after that freeze was S029 opened for development comparison.

## 3. Independent Core model-selection result

Before exposure, Core selected:

- Q1: EESM + monotonic rate calibration as the 6-hour baseline;
- Q2: physics-informed compact competition built around EESM/MIESM, SINR statistics, SVD/effective-rank/correlation features, with simple tree residual models before large deep models;
- Q3: SVD-derived TxBF features + EESM/MIESM + calibrated mapping;
- validation: group/trajectory/location/terminal or chronological holdout rather than random correlated rows;
- figures: calibration, prediction-vs-actual, ECDF/error quantiles, worst-group diagnostics and residual plots.

After solution exposure, S029 was found to use a highly overlapping physics-first family: EESM, MIESM, quantile/LSE variants, SVD TxBF features, monotonic mapping and unsupervised one-dimensional alignment.

This is positive Dev evidence that the Core can independently select a plausible model family.

## 4. Dev findings that changed generic Core rules

S029-specific answers were not promoted to Train knowledge. Only generic gates were added:

1. preserving device proportions in a random row 80/20 split does **not** guarantee independent generalization or avoid temporal/trajectory leakage;
2. unlabeled target-domain distribution alignment cannot prove predictive accuracy;
3. using target-batch median/IQR/mean/covariance is a **transductive** deployment contract and must be evaluated as such;
4. abstract/body/table/figure/code headline metrics must share Result Registry provenance;
5. a planned t-test/Wilcoxon procedure is not evidence unless statistics/p-values/effect sizes are actually reported;
6. appendix launcher scripts that import omitted algorithm-defining modules are not self-contained code and cannot justify R3;
7. physical algorithm labels such as MIESM must be checked against the actual mapping formula and modulation/coding assumptions.

## 5. S029 Result Registry diagnostics

### Q1

- abstract: RMSE ≈ 61.2 Mbps, Spearman ≈ 0.78;
- body aggregate: RMSE ≈ 62.55, MAE ≈ 49.61, Spearman ≈ 0.76;
- leave-one-file RMSE: 61.83 / 67.13 / 63.21.

The abstract headline currently has unresolved provenance relative to visible body results.

### Q2

- abstract MIESM RMSE improvement ≈ 8% is consistent with the visible Fig. 5.8 scale;
- abstract Spearman = 0.82 conflicts with Fig. 5.11, whose visible axis upper bound is ≈0.7916;
- the body discusses paired t-test/Wilcoxon p-values, but no reported p-value was found.

### Q3

TxBF/valid is explicitly unlabeled.

- abstract E1: about 228 → 311 Mbps; E4 aligned ≈297 Mbps;
- body E1: raw mean 269.12, DA 289.18, DAiqr 324.63;
- body E4: raw 284.51, aligned 320.65.

Therefore Q3 headline numbers drift across surfaces, and target-domain alignment can only support distribution-consistency claims, not accuracy claims.

## 6. Code evidence level

The appendix visibly prints:

- `quick_run.py`
- `quick_run_q2.py`
- `quick_run_q3.py`

but these import omitted modules such as `linkrate_baseline.train_eval`, `features`, `esm`, `io`, and `inference`. An absolute Windows output path is also present.

S029 therefore has **R2-equivalent Dev static evidence**, not R3. This does not become Train reproduction evidence.

## 7. Visual audit

The original 57-page PDF was rendered into contact sheets and reviewed. The evidence structure is compact:

- early pages: physical model and monotonic mapping diagrams;
- Q2: seven-model comparison scatter panels followed by RMSE/NRMSE/MAE/Spearman comparison figures;
- Q3: boxplot, aggregate-domain density plot and P25/P50/P75 alignment comparison;
- pages 36-57: printed code appendix.

The transferable figure lesson is to distinguish labeled accuracy figures from unlabeled distribution-alignment figures.

## 8. Retrieval hard-boundary fix

A pre-existing retrieval issue was fixed in v1.29:

- ordinary `evaluation` and `production` retrieval now use only **reviewed Train pages**;
- Dev/Test pages never enter ordinary Core retrieval;
- indexed-but-not-yet-reviewed Train pages are also excluded;
- S039-S041 had old `CORE_REVIEWED_FULL_TEXT_VISUAL_FULL_SCAN` status but missing `reviewed_pages`; these metadata were non-destructively backfilled without rereading or changing knowledge.

## 9. Dev budget decision

S030-S031 remain unused Dev reserve.

After sealing v1.29, resume Train at **S032 / 2025-C**. Do not consume all Dev papers sequentially.

