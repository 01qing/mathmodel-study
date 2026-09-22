# MathModel-Core v1.34 Validation

## Overall status

**PASS for the v1.34 release contract, with evidence scope explicitly bounded.**

## S036 specialist regression

- `PASS 45/45`
- verifies S036 Train identity, 76 reviewed pages, R1 ceiling, Q1 split leakage finding, Q2 fixed-period contract, Q3 multi-metric conflict, Q4 score replay / graph contradiction, final 2025-C map, Mini Transfer first-fail history, Dev/Test protection and next-learning pointer.

## Historical Core regressions

- **22/22 PASS** after rerunning the v1.6, v1.10-v1.28, v1.8 code-learning and v1.9 training regression scripts from the Skill root.
- A first raw batch was launched from the wrong working directory and `test_v18_code_learning.py` failed to locate the existing GTeacher cards; rerunning from the Skill root passed. The failure was an execution-harness cwd issue, not missing knowledge assets.

## Library and retrieval integrity

- library validation: **PASS**
- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- frozen split SHA256 unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`
- ordinary `evaluation` and `production` retrieval remain reviewed-Train-only; S035/S036 appear as reviewed Train evidence while S030/S031 and Test remain excluded.

## 2025-C closure

- S032: R2
- S033: R2
- S034: R1
- S035: R1
- S036: R1
- final Same-Problem Method Competition Map: **complete for S032-S036**
- Method Composer seven-gate compatibility checks: recorded in the final map
- Figure Decision Rules: `knowledge_base/figure_decision_rules/2025-C-final.json`

## Mini Transfer / Capability Evidence Gate

- scope: **synthetic non-paper mechanism transfer**, not Dev/Test and not author-paper reproduction
- first run: **FAIL**
- diagnosis: fixed physical period was correct, but nonlinear amplitude/phase optimization remained brittle
- repair: fixed-frequency linear basis `a*sin(wx)+b*cos(wx)+C` + robust IRLS + reject gate
- repaired status: **PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX**
- current persisted reconstructed fixture summary: free-period robust mean clean RMSE `4.297353`, first fixed nonlinear `10.041471`, repaired fixed linear IRLS `0.041509`, repaired wins `18/18`, invalid rejects `12/12`.
- exact numerical identity with any earlier chat-only run is **not claimed**; the persisted fixture and log are the release evidence.
- controlled `No-Core / Previous-Core / New-Core` ablation: **NOT_RUN** because no strict three-Core harness is available. Therefore no whole-Core causal-improvement claim is made.

## Reproduction boundary

S035/S036 source-code paths/notebooks are referenced in the papers but actual author source files are unavailable in the current excellent-paper collection; visual review does not raise reproduction level. No R2/R3+ claim is made for S035/S036.

## Dev/Test protection and next stage

- S030/S031: Dev reserve, unread
- S037/S038: Test, frozen
- S039-S041: historical reviewed Train assets already present
- next unread Train: **S042 / 2025-F**
