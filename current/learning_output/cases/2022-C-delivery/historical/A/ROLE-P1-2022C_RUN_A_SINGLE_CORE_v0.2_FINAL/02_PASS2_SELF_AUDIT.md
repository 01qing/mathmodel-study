# ROLE-P1-2022C-v0.2 — Pass 2 Single-Core Self-Audit

Status: `PASS2_FROZEN`
Audit target: `01_PASS1_INITIAL_FROZEN.md` + `frozen_runs.pkl`
Core: `MathModel-Core v1.41.0 SEALED / READ-ONLY`
Repair budget after this audit: **at most one repair cycle**

## 1. First-fail record

The first material defect found after Pass-1 freeze was **output-workbook portability/recalculation failure**:

- each of the four original result workbooks uses a dynamic-array `LET + XLOOKUP` formula family;
- when independently imported/evaluated through the benchmark spreadsheet toolchain, `Sheet1!B2` evaluated as `#VALUE!`;
- therefore the `.xlsx` files cannot be treated as independently portable/recalculation-verified evidence, even though the underlying frozen event histories are present.

This first-fail is preserved here **before repair**. It is not silently overwritten.

## 2. Formula and objective audit

### Objective 1

Pass-1 primitive counts the number of non-hybrid bodies between each consecutive pair in the hybrid subsequence and applies one penalty whenever this count is not 2. This matches the printed scoring rule. Independent recomputation reproduces all four Pass-1 penalties exactly.

### Objective 2

Pass-1 splits the drive sequence at transitions from the opposite drive type back to the first drive type, then penalizes each block whose four-wheel/two-wheel counts differ. This matches the rule illustrated by the official `442242444224 -> 4422,42,44422,4` example. Independent recomputation reproduces all four Pass-1 penalties exactly.

### Objective 3

All four selected schedules contain zero `send_return` / `recv_return` operations. Thus `S3=100` in every frozen headline result. Event-log counts and stored scores agree.

### Objective 4 — specification ambiguity

The frozen implementation uses the literal printed expression

`S4 = 100 - 0.01*(T-(9C+72))`.

For `result12` and `result21`, `T < 9C+72`, so the literal formula gives respectively `100.15` and `103.09`. The statement also says the weighted score has a theoretical maximum of 100, creating an internal specification tension. No unprinted cap is introduced in the canonical result. Instead the audit records a capped-at-100 sensitivity value:

| Result | Literal S4 | Literal total | S4 capped at 100 | Capped-total sensitivity |
|---|---:|---:|---:|---:|
| result11 | 94.03 | 24.003 | 94.03 | 24.003 |
| result12 | 100.15 | 52.715 | 100.00 | 52.700 |
| result21 | 103.09 | 26.909 | 100.00 | 26.600 |
| result22 | 99.31 | 56.731 | 99.31 | 56.731 |

Audit conclusion: **not a silent formula error; unresolved statement ambiguity**. Canonical registry keeps literal scores and records capped values only as sensitivity.

## 3. Constraint / simulator audit

The standalone validator reconstructed and checked the complete frozen event histories. Across all four runs there were **0 hard failures**.

Checks that passed:

- exactly 318 bodies and an output permutation of IDs 1..318;
- output body attributes match the official input snapshots;
- all nonblank states use an official region code;
- fresh receiving events preserve the original painted-body order;
- receiving/sending transverse-machine durations match lane-dependent official durations;
- each transverse machine has no overlapping action interval;
- all six incoming lanes preserve FIFO order;
- an independent FIFO-blocking reconstruction matches recorded lane parking arrivals and mandatory moves;
- total completion time matches the final send-out event end time;
- output sequence order matches the send-out event order;
- constraint 8 (sender cannot idle when an incoming-lane position 1 is available) passes;
- Question-1 priority constraint 7 passes for the complete sending stream;
- Question-1 return-lane priority constraint 6 is vacuously satisfied because the selected Q1 schedules never use the return lane;
- all four score components and weighted totals reproduce independently from the frozen output sequence and log.

## 4. Sampled matrix occupancy warning

The per-second matrices contain a small number of integer-second duplicate parking-region codes. The independent event-level reconstruction does **not** find a physical lane collision. The duplicates arise at same-second event boundaries under the selected “last region at this second” sampling convention: a departing body can retain the old parking code at the same integer second that a newly admitted/following body obtains that code.

This is preserved as warning `SAMPLED_CODE_DUPLICATE`, not converted into a hard simulator failure. Because the official output format has no separate code for “between two parking positions”, the exact sampling semantics at such boundaries remain a claim limitation.

## 5. Leakage and identity audit

- Required Core wrapper SHA-256 reproduced exactly: `a4ef5b69d31ab2b5de032e9fa9e8c78f15a09b773bfca3ace57870cdb418016f`.
- All five official source identities matched their frozen byte sizes and Git-blob SHA-1 values.
- No Run-B artifact was used.
- No 2022-C excellent paper, reference answer, solution article, or prior worked solution was opened during this run.
- No external web/Notion/GitHub solution search was used after the run started.

Audit conclusion: **no detected contamination or Core substitution**.

## 6. Model-label / primitive audit

Pass 1 labels the selected mainline as a **deterministic multistart lane-partition heuristic evaluated by an exact discrete-event simulator**. It does not call the heuristic an exact optimizer and makes no global-optimum claim. The label is consistent with the available computational primitive and frozen run state.

## 7. Provenance audit

Headline scores are supported by:

1. frozen run objects (`frozen_runs.pkl`);
2. action logs;
3. output-sequence CSVs;
4. canonical per-second static matrices (`*_matrix.csv.gz`);
5. official input snapshots;
6. independent validator and `validation_report.json`.

A limitation remains: the exact original candidate-search/optimizer source that generated the selected schedules was not preserved as a standalone script before Pass-1 freeze. The final bundle can reproduce and validate the selected schedules, but cannot honestly claim bit-for-bit rerunning of the original search trajectory from scratch.

## 8. Audit verdict and repair decision

Material defect requiring the single allowed repair:

`F1 — the original dynamic-formula XLSX outputs are not portable-recalculation verified.`

One repair cycle will therefore:

- preserve the original four `.xlsx` workbooks unchanged;
- add canonical static per-second matrices as gzip CSV files derived directly from the frozen histories;
- add action logs/output sequences and the standalone validator;
- explicitly downgrade the XLSX portability claim;
- preserve the time-score and integer-second sampling ambiguities as claim limits rather than inventing unsupported fixes.

No second model-search or score-improvement cycle is permitted or performed.
