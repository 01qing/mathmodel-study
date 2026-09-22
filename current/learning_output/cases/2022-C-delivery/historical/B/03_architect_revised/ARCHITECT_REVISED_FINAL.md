# Architect Revised Final Artifact — one repair only

**artifact_id:** `ROLE-P1-2022C-RUNB-ARCH-REVISED-v1`  
**repair cycle:** 1 of 1  
**parent:** `ROLE-P1-2022C-RUNB-ARCH-INITIAL-v1`

## Repair scope
The Reviewer first-fail was implementation visibility / constraint replay. This repair does **not** change the mathematical model, policies, assumptions, output sequences, scores, or claimed method. It adds the exact executable discrete-event simulator, verified source snapshot, deterministic action logs, matrix checksums, and the four submission workbooks generated from the same run state.

## Executable primitive
`revised_solver.py` contains the full state transition loop, lane/return movement, shuttle event timing, Q1 priority gates, Q2 relaxation, score-aware greedy dispatch, conservative recycle rule, scoring, and matrix-state reconstruction.

## Provenance
`official_inputs_snapshot.json` was derived only from the five identity-verified official inputs. `revised_execution.json` stores per-case output sequence, action log, return counts, internal violation list, exact score components, matrix checksum, and result-file hash.

## Claim limits
- No global optimality or best-known claim.
- Policy search is same-instance optimization, not out-of-sample generalization.
- The 9 s paint availability takt remains an explicit inference from the official `9C+72` theoretical-fastest formula.
- During a 9 s adjacent parking move, the source parking region is used until arrival because the official 74-code dictionary has no in-between lane-motion region.
- Spreadsheet transport generation does not change the simulator or scores.
