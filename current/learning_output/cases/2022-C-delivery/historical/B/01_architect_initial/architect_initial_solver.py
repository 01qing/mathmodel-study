#!/usr/bin/env python3
"""Frozen Architect initial implementation note for ROLE-P1-2022C-v0.2.

Actual primitives executed:
- one-second discrete-event PBS simulator;
- six FIFO lanes (10 slots each), one FIFO return lane (10 slots);
- mandatory adjacent movement, 9 s per slot, source slot held until movement completes;
- unary non-preemptive receive/send shuttles;
- exact Q1 priority gates 6/7; common non-idling gate 8;
- Q2 removes only gates 6/7;
- score-aware greedy lane assignment and lane-head dispatch;
- conservative recycle only when one additional non-hybrid is needed; max one recycle/body.
No GA/PSO/MILP/CP-SAT label is claimed.

Registered timing assumption:
paint bodies become available in fixed input order at 9 s takt, inferred from the
official stated theoretical fastest completion time 9*C+72. Same-time
zero-duration transitions record the last official region code.

Frozen policy permutations and exact output sequences/results are stored in
architect_initial_results.json.
"""
