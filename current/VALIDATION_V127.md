# MathModel-Core v1.27 Validation

## New specialist validation

- `test_v127_regressions.py`: **PASS 82/82**.
- `test_v127_2025A_retrieval.py`: **PASS**.
- S027 Result Registry validation: **PASS**.

## Historical compatibility

- Historical rule regressions through v1.25 were rerun and passed before the v1.26 instantaneous-state assertion was reached.
- v1.26 regression initially expected the Figure Rules to remain exactly at S025+S026; this was a historical instantaneous-state assertion, not a knowledge failure. It was changed to the true invariant: S025/S026 assets must remain present while later Train papers may legitimately extend the basis.
- After repair: v1.26 **PASS 68/68** and v1.27 **PASS 82/82**.
- Full old retrieval bulk replay is not claimed in this version because the environment hit batch execution time limits. The retrieval engine and chunk corpus are byte-identical to v1.26, while the new S027 retrieval regression passed.

## Retrieval/corpus invariants

- `search_cases.py` SHA256 unchanged from v1.26: `ac5838c8f2f1b04304935f1c7c3f85be763a043a978747ce0d3e68114886dfc9`.
- `chunks.json` SHA256 unchanged from v1.26: `ff4c3c4c631fe7b1f65159f0c7b7df653f07ba65e1066b9bee4b8ef9e942b72e`.
- `split_manifest.json` SHA256 unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`.
- `validate_library.py`: **PASS**, papers=45, chunks=6752, split=32/7/6, group isolation and frozen split hash PASS.

## Reproduction boundary

S027 remains **R2**, not R3. Printed appendix size does not imply executability: Q1 core priority/cache helpers, Q2 `main()`, and Q3 optimizer-core helper are absent from the visible appendix, and no original runnable project/input bundle has been executed.

## Mini Transfer Test

Not due at v1.27 because 2025-A Train case group is incomplete (S028 pending).
