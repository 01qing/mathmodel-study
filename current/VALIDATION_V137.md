# MathModel-Core v1.37 Validation

## Overall status
**PASS for the v1.37 pre-release validation contract, with evidence scope explicitly bounded.** Final ZIP/SHA256 integrity is recorded in the release manifest after packaging.

## S044 specialist regression
- `test_v137_s044_regressions.py`: **82/82 PASS**.
- First run was preserved as **FAIL** on a literal harness wording mismatch (`fixed score` vs the stronger stored wording that fixed score dictionaries `inject` the ranking). The assertion alone was repaired to require the semantic evidence; no S044 finding or boundary was weakened.

## S044 source / Result Registry replay
- source SHA256 matches frozen registry: `d8e40c2d4765e4c50350715f3e5f739e2a2ce11974664c506a639e921e7ad840`.
- original-PDF visual audit: **116/116 pages**.
- printed-code static audit: **pp86-116**.
- Q2 Table 13: all ten displayed totals exactly equal element + openness components.
- Q2 Table 15: criterion is strictly `Kappa > 0.833`, reported Kappa is `0.833`; strict pass = **false**.
- Q3 prose p-values: Pearson `0.012`, Spearman `0.018`; Table 17 pairs them as Pearson `0.018`, Spearman `0.012`; label swap preserved in registry.
- Q3 Table 19 CV metrics `30.0 / 4.5 / 0.78` exactly equal constants returned by printed code; printed R² is additionally clamped to `[0.75,0.95]`.
- Replay status: `PASS_AUDIT_REPLAY_WITH_IDENTIFIED_FAILURES`; PASS means the contradictions/constants are reproducibly detected, not that author results are valid.

## Library / workspace / retrieval protection
- `validate_library.py`: **PASS** — 45 papers, 6752 chunks, **32 Train / 7 Dev / 6 Test**; frozen split and reviewed-page checks pass.
- `validate_learning_workspace.py`: **PASS** when invoked from the Skill root. An initial invocation from the wrong CWD produced false missing-root paths and is preserved as invocation-context evidence; the validator itself was not weakened.
- `test_v137_2025F_retrieval.py`: **PASS** — S044 is retrieved and evaluation/production candidates are reviewed-Train-only.
- S045 remains unread Train; S030/S031 remain unread Dev reserve; all Test papers remain frozen.

## Historical compatibility
Canonical historical Core regression set (`v1.6`, `v1.8` code-learning, `v1.9` training, `v1.10-v1.28`): **22/22 PASS**. A parallel wrapper exceeded its outer execution window after 21 tests had written PASS statuses; the missing v1.6 regression was rerun separately and passed. Timeout is not counted as PASS or FAIL.

Recent inherited specialist checks:
- v1.29 Dev: **67/67 PASS**
- v1.30 S032: **75/75 PASS**
- v1.31 S033: **119/119 PASS**
- v1.32 S034: **163/163 PASS**
- v1.33 S035: **31/31 PASS**
- v1.34 S036: **45/45 PASS**
- v1.35 S042: **56/56 PASS** after timepoint-only adaptation
- v1.36 S043: **72/72 PASS** after timepoint-only adaptation
- v1.37 S044: **82/82 PASS**

The original active v1.35/v1.36 tests were snapshotted before v1.37 adaptation. First failures (`version compatible`, `version`, then old exact `due only after S045` wording) and one transient adaptation SyntaxError are documented. Only stale version/latest/unread-next-paper wording was widened; S042/S043 substantive assertions, reproduction semantics, Dev reserve and Test protection were not relaxed.

## Evidence-scope boundary
This PASS means archive/library/retrieval/source/formula/result-registry contracts and regressions pass. It does **not** mean:
- S044 printed code was executed on original data;
- the advertised IGA/MKL/contrastive/PH/HMM/NeRF/STGCN methods were faithfully implemented by the appendix;
- the paper's aesthetic claims are externally validated;
- MathModel-Core v1.37 is causally better than v1.36 on unseen tasks.

S044 remains **R2**. 2025-F group-level Mini Transfer/Capability Evidence/controlled Core ablation are not due until S045 closes the Train group.
