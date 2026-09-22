# v1.36 inherited specialist-test adaptation

## First failure preserved

After S043 became an authorized reviewed Train paper, the inherited `test_v135_s042_regressions.py` first failed on its release-time assertion that the root state must still be exactly v1.35/S042. The first-fail log is preserved at `learning_output/validation/v136/recent_130_135_first_run.log`.

This is a **time-point harness failure**, not loss of the S042 semantic findings.

## Snapshot and adaptation

Before editing, the active v1.35 test was copied byte-for-byte to:

`.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v136_s043/test_v135_s042_regressions.py`

Snapshot SHA256: `e9c2ef995da196d469fccbe5fa7da5c209aa15ebace4b4449477a571100b2700`

Adapted active SHA256: `f7cfb776c029dd989ba4d335fb17ed0d5367bf6cda6db062ffb2cf5981a307ba`

Only release-time assertions were widened:

- exact v1.35/S042 root state -> legal v1.35 or v1.36 progression;
- S043 must remain unread -> S043 may be legally reviewed, while S044/S045 stay unread;
- 2025-F map must remain 1/4 -> legal 1/4 or 2/4 progression;
- next pointer S043 -> legal S043/S044 progression.

Not relaxed:

- S042 R2 evidence;
- S042 Result Registry findings;
- split SHA and Train/Dev/Test identity;
- S030/S031 Dev reserve;
- all Test unread gates;
- S044/S045 unread at the v1.36 release point.

After adaptation, the inherited v1.35 specialist suite passed **56/56**.
