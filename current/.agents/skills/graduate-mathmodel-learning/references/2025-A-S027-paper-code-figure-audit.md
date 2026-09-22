# 2025-A S027 MathModel-Core paper/code/figure audit

## Scope

- Paper: S027, *NPU 核内调度算法设计与优化研究*
- Split: Train
- Pages: 120/120 full text reviewed
- Visual: original 120-page PDF rendered and scanned; visual audit is separate from reproduction level
- Code: printed Python appendix statically audited
- Reproduction: **R2**. R3 is blocked by missing algorithm-defining helpers / runnable source-data bundle.

## Q1

Baseline: Kahn ready-set + FREE-first + critical-path/slack + memory delta.

Author route: MCBGS deterministic multi-constraint greedy. The paper describes Type + Size + Criticality, but the printed appendix calls helper functions whose definitions are absent. The headline 89.2%/85.5%/89.2% reductions match aggregate-sum weighted reduction, not arithmetic mean across six workload percentages. Both macro and aggregate summaries must be stored.

## Q2

Baseline: lifetime sweep + deterministic Best-Fit/linear-scan + minimum true incremental-transfer victim.

Author route: MOACADSA-style allocation/spill. Abstract says Best-Fit, visible code behaves as First-Fit. Paper victim equation is argmin; visible code reverse-sorts a different size*lifetime score and selects maximum. Table 5.11 headline MOACADSA values are not the simple mean or total of Table 5.12, so aggregation provenance remains unresolved.

## Q3

Baseline: epsilon-constraint; enforce official transfer cap first, then minimize cycles.

Author route: DOSA/resource-aware optimization. Most prose/code uses 15% traffic tolerance but Eq.(6.127) gives 10%; FlashAttention_Case0 is feasible under 15% but exceeds 10%. Table 6.14 traffic bytes increase while its change-rate column is negative. The appendix hard-coded Q2 baseline also differs from the paper tables, and `_apply_optimization_strategies` is not defined in the printed appendix.

## Candidate competition / Method Composer

Do not rank S025/S026/S027 by table values before one common evaluator aligns DAG parsing, spill semantics, cache constraints, Bytes/Cycles and transfer cap. Current robust route is deterministic baseline first; advanced heuristic only after matched-budget improvement and exact-small-instance calibration.

## Figure decision lessons

S027 is formula/table/algorithm-heavy (9 numbered figures, 14 numbered tables, ~29 pages printed code). For a new NPU scheduling problem, add evidence the paper underuses: exact-gap calibration, runtime-quality budget, micro-vs-aggregate improvement, and an actual feasible cycle-vs-transfer plot with the hard-cap line.
