# MathModel-Core v1.29 Release Reconstruction Note

This v1.29 release tree was recreated in the current Chat from the sealed v1.28 artifact plus the persisted `PROGRESS_V129.md`, `VALIDATION_V129.md`, and the frozen S029 Dev pre/post comparison files.

The reconstruction does **not** claim byte identity with any transient v1.29 work tree that may have existed previously. It does recreate and verify the persisted v1.29 contracts:

- S029 remains Dev-only and was opened only after a frozen problem-only baseline;
- S030/S031 remain unused Dev reserve;
- all Test papers remain unread;
- ordinary evaluation/production retrieval is restricted to reviewed Train pages;
- S039-S041 reviewed-page metadata is non-destructively backfilled from pre-existing reviewed status/assets;
- S029 specialist regression is recreated at 67/67 PASS;
- 22 historical Core regression scripts pass after documented harness adaptation for the intentional S029 Dev exposure;
- library integrity remains 45 papers / 6752 chunks / 32 Train / 7 Dev / 6 Test.

Historical v1.25-v1.28 tests originally encoded `S029 reviewed_pages=[]`. Their first failure after legitimate Dev exposure is preserved in the adaptation record; the pre-adaptation scripts are preserved under `history_snapshots_pre_v129_dev_exposure/`. The adaptation changes the obsolete state assertion, not the retrieval boundary.
