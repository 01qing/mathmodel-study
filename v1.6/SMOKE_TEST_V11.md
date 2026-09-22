# v1.1 Static Code Audit Smoke Test

A deliberately faulty Python file was scanned.

Expected rules:
- absolute-user-path
- accuracy-only-risk
- fit-transform-test
- metric-y-pred-first
- pca-fit-test
- preprocess-before-split
- shuffle-false

Detected:
- absolute-user-path
- accuracy-only-risk
- fit-transform-test
- metric-y-pred-first
- pca-fit-test
- preprocess-before-split
- shuffle-false

Result: **PASS**

The clean pipeline produced 0 findings.
