# v1.38 first replay failure diagnosis

The first S045 Result Registry replay asserted that all Table 6.6 one-decimal scores matched Python `round(float, 1)`. It failed on half-tie rows such as 75.85 and 36.65 because Python uses binary floating representation and bankers-style tie behavior, while the paper's displayed one-decimal values follow ordinary decimal half-up presentation (75.9, 36.7).

This is a **replay-harness rounding-contract issue**, not evidence that the paper's Table 6.6 weighting arithmetic is wrong. The replay was repaired to use decimal arithmetic with `ROUND_HALF_UP`, and the first failure is preserved.
