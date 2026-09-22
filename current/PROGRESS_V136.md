# MathModel-Core v1.36 Progress

## Version role
v1.36 is the second 2025-F Train increment. MathModel-Core remains one shared Core; no role Skill split is created.

## S043 / 2025-F / Train
- title: 《江南古典园林的美学特征建模》
- pages: 71
- full-text review: complete
- original-PDF visual audit: **71/71 pages**
- code availability: p71 states the Q1-Q3 code is in an attachment, but that attachment is not present in the current PDF-only source package
- reproduction level: **R1**; R2+ is not claimed

### Main audited findings
- Q1 score-scale contract: Eq.(4-27) is a weighted combination of normalized terms/correlation and has theoretical maximum 1 under its stated definitions, but grade bands extend to 2.0 and the best reported Interest is 1.6294.
- Q1 optimizer semantics: the paper converts three goals to a weighted scalar objective, so the executable contract is scalarization rather than Pareto search. A heuristic GA is also said to obtain a global optimum with `Gap=0` without a visible exact bound/certificate.
- Q1 validation: fitness-vs-Interest correlation is endogenous because Interest is already the largest fitness component; it is not independent perceptual validation.
- Q2 scale replay: Eq.(5-14) nominally combines bounded components but table scores reach 4.620; Eq.(5-26) replays Jichang to 0.8905 rather than 5.730 and Liuyuan to 0.853 rather than 5.376.
- Q2 reference closure: Jichang is fixed to 100, yet self-similarity in Eq.(5-37) yields 115 before positive adjustment factors; the declared `Smax=100` therefore requires an unreported renormalization/clipping rule.
- Q3 matrix replay: 45 off-diagonal similarities replay to mean **0.6642666667**, population SD **0.0678113068**, not 0.632/0.089. The matrix range is 0.523-0.847 while adjacent prose says all similarities exceed 0.93.
- Q3 cluster summaries: large/medium/small within-group means replay to **0.6606666667 / 0.7403333333 / 0.6733333333**, not 0.721/0.741/0.735. Several pair values and rank/type narratives drift across tables.
- Q3 headline drift: abstract assigns 6.353 first place to Zhuozheng and 174.1 first-place fantasy score to Liuyuan; body tables instead give Jichang 6.353 first and Jichang 100/Liuyuan 95.1.
- Q3 method contract: Ward requires a compatible Euclidean representation; the text alternates between clustering from a fused similarity matrix and an Euclidean Ward formula. Code attachment is unavailable, so implementation cannot resolve this ambiguity. Similarity transitivity is also not a valid general assumption.

## Candidate Model Competition / 6-hour baselines
- Q1: keep middleline/walkable graph + transparent visibility/scene-change descriptors; use k-shortest/simple feasible candidates or epsilon-constrained ranking before a GA. Promote Pareto evolutionary search only if a tradeoff set is genuinely needed.
- Q2: use a small interpretable dimensionless descriptor set with externally declared normalization and sensitivity; external/held-out preference ratings are required before treating the constructed fantasy score as validated.
- Q3: prefer the compact path/scenic/spatial representation over d>>n representations, but use metric-compatible clustering, one matrix registry, bootstrap stability and independent labels/outcomes for generalization claims.

## New reusable Core gates
- derive theoretical score support before accepting grading/result scales;
- heuristic `global optimum/Gap=0` needs an exact certificate;
- scalar weighted sums are not Pareto search;
- correlation statistics require an explicit paired observation axis;
- reference anchors must pass self-score replay;
- all similarity statistics/cluster summaries must regenerate from one matrix registry;
- Ward requires an Euclidean distance/embedding contract;
- similarity is not generally transitive;
- absent attachment code keeps a paper at R1.

## 2025-F status
S042 (R2) and S043 (R1) are reviewed; S044-S045 remain unread Train. The Same-Problem Method Competition Map is provisional at 2/4. Mini Transfer Test / Capability Evidence Gate / controlled Core ablation remain **NOT_DUE until after S045**.

## Next stage
S030/S031 remain Dev reserve; all Test papers remain frozen. Next unread Train: **S044 / 2025-F**.
