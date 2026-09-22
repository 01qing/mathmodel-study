# ROLE-P1-2022C-v0.2 — Pass 3 Final Artifact

Status: `FINAL_FROZEN_AFTER_ONE_REPAIR`
Condition: Run A — Single-Core Generalist
Core: MathModel-Core v1.41.0 SEALED / READ-ONLY

## 1. Repair scope

Exactly one repair cycle was used after Pass-2 first-fail. **No schedule was re-optimized, no headline score was improved, and no second repair cycle was run.**

The repair is reproducibility/provenance only:

- original Pass-1 frozen run objects and scores remain unchanged;
- original result workbooks remain unchanged as historical outputs;
- canonical static per-second matrices are added as `materialized/*_matrix.csv.gz`;
- action logs and output sequences are added;
- a standalone independent validator is frozen;
- XLSX recalculation portability is explicitly marked `NOT_VERIFIED` rather than silently assumed.

## 2. Final solution architecture

The solution treats PBS as a deterministic discrete-event resequencing system.

### State

At event time `t`, the state contains:

- next unadmitted painted body;
- ordered occupants and release/move times for each of six incoming FIFO lanes;
- return-lane state;
- receiving/sending transverse-machine availability;
- bodies already delivered to total assembly;
- per-body region history.

### Decisions

- receiving decision: assign the next fresh body to a feasible incoming lane (or, if applicable, prioritize a body leaving the return lane);
- sending decision: select a body that has reached incoming-lane position 1 and either deliver it to total assembly or send it to the return lane.

The selected frozen schedules use no return-lane operation.

### Dynamics

- incoming/return parking-position movement is mandatory as soon as the next position becomes free and consumes 9 seconds;
- transverse-machine action times use the official lane-dependent round-trip durations;
- each machine is non-preemptive and returns to its center position before another action;
- Q1 enforces priority constraints 6 and 7; Q2 removes only these two constraints;
- constraint 8 is enforced in both questions.

## 3. Candidate Model Competition and chosen mainline

Pass-1 candidates were:

1. B0 direct FIFO lane-4 baseline;
2. B1 static attribute partition;
3. B2 score-aware greedy lane assignment;
4. B3 deterministic multistart lane-partition heuristic;
5. optional return-lane variants.

The frozen mainline is **B3 + exact discrete-event feasibility/score evaluation**. It is a heuristic schedule generator, not an exact global optimizer.

## 4. Six-hour robust baseline

All 318 bodies pass through lane 4 in original order, no return route:

`T0 = 9*318+72 = 2934 s`.

| Dataset | P1 | P2 | R | T | Literal weighted score |
|---|---:|---:|---:|---:|---:|
| Attachment 1 | 203 | 19 | 0 | 2934 | 13.100 |
| Attachment 2 | 148 | 19 | 0 | 2934 | 35.100 |

## 5. Final frozen headline results

| Result | Problem | Dataset | P1 | P2 | Returns | T (s) | Literal weighted score | Capped-S4 sensitivity |
|---|---|---|---:|---:|---:|---:|---:|---:|
| result11 | Q1 | Attachment 1 | 175 | 18 | 0 | 3531 | **24.003** | 24.003 |
| result12 | Q1 | Attachment 2 | 104 | 19 | 0 | 2919 | **52.715** | 52.700 |
| result21 | Q2 | Attachment 1 | 167 | 22 | 0 | 2625 | **26.909** | 26.600 |
| result22 | Q2 | Attachment 2 | 93 | 20 | 0 | 3003 | **56.731** | 56.731 |

These are reproduced heuristic feasible-schedule results. They are **not** global optima and are **not** Run-A-vs-Run-B comparison results.

## 6. Validation outcome

`validation_report.json` reports:

- Core identity: PASS;
- five-source identity: PASS;
- event/constraint validation: PASS;
- independent score recomputation: PASS;
- hard failures: **0**.

Warnings retained:

- `TIME_SCORE_GT_100` for result12/result21 under the literal printed formula;
- `SAMPLED_CODE_DUPLICATE` at a small number of same-second event boundaries;
- original dynamic-formula result workbooks: portability/recalculation `NOT_VERIFIED` in the independent spreadsheet engine.

## 7. Canonical evidence hierarchy

For evaluation of this run, use evidence in this order:

1. `frozen_runs.pkl` — frozen computational state;
2. `materialized/*_matrix.csv.gz` — canonical static per-second matrices;
3. `materialized/*_action_log.csv` — event provenance;
4. `materialized/*_output_sequence.csv` — final sequence provenance;
5. `validation_report.json` + `validate_frozen_runs.py` — independent audit;
6. `results/*.xlsx` — requested workbook-form deliverables, retained but **not portable-recalc verified**.

## 8. Final Result Registry status

All four headline result rows are classified:

`REPRODUCED_FROM_FROZEN_RUN_STATE / EVENT_VALIDATED / SCORE_RECOMPUTED / HEURISTIC_FEASIBLE / NOT_OPTIMALITY_PROVEN`.

## 9. Final unresolved risks

1. The statement's “theoretical maximum 100” conflicts with the uncapped printed time-score expression when `T<9C+72`.
2. Integer-second output semantics at simultaneous parking-position handoff are underspecified.
3. The original search trajectory/source is not preserved; only the selected schedule state and full validation/provenance are preserved.
4. Original `.xlsx` formula portability was not verified by the independent spreadsheet engine.
5. No comparison with Run B is available.

## 10. Freeze conclusion

The benchmark's requested six terminal artifacts are now frozen. The run is complete **with explicit limitations**, and the appropriate status is:

`RUN_A_FINAL_FROZEN — EVENT_AND_SCORE_VALIDATION_PASS — XLSX_PORTABILITY_LIMITED — NO_OPTIMALITY_OR_RUN_B_SUPERIORITY_CLAIM`
