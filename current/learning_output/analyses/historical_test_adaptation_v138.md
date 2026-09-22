# Historical test adaptation for v1.38

The original v1.37 S044 specialist test was snapshotted byte-for-byte before S045 became legally reviewed. Its semantic S044 audit assertions are preserved. Only version-timepoint assertions were relaxed to accept the legal v1.38 state: S045 may now be fully reviewed, the 2025-F map may be final, and the next-learning pointer may advance to post-Train Dev validation. Dev/Test isolation assertions were not weakened.

Additional v1.38 timepoint adaptations:

- `test_v132_s034_regressions.py`: the old literal next-stage sentence `S030/S031 remain Dev reserve` was replaced by a semantic boundary check that both `S030/S031` and `Dev` remain present. Their actual paper metadata assertions still require both papers to be Dev and unread; all Test papers remain frozen.
- `test_v135_s042_regressions.py`: allowed the legal v1.38/S045 final state, including S045 reviewed and the 2025-F final map. S042 paper/code/result assertions and Dev/Test isolation were unchanged.
- `test_v136_s043_regressions.py`: allowed the same legal S045/final-map progression and `S045:R2` as the latest state. S043 R1/source-access/result-registry assertions and Dev/Test isolation were unchanged.
- Byte-for-byte snapshots plus SHA256 files for all three pre-adaptation scripts are stored under `history_snapshots_pre_v138_s045/`.

These changes widen only **version-timepoint lifecycle assertions**. They do not reinterpret a substantive historical failure as a pass.

