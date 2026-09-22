# v1.34 historical compatibility adjustments

First historical rerun returned 19/22 PASS. The three failures were non-substantive timepoint/string contracts:

- v1.21/v1.22 expected `session_id.startswith("v1.")`; reconstructed v1.34 used `v1340-...`. Renamed current session to `v1.34-S036-MathModel-Core`.
- v1.26 expected the literal phrase `Mini Transfer Test`; current next-learning note said `Mini Transfer`. Restored the canonical phrase without changing the protocol.

No paper evidence, split, numerical result, model-selection rule, or Dev/Test boundary was weakened. The first 19/22 rerun remains preserved in `historical_regressions_first_run.log`.
