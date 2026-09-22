# MathModel-Core v1.35 Validation

## Overall status

**PASS for the v1.35 release contract, with evidence scope explicitly bounded.**

## S042 specialist regression

- `test_v135_s042_regressions.py`: **56/56 PASS**
- verifies S042 Train identity, 182 reviewed pages, R2 ceiling, required Core-schema assets, Result Registry contradictions, printed-code static-audit scope, provisional 2025-F map, frozen split hash, Dev/Test protection and next-learning pointer.

## Result Registry / source replay

- source SHA256: `b1132adba756118ab037d8af0af25cf5cd110e51092288042d5c5ae9b3b72a0c`
- visual audit: **182/182** original-PDF pages
- printed-code static audit: **pp103-182**, 12 named source listings
- arithmetic/contract replay: **PASS_AUDIT_REPLAY_WITH_IDENTIFIED_CONTRADICTIONS**
- verified arithmetic includes 10-garden pair count 45, 11-garden pair count 55, 179D class total, and the 88/179 = 49.16% share.
- identified contradictions/uncertainties remain findings, not silently corrected author results: path hard bound `<=100` vs reported 222; HV `0.4884` vs later `>=90%` coverage language; missing HV/GD reference contracts.

## Library and retrieval integrity

- `validate_library.py`: **PASS**
- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- frozen split SHA256 unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`
- `validate_learning_workspace.py`: **PASS** when run from the Skill root
- evaluation retrieval: **PASS**, S042 is top match and every returned page is reviewed Train evidence
- production retrieval: **PASS**, S042 is top match and every returned page is reviewed Train evidence

## Historical compatibility

The canonical historical Core regression set was rerun from the Skill root:

- v1.6
- v1.8 code-learning
- v1.9 training
- v1.10 through v1.28

Result: **22/22 PASS**.

The inherited recent specialist suites were also rerun. The first run exposed stale release-time assertions in old specialist tests, not knowledge loss. Original active tests were snapshotted byte-for-byte before adaptation. Only old exact-version / future-Train-unread / provisional-map / old-next-pointer assertions were changed to permit already-authorized Train progression. Semantic findings, arithmetic/source checks, reproduction levels, frozen split, S030/S031 Dev reserve and all Test unread gates were retained.

Final inherited recent results:

- v1.29 Dev: **67/67 PASS**
- v1.30 S032: **75/75 PASS**
- v1.31 S033: **119/119 PASS**
- v1.32 S034: **163/163 PASS**
- v1.33 S035: **31/31 PASS**
- v1.34 S036: **45/45 PASS**

Adaptation evidence: `learning_output/analyses/historical_test_adaptation_v135.md`; original snapshots: `.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v135_s042/`.

## Evidence-scope boundary

PASS here means archive/library/retrieval/contracts and registered arithmetic/semantic audit checks pass. It does **not** mean:

- S042 author code was executed end-to-end;
- the paper's perceptual/aesthetic claims are externally validated;
- MathModel-Core v1.35 is causally better than v1.34 on unseen problems.

S042 remains **R2**. Controlled `No-Core / Previous-Core / New-Core` capability ablation is not due for 2025-F until S045 closes the Train case group.

## Dev/Test protection and next stage

- S030/S031: Dev reserve, unread
- S037/S038: Test, frozen
- S043/S044/S045: unread Train reserve for 2025-F
- next unread Train: **S043 / 2025-F**
