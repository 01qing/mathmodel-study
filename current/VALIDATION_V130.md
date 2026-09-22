# MathModel-Core v1.30 Validation

## Overall status

**PASS for S032 Train integration, with R2 evidence boundary.**

## Source and split protection

- S032 canonical source SHA256: `6f14d27f0371e94857a592c7469eeec37172009384bdba8a847c26019e8d96c8`
- S032 pages: 71
- Full original-PDF visual audit: 71/71 pages
- S032 split: Train
- S033-S036 remain unreviewed
- S030/S031 remain unused Dev reserve
- Test papers remain `reviewed_pages=[]`
- frozen split SHA256 remains `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

## Specialist regressions

- inherited v1.29 Dev-boundary regression: **67/67 PASS**
- S032 / v1.30 specialist regression: **75/75 PASS**

The S032 specialist suite verifies paper assets, Candidate Model Competition, Result Registry entries, printed-code contract findings, generic rule files, source hash, Dev/Test protection, adopted capability prompt, and Q1 metric replay.

## Historical compatibility

Historical Core regression scripts were rerun on the v1.30 tree.

- unique scripts expected: 22
- unique scripts passed: **22/22**
- failures: 0
- scope: compatibility/regression only, **not new-problem capability proof**

The first monolithic run was interrupted while entering later tests; the remaining scripts were rerun in bounded chunks. The persisted summary confirms all 22 unique historical scripts passed. No interrupted run is counted as a PASS by itself.

## Library integrity

`validate_library.py`: **PASS**

- papers: 45
- chunks verified: 6752
- split: 32 Train / 7 Dev / 6 Test
- group isolation: PASS
- frozen split hash: PASS
- chunk/page round-trip: PASS
- review-page bounds: PASS
- ordinary retrieval smoke: reviewed-Train-only PASS

## S032 retrieval

`test_v130_2025C_retrieval.py`: **PASS**

For both ordinary `evaluation` and `production` modes, query `围岩裂隙 JRC 正弦拟合 三维重构` returns S032 as the top match while all returned pages remain reviewed Train pages. Dev/Test solutions are excluded.

## Result Registry replay

`replay_s032_registry.py`: completed.

For a single pooled confusion matrix, the F1 values implied by reported IoU are approximately:

- morphology: 76.2376% vs reported 76.6% (difference +0.3624 percentage point)
- U-Net: 79.0810% vs reported 80.4% (difference +1.3190 pp)
- improved U-Net: 84.4598% vs reported 84.8% (difference +0.3402 pp)

These are recorded as **aggregation provenance required**, not automatic author errors, because the paper does not specify whether the table uses pooled, macro or per-image averaging.

## Reproduction / capability boundary

S032 remains **R2**: full text + full original-PDF visual review + printed-code static audit. No complete source/data execution was performed, and several algorithm-defining primitives are omitted or conflict with the prose. Therefore R3-R7 are not claimed.

v1.30 also obeys the Capability Evidence Gate: specialist/historical/retrieval PASS proves persistence and contract compatibility, **not** that Core has already improved on unseen 2025-C tasks. The case-group Mini Transfer and `No-Core / Previous-Core / New-Core` controlled ablation are intentionally deferred until S032-S036 are complete.

## Release decision

**PASS. v1.30 may be sealed.** Next paper: S033 / 2025-C Train.
