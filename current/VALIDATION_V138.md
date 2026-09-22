# MathModel-Core v1.38 Validation

## Overall status

**PASS for the v1.38 pre-release validation contract, with evidence scope explicitly bounded.** Final ZIP/SHA256 integrity is recorded in the external release manifest after packaging.

## S045 specialist regression and source audit

- `test_v138_s045_regressions.py`: **127/127 PASS** after final 2025-F closure fields were written.
- source SHA256 matches frozen inventory: `0cd7b0001352da9a88dc4d70df750389eb7989d5d2520959e1222a3f05ba2e76`.
- original-PDF visual audit: **94/94 pages**.
- printed-code static audit: **pp62-94**.
- reproduction level: **R2**; R3-R7 are not claimed.

## Result Registry / formula replay

`replay_s045_registry.py`: **PASS** for the registered arithmetic/static-contract scope.

- Table 6.6: **10/10** displayed scores replay under decimal `ROUND_HALF_UP`.
- The first replay attempt using ordinary Python float rounding failed on half-tie rows such as `75.85` and `36.65`; this was diagnosed as a replay-harness rounding-contract issue, not author arithmetic failure, and the first failure is preserved.
- Eq.(5.67) displayed formula does **not** contain the verbally claimed route-length term.
- Q2 sensitivity axis is explicitly preserved as a semantic **FAIL**: scenario-indexed scores were ranked as if garden-indexed.
- Q3 pair-specific changes `-0.791 -> 0.209` and `-0.857 -> 0.143` are preserved as provenance failures.
- Original PDF p59 visually resolves Eq.(7.13) with absolute-value bars that text extraction lost.

Registry status `PASS_AUDIT_REPLAY_WITH_IDENTIFIED_FAILURES` means the contradictions are reproducibly detected; it does not validate the author's end-to-end model.

## 2025-F final group closure

- S042-S045: **4/4 reviewed**.
- Final Same-Problem Method Competition Map: `FINAL_FOUR_OF_FOUR_TRAIN_PAPERS_REVIEWED`.
- Method Composer: all seven compatibility gates present.
- Final Figure Decision Rules: `FINAL_AFTER_S042_S045`.
- Mini Transfer: first `FAIL` on invalid `A -> D` crossover edge -> diagnosis -> path-preserving splice/final edge replay -> **`PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX`**.
- Capability Evidence Gate: clean blind Core gain **NOT_ESTABLISHED**; controlled `No-Core / Previous-Core / New-Core` **NOT_RUN**. No algorithm proxy was substituted for a Core configuration.

## Library / workspace / retrieval protection

- `validate_library.py`: **PASS** — 45 papers, 6752 chunks, **32 Train / 7 Dev / 6 Test**.
- all **32 Train papers are reviewed**.
- S029 remains Dev-only evidence from the prior leakage-safe Dev cycle.
- S013-S016 and S030-S031 remain unread Dev papers/reserve.
- all Test papers S021-S024 and S037-S038 remain unread/frozen.
- `validate_learning_workspace.py`: **PASS** from the Skill root. A prior wrong-CWD failure is preserved as invocation-context evidence and was not treated as a model failure.
- `test_v138_2025F_retrieval.py`: **PASS** — S045 is retrieved and ordinary evaluation/production candidate pools remain reviewed-Train-only with the final 2025-F map attached.

## Historical compatibility

Canonical historical Core regression set (`v1.6`, `v1.8` code-learning, `v1.9` training, `v1.10-v1.28`): **22/22 PASS**.

The first v1.8 run under the parallel historical wrapper used the wrong working directory and failed to locate the existing GTeacher code cards. That first failure is preserved. Rerunning the unchanged v1.8 test from the Skill root passed **10/10**; timeout/wrong-CWD was not silently counted as PASS.

Recent inherited specialist checks after v1.38 legal-timepoint adaptations:

- v1.29 Dev: **67/67 PASS**
- v1.30 S032: **75/75 PASS**
- v1.31 S033: **119/119 PASS**
- v1.32 S034: **163/163 PASS**
- v1.33 S035: **31/31 PASS**
- v1.34 S036: **45/45 PASS**
- v1.35 S042: **56/56 PASS**
- v1.36 S043: **72/72 PASS**
- v1.37 S044: **82/82 PASS**
- v1.38 S045: **127/127 PASS**

For v1.32/v1.35/v1.36, byte-for-byte snapshots and SHA256 values were saved before widening only stale version/latest/unread-next-paper wording to accept the legal v1.38 closure state. Their substantive paper/code/result assertions, Dev boundaries and Test protection were not relaxed. The adaptation record is `learning_output/analyses/historical_test_adaptation_v138.md`.

## Evidence-scope boundary

This PASS means the registered source/formula/code-static-audit/result-registry/library/retrieval/split/regression contracts pass. It does **not** mean:

- S045 author code was executed end-to-end on original data;
- the advertised GA or GMM-MRF pipeline was faithfully implemented by the appendix;
- the aesthetic similarity/illusion scores are externally validated;
- the post-learning Mini Transfer establishes R7;
- MathModel-Core v1.38 is causally better than v1.37 or No-Core on a clean unseen benchmark.

The next stronger evidence is a frozen **clean Dev** cycle on unread 2024-D problem/data before opening S013-S016 solution artifacts.
