# MathModel-Core v1.28 Validation

## New specialist validation

- `test_v128_regressions.py`: **PASS 129/129**.
- `test_v128_2025A_retrieval.py`: **PASS**.
- `run_2025A_mini_transfer.py`: **PASS_AFTER_RULE_REVISION**.
- Mini Transfer report: `learning_output/mini_transfer/2025-A/mini_transfer_report.json`.

The specialist suite was expanded beyond the earlier 96-check draft to include the finalized Method Map, Mini Transfer, Result Registry, retrieval metadata and Dev/Test protection. No checks were removed merely to preserve the old count.

## Historical rule compatibility

Current-worktree historical rule regressions were rerun from v1.6 through v1.28, including early code-learning regressions: **PASS**.

Two inherited tests (v1.26/v1.27) encoded the transient historical fact that S028 was still unread. In the v1.28 worktree only, these assertions were changed to true historical invariants: S025-S027 knowledge must remain, S028 must remain Train, and later legal review may extend the map. Archived v1.26/v1.27 ZIP files were not modified.

## Historical retrieval compatibility

Representative/latest retrieval chains were rerun separately because bulk replay can exceed the single-command execution limit:

- 2024-A: PASS.
- 2024-B latest S008 retrieval: PASS.
- 2024-C latest S012 retrieval: PASS.
- 2024-E latest S020 retrieval: PASS.
- 2025-E teacher code-link regression: PASS.
- 2025-A S025, S026, S027, S028 retrieval regressions: PASS.

The earlier attempt to run many retrieval scripts in one shell exceeded the environment time limit; it was treated as an execution-limit event, not a model failure. The tests above were rerun individually.

## Corpus / split invariants

`validate_library.py`: **PASS**

- papers: **45**
- chunks verified: **6752**
- split counts: **32 Train / 7 Dev / 6 Test**
- group isolation: PASS
- chunk/page roundtrip: PASS
- reviewed-page bounds: PASS
- invalid input rejection: PASS
- train-only retrieval smoke: PASS

Frozen `split_manifest.json` SHA256 is unchanged and exactly matches the stored hash:

`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

## S028 reproduction boundary

S028 remains **R2**:

- R1 satisfied: full 77-page reading.
- R2 satisfied: paper + printed Python appendix static audit.
- visual audit satisfied separately: original 77-page PDF all-page contact-sheet scan.
- R3 not claimed: no complete original runnable source/data bundle and key optimizer/helper chains are incomplete.
- R4/R5 not claimed: no original-data partial/end-to-end reproduction.
- R6 not claimed: author pipeline not independently reimplemented end to end.
- R7 not claimed: group Mini Transfer validates Core-selected rules, not transfer of the S028 author pipeline.

## Mini Transfer evidence

Status: **PASS_AFTER_RULE_REVISION**.

The first Q1 transfer attempt revealed a real priority-ordering flaw. The rule was revised, then a frozen 12-node instance with 15400 legal topological orders was exhaustively enumerated. Exact peak=7; old rule=13; revised rule=7. Q2 and Q3 mini tests independently confirmed deficit-aware spill subset selection and hard-epsilon-first feasibility logic.

No S029-S031 Dev solution content or Test solution content was used.
