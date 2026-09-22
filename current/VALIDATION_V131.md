# MathModel-Core v1.31 Validation

## Overall status

**PASS for S033 Train integration, with explicit R2 and capability-evidence boundaries.**

## Source and split protection

- S033 SHA256: `bc6529349c3a053b7774731f2fa3e383f6337807fd33954ee7726b04949878fd`
- S033 pages: **78**
- original-PDF visual audit: **78/78 pages**
- printed appendix audit: **pages 52-78**
- S033 split: Train
- S034-S036: Train reserve, `reviewed_pages=[]`
- S030/S031: Dev reserve, `reviewed_pages=[]`
- all Test papers: `reviewed_pages=[]`
- frozen split SHA256: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

## S033 specialist regression

`test_v131_s033_regressions.py`: **119/119 PASS**.

The final suite verifies S033 source identity, all-page review/R2 ceiling, Candidate Model Competition, Result Registry and code-audit findings, generic error-pattern gates, S032-S033 provisional cross-paper state, retriever summary, replay arithmetic, split protection and unread Dev/Test/future-Train reserves.

Two initial dry runs failed only because the test asserted phrases that did not exactly match the persisted SKILL headings. Those harness-string mismatches were recorded in `specialist_first_run_failure.txt`; the rules themselves were already present. The assertions were aligned to the exact persisted wording rather than weakening the rule content.

## Inherited specialist regressions

- inherited v1.30 S032 specialist suite: **75/75 PASS**
- inherited v1.29 Dev-boundary suite: **67/67 PASS**

For v1.30, the original release-time test requiring S033 to be unread is preserved byte-for-byte in `history_snapshots_pre_v131_s033/`; the live historical compatibility test only advances the future-reserve gate to S034-S036.

## Historical compatibility

The 22 historical Core regression scripts from v1.6, v1.8 code-learning, v1.9 training, and v1.10-v1.28 were rerun: **22/22 PASS**.

One first-batch historical run stopped at the v1.26 test because `next_learning.md` lacked the literal string `Mini Transfer Test`, although the same protocol was present in abbreviated wording. The context text was made explicit and the full 22-script suite was then rerun from the beginning and passed. No timeout or interrupted run is counted as a PASS by itself.

## Library integrity

`validate_library.py`: **PASS**.

- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- case-group isolation: PASS
- frozen split hash: PASS
- chunk/page round-trip: PASS
- review-page bounds: PASS
- ordinary retrieval smoke: reviewed-Train-only PASS
- quality evaluation: **NOT_RUN** because no gold unseen-task labels are part of this integration validation

`validate_learning_workspace.py`: **PASS**.

## Retrieval regressions

The new S033 query `Canny GMM 神经网络 二阶导数 信息熵 补充钻孔` was tested in both ordinary modes. S033 is the top match in both `evaluation` and `production`; every returned page is a reviewed Train page and Dev/Test are excluded. The returned 2025-C map status is `PROVISIONAL_2_OF_5_TRAIN_PAPERS`, and S033 carries its R2 Core summary.

Representative existing retrieval checks for 2024-A, 2024-B, 2024-C, 2024-E, 2025-A and the 2025-E supplemental code-link path also passed. A monolithic retrieval batch timed out after the first four successful checks; the remaining checks were run individually. The timeout itself is not treated as success or failure.

## Result Registry replay

`replay_s033_registry.py`: **11/11 PASS** for audit/replay scope.

Notable replays include:

- Q2 nine-row GD/Newton mean = **0.5864111111**;
- Q2 nine-row neural/Adam mean = **0.7969777778**;
- Q4 reported spacing 412.3105 mm is below the stated 500 mm hard minimum;
- with `p=0.5`, the paper-style term `-p log2 p` gives 0.5 while Bernoulli Shannon entropy is 1 bit;
- Q4 body depth intervals beginning at 2000 mm cannot be produced by the visible `depth_max<=500 mm` loader;
- Q2 displayed period is constant at 94.25 mm and must be registered as fixed-vs-estimated semantics.

These checks detect contracts; they do not reproduce the author's complete algorithms.

## Reproduction and capability boundary

S033 remains **R2**: full text + full original-PDF visual audit + printed-code static audit. R3-R7 are not claimed because the printed chain omits headline Q1/Q2/Q3 primitives, Q4 relies on fixed/simulated upstream data and incomplete state/entrypoint logic, and no original-data executable run was performed.

The Capability Evidence Gate remains active: v1.31 regression/retrieval/replay PASS does **not** prove that v1.31 solves unseen 2025-C problems better than v1.30 or No-Core. That comparison is intentionally deferred until S032-S036 close and the case-group Mini Transfer / controlled ablation is run.

## Release decision

**PASS. v1.31 may be sealed.** Next paper after sealing: **S034 / 2025-C / Train**.
