# Historical regression harness adaptation after S029 Dev exposure

The first rerun of old v1.25-v1.28 tests failed because those historical scripts encoded the then-true assertion `S029 reviewed_pages=[]` and exact current-version state. In v1.29 S029 was intentionally opened only after a frozen problem-only Dev baseline, so that old assertion is no longer the correct invariant.

The original pre-adaptation scripts are preserved under `scripts/history_snapshots_pre_v129_dev_exposure/`. The adapted tests keep the substantive invariants: S029 remains `split=dev` and excluded from ordinary retrieval; S030/S031 remain unread Dev reserve; all Test papers remain unread; v1.25-v1.28 Train assets remain present. Exact current-version assertions are replaced by version-at-least + historical-asset preservation checks. No Dev/Test retrieval gate is weakened.
