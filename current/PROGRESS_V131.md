# MathModel-Core v1.31 Progress

## 1. Version role

v1.31 continues the frozen **Train** path with **S033 / 2025-C / Train**, the second of five 2025-C Train papers. It is an incremental successor to sealed v1.30; no role Skill is split or copied. S030/S031 remain unused Dev reserve and all Test solution content remains frozen.

The capability-oriented protocol remains unchanged: regression/integrity PASS proves persistence and contract compatibility, not new-problem capability improvement. The 2025-C Mini Transfer Test and `No-Core / Previous-Core / New-Core` controlled ablation remain deferred until S032-S036 are complete.

## 2. Source identity and evidence level

- Paper: `S033`
- Case group: `2025-C`
- Title: 《围岩裂隙精准识别与三维模型重构》
- Split: Train
- Original PDF pages: **78**
- Frozen/source SHA256: `bc6529349c3a053b7774731f2fa3e383f6337807fd33954ee7726b04949878fd`
- Full-text review: complete
- Original-PDF visual audit: **78/78 pages**, via 13 contact sheets
- Printed Python appendix static audit: **pages 52-78**
- Reproduction level: **R2**

R3+ is not claimed. The printed appendix omits several headline algorithms and does not form a self-contained executable Q1-Q4 chain with original data.

## 3. S033 model competition and audit

### Q1 fracture identification

The paper compares multi-feature K-Means, direction-enhanced Canny and YOLOv8. One body section describes YOLOv8 as visually better, while the abstract/final route chooses Canny because of annotation cost, interpretability and practical deployment. MathModel-Core therefore records **predictive winner** and **deployment recommendation** as separate decisions rather than forcing one global winner.

The 6-hour baseline remains Canny/ridge-style filtering + morphology/connected-component cleanup; with reliable labels, add a compact U-Net/segmentation model and compare on held-out boreholes/images. The author appendix only exposes a Canny fragment; augmentation, illumination/NLM/Gabor/LBP, K-Means and YOLOv8 training/evaluation are not self-contained. The visible Q1 code also points to a `fujian3` path, creating cross-question provenance drift.

### Q2 sinusoidal fracture grouping and fitting

The author route uses GMM grouping and compares a gradient-descent/Newton scheme with a no-hidden-layer linear neural parameterization optimized by Adam. Core keeps **unknown-count/topology-aware grouping + fixed-period bounded robust sinusoidal fitting + reject state** as the preferred baseline when borehole diameter fixes `P=pi*D`.

Important audit findings:

- visible example hard-codes `n_components=3`, yet the paper reports 5/1/3 fractures for the three example images;
- a BIC helper exists but is bypassed by the fixed `n_components=3` call;
- pixel-mode GMM uses coordinate features only and does not visibly implement the claimed direction-consistency feature;
- `Total_Fractures=len(labels)` counts assignments rather than GMM components/fractures;
- the printed appendix contains neither the GD/Newton fitting chain nor the Adam/neural sine optimizer;
- fitting the neural parameterization on the same fracture and reporting R² on that same curve is **same-instance self-fit**, not evidence of cross-fracture learned generalization;
- comparison prose says seven fracture groups while the visible table contains nine rows;
- the nine-row arithmetic replays to about **0.586411** for GD/Newton and **0.796978** for the neural/Adam route; the word “significantly” is not backed by a reported test/effect-size interval;
- all final displayed periods are `94.25 mm`, so the registry distinguishes a fixed physical period from a genuinely estimated parameter.

### Q3 roughness / JRC

The paper studies equal/adaptive sampling and proposes a second-derivative `Z3` improvement. Core does not promote that enhancement yet. The body alternates among multiple JRC mappings, later claims an area correction while the displayed improved formula contains no area term, and Appendix C implements only the original `51.85*Z^0.6-10.37` form.

A key generic gate is added: slope/curvature roughness formulae require an **ordered physical profile**. `cv2.findContours(..., RETR_EXTERNAL, CHAIN_APPROX_NONE)` produces a closed 2D boundary, not automatically a single-valued `y(x)` profile. The visible code also selects `min(Z1,Z2)` without a body-defined estimator contract.

A further range-contract issue is registered: the paper states a conventional JRC range of 0-20, reports values up to **38.01**, then uses `1-|JRC1-JRC2|/20` as a Q4 similarity. Without explicit calibration/clipping semantics, this downstream score is not safely bounded.

### Q4 3D connectivity, uncertainty and supplementary drilling

The conceptual chain is useful, but the numerical evidence is weak. The paper explicitly states that the six boreholes/fracture parameters in this stage are simulated/set by engineering common sense, and the appendix uses fixed fracture data. Those outputs are therefore **scenario evidence**, not demonstrated attachment-derived reconstruction results.

The weighted geometry/JRC/overlap fusion followed by a sigmoid is called connectivity probability without labeled calibration. The binary uncertainty expression omits the `(1-p)` Bernoulli entropy term. Current local mean entropy is called information gain even though no observation model or expected posterior entropy reduction is computed; some fallback `info_gain` values are even constants.

The hard-constraint replay is decisive: body text requires supplementary-hole spacing `>=500 mm`, Table 8 reports a third point with **412.3105 mm**, and Appendix D uses a **300 mm** threshold. The visible loader also keeps only `depth_max<=500 mm`, while the body reports connectivity intervals at 2000-7000 mm. `self.uncertainty_data` is not visibly assigned before use, and the printed main does not call the borehole optimizer. The final drilling table therefore cannot be reproduced by the visible entrypoint.

## 4. Result Registry and generic rules

The S033 Result Registry now records 14 source-level contracts, including Q1 predictive/deployment semantics; Q2 table arithmetic, cluster-count and fixed-period contracts; Q3 formula/area/range drift; and Q4 simulated-data provenance, pseudo-probability, Bernoulli entropy, pseudo-information-gain, spacing, depth and incomplete-chain findings.

`replay_s033_registry.py` performs **11/11 audit/replay checks**. A replay PASS means the registered arithmetic or semantic inconsistency was reproducibly checked; it is not author-code reproduction and does not raise S033 above R2.

Generic reusable gates added from S033 include: same-instance fit is not generalization; cluster-count/result contracts must close; a closed contour is not automatically a roughness profile; binary-event entropy must include both event states; expected information gain needs an observation/posterior-update model; synthetic upstream inputs must remain scenario evidence; fixed physical parameters must not be described as estimated; and bounded similarity normalizers must match the actual upstream value range.

## 5. 2025-C Same-Problem Map after S032 + S033

The provisional map now marks S032 and S033 reviewed, with S034-S036 pending.

Current evidence favors the following provisional direction: Q1 route by label budget and held-out grouped metrics while separating predictive quality from deployment cost; Q2 use unknown-count/topology-aware grouping with fixed-period bounded robust fitting and reject; Q3 retain ordered physical profile + canonical JRC + sampling sensitivity until sophisticated improvements gain executable/calibrated evidence; Q4 use attachment-derived inputs, transparent/calibrated connectivity semantics, propagated uncertainty, hard-feasible candidates and true expected-information-gain or robust MCDA.

No final 2025-C winner is selected and no Mini Transfer is run yet.

## 6. Test/retrieval evolution during v1.31

The original v1.30 S032 specialist test included a release-time assertion that S033 was unread. Before adapting it, the exact original test was snapshotted with SHA256 `9e6f691dfda0063f29bcaf0efd453a9eed70e24002b1cdff70116e616dfd099f`. The live test now preserves all 75 S032 semantic checks but replaces that obsolete future-paper assertion with a gate that S034-S036 remain unread.

During the v1.31 historical rerun, `test_v126_regressions.py` initially failed because `next_learning.md` used the shorthand “2025-C Mini Transfer” instead of the historical exact phrase “Mini Transfer Test”. The protocol itself was present; the context file was made explicit and the unweakened historical test then passed.

The retriever documentation was also corrected to match the actual v1.29+ code boundary: ordinary `evaluation` **and** `production` retrieval are reviewed-Train-only. Dev uses a dedicated post-freeze validation path; Test remains protected.

## 7. Next action

After v1.31 release validation and sealing, continue **S034 / 2025-C / Train**. Keep S030/S031 as Dev reserve and keep all Test paper answers/code/figures/parameters/conclusions unread. Do not run the 2025-C Mini Transfer/controlled ablation before S036 closes the case group.
