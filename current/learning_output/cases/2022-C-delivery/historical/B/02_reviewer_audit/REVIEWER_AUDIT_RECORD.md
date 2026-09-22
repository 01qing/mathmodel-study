# Reviewer Audit Record — FROZEN

**reviewed_version:** `ROLE-P1-2022C-RUNB-ARCH-INITIAL-v1`  
**decision:** **HOLD**

## First-fail (recorded before any repair)
- **Severity:** MATERIAL
- **Location:** `architect_initial_solver.py` + missing action/event trace
- **Failure class:** implementation visibility / constraint replay gap
- **Original claim:** schedule implementation and frozen headline results are replay-valid.
- **Evidence:** the frozen solver file is descriptive rather than executable; the frozen result JSON has output permutations, return totals and T but no exact event/action trace.
- **Consequence:** sequence-based score arithmetic can be independently recomputed, but the Reviewer cannot prove shuttle exclusivity, capacity, mandatory movement, Q1 priorities 6/7, sender non-idling, or the reported completion times.
- **Minimal repair:** exact executable DES + deterministic config + action/event log + matrices from the same run_id.
- **Retest required:** execute all four cases; independent score replay; Q1 priority replay; resource/capacity/non-idling replay; matrix/event consistency.

## Formula findings
Weighted score formula, hybrid-gap rule, drive-block rule and final-block handling independently recompute exactly from the frozen output sequences. Time arithmetic is correct conditional on reported T, but T provenance is not independently replayable.

## Code findings
The artifact accurately names the method as discrete-event greedy and does not misuse a complex optimizer label. However, the executable definition is absent, which is a material audit failure.

## Data/evaluation findings
The two official datasets each contain 318 unique bodies. Same-instance tuning is explicitly labeled and not presented as generalization. No reference-ranking claim is used as truth.

## Result Registry audit
All four reported total scores, hybrid-bad counts and drive-block-bad counts exactly match an independent score implementation applied to the frozen output permutations. Schedule feasibility remains **HOLD** because there is no replayable event trace.

## Reproduction level
`R1` — formulas/results can be statically checked, but the actual scheduling code path is not available in the frozen artifact.

## Decision
**HOLD.** No unqualified PASS. The only verified scope is source identity + output permutation integrity + sequence-score arithmetic.
