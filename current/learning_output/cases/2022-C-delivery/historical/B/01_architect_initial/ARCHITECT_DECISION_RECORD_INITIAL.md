# Architect Decision Record — INITIAL

**artifact_id:** `ROLE-P1-2022C-RUNB-ARCH-INITIAL-v1`  
**status:** FROZEN after this record and its manifest were hashed.  
**Core:** MathModel-Core v1.41.0 read-only.  
**Exposure:** official problem, four official XLSX files, sealed Core only.

## Problem contract
Decision unit is one of 318 painted bodies. Inputs are fixed paint departure order plus model/power/drive attributes. Decisions are receiving-lane assignment, legal lane-head dispatch, assembly versus return routing, and allowed idle. The output is the second-resolution 74-region matrix. Hard constraints are six 10-slot FIFO lanes, one 10-slot return lane, unary non-preemptive shuttles, one-way mandatory movements, Q1 priority constraints 6/7, and common sender non-idling constraint 8.

## Subproblem map
Source/schema audit -> event simulator -> official score evaluator -> feasible dispatch policy -> Q1/Q2 policy -> output-matrix renderer -> independent replay. Primary uncertainty is the paint-body availability cadence.

## Candidate Model Competition
| Candidate | Fit | Extra assumptions | Cost | Validation | Switch/abandon |
|---|---|---|---|---|---|
| Baseline deterministic FIFO/nearest-lane | feasibility-first | event semantics | low | event replay | keep as 6-hour fallback |
| **Preferred DES + score-aware greedy + small policy search** | direct fit to resource/FIFO structure | 9 s paint takt; source-slot coding during a 9 s lane move | medium | full sequence + score replay | switch if exact-prefix gap is large or replay fails |
| Rolling-horizon MILP/CP-SAT | strong locally | horizon/end effects | high | exact small-instance calibration | adopt only if matched-budget gain is material |
| Direct GA/PSO chromosome | weak without exact repair | repair semantics | high | none yet | not recommended now |

## 6-hour robust baseline
A deterministic legal dispatcher: no deliberate return, central/near-central lane preference, and legal head output. It prioritizes a submission that passes replay over search complexity.

## Data contract
Both data files contain 318 unique rows. 附件1 has 212 hybrid / 106 non-hybrid; 附件2 has 159 / 159. Each has 29 four-drive bodies. `车型` is preserved but is not an official scoring field. This is same-instance combinatorial optimization, not a train/test generalization study.

## Mathematical contract
For output permutation `pi`:
`P_H = sum I(g_j != 2)` over consecutive hybrid bodies; `P_D` is the number of official drive blocks with unequal four-/two-drive counts; `P_R=R`; `T0=9C+72`.
The weighted score is
`S = 100 - 0.4 P_H - 0.3 P_D - 0.2 P_R - 0.001 (T-T0)`.
The final drive block is scored. A first hybrid has no predecessor gap.

## Implementation
Discrete-event state with six `lane[1..10]`, one `return[1..10]`, receive/send shuttle clocks, 9 s adjacent moves, and direct official score primitives. Q1 return-head priority is a hard receive gate; Q1 earliest-arrival lane-1 priority is a hard send gate. Q2 removes only those two gates.

## Validation protocol
Identity hashes; 74-code dictionary; permutation uniqueness; independent score replay; resource/capacity replay; Q1 priority replay; sender non-idling replay; timing lower-bound check; small score counterexamples. Any violation blocks PASS.

## Initial executed results
| Case | Total | Hybrid bad | Drive-block bad | Returns | T |
|---|---:|---:|---:|---:|---:|
| Q1/附件1 | 16.398 | 187 | 21 | 12 | 3036 |
| Q1/附件2 | 37.858 | 139 | 19 | 4 | 2976 |
| Q2/附件1 | 21.704 | 172 | 21 | 14 | 3330 |
| Q2/附件2 | 51.171 | 101 | 19 | 10 | 3663 |

No optimum/best claim is made.

## Switch/abandon conditions and risks
Switch to rolling-horizon exact search if a replay-valid exact-prefix comparison shows material stable gain. Abandon any route needing post-hoc feasibility repair that changes the scored sequence. Main risks: the 9 s input-availability cadence is inferred from the official time formula; the body is coded at the source parking region during a 9 s inter-slot move because no intermediate region code exists; policy tuning is in-instance; no global optimality certificate exists.
