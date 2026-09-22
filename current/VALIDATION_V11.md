# v1.1 Validation

## Real-code audit asset

- Audited public repository: `Bureaux-Tao/modeling2021-D`
- Audited source files: 7
- Findings: 18
- Critical: 2
- High: 11
- Medium: 3
- Low: 2
- Strength findings: 2
- Unresolved evidence gaps: 1
- External-code audit validator: PASS

## Generic static scanner

- Scanner execution: PASS
- Expected risk rules detected: PASS
- Detected rules: absolute-user-path, accuracy-only-risk, fit-transform-test, metric-y-pred-first, pca-fit-test, preprocess-before-split, shuffle-false
- Clean-file findings: 0

## Package

- Python scripts: 22
- Python syntax errors: 0
- JSON parse errors: 0
- Real participant code numerical reproduction: NOT_RUN
- Real 2021 D dataset benchmark: NOT_RUN

## Interpretation

v1.1 is the first version tested against **real public participant code**, not only synthetic modeling data.
The code-text findings are source-verified; numerical outputs remain unverified until the public CSV/XLSX data can be materialized and executed.
