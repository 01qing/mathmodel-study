# v1.31 historical specialist-test adaptation

- Original v1.30 specialist test snapshot SHA256: `9e6f691dfda0063f29bcaf0efd453a9eed70e24002b1cdff70116e616dfd099f`
- Snapshot: `.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v131_s033/test_v130_s032_regressions.py`
- Reason: the original release-time assertion required `S033 reviewed_pages=[]`. S033 is now the intentionally reviewed next Train paper in v1.31, so that future-paper assertion is obsolete in a living work tree.
- Adaptation: only that one assertion is replaced by a reserve gate requiring `S034/S035/S036` to remain unread. All S032 semantic checks, Dev/Test gates, source audit, arithmetic checks and the exact 75-check count remain unchanged.
- Policy: this is a test-harness evolution, not a rewrite of v1.30 release history. The original test is preserved byte-for-byte in the snapshot.
