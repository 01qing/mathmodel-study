# MathModel-Core v1.28 Progress

## Scope

- Version: **1.28.0**
- Train paper: **S028 / 2025-A / 面向 Davinci 架构的 NPU 核内调度算法研究**
- Frozen architecture: one shared **MathModel-Core**; no Master / Architect / Engineer / Writer / Reviewer split.
- S028 review: **77/77 full text + original PDF all-page visual contact-sheet audit + printed Python appendix static audit**.
- Reproduction level: **R2**. Visual audit is recorded separately and does not raise R0-R7.
- 2025-A Train case group: **S025-S028 complete**.

## Upgraded protocol completed

1. Full-text learning: completed.
2. Code/formula/figure audit: completed.
3. Candidate Model Competition: Q1/Q2/Q3 completed.
4. Six-hour Baseline: Q1/Q2/Q3 completed.
5. Transferable modules: completed.
6. Error patterns: completed.
7. Reproduction Level: R2 with explicit R3 blockers.
8. Same-Problem Method Competition Map: **finalized across S025-S028**.
9. Skill rules: v1.28 group-level rules appended.
10. Regression tests: extended S028 specialist suite **129/129 PASS**; S028 retrieval PASS; historical rule regressions PASS; library/split validation PASS.
11. Mini Transfer Test: **PASS_AFTER_RULE_REVISION** without exposing Dev/Test solution artifacts.

## High-value S028 findings

### Q1 scheduling

- The paper itself compares MinPeak/EarlyFree/LateAlloc plus SA/TS/GA and ultimately keeps the deterministic EarlyFree route for contest practicality.
- Printed `MinPeak` / `LateAlloc` priority tuples use negative allocation size in a min-heap, which can make **larger ALLOC execute earlier**, contrary to the prose intuition.
- The complexity section uses concrete values such as `O(1.39)` / `O(3.30)` as if they were asymptotic complexity and omits essential candidate-evaluation terms.
- Core conclusion: start from legal Kahn ready-set scheduling; execute legal FREE immediately; then rank by critical-path/slack urgency before incremental-memory tie-break. Stochastic refiners must earn their cost under a common budget.

### Q2 allocation / spill

- Table 14 visible allocator rows have FlashAttention_Case1 minimum **54720**, but Table 16 final reports **33792**. The source of the additional improvement is unresolved.
- The objective contract drifts from normalized `Peak + transfer` to `Time + transfer` later in the algorithm narrative.
- Printed VN-SA defining primitives are incomplete; `get_last_use_time` uses a node-id proxy that need not equal true next-use under a changed schedule.
- Core conclusion: use a lifetime sweep, coalescing free-list, deterministic allocation, exact incremental transfer accounting, and deficit-aware minimum-cost victim subset for small active sets.

### Q3 constrained multiobjective optimization

- S028 uses a 10% transfer allowance while S025 records a 5% candidate contract. The **original task statement must be the sole canonical source** before optimization.
- Table 21 Conv_Case0 uses old transfer **242072**, not Q2 final **230496**. Replaying against Q2 final changes the reported transfer improvement from **14.73% to 10.4496%**.
- The paper says “lower transfer first, then time”; for FlashAttention_Case0 MOPSO has **3847 < 3917**, yet Table 21 selects the NSGA-II 3917 point.
- The same FlashAttention_Case0 NSGA result is shown with execution time **201731** in Table 20 and **2017** in Table 21.
- Printed reconstruction of a loaded GP solution regenerates a random GP tree instead of faithfully recovering the solution.

## 2025-A final Method Competition Map

### Robust baseline

- **Q1**: Kahn/FREE-first + critical-path/slack + incremental-memory tie-break.
- **Q2**: lifetime sweep + coalescing Best-Fit/linear scan + deficit-aware minimum incremental-transfer spill.
- **Q3**: canonical epsilon hard cap + feasibility-first cycle minimization.

### High-risk / high-reward

- topology-preserving SA/TS/LNS for Q1;
- held-out-trained GP/hyper-heuristic for Q2;
- NSGA-II/MOPSO or other MOEA for Q3 when multiple operating points are genuinely needed.

These routes are promoted only after a shared evaluator, matched compute budget, multiple seeds where stochastic, and exact small-instance calibration.

## Mini Transfer Test

A self-constructed 12-node DAG variant was used; no S029-S031 Dev solution was exposed.

- Q1 legal topological orders enumerated: **15400**.
- Exact minimum peak: **7**.
- First Core tie-break ordering (memory delta before critical-path urgency): **13**, an **85.71%** gap.
- Revised ordering (critical-path urgency before memory delta): **7**, exact on the frozen confirmation instance.
- Q2 toy spill deficit: naive cheapest-victim-first cost **16**; exact deficit-aware subset cost **12**.
- Q3 toy epsilon constraint: faster candidate B violates the hard cap and is rejected; feasible candidate A is selected.

Status: **PASS_AFTER_RULE_REVISION**. The initial failure is retained as evidence that the transfer test changed the Core rule rather than merely confirming it.

This does **not** raise S028 from R2. The test validates MathModel-Core selection/composition logic, not S028 author code.

## Train / Dev / Test protection

- Corpus: **45 papers / 6752 chunks**.
- Split: **32 Train / 7 Dev / 6 Test**.
- 2025-A Train S025-S028: complete.
- 2025-B S029-S031: Dev, reviewed pages remain **0** at v1.28 seal.
- All Test reviewed pages remain **0**.
- Frozen split SHA256: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`.

## Next

Enter **2025-B Dev** only under the Dev protocol: first obtain/expose the original problem statement/data without opening Dev solution artifacts, independently solve/freeze a Core baseline, then compare against one Dev paper for rule/model-selection/workflow tuning. If clean problem-only material is unavailable, use a non-Dev variant rather than opening S029-S031 answers prematurely.
