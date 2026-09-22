# v1.0 End-to-End Smoke Test

## Pipeline

```text
synthetic data contract
→ benchmark
→ benchmark validator
→ final fit
→ final-fit validator
→ paper-comparison evidence bundle
→ comparison validator
→ simulated Agent Review
→ reviewed-comparison validator
→ knowledge extraction
```

## Results

- Leakage-safe benchmark: **PASS**
- Q2 recommended pipeline: `mi+elasticnet`
- Q3 labels with independent recommendation: **5/5**
- Official-test isolation flag in benchmark: `False`
- Final fit: **PASS**
- Final Q2 selected features: **10**
- Synthetic test rows predicted: **6**
- Q3 final classifiers completed: **5/5**
- Test used for final model selection: `False`
- Test used for final hyperparameter selection: `False`
- Paper comparison evidence bundle: **PASS**
- Pre-review knowledge extraction gate: **enforced**
- Reviewed comparison validation: **PASS**
- Knowledge extraction: **PASS**
- Synthetic knowledge cards written: **2**

## Scope

This test validates engineering behavior only.

It does **not** establish:
- real 2021 D data statistics,
- real 2021 D model rankings,
- real test predictions,
- reproduction of excellent-paper numerical claims,
- a fresh blind-eval score.

All of those remain `NOT_RUN`.
