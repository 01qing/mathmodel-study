# MathModel-Core v1.32 Progress

## 1. Version role

v1.32 continues the frozen **Train** path with **S034 / 2025-C / Train**, the third of five 2025-C Train papers. It is an incremental successor to sealed v1.31. No role Skill is split or copied. S030/S031 remain unused Dev reserve, and all Test solution content remains frozen.

The capability-oriented protocol remains active: integration/regression PASS establishes persistence, isolation and contract consistency, not new-problem capability improvement. The 2025-C Mini Transfer Test, Capability Evidence Gate and `No-Core / Previous-Core / New-Core` controlled ablation remain **NOT_DUE** until S032-S036 are complete.

## 2. Source identity and evidence level

- Paper: `S034`
- Case group: `2025-C`
- Title: 《围岩裂隙精准识别与三维模型重构》
- Split: Train
- Original PDF pages: **68**
- Source SHA256: `23dfbdeb5af6468a92428c0171ccfd569b6571066837df96b1960f47248b1d1f`
- Full-text review: complete
- Original-PDF visual audit: **68/68 pages**, via 12 contact sheets
- Formula/pseudocode/result-surface audit: complete
- Author code: Appendix A references **Attachment 9: code for each question**, but the available excellent-paper collection contains PDFs only; the referenced code artifact is not available
- Reproduction level: **R1**

R2+ is not claimed. Full visual review and pseudocode inspection do not substitute for static audit of the actual referenced code artifact.

## 3. S034 model competition and audit

### Q1 fracture identification

The author uses six complementary classical detectors for coarse voting and then scores connected components with 12 manually weighted features using a 6/10 threshold. The Q1 confusion-count arithmetic is internally consistent: the three-image macro Precision/Recall/F1 replay to approximately **0.895512 / 0.922012 / 0.908568**, matching the reported 89.5% / 92.2% / 90.8% after rounding.

The decisive evidence gap is not arithmetic but **ground-truth provenance and independence**. The paper does not establish who/what produced the reference fracture masks, how ambiguous pixels were handled, or whether the manual feature weights and threshold were tuned independently from the three evaluated images. MathModel-Core therefore retains a transparent classical ridge/edge + morphology/component pipeline as the 6-hour baseline. If reliable labels exist, a small interpretable classifier for component scoring should be tested before escalating to a deep segmenter.

### Q2 sinusoidal fracture grouping and fitting

Model 1 combines DBSCAN, band merging and RANSAC/least-squares sinusoid fitting; Model 2 uses adaptive windows plus a reduced Hough formulation. The comparison table favors Model 1 with reported effective-fit rate **0.78 vs 0.42**, median R² **0.847 vs 0.741**, and RMSE **3.1 vs 5.6**. However, the table's p-values are not accompanied by a named test, statistic, sample unit, pairing rule or sample size, so significance provenance remains unresolved.

Two implementation contracts are also incomplete. Eq.35 is described as a horizontal merge criterion while using `|y_A-y_B|`; Algorithm 3 outputs `P*` although the visible initialization/estimation steps name only R/beta/C. More importantly, Model 1 reports freely varying periods around **80-110 mm**, while the cylindrical unfolded-image geometry later identifies a physical circumference period. The Core therefore keeps **fixed-period bounded robust sinusoidal fitting with reject logic** as the preferred baseline when borehole diameter is known.

### Q3 roughness / JRC

The Fourier + DWT decomposition and four sampling schemes are useful as **multiscale and numerical-sensitivity diagnostics**. They are not by themselves evidence that the enhanced JRC estimator is physically more accurate. The Bootstrap pseudocode switches estimator language from least squares to maximum likelihood and prints the percentile interval endpoints in reverse conventional order. Dense-sampling convergence is described as a “true JRC” despite the absence of an independent physical ground truth.

The enhanced-JRC coefficients `alpha=0.15±0.03` and `beta=0.02±0.01` have no visible calibration provenance. There is also a cross-stage range contract: Q3/Q4 JRC outputs extend well above 20, while Q4 later uses `JRCmax=20` as a similarity scale. MathModel-Core therefore preserves the stable route: **ordered physical centerline -> one canonical JRC -> sampling-budget convergence/sensitivity**, and treats uncalibrated correction terms as heuristic until independently justified.

### Q4 3D connectivity and supplementary drilling

The author reconstructs 3D fracture geometry, multiplies five factors into a quantity called connectivity probability, thresholds the graph, uses DFS for connected components, builds a distance-decay/IDW information field, and greedily selects supplementary borehole locations.

The chain is transparent but several semantics are overclaimed. Without labeled connectivity calibration, the five-factor product is a **compatibility score**, not a calibrated probability. A deterministic distance-decay/IDW field is a **spatial coverage/information surrogate**, not posterior uncertainty. Its marginal decrease after adding a borehole is not expected information gain unless an observation model and expected posterior update are defined.

The Result Registry records a direct headline drift: the abstract says **32/50 = 64% isolated**, while the body says about **85%** are unconnected. These cannot be the same isolation statistic. The reported uncertainty reduction `0.523 -> 0.395` replays to **24.474%**, consistent with 24.5% after rounding.

The 500 mm spacing rule also exposes a set-definition issue. The three proposed new locations satisfy new-new spacing, with minimum **800 mm**. But `(800,1300)` is about **424.264 mm** from existing hole 4 `(500,1000)`. If the engineering rule applies to all boreholes, the mathematical constraint is incomplete because it only constrains new-new pairs. Final recommendations must replay every interacting hard-constraint set before ranking.

## 4. New generic Core gates from S034

v1.32 adds or strengthens these reusable rules:

- confusion metrics require ground-truth-mask provenance and split/tuning independence, not just correct arithmetic;
- p-values require named test/statistic/sample-unit/sample-size/pairing provenance;
- every pseudocode output parameter must have a visible generation/estimation/update primitive;
- Bootstrap estimator and percentile-CI endpoint order must match the claimed procedure;
- high-resolution numerical convergence is a numerical reference, not physical ground truth;
- heuristic `[0,1]` factor products are scores until calibration justifies probability semantics;
- deterministic coverage fields are not posterior uncertainty, and coverage reduction is not expected information gain;
- hard pairwise constraints must explicitly cover all relevant interacting sets, including existing-new as well as new-new;
- a paper statement that “code is in an attachment” does not qualify for R2 unless that code artifact is actually available and audited.

## 5. 2025-C Same-Problem Map after S032 + S033 + S034

The provisional 2025-C map now marks **S032, S033 and S034 reviewed**, with **S035-S036 pending**.

Current cross-paper evidence increasingly favors:

- Q1: route by label budget and evaluate at original-image/borehole level; separate predictive quality from deployment cost and demand metric-label provenance;
- Q2: unknown-count/topology-aware instance grouping + **fixed-period bounded robust fitting + reject state** when borehole geometry fixes the period;
- Q3: ordered physical profile + canonical roughness/JRC + explicit sampling sensitivity; use Fourier/DWT/adaptive sampling as diagnostics until enhanced estimators have calibration or independent truth;
- Q4: use attachment-derived upstream inputs, distinguish compatibility from probability, propagate uncertainty honestly, enforce all hard feasibility constraints, and reserve “expected information gain” for a genuine observation/posterior-update model.

The Method Composer remains provisional. Compatible local modules are recorded only after checking input/output interfaces, variable definitions, data distribution, mathematical assumptions, units, train/execution stage and evaluation metrics. No final 2025-C winner is selected before S035/S036.

## 6. Validation evolution

The S034 specialist suite contains **163/163 PASS** checks covering source identity, R1 ceiling, Candidate Model Competition, Result Registry, code-access boundary, method modules, provisional Same-Problem Map, seven-gate Method Composer state, figure evidence, retrieval metadata, split protection and independent arithmetic replay.

Inherited suites also pass:

- v1.29 Dev-boundary: **67/67 PASS**
- v1.30 S032: **75/75 PASS**
- v1.31 S033: **119/119 PASS**

The 22 historical Core regression scripts from v1.6, v1.8 code-learning, v1.9 training and v1.10-v1.28 were rerun with per-script exit-code enforcement: **22/22 PASS**.

Historical time-point assertions were adapted without weakening substantive gates. Pre-v1.32 copies of the v1.30 and v1.31 specialist tests are preserved under `history_snapshots_pre_v132_s034/`. S034 is now legitimately reviewed Train evidence; S035/S036 remain unread. S030/S031 remain Dev reserve and all Test papers remain unread.

## 7. Next action

After v1.32 release validation and sealing, continue **S035 / 2025-C / Train**. Do not consume S030/S031 Dev reserve and do not open Test solution artifacts. The 2025-C Mini Transfer Test, Capability Evidence Gate and controlled Core ablation remain **NOT_DUE** until S036 closes the five-paper Train group.

## 8. Release-contract check

Before sealing, a dedicated v1.32 release validator was added and rerun. The final result is **50/50 PASS**. Its first dry run exposed only a validator-schema mismatch (`pending` vs the persisted `papers_pending` field); that first failure is retained rather than overwritten. No S034 evidence, split rule, Method Composer result or reproduction level was changed to make the release validator pass.
