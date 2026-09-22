# v0.9 Smoke Test

## Result

- Benchmark script: PASS
- Contract validator: PASS
- Q2 candidates: 4
- Q2 recommended: `enet+elasticnet`
- Q2 practical tie: `True`
- Q3 labels with recommendation: 5/5
- Test used in benchmark: `False`

## Synthetic recommendations

Q2:
- `enet+elasticnet`
- Top pipelines are a practical tie on outer-fold RMSE; recommend enet+elasticnet because it has lower declared complexity/risk.

Q3:
- Caco-2: `all+rf` — Recommend all+rf by the declared rule: balanced accuracy, then MCC, PR-AUC and variability.
- CYP3A4: `all+logistic` — Top pipelines are a practical tie on balanced accuracy; recommend all+logistic because it has lower declared complexity/risk.
- hERG: `all+logistic` — Top pipelines are a practical tie on balanced accuracy; recommend all+logistic because it has lower declared complexity/risk.
- HOB: `all+rf` — Recommend all+rf by the declared rule: balanced accuracy, then MCC, PR-AUC and variability.
- MN: `all+rf` — Recommend all+rf by the declared rule: balanced accuracy, then MCC, PR-AUC and variability.

## Scope

This is a synthetic logic test, not a result for the real 2021 D dataset.
Its purpose is to verify:
- nested-CV execution,
- model comparison,
- tie handling,
- decision explanations,
- test isolation.
