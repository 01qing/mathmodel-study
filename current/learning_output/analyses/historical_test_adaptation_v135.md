# v1.35 historical specialist-test adaptation

## Why this was needed

The first inherited-recent compatibility run in v1.35 exposed **release-time assertions**, not knowledge loss:

1. `test_v130_s032_regressions.py` failed because it still required later legitimate 2025-C Train papers S035/S036 to remain unread.
2. After that time-point gate was adapted, `test_v132_s034_regressions.py` failed because it required the root `VERSION` to remain exactly `1.32.0`.

Both failures were reproduced from the preserved pre-v1.35 snapshots at the original script depth and saved under `learning_output/analyses/v135_S042/historical_snapshot_expected_failures/`.

## Adaptation rule

Original active tests were preserved byte-for-byte in:

`.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v135_s042/`

Only these time-dependent assertions were changed:

- exact old version number -> minimum historical version;
- future Train paper must be unread -> later authorized Train review is allowed;
- provisional 2025-C map/retriever state -> legal progression through final closure is allowed;
- old next-paper pointer -> legal progression beyond the historical paper is allowed;
- Mini Transfer `NOT_DUE` -> either historically not due or later valid completed lifecycle.

**Not relaxed:** S032-S036 semantic findings, arithmetic replays, source hashes, reproduction levels, error-pattern presence, frozen split hash, S030/S031 Dev reserve, or any Test-paper unread gate.

After adaptation, inherited recent suites passed:

- v1.29 Dev: 67/67
- v1.30 S032: 75/75
- v1.31 S033: 119/119
- v1.32 S034: 163/163
- v1.33 S035: 31/31
- v1.34 S036: 45/45

## Snapshot / active hashes

```json
{
  "test_v130_s032_regressions.py": {
    "snapshot_sha256": "70500af6926658f19dce868d8d1cc11ecca1e5c0db3574b30cdc7e8b7de5afdd",
    "active_post_patch_sha256": "97bbc50e2c5081387511375d976bbd88c5488fde07d607e2c2735dfa177ccc9a"
  },
  "test_v131_s033_regressions.py": {
    "snapshot_sha256": "726c534efd0e07afa363014b77ed26d3d1b226e275be055b41199005af6d08ee",
    "active_post_patch_sha256": "9bc37cd013d1a49f5a724f16d42ffbafdad2f76e1d81477264fff9fea0fd44d4"
  },
  "test_v132_s034_regressions.py": {
    "snapshot_sha256": "43c517a83b2537f3a3d2708922d1c1f9c2b0d62634dc9cb186627d5434072f13",
    "active_post_patch_sha256": "9ee4170f2c9603078bfbcfab3af8ac09234bd0088ab477cc4e483ba844660c85"
  },
  "test_v133_s035_regressions.py": {
    "snapshot_sha256": "bb68acb99ac1263360337d9ee69e778d52b8d842b5569d2d0ecd0e0dfb5fc96c",
    "active_post_patch_sha256": "1fb44a8f9e66c181b4802d572af45ae25383ed5845e3709b905d658c8662ef0a"
  },
  "test_v134_s036_regressions.py": {
    "snapshot_sha256": "497b570a8289422d12ee1f8e5215bc1a2e2e09e2879fa70e3ef5cf41cfaa52c3",
    "active_post_patch_sha256": "7c6bc0ba1c55b66dbaaed38f064df372760f9b35ba42e4288f68d086a0b79f07"
  }
}
```
