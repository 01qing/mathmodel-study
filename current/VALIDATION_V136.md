# MathModel-Core v1.36 Validation

## Overall status

**PASS for the v1.36 release contract, with evidence scope explicitly bounded.**

## S043 specialist regression
- `test_v136_s043_regressions.py`: **72/72 PASS**
- verifies S043 Train identity, 71 reviewed pages, R1 ceiling, required Core-schema assets, formula-range/result-registry contradictions, code-attachment absence, provisional 2025-F 2/4 map, frozen split, Dev/Test protection and next-learning pointer.

## Result Registry / source replay
- source SHA256: `692c9e30cd2ce0765b17bfbe3a5b1265e32c2ddae42b636a8ad261090e8b73c1`
- visual audit: **71/71** original-PDF pages
- p71: paper states attachment contains Q1-Q3 code, but the attachment is not available in the current source package; therefore **R1**.
- Q2 openness arithmetic: Jichang **0.8905** vs reported 5.730; Liuyuan **0.853** vs 5.376.
- Q3 Table 6.2: 45 off-diagonal pairs; mean **0.6642666667**, population SD **0.0678113068**, sample SD **0.0685775606**.
- cluster means from the same matrix: large **0.6606666667**, medium **0.7403333333**, small **0.6733333333**.
- identified inconsistencies remain registered audit findings and are not silently corrected author results.

## Library and retrieval integrity
- `validate_library.py`: **PASS**
- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- frozen split SHA256 unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`
- `validate_learning_workspace.py`: **PASS**
- evaluation retrieval: **PASS**, includes S043 and every returned page is reviewed Train evidence
- production retrieval: **PASS**, includes S043 and every returned page is reviewed Train evidence
- a combined two-mode retrieval command exceeded its execution window; it is not counted as failure. The two modes were then verified separately.

## Historical compatibility
Canonical historical Core regression set:
- v1.6
- v1.8 code-learning
- v1.9 training
- v1.10 through v1.28

Result: **22/22 PASS**. The first monolithic shell batch exceeded the outer execution window after early passing scripts; remaining tests were rerun in smaller bounded batches and all passed. Timeout is not interpreted as pass/fail.

Inherited recent specialist checks:
- v1.29 Dev: **67/67 PASS** (recorded in the first-run log before the wrapper window ended)
- v1.30 S032: **75/75 PASS**
- v1.31 S033: **119/119 PASS**
- v1.32 S034: **163/163 PASS**
- v1.33 S035: **31/31 PASS**
- v1.34 S036: **45/45 PASS**
- v1.35 S042: first **FAIL** on stale exact-version state, then **56/56 PASS** after time-point-only adaptation.

The original v1.35 test is preserved byte-for-byte under `history_snapshots_pre_v136_s043/`; adaptation evidence is `learning_output/analyses/historical_test_adaptation_v136.md`. No S042 semantic finding, split boundary, Dev reserve or Test gate was relaxed.

## Evidence-scope boundary
PASS means registered archive/library/retrieval/formula/result contracts and regressions pass. It does **not** mean:
- S043 attachment code was statically audited or executed;
- the paper's aesthetic/perceptual claims are externally validated;
- GA global optimality is established;
- MathModel-Core v1.36 is causally better than v1.35 on unseen tasks.

S043 remains **R1**. Controlled capability ablation is not due for 2025-F until S045 closes the Train case group.

## Dev/Test protection and next stage
- S030/S031: Dev reserve, unread
- S037/S038 and all Test papers: frozen
- S044/S045: unread Train reserve for 2025-F
- next unread Train: **S044 / 2025-F**
