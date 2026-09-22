# S033 / 2025-C MathModel-Core Training Report

## Status

- Split: **Train**
- Paper: S033 / C题-2《围岩裂隙精准识别与三维模型重构》
- Pages: **78**
- Source SHA256: `bc6529349c3a053b7774731f2fa3e383f6337807fd33954ee7726b04949878fd`
- Full-text review: complete
- Original-PDF visual audit: **78/78**, 13 contact sheets
- Printed Python appendix audit: **pp.52-78**
- Reproduction level: **R2**

R3+ is not claimed. The appendix omits several headline methods and the Q4 result chain uses hidden/fixed scenario data plus incomplete state/entrypoint logic.

## Q1

Author compares multi-feature K-Means, direction-enhanced Canny and YOLOv8. The body says YOLOv8 looks better, but the abstract/final discussion chooses Canny for annotation cost, interpretability and practical deployment. Core records these as **different objectives** rather than forcing one winner.

6-hour baseline: Canny/ridge + morphology first; if reliable masks exist, compact U-Net second. Compare on held-out boreholes/images and report accuracy plus annotation/runtime cost. The appendix only exposes Canny and does not make the three-way comparison reproducible.

## Q2

Author uses GMM grouping and compares gradient-descent/Newton with a no-hidden-layer linear neural parameterization optimized by Adam. Core retains **fixed-period bounded robust least squares** as the preferred baseline when borehole diameter fixes `P=pi*D`.

Key audit: the visible example hard-codes GMM `n_components=3`, while the paper reports 5/1/3 fractures; the BIC helper is bypassed. Appendix B does not show either sine optimizer. The so-called neural model is fitted through the same curve residual and has no independent cross-fracture holdout, so its higher in-sample R² is not evidence of learned generalization. Table 1 has 9 rows although the paragraph says seven; means replay to about 0.5864 and 0.7970.

## Q3

The paper studies equal/adaptive sampling and proposes a second-derivative `Z3` JRC improvement. Core does **not** promote it yet. The body alternates among multiple JRC formulas, the summary claims an area correction while the displayed improved formula has no area term, and Appendix C implements only the original `51.85*Z^0.6-10.37` form.

A new generic gate is learned: slope/curvature roughness formulas need an ordered physical profile. `cv2.findContours` returns a closed boundary and cannot automatically serve as single-valued `y(x)`. The paper also states a conventional JRC range of 0-20, reports Q3 values up to 38.01, and later normalizes Q4 JRC similarity by 20; this upstream/downstream range contract is therefore not safely bounded without calibration or justified clipping.

## Q4

The conceptual chain (3D plane -> connectivity -> uncertainty -> new measurement) is useful, but evidence is weak. Section 6.5 explicitly uses six simulated/common-sense boreholes/fractures; weighted compatibility is called probability without calibration; the entropy formula omits the Bernoulli `(1-p)` term; local current entropy is called information gain without a posterior-update model.

The most concrete result failure is the drilling constraint: the paper states minimum spacing `>=500 mm`, yet Table 8 row 3 reports `412.3105 mm`; Appendix D uses `>=300 mm`. The visible loader also filters `depth_max<=500 mm`, while body Table 6 reports 2000-7000 mm connectivity.

## Cross-paper effect after S032 + S033

- Q1: separate **predictive winner** from **deployment recommendation**; holdout metrics decide the former, annotation/runtime/interpretability the latter.
- Q2: evidence is converging toward fixed-period robust geometric fitting, not neural complexity.
- Q3: both S032 and S033 propose sophisticated roughness improvements that are not yet supported by complete executable/calibrated evidence; keep the physical baseline.
- Q4: both papers use heuristic connectivity/uncertainty decision layers; Core should keep them as transparent scores until calibration and true expected-information-gain validation exist.

S034-S036 remain unread. No final 2025-C winner and no Mini Transfer yet.
