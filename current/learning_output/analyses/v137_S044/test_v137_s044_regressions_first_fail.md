# v1.37 / S044 specialist regression — first FAIL

- Status: **FAIL (preserved)**
- Failed check: `Q2 fixed output`
- Original assertion searched for the literal phrase `fixed score`.
- The audited code-case stores the stronger wording: `final illusion/element/openness score dictionaries exactly inject the ranking values instead of returning the earlier computed score pipeline`.
- Diagnosis: **test-harness wording mismatch**, not a semantic evidence failure.
- Repair policy: change only the assertion wording to require both `score dictionaries` and `inject`; do not alter the underlying audit, Result Registry, Train/Dev/Test boundary, or recommendation rule.
