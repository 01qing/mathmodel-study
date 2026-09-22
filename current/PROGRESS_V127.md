# MathModel-Core v1.27 Progress

## Scope

- Version: **1.27.0**
- Train paper: **S027 / 2025-A / NPU 核内调度算法设计与优化研究**
- Frozen protocol: MathModel-Core single shared core; no role-Skill split.
- S027 review: 120/120 full text + original PDF all-page visual contact-sheet audit + printed Python appendix static audit.
- Reproduction level: **R2**. Visual audit is recorded separately and does not raise reproduction level.

## Upgraded protocol completed

1. Full-text learning: completed.
2. Code/formula/figure audit: completed.
3. Candidate Model Competition: Q1/Q2/Q3 completed.
4. Six-hour Baseline: Q1/Q2/Q3 completed.
5. Transferable modules: completed.
6. Error patterns: completed.
7. Reproduction Level: R2 with explicit R3 blockers.
8. Same-Problem Method Map: updated to S025+S026+S027; S028 remains pending Train.
9. Skill rules: v1.27 incremental rules appended.
10. Regression tests: S027 specialist 82/82 PASS; S027 retrieval PASS; library/split validation PASS.
11. Mini Transfer Test: **NOT DUE** until S028 completes the 2025-A Train group.

## High-value S027 findings

### Q1
- MCBGS paper priority claims Type+Size+Criticality, but printed code omits the helper definitions that implement those components.
- Headline reductions 89.2%/85.5%/89.2% match aggregate-sum weighted reductions; the arithmetic mean of six casewise reductions is about 76.55%/59.34%/76.51%. Both must be labeled separately.
- S027 Cmax matches S025/S026 on five workloads; Conv_Case0 is 12432, between S025=7660 and S026=14592.

### Q2
- Abstract says Best-Fit while body/code implement First-Fit.
- Paper spill rule is argmin/lowest cost; visible code reverse-sorts a different score and selects the largest.
- Table 5.11 headline MOACADSA row is not the simple mean or total of Table 5.12. Aggregation provenance is unresolved.
- S027 reports lower transfer than S025 on 5/6 workloads, but this is not promoted before common-evaluator replay.

### Q3
- Transfer cap drifts between 15% and 10%; under 10%, FlashAttention_Case0 violates the cap, while all six fit under 15%.
- Aggregate replay: cycles -12.6197%, traffic +7.1788%. Table change signs for traffic contradict the raw values/text.
- Q3 appendix hard-coded baselines drift from Q2 tables and `_apply_optimization_strategies` is missing.
- Visible code processes one case at a time; cross-instance/multi-sequence collaboration is not implementation-evidenced.

## New reusable gates

- macro-per-instance vs aggregate/micro improvement semantics
- allocator-name primitive test (First-Fit vs Best-Fit)
- spill argmin/argmax direction test
- optimizer/helper coverage before R3
- canonical hard-cap parameter source
- Result Registry baseline run-id reuse across questions
- sign/semantic delta generated from raw before/after values
- multi-instance coordination requires explicit coupled state/constraints

## Train/Dev/Test protection

- Corpus: 45 papers / 6752 chunks
- Split: 32 Train / 7 Dev / 6 Test
- Train reviewed through S027 according to frozen sequence.
- S028 remains unread/pending Train at v1.27 seal.
- S029-S030 Dev reviewed pages: 0.
- All Test reviewed pages: 0.
- Split manifest hash unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`.

## Next

Review **S028 / 2025-A** with the same upgraded MathModel-Core protocol. After S028, freeze the four-paper 2025-A Method Competition Map and run one Mini Transfer Test without exposing Test solutions.
