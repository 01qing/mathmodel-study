# Historical test adaptation for v1.32 / S034

- Original v1.31 specialist test snapshot preserved at `history_snapshots_pre_v132_s034/test_v131_s033_regressions.py`.
- Snapshot SHA256: `b39b1f098f9fca271d032a75bc57a39dfc7710326b12729c5254950577511dc2`.
- Active compatibility test was changed only at time-point assertions: S034 is now legitimately reviewed Train evidence, while S035/S036 remain unread.
- No Dev/Test gate was relaxed; S030/S031 and all Test papers remain unread.
- The adaptation prevents a historical assertion ("S034 must still be unread") from blocking the legitimate next Train paper.
- Active test SHA256 after adaptation: `726c534efd0e07afa363014b77ed26d3d1b226e275be055b41199005af6d08ee`.

## v1.30/S032 compatibility test

- Pre-v1.32 active test snapshot preserved at `history_snapshots_pre_v132_s034/test_v130_s032_regressions.py`.
- Snapshot SHA256: `e75414ec7ac951117a6d3b0ecf5631128fa172ae2d17f92e5176702d11f8822d`.
- Only the future-reserve assertion was advanced: S034 may now be legitimately reviewed; S035/S036 must remain unread.
- Active SHA256: `70500af6926658f19dce868d8d1cc11ecca1e5c0db3574b30cdc7e8b7de5afdd`.

## v1.26 literal protocol-name compatibility during final v1.32 validation

The first full historical batch after S034 integration exposed a wording-only compatibility failure in
`test_v126_regressions.py`: `next_learning.md` used the shorthand `2025-C Mini Transfer` instead of
the historical literal `Mini Transfer Test`. The protocol was not removed or changed. The current
context was made explicit as `2025-C Mini Transfer Test`, and the original v1.26 test was kept
unweakened. The first failure is preserved in
`learning_output/analyses/v132_S034/historical_v126_first_failure.txt`.

A prior shell batch also printed a false terminal `ALL_22_PASS` marker because pipeline exit status was
not enforced. That marker is invalid and superseded by the per-script exit-code rerun recorded in
`historical_22_regressions_final.log`.
