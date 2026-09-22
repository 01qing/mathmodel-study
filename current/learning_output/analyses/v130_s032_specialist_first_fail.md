# v1.30 S032 specialist regression first run

- First run status: **FAIL (test harness count assertion only)**.
- Observed: all semantic `ck(...)` checks completed, but final hard-coded assertion expected 62 while the actual suite contained 63 checks.
- Diagnosis: bookkeeping/count drift in the newly generated specialist test; no S032 evidence assertion failed.
- Repair: preserve the pre-fix script and change only the terminal expected count from 62 to 63, with an explanatory comment.
- Requirement: rerun the full suite; this first failure remains part of the persistent evidence trail.
