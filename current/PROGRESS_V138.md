# MathModel-Core v1.38 Progress

## 1. Version role

v1.38 closes the **2025-F Train case group** and completes review coverage of all **32 frozen Train papers**. MathModel-Core remains the single shared Core; no Master/Architect/Engineer/Writer/Reviewer split is created.

## 2. S045 / 2025-F / Train

- title: 《江南古典园林美学特征的量化建模与分析》
- pages: **94**
- source SHA256: `0cd7b0001352da9a88dc4d70df750389eb7989d5d2520959e1222a3f05ba2e76`
- full-text review: complete
- original-PDF visual audit: **94/94 pages**
- printed-code static audit: **pp62-94**
- reproduction level: **R2**
- R3+ is not claimed because the printed appendix materially diverges from the described GA/GMM-MRF/similarity pipelines and no self-contained author project/original-data executable chain was run.

## 3. S045 model-selection and audit findings

### Q1 route modeling

The transferable layer is `walkable geometry -> skeleton/key-node graph -> transparent route descriptors -> raw objective registry -> feasible route search`. The paper's formulas do not preserve one objective contract: Eq.(5.67) verbally includes route length and lists `lambda1/lambda2/lambda3`, but the displayed edge cost contains only `-lambda2*S + lambda3*R`; Eq.(5.71) later uses path length/repetition as GA fitness and drops the earlier scenic-interest term. Printed code uses `dijkstra_adj()` rather than an executable GA loop. Arbitrary positional crossover/random-node replacement also does not preserve graph adjacency by construction.

Core therefore promotes exact/k-shortest/RCSP/epsilon-style feasible baselines first and requires every decoded/repaired route to replay all hard graph/geometry constraints before evolutionary search can be trusted.

### Q2 illusion score / spatial clustering

Table 6.6 is arithmetically consistent with `Hg = 0.45*S + 0.55*R` under ordinary decimal half-up display rounding: all **10/10** rows replay. However, Jichang Garden is used as calibration/reference anchor, so its top rank cannot be reused as independent validation. The printed code does not implement the advertised GMM-MRF/EM/ICM/BIC chain; it uses KMeans/MiniBatchKMeans, contains `np.random.random()` placeholder openness, and mixes hard-set K values.

A new semantic failure was preserved: sensitivity code produces one aggregate score per parameter scenario, ranks that scenario vector, and compares it with a garden ranking only because both arrays happen to have length 10. Rank correlation now requires an explicit `entity_id x run_id` score matrix.

### Q3 similarity / external Heyuan application

The composite vector mixes large-unit length/count variables with bounded proportions before cosine similarity without an explicit reference-fitted scaling contract. Eq.(7.3) is set Jaccard, whereas Eq.(7.11) is a continuous `sum(min)/sum(max)` coefficient; these must be named separately. The external Heyuan example has no independent target/preference truth and therefore supports applicability/face validity, not accuracy/generalization.

Printed code hard-codes Heyuan similarities and changes `-0.791 -> 0.209` and `-0.857 -> 0.143` without one global registered transformation. Visual review of original PDF p59 also resolved Eq.(7.13) as `1-|A_natural/A_total-A_artificial/A_total|`; text extraction had dropped the absolute-value bars.

## 4. 2025-F Final Same-Problem Method Competition Map

S042-S045 are now **4/4 reviewed**. The final route is modular rather than a paper-level winner:

- **Q1:** feasible geometry/graph -> transparent scene-change/visibility descriptors -> raw objectives -> exact/k-shortest/RCSP/epsilon baseline -> only then genuine Pareto/GA if same-budget evidence justifies it -> final feasibility replay.
- **Q2:** deterministic auditable descriptors -> redundancy/unit audit -> simple clustering baseline -> optional spatial probabilistic model only with real primitive coverage and held-out gain -> non-circular calibration -> full entity-by-run sensitivity -> independent expert/held-out validation.
- **Q3:** compact auditable features -> reference/train-fitted scaling by feature block -> metric matched to data type -> immutable similarity-matrix registry -> clustering/stability as descriptive evidence -> external pair/preference/downstream truth gate.

Method Composer seven-gate compatibility checks are finalized in `knowledge_base/cross_paper_maps/2025-F-S042-S045.json`.

## 5. 2025-F Mini Transfer and Capability Evidence Gate

A post-learning non-garden warehouse inspection graph was used as a mechanism transfer. Naive positional one-point crossover between two individually feasible parent routes produced child edge `A -> D`, which is not in the graph: **first run FAIL**. The rule was repaired to splice only at a common feasible graph vertex (or construct a verified bridge) and replay every final decoded edge; the repaired child passed.

A supplementary heterogeneous-similarity fixture showed raw cosine >0.999 for both structurally different and structurally similar objects when one large-scale coordinate dominated. After declared block scaling, the intended separation returned. Overall status: **`PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX`**.

This is **not** clean blind R7 evidence. Clean Core-level capability gain remains `NOT_ESTABLISHED`. Controlled `No-Core / Previous-Core / New-Core` remains `NOT_RUN` because the current workspace does not provide one fixed agent harness that can instantiate all three conditions with identical base model, prompt, tools, budget, randomness contract and evaluator.

## 6. Frozen split state after Train completion

- total papers: **45**
- retrieval chunks: **6752**
- Train: **32/32 reviewed**
- Dev: **7 total**; S029 previously exposed under Dev protocol only; S013-S016 and S030-S031 remain unread
- Test: **6 total / 0 reviewed**; S021-S024 and S037-S038 remain frozen

## 7. Next stage

After v1.38 is formally sealed, begin the next **clean Dev cycle** on unread **2024-D** using:

`problem/data only -> independent Core solution -> freeze artifacts/hash -> then open Dev paper -> gap analysis -> generic rule/workflow update`.

S030/S031 remain secondary Dev reserve because S029 has already exposed 2025-B same-problem solution information. Test remains untouched.
