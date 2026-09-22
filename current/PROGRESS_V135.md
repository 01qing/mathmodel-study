# MathModel-Core v1.35 Progress

## Version role
v1.35 is the first 2025-F Train increment after 2025-C closed in v1.34. MathModel-Core remains one shared Core; no role Skill split is created.

## S042 / 2025-F / Train
- title: 《江南古典园林的美学特征建模》
- pages: 182
- full-text review: complete
- original-PDF visual audit: 182/182 pages
- printed Python appendix: pp103-182, 12 named source listings statically audited
- reproduction level: **R2**
- R3+ is not claimed because the original author project/original attachment execution chain was not run end-to-end.

### Main audited findings
- Q1: prose/code treat low transition probability as higher surprise, while Eq.(4) adds raw probability positively; printed code uses `-log(prob)`. A hard route-node bound `<=100` conflicts with reported paths up to 222 because the decoded/repaired path is not revalidated after bridge completion.
- Q1 Pareto evidence: HV `0.4884`, later `>=90% coverage`, and GD-to-theoretical-front claims require explicit reference point/front, normalization and objective-direction provenance.
- Q2: interpretable ecology/morphology/space-syntax scoring is useful, but forcing Jichang Garden indicators to 100 and then using its top rank as validation is anchor-target circular calibration. Reported correlations near `0.99` trigger redundancy/double-counting review.
- Q3: 179D representation with only 10/11 independent gardens is exploratory. All-pair high similarity triggers a similarity-concentration gate; KMeans followed by ANOVA on the same feature space is post-selection/double-dipping, not independent cluster validation. Broad-exception default feature vectors create silent-failure provenance risk.

## New reusable Core gates
- final decoded/repaired objects must replay all hard constraints;
- Pareto HV/GD metrics require reference contracts;
- calibration anchors and validation targets must be separated;
- same-feature clustering + same-feature significance testing is descriptive only;
- all-high similarity is not proof of generalization/discrimination;
- algorithm exceptions must propagate explicit missingness/failure state instead of plausible silent default vectors.

## Validation status
- S042 specialist regression: **56/56 PASS**
- library validation: **PASS**, 45 papers / 6752 chunks / 32 Train / 7 Dev / 6 Test
- workspace validation: **PASS**
- evaluation + production retrieval: **PASS**, reviewed-Train-only and S042 retrieved as top match
- historical Core regression set: **22/22 PASS**
- inherited recent suites after time-point-only harness adaptation: v1.29 67/67, v1.30 75/75, v1.31 119/119, v1.32 163/163, v1.33 31/31, v1.34 45/45
- first stale-harness failures and original test snapshots are preserved; no Dev/Test gate was relaxed.

## 2025-F status
S042 reviewed; S043-S045 remain unread Train. Same-Problem Method Competition Map is provisional. Mini Transfer Test / Capability Evidence Gate / controlled Core ablation are due only after S045.

## Boundary and next stage
S030/S031 remain Dev reserve; S037/S038 and all Test papers remain frozen. Next unread Train: **S043 / 2025-F**.
