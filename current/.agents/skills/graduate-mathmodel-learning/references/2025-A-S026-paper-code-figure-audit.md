# 2025-A S026 — MathModel-Core paper/code/figure audit

## Scope
- Paper: S026, 2025-A, train.
- 98/98 pages full-text reviewed.
- Original PDF visually scanned across all 98 pages using contact sheets; selected result pages inspected individually.
- Printed MATLAB Appendix A statically audited.
- Reproduction level: **R2**. No original `.m` bundle + input CSV + MATLAB runtime execution; Q3 DPEA code is not visible in the appendix.

## Q1
Author: type/size/criticality priority greedy + adaptive tabu/neighborhood search.

Visible appendix:
- Greedy initializer uses coarse Op-type scores only (`FREE=1000`, compute=100, normal ALLOC=10, conflicting L0 ALLOC=-1000); no size or criticality term is used.
- `tabu_length=20` is fixed; only neighborhood size adapts.
- Tabu list concatenates move strings into a flat character sequence, then truncates by character count; this is not a FIFO queue of exact moves.

Core decision:
- Six-hour baseline: Kahn ready-set + FREE-first + critical-path/slack tie-break + exact Cmax replay.
- S025 SA and S026 tabu are optional refiners under matched evaluator/runtime budgets.
- S026 reported Q1 equals S025 on 5/6 workloads and is worse on Conv_Case0 (14592 vs 7660).

## Q2
Author: ABQPSO mixed encoding for sequence/offset/spill flag/spill offset + repair/local search.

Visible appendix:
- `Mbest` and local attractor `P` are computed but never used.
- Particle update is inertia + c1/c2 velocity style; defining quantum-behaved update is not verified.
- Fitness mixes raw Bytes and Cycles: `1.0*extraData + 0.1*execTime + penalty` without normalization.
- Local search can update `globalBest` fields without updating scalar `globalBestFitness`, creating stale-score/logging risk.
- Feasibility replay and event-driven pipeline runtime evaluation are useful reusable modules after repair.

Cross-paper warning:
- S026 reports higher Q2 transfer than S025 on all six workloads. Do not declare S025 superior until both are run through one common evaluator with the same source data and semantics.

## Q3
Author: DPEA dual-population multi-objective evolutionary algorithm.

Audit:
- No executable DPEA appendix implementation found.
- Q2 Eq.5.20 charges COPY_IN-used spill as `1*size`, non-COPY_IN as `2*size`.
- Q3 Eq.6.67 changes semantics: lambda=0 for COPY_IN-used spill and 1 otherwise, omitting COPY_IN spill cost.
- The contest hard transfer-tolerance cap is not explicitly encoded before Pareto ranking.
- Table 6.8 improvement percentages are arithmetically consistent relative to S026 Table 5.7, but are not traceable to executable Q3 code.

Core decision:
- Default Q3 baseline is epsilon-constraint: enforce transfer cap first, then minimize makespan with resource-aware list scheduling/local search.
- DPEA/NSGA-II only enter mainline with executable implementation, corrected metric semantics, actual feasible Pareto plot, multi-seed/matched-budget superiority.

## Figure decision lessons
- Operation-distribution figures are descriptive, not optimizer evidence.
- Cache-residency trajectories should include matched baseline/candidate under common axes.
- Cache Gantt plots explain lifecycle overlap and spill timing but not optimality.
- A multi-objective paper must show the actual feasible Pareto front, cap line and selected operating point; radar before/after is not a Pareto proof.
