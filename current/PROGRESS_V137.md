# MathModel-Core v1.37 Progress

## Version role
v1.37 is the third 2025-F Train increment. MathModel-Core remains the single shared Core; no Master/Architect/Engineer/Writer/Reviewer split is created.

## S044 / 2025-F / Train
- title: 《多模态数据融合视角下江南古典园林美学特征量化建模研究》
- pages: **116**
- source SHA256: `d8e40c2d4765e4c50350715f3e5f739e2a2ce11974664c506a639e921e7ad840`
- full-text review: complete
- original-PDF visual audit: **116/116 pages**
- printed-code static audit: **pp86-116** (Q1 pp86-94, Q2 pp95-108, Q3 pp109-116)
- reproduction level: **R2**; R3+ is not claimed because the printed code is incomplete/materially inconsistent with the paper and no original-data executable chain was run.

## Main model-selection and audit findings
### Q1 route optimization
The transferable part is the transparent `walkable graph -> curvature/turning/crossing + field-of-view scene change -> raw route objectives` chain. The paper describes improved GA/Pareto optimization, but the printed `multi_objective_route_planning()` only invokes Dijkstra to return a single shortest path; no population, selection, crossover, mutation or Pareto archive primitive is present. Eq.(17) also scalarizes the advertised objectives. Core therefore requires complex optimizer labels to map to reachable defining primitives before promotion above a transparent baseline.

### Q2 illusion score
The paper presents element/open-close descriptors plus AHP-entropy weighting. Printed code instead contains `np.random` placeholders for several nominally real features, labels one weighting routine AHP-CRITIC while using fixed weights, and finally overwrites computed outputs with fixed score dictionaries matching Table 13. These paths are retained as negative evidence, not learned as valid numerical results. Table 13 totals do replay exactly as element + openness components. Table 15 states `Kappa > 0.833` while reporting `0.833`, so the displayed value fails the stated strict criterion.

### Q3 multimodal similarity/generalization
The paper advertises geometry/image/text fusion, MKL, contrastive learning, persistent-homology topology similarity, HMM behavior similarity, and an extended perspective model. The printed code has stub loaders/empty feature assembly, omits training, uses an initialized-but-untrained embedding network, and relabels distances from the same embedding as topology/behavior scores. Pairwise examples from a very small garden set require **garden/entity-level split before pair generation**. The perspective validator clamps R² to `[0.75,0.95]` and returns fixed CV metrics `MSE=30.0, MAE=4.5, R²=0.78`, exactly matching Table 19; these are not accepted as computed generalization evidence. Prose and Table 17 also swap Pearson/Spearman p-value labels.

## Core gates added/strengthened
- complex algorithm name -> executable primitive coverage;
- random placeholder contamination must be excluded from real result chains;
- fixed/hard-coded outputs cannot replace computation;
- validation metrics may not be clipped or returned as constants;
- pair/triplet data must be split by the underlying independent entity before construction;
- every claimed modality must have actual source and method primitives;
- self-similarity diagonal/identity structure is not external validation.

## 2025-F method competition status
2025-F is **3/4 reviewed**:
- S042: R2
- S043: R1
- S044: R2
- S045: unread Train

The Same-Problem Method Competition Map remains provisional. Current direction favors transparent geometry/visibility/change objectives for Q1, deterministic auditable descriptors and independently validated weighting for Q2, and compact deterministic representations or pretrained modality encoders with entity-level holdout for Q3. Final Method Map, Mini Transfer Test, Capability Evidence Gate and controlled `No-Core / Previous-Core / New-Core` ablation remain **NOT_DUE until S045 is completed**.

## Next stage
S030/S031 remain unread Dev reserve; S037/S038 and all Test papers remain frozen. Next unread Train: **S045 / 2025-F**.
