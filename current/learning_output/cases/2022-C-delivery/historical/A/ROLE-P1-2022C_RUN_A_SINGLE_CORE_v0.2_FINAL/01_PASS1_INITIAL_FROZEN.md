# ROLE-P1-2022C-v0.2 — Pass 1 Initial Artifact (Frozen Reconstruction)

Status: `PASS1_FROZEN_RECONSTRUCTED_FROM_EXISTING_RUN_STATE`
Core: `MathModel-Core v1.41.0 SEALED / READ-ONLY`
Condition: Run A — Single-Core Generalist

## Freeze note

The original interaction reached its execution ceiling before a formal Pass-1 markdown file was written. This document freezes the **pre-audit computational state already produced**: `frozen_runs.pkl`, the four result workbooks, the headline scores, and the independently selected modeling route. No new model search or result improvement is introduced here. The formal self-audit starts only in `02_PASS2_SELF_AUDIT.md`.

## 1. Problem contract

Input: one fixed painted-body sequence with vehicle ID, model class, power type, and drive type. PBS has six FIFO incoming lanes of 10 parking positions each, one 10-position return lane, a receiving transverse machine, and a sending transverse machine. Each lane-position move consumes 9 s. The two transverse machines have lane-dependent round-trip times. Question 1 enforces all PBS constraints; Question 2 removes only priority constraints 6 and 7.

Output: a second-by-second region-code matrix for every body until the last body reaches the PBS-total-assembly receiving port, plus the four weighted objective scores.

## 2. Question decomposition

1. Parse official vehicle data and region codes.
2. Construct a discrete-event PBS state transition model.
3. Generate lane-assignment/sending policies under Question-1 and Question-2 rule sets.
4. Simulate the complete schedule and materialize each body's per-second coded state.
5. Extract the total-assembly output sequence.
6. Recompute four official score components and weighted total.
7. Validate hard PBS constraints and source/result provenance.

## 3. Candidate Model Competition

Candidate families considered in Pass 1:

- **B0 direct FIFO baseline:** send all bodies through incoming lane 4, preserving input order.
- **B1 static attribute partition:** split bodies into lanes by power/drive categories, then use feasible FIFO sending.
- **B2 score-aware greedy policy:** choose lane assignments to improve hybrid spacing and drive alternation while respecting capacity/timing.
- **B3 deterministic multistart lane-partition policy:** evaluate multiple fixed/parameterized lane partitions and retain a feasible high-scoring realization.
- **Return-lane variants:** considered as an extra resequencing mechanism, but not selected in the frozen headline schedules.

The frozen mainline is B3 with an exact discrete-event simulation. No optimality claim is made.

## 4. Six-hour robust baseline

A conservative baseline sends all 318 bodies through lane 4 in original order. It uses no return-lane operation and reproduces the problem statement's reference time

`T0 = 9C + 72 = 9*318 + 72 = 2934 s`.

Literal official-formula baseline scores:

| Dataset | Obj.1 penalty | Obj.2 penalty | Return uses | T (s) | Weighted total |
|---|---:|---:|---:|---:|---:|
| Attachment 1 | 203 | 19 | 0 | 2934 | 13.100 |
| Attachment 2 | 148 | 19 | 0 | 2934 | 35.100 |

## 5. Mainline mathematical/data contract

For an output sequence `pi=(pi_1,...,pi_C)`:

- Objective 1 score: `S1 = 100 - P1`, where `P1` is the number of adjacent hybrid-body pairs in the hybrid subsequence having a number of intervening non-hybrid bodies different from 2.
- Objective 2 score: `S2 = 100 - P2`; split the drive sequence according to the official transition rule determined by the first drive type, and count blocks whose four-wheel/two-wheel counts are not 1:1.
- Objective 3 score: `S3 = 100 - R`, where `R` is return-lane use count.
- Objective 4 literal score: `S4 = 100 - 0.01*(T - (9C+72))`.
- Weighted total: `S = 0.4*S1 + 0.3*S2 + 0.2*S3 + 0.1*S4`.

No lower bound at 0 and no upper cap at 100 were added in Pass 1 because neither is explicitly specified in the printed component formulas.

## 6. Implementation primitive

The computational primitive is a deterministic discrete-event PBS simulator. Its frozen run state contains:

- action log `(start_time, action_type, vehicle_id, lane, action_duration)`;
- total completion time;
- total-assembly output sequence with vehicle attributes;
- per-vehicle second-by-second coded region history;
- score decomposition.

All four selected frozen schedules use zero return-lane operations.

## 7. Reproduced headline results

| Key | Problem | Dataset | P1 | P2 | R | T (s) | S1 | S2 | S3 | S4 literal | Weighted total |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| result11 | Q1 | Attachment 1 | 175 | 18 | 0 | 3531 | -75 | 82 | 100 | 94.03 | 24.003 |
| result12 | Q1 | Attachment 2 | 104 | 19 | 0 | 2919 | -4 | 81 | 100 | 100.15 | 52.715 |
| result21 | Q2 | Attachment 1 | 167 | 22 | 0 | 2625 | -67 | 78 | 100 | 103.09 | 26.909 |
| result22 | Q2 | Attachment 2 | 93 | 20 | 0 | 3003 | 7 | 80 | 100 | 99.31 | 56.731 |

## 8. Pass-1 validation design

Planned/partial checks at freeze:

- official Core/source identity;
- 318-body permutation and source-attribute preservation;
- machine non-overlap and lane-dependent timing;
- FIFO lane order;
- lane movement timing and direction;
- Question-1 priority rule 7 and universal no-idle rule 8;
- independent score recomputation;
- result matrix/code validity;
- provenance and workbook portability.

## 9. Pass-1 Result Registry

The four rows in Section 7 are `REPRODUCED_FROM_FROZEN_RUN_STATE`. They are heuristic feasible-schedule results only, not global optima and not comparisons against Run B.

## 10. Unresolved risks at Pass-1 freeze

1. The printed time-score formula can exceed 100 when `T < 9C+72`; a capped-vs-literal sensitivity audit is required.
2. The result workbooks use dynamic-array formulas and require a compatible recalculation engine; static materialization still requires audit.
3. The computational run object was preserved, but the exact optimizer/search source was not yet frozen as a standalone script.
4. No superiority, optimality, or Run-B comparison claim is permitted.
