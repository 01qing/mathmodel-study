# MathModel-Core v1.32 Validation

## Overall status

**PASS for S034 Train integration, with explicit R1 and capability-evidence boundaries.**

## Source and split protection

- S034 SHA256: `23dfbdeb5af6468a92428c0171ccfd569b6571066837df96b1960f47248b1d1f`
- S034 pages: **68**
- original-PDF visual audit: **68/68 pages**
- formula/pseudocode/result-surface audit: complete
- referenced code artifact: **Attachment 9 is named by the paper but not present in the available excellent-paper collection**
- S034 split: Train
- S035-S036: Train reserve, `reviewed_pages=[]`
- S030/S031: Dev reserve, `reviewed_pages=[]`
- all Test papers: `reviewed_pages=[]`
- frozen split SHA256: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

## S034 specialist regression

`test_v132_s034_regressions.py`: **163/163 PASS**.

The suite verifies S034 source identity, 68-page review, R1 ceiling, Candidate Model Competition, Result Registry, referenced-code access boundary, reusable error patterns, transferable modules, S032-S034 provisional Same-Problem Map, seven-gate Method Composer state, figure decision assets, arithmetic replay, reviewed-Train retrieval metadata and unread future/Dev/Test protection.

## Inherited specialist regressions

- v1.29 Dev-boundary suite: **67/67 PASS**
- v1.30 S032 suite: **75/75 PASS**
- v1.31 S033 suite: **119/119 PASS**

Pre-v1.32 copies of the v1.30 and v1.31 release-time specialist tests are preserved before advancing their future-paper assertions. Only obsolete time-point assumptions were changed: S034 may now be reviewed because it is the legitimate next Train paper; S035/S036 must remain unread. No Dev/Test boundary was relaxed.

## Historical compatibility

The 22 historical Core regression scripts from v1.6, v1.8 code-learning, v1.9 training and v1.10-v1.28 were rerun with per-script exit-code enforcement: **22/22 PASS**.

A first historical batch had exposed a wording-only v1.26 compatibility issue because `next_learning.md` used a shorthand instead of the literal `Mini Transfer Test`. The protocol was not changed; the context was made explicit and the unweakened historical suite passed. A prior shell marker that could print `ALL_22_PASS` without strict pipeline exit handling is explicitly superseded by the later per-script exit-code rerun.

## Library integrity

`validate_library.py`: **PASS**.

- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- group isolation: PASS
- frozen split hash: PASS
- chunk/page round-trip: PASS
- review-page bounds: PASS
- train-only retrieval smoke: PASS
- quality evaluation: **NOT_RUN**, because this integration validation does not contain unseen-problem gold labels

`validate_learning_workspace.py`: **PASS** when run from the Skill root, which is the script's declared cwd contract. A manual invocation that passed the root as an unused positional argument while running from another cwd was preserved as an invocation failure; it is not treated as a content/regression failure.

## Retrieval regression

`test_v132_2025C_retrieval.py`: **PASS**.

The S034-specific query returns S034 as the top result in both ordinary `evaluation` and `production` modes. Every returned page belongs to a reviewed Train paper; S029-S031 Dev and all Test papers are excluded. The 2025-C case-group status is `PROVISIONAL_3_OF_5_TRAIN_PAPERS`, and S034 is exposed with reproduction level R1.

## Result Registry replay

`S034_result_registry_replay.json`: **PASS** for **15 boolean arithmetic/contract checks plus 1 non-boolean diagnostic**.

Notable replays include:

- Q1 macro Precision ≈ **0.8955116**;
- Q1 macro Recall ≈ **0.9220119**;
- Q1 macro F1 ≈ **0.9085682**;
- `32/50 = 64%` exactly, which conflicts with the separate body statement of about 85% unconnected;
- `0.523 -> 0.395` equals **24.474%**, consistent with the reported 24.5% rounding;
- proposed new-new borehole minimum spacing = **800 mm**;
- nearest existing-new spacing diagnostic = **424.264 mm**, below the 500 mm textual rule if that rule applies to all holes.

These checks validate arithmetic and registered method contracts. They do **not** reproduce the author's algorithms or validate the underlying predicted masks/connectivity/information fields.

## Reproduction boundary

S034 remains **R1**. Full text and full original-PDF visual review are complete, and formula/pseudocode/result surfaces were audited. R2 is not claimed because the paper's Appendix A only references `Attachment 9: code for each question`, while the available source package does not contain that code artifact. R3-R7 are therefore also not claimed.

## Capability Evidence Gate

v1.32 regression/retrieval/registry PASS does **not** prove that v1.32 solves unseen 2025-C problems better than v1.31 or No-Core. That capability comparison remains intentionally deferred until S032-S036 are all complete. At group close, run the Mini Transfer Test and, where feasible, a fixed-budget `No-Core / Previous-Core / New-Core` controlled ablation.

## Release decision

**PASS. v1.32 may be sealed.** Next paper after sealing: **S035 / 2025-C / Train**.

## Release-contract validation

`validate_v132_release.py`: **50/50 PASS** on the final work tree. It checks v1.32 identity, required S034 assets, R1 evidence ceiling, frozen split hash, S035/S036 unread state, S030/S031 Dev reserve, all Test unread, strict historical 22/22 evidence, current specialist/retrieval/library/workspace logs, Result Registry replay, next-learning pointer and the provisional 3/5 2025-C Method Map.

The validator's first dry run failed because the validator expected a JSON key named `pending` while the persisted cross-paper map correctly uses `papers_pending`. That validator-schema bug was fixed without changing the Method Map or any training rule; the first failure is preserved as `validate_v132_release_first_failure.log`.
