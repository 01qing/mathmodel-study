# S034 / 2025-C MathModel-Core Training Report

## Status

- Split: **Train**
- Paper: S034 / C题-3《围岩裂隙精准识别与三维模型重构》
- Pages: **68**
- Source SHA256: `23dfbdeb5af6468a92428c0171ccfd569b6571066837df96b1960f47248b1d1f`
- Full-text review: complete
- Original-PDF visual audit: **68/68**, 12 contact sheets
- Author code: Appendix A references Attachment 9, but the available excellent-paper package contains PDFs only; code artifact unavailable
- Reproduction level: **R1**

R2+ is not claimed. Formula, pseudocode, figure and result surfaces were audited, but no printed/attachment code was available to inspect.

## Q1

Author uses six complementary classical detectors for coarse pixel voting, followed by a 12-feature connected-component score with a 6/10 acceptance threshold. Table 5 arithmetic is internally consistent: the three-image macro Precision/Recall/F1 replay to about **0.8955 / 0.9220 / 0.9086**, matching 89.5% / 92.2% / 90.8% after rounding. The missing evidence is **reference-mask provenance** and independent tuning/holdout: the paper does not state who/what created the ground truth or whether the manual weights/threshold were chosen independently of the evaluated images.

6-hour baseline remains a transparent ridge/edge + morphology/component pipeline. If labels exist, learn the 12-feature weights with logistic/tree models before escalating to a deep segmenter.

## Q2

Model 1 is DBSCAN + horizontal-band merge + RANSAC/least-squares sinusoid; Model 2 is adaptive sliding windows + reduced Hough. Table 6 prefers Model 1 (0.78 vs 0.42 effective-fit rate, median R² 0.847 vs 0.741, RMSE 3.1 vs 5.6), but its p-values have **no named test/statistic/sample-unit/sample-size provenance**.

Two method contracts are weak: Eq.35 calls the merge criterion horizontal but uses `|y_A-y_B|`; Algorithm 3 outputs `P*` although its initial fit names only R/beta/C. Model 2 explicitly fixes P, while Model 1 Table 7 lets P vary 80-110 mm even though later Q3 correctly states the cylindrical period is fixed by borehole circumference. Core therefore retains fixed-period bounded robust fitting as the preferred baseline.

## Q3

The paper's Fourier + DWT decomposition is useful as a **multiscale diagnostic**, and the four sampling schemes make numerical sensitivity visible. It is not yet evidence that the enhanced estimator is more physically accurate. Bootstrap pseudocode switches from least squares to MLE and reverses the conventional percentile CI endpoints. The text calls dense-sampling convergence a 'true JRC' even without external ground truth. RAF coefficients `alpha=0.15±0.03`, `beta=0.02±0.01` have no visible calibration provenance.

The stable Core route remains ordered physical centerline -> one canonical JRC -> estimate-vs-sampling-budget convergence; adaptive sampling is promoted for efficiency only after a declared numerical reference or external truth.

## Q4

The five-factor product, DFS thresholding and distance-decay/IDW drilling chain is transparent but semantically overclaimed. Without connectivity labels, the product is a **compatibility score**, not calibrated probability. The distance-decay field is a deterministic **coverage surrogate**, not a posterior distribution; its marginal reduction is not expected information gain.

Result Registry finds a direct headline drift: the abstract says **32/50 = 64% isolated**, while section 6.3.3 says about **85%** unconnected. The reported uncertainty reduction **0.523 -> 0.395** does replay to **24.474%**, consistent with 24.5% rounding.

The 500 mm spacing constraint has a set-definition issue. New-new distances are all >=800 mm, so Eq.71 is satisfied as written. But the first proposed location (800,1300) is about **424.3 mm** from existing hole 4 at (500,1000). If 'boreholes must remain >=500 mm apart' applies to all holes, the model is missing existing-new feasibility constraints.

## Cross-paper effect after S032 + S033 + S034

- Q1: label-budget routing is now supported by three papers; metric provenance/holdout identity is more important than model complexity.
- Q2: all evidence increasingly favors physical fixed-period robust fitting plus explicit reject over extra free parameters or pseudo-complexity.
- Q3: multiscale/adaptive ideas are useful diagnostics, but no three-paper evidence yet validates uncalibrated JRC correction formulas over the canonical physical baseline.
- Q4: three independent Train papers repeatedly blur compatibility score/probability and hotspot/coverage/EIG; this is now a strong Core gate. Hard constraints must be replayed before ranking.

S035-S036 remain unread. No final 2025-C winner, Mini Transfer, Capability Evidence Gate or controlled Core ablation is due yet.
