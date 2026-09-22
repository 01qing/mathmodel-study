# 2025-A S028 paper/code/figure audit

- Split: Train. Pages: 77. Reproduction: R2.
- Full original PDF visual audit completed; pages 59–77 are printed code appendix.
- Q1: EarlyFree is a strong contest baseline, but MinPeak/LateAlloc printed priority uses `-Size` in a min-heap, so large ALLOC can be advanced rather than delayed. Complexity table misuses concrete O-notation.
- Q2: Table 14 FlashAttention1 minimum is 54720 while narrative/Table16 final is 33792; provenance unresolved. Eq.4-10 uses Peak+transfer, later VN-SA text uses Time+transfer.
- Q3: paper uses 10%/110% transfer cap while S025 records 5%; original problem contract must resolve. Conv0 Table21 baseline mixes Table15 rather than Q2 final. FlashAttention0 violates transfer-first selection and has 201731 vs 2017 time drift. Printed NSGA/MOPSO reconstruction replaces loaded GP rule with a random tree.
- Core lesson: simple deterministic baseline first; expensive search must earn its budget. Final values, baselines and Pareto operating points are generated from one Result Registry.
