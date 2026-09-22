# v1.37 historical test adaptation record

## First failures preserved

During v1.37/S044 inherited regression, the active v1.35 and v1.36 tests failed only on version-timepoint assertions after S044 was legally reviewed as Train:

- v1.35: `AssertionError: version compatible`
- v1.36: `AssertionError: version`

The pre-adaptation test files are snapshotted byte-for-byte under `scripts/history_snapshots_pre_v137_s044/` with SHA256 files.

## Adaptation boundary

Only stale timepoint assertions were widened:
- current version/latest paper may advance legally to v1.37/S044;
- S044 is no longer required to be unread after its lawful Train review;
- 2025-F method-map status may advance from one/two reviewed papers to three;
- next-learning pointer may advance to S045.

Not changed:
- S042/S043 substantive source, formula, result and code-access assertions;
- S030/S031 Dev reserve boundary;
- any Test split/read protection;
- reproduction-level semantics;
- reviewed-Train retrieval boundary.

## Second v1.35 rerun failure

After the timepoint adaptation, v1.35 next failed on the exact legacy phrase `due only after S045`. The current `next_learning.md` states the same semantic contract as `NOT_DUE until S045 is completed`. This is another wording-only timepoint assertion. The active v1.35/v1.36 tests were therefore changed to require both `NOT_DUE` and `S045`, preserving the same scheduling gate.

To keep inherited check counts stable, each adapted test replaces the obsolete `S044 unread` check with `S044 legal progression` rather than simply deleting a check.

A transient SyntaxError occurred while preserving the inherited check count because a `for` statement was inserted after a semicolon. This was an adaptation-script syntax mistake, not a Core regression; it was fixed by placing the loop on its own line before rerunning.
