# 2025-F Mini Transfer Test

## Evidence class

This is a **post-learning synthetic mechanism transfer**, not a clean blind Dev/Test benchmark and not paper R7 evidence. It was constructed only after S042-S045 were reviewed.

## First run: FAIL

A non-garden warehouse inspection graph was used. Two parent routes were individually feasible. A positional one-point crossover at the same array index produced a child containing a non-edge transition. Therefore the claim “one-point crossover preserves path connectivity” failed immediately.

This first failure is preserved in `first_fail.json`.

## Diagnosis and rule change

The representation was treating a graph path as an arbitrary sequence. Equal-length node arrays do not imply interchangeable suffixes. The repaired rule is:

`splice only at a common graph vertex (or construct a verified feasible bridge) -> decode -> replay every edge and all route hard constraints`.

The repaired child passed the graph-feasibility replay. This validates the **mechanism** learned from S045/S042: route optimization must verify the final decoded object, not only the genetic representation.

## Supplementary heterogeneous-similarity check

A synthetic mixed-unit feature vector was also checked. Raw cosine produced >0.999 similarity for both a structurally different and a structurally similar candidate because a very large length coordinate dominated. After declared block scaling, the intended structural candidate separated clearly. This supports the S045 scale-before-similarity gate, but remains a constructed mechanism check.

## Status

`PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX`

This is **not** evidence that v1.38 as a whole outperforms v1.37 or No-Core. A controlled Core ablation needs one fixed agent harness and remains separate.
