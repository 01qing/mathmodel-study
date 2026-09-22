# MathModel-Core v1.41 Validation

## Overall status

**PASS for the v1.41 SEALED release contract. Final archive integrity/SHA256 is recorded in the external release manifest and package validation.**

## 2024-D specialist closure

- `test_v141_2024D_group.py`: **38/38 PASS** after preserving the initial Mini-Transfer fixture failure and repair.
- S015: 96/96 text, 96/96 visual, 17/17 local audit checks, R2.
- S016: 114/114 text, 114/114 visual, 19/19 local audit checks + 11/11 visual follow-up mechanism checks, R2.
- S013-S016 final Method Competition Map and seven-gate Method Composer are present.
- Frozen pre-solution 2024-D files remain hash-consistent.

## Mini Transfer

Final: **6/6 mechanism checks PASS**, status `PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX`.

This is post-Dev synthetic mechanism evidence only. It is not clean blind, not R7, and does not establish causal Core gain.

## Historical compatibility

- Final historical/recent regression set: **34/34 scripts complete without substantive failure**.
- Untouched first run exposed legal-timepoint failures in v1.20-v1.24 and v1.32/v1.34-v1.38 harnesses. Original scripts/logs/hashes are preserved.
- Adaptations only widen version/latest/next-pointer or later Dev-review lifecycle assertions. Train-specific formula/code/result assertions and Test unread protection were not relaxed.
- One aggregate runner exceeded its execution window; that timeout is not counted as PASS or FAIL. Scripts were rerun individually/batched unchanged.

## Workspace / library / retrieval protection

- `validate_library.py`: **PASS — 45 papers / 6752 chunks / 32 Train / 7 Dev / 6 Test**.
- `validate_learning_workspace.py`: first wrong-CWD invocation preserved; unchanged root rerun **PASS**.
- Production/evaluation probe: **reviewed-Train-only PASS**; no Dev/Test match entered the sampled candidate set.
- `test_v138_2025F_retrieval.py`: **PASS**, preserving the latest Train retrieval contract.

## Previous-Core identity

Formal v1.40 Previous-Core ZIP was rehashed and matches its release SHA256:
`beaa23ed9210be9c3075e13b84732598a27c25ed0f58ff0759e5b68f74da470c`.

This verifies release identity only; it is not a capability comparison.

## Evidence-scope boundary

This PASS means registered source/page/static-code/result-registry/case-group/workspace/library/retrieval/regression contracts pass. It does **not** mean:
- S013-S016 author code was executed end-to-end on original data;
- v1.41 is causally better than v1.40 or No-Core;
- the Mini Transfer establishes R7;
- historically exposed Test can be reused as fresh blind evidence.

Controlled `No-Core / Previous-Core / New-Core` remains `NOT_RUN`.
