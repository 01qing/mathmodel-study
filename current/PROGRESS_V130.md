# MathModel-Core v1.30 Progress

## 1. Version role

v1.30 resumes the frozen **Train** path after the v1.29 S029 / 2025-B Dev validation. The reviewed paper is **S032 / 2025-C / Train**, the first of five 2025-C Train papers. S030/S031 remain unused Dev reserve and all Test solution content remains frozen.

This version also formalizes the four adopted capability-oriented rules:

1. Capability Evidence Gate;
2. Controlled Core Ablation (`No-Core / Previous-Core / New-Core` under the same task/budget/tools/evaluator);
3. Persistent Evidence Contract;
4. Lean Core + Retrieval.

The consolidated prompt is stored as `MathModel-Core_采纳后统一训练提示词_v1.30.txt`.

## 2. Source identity and evidence level

- Paper: `S032`
- Case group: `2025-C`
- Title: 《围岩裂隙精准识别与三维模型重构》
- Split: Train
- Original source pages: **71**
- Frozen source SHA256: `6f14d27f0371e94857a592c7469eeec37172009384bdba8a847c26019e8d96c8`
- Full-text review: complete
- Original-PDF visual audit: **71/71 pages**, via 12 contact sheets
- Printed Python appendix static audit: pages **53-71**
- Reproduction level: **R2**

R3+ is not claimed: the appendix is not a complete executable project and several headline algorithm primitives are missing or drift from the prose.

## 3. S032 task decomposition and Core model competition

### Q1 - fracture pixel segmentation

Author route: CLAHE + bilateral filtering + Sobel, then improved U-Net with ResNet50 encoder, multi-scale/ASPP-style context and attention. Reported Table 4 values include Accuracy 98.7%, IoU 73.1%, Recall 79.1% and F1 84.8% for the improved U-Net.

Core 6-hour baseline: split by original borehole/image first, then use morphology as a sanity baseline and a compact U-Net with simple imbalance-aware loss. Promote ResNet50/ASPP/attention only if **held-out-borehole/image** IoU/F1 gains are stable.

Key audit: the printed appendix does not expose a defensible source-image/borehole train/val/test split, the claimed improved loss is external to the shown training function, and the printed loop does not show the claimed FP16/gradient-clipping path. Apparent IoU/F1 algebraic differences are retained as an aggregation-provenance question rather than declared automatically wrong.

### Q2 - fracture grouping and sinusoidal parameter fitting

Author route: connected-region grouping + DBSCAN, skeleton extraction, fixed-period sinusoidal fit; prose additionally describes frequency initialization, LM, RANSAC, Huber/IRLS-like robustness.

Core 6-hour baseline: component extraction + topology/orientation-aware fragment merge + **bounded robust least squares** with period fixed to the borehole circumference; canonicalize amplitude/phase and add an explicit reject/unmodelled state.

Key audit:
- printed code mainly shows centroid DBSCAN and plain `scipy.optimize.least_squares`, not the full RANSAC/Huber/IRLS chain;
- the paper first defines amplitude `R=max(y)-min(y)`, while later initialization/code use half-range `(max-min)/2`;
- Table 5 contains a physically suspicious fit (`R=975.632 mm`, `R²=0.6207`), demonstrating the need for a plausibility/reject gate;
- Q2 printed code reconstructs the mask from JSON polygon annotations rather than consuming Q1 predictions, so it is an **oracle-intermediate** downstream evaluation rather than end-to-end evidence.

### Q3 - complex-fracture roughness / JRC

Author route: multi-scale LoG attention fusion, equal-spacing vs curvature-weighted sampling, Z2-to-JRC empirical mapping, and segmented JRC.

Core 6-hour baseline: extract one physically calibrated contour, apply mild smoothing, compute Z2/JRC over several sampling densities, report raw Z2, JRC, saturation and sensitivity; do not introduce per-image tuning constants without external/train-only calibration.

Key audit:
- printed appendix does not show the headline LoG-attention implementation;
- per-image `SCALE_FACTORS` multiply Z2 before JRC;
- JRC is hard-clipped to `[0,20]`, while the body describes a mean around 75 in one result discussion;
- the curvature-weighted sampler uses cumulative `distance / weight`, where weight increases with curvature; this tends to allocate **less** transformed measure and fewer samples to high-curvature segments, opposite the stated densification intent;
- Q3 again constructs masks from JSON annotations, bypassing Q1 prediction error.

### Q4 - connectivity, uncertainty and supplementary drilling

Author route: weighted geometric connectivity + sigmoid JRC correction + synergy bonus, uncertainty via CV/entropy, then AHP and projection-pursuit improved GA for three supplementary boreholes.

Core 6-hour baseline: call the hand-built quantity a **geometry compatibility score** unless calibrated; propagate Q1-Q3 uncertainty via bootstrap/Monte Carlo; map high-uncertainty areas; select new holes by expected information gain / coverage under engineering constraints, or use transparent robust MCDA with weight sensitivity.

Key audit:
- weighted `[0,1]` score is not automatically a probability;
- the prose says `Pjrc` uses the geometric mean of `k1,k2`, but Eq. 4-21 is printed as an incompatible additive expression;
- one entropy implementation correctly normalizes histogram counts, another uses `density=True` heights directly in Shannon entropy;
- the appendix hard-codes a neighbor list inconsistent with the 2x3-array/body discussion (body explicitly discusses 1#-4# and 3#-6#);
- AHP is described conceptually but shown with directly assigned weights; no judgment matrix consistency evidence is visible;
- the two arithmetic-crossover children in Eq. 4-39/4-40 are identical;
- projection-pursuit mean score 9.95 vs AHP 8.40 is an endogenous score comparison and is not independent evidence of better real drilling decisions or statistical significance;
- PPIGA implementation is not present in the printed appendix.

## 4. Result Registry highlights

The v1.30 registry records source-level results and keeps conflicts unresolved where provenance is insufficient. Important entries include:

- Q1 Table 4 metrics and the F1/IoU aggregation-provenance replay;
- Q2 extreme fit `R=975.632 mm, R²=0.6207`;
- Q2 amplitude-definition drift;
- Q2/Q3 oracle-intermediate bypass;
- Q3 body JRC ≈75 vs appendix clip `[0,20]`;
- Q3 per-image scale-factor injection and reversed curvature-sampling direction;
- Q4 9.95 vs 8.40 score-comparison boundary;
- Q4 entropy implementation conflict;
- Q4 `Pjrc` formula/prose conflict;
- Q4 duplicate crossover children and adjacency-graph drift.

`replay_s032_registry.py` performs arithmetic/provenance replay only; it is explicitly **not author-code reproduction**.

## 5. Generic rules promoted into Core

Only generic, reusable gates were promoted. The main additions are:

- source image/object/group split before patching/augmentation;
- metric-identity checks require macro/micro/per-image provenance before declaring inconsistency;
- nonlinear fits need physical bounds, residual diagnostics and reject state;
- sample/dataset-specific calibration constants need provenance and held-out validation;
- clipping saturation must be reported and raw latent metrics inspected;
- histogram density is not discrete probability mass for Shannon entropy;
- weighted compatibility score is not a probability without calibration;
- multi-stage pipelines must propagate upstream uncertainty;
- ground-truth intermediate features in downstream evaluation must be labeled **oracle upper bound**, separate from end-to-end results;
- higher optimized composite score is not external validation of recommendation quality.

## 6. 2025-C Same-Problem Map status

A provisional 2025-C map now exists for S032-S036. Only S032 is reviewed. S033-S036 remain unread/unreviewed for this stage. No final cross-paper winner is selected and no 2025-C Mini Transfer is run yet.

Current provisional baseline by question:

- Q1: grouped-image compact segmentation baseline;
- Q2: bounded robust fixed-period sinusoid + reject;
- Q3: physical-unit contour + sampling sensitivity + raw Z2/JRC saturation audit;
- Q4: transparent compatibility + propagated uncertainty + expected information gain / robust MCDA.

## 7. Next action

Seal v1.30 after validation, then continue **S033 / 2025-C Train**. Keep S030/S031 Dev reserve untouched and keep all Test solutions frozen. The 2025-C Mini Transfer and controlled Core ablation are due after S036 closes the case group.
