# S029 / 2025-B Dev — Post-solution Gap Analysis

## Protocol

- Split: **Dev**.
- The problem-only baseline was frozen **before** opening the excellent paper.
- Frozen baseline SHA256: `f0c9a3e4878c8b16272b8e9c1634e08008aa4c712b3cf1fe3fe9090cafc8341e`.
- This document is **development validation**, not Train evidence.
- S029-specific methods/results must not be injected into Train retrieval; only generic rule/workflow corrections may update MathModel-Core.

## Independent Core prediction vs Dev paper

The frozen Core independently selected a physics-first route: EESM + monotonic calibration for Q1, compact physics-informed competition including MIESM for Q2, and SVD-derived TxBF features for Q3. After opening S029, these choices were found to align strongly with the paper's main route. This is positive Dev evidence that the Core is selecting a plausible model family rather than merely memorizing a Train paper.

## Most important Dev corrections

1. **Random row split is not an independence guarantee.** The paper states that random 80/20 row holdout with stable device proportions avoids time leakage. It does not: adjacent observations from the same device/trajectory/location can cross folds. Prefer device/trajectory/location/file/time-block holdout and retain row holdout only as a diagnostic.
2. **Unlabeled target alignment cannot prove prediction accuracy.** TxBF/valid is unlabeled. Median/IQR alignment can show distributional consistency, not closeness to true rates.
3. **Target-batch statistics make the method transductive.** DA/DAiqr uses target-domain median/IQR. Deployment must state whether a target batch/window is available and how statistics are updated online.
4. **Headline metrics need provenance.** Q2 abstract claims Spearman 0.82, but Fig. 5.11 visibly tops out near 0.792. Q3 abstract means also differ materially from the body result section.
5. **A significance plan is not a significance result.** The paper says to report paired t-test/Wilcoxon p-values, but no p-value was found in the visible report.
6. **Appendix wrappers are not a self-contained implementation.** `quick_run*.py` imports omitted `linkrate_baseline` core modules; split/model internals cannot be verified from the printed appendix alone.

## What should change in MathModel-Core

- Add a group-independence gate: preserving device proportions is not equivalent to holding out devices/trajectories/time blocks.
- Add an unlabeled-target evidence taxonomy: distribution shift correction ≠ accuracy improvement.
- Add a transductive/inductive deployment contract for any method using target-batch statistics.
- Extend Result Registry to compare abstract/body/table/figure/code headline numbers.
- Require statistical tests to have actual statistic/p-value/effect-size output, not only a planned method paragraph.
- Require appendix self-containedness before a Dev/Train paper can move beyond static audit.

## What should NOT change

- Keep baseline-first model selection.
- Keep physics-first EESM/SVD features as a preferred starting point for MIMO-OFDM rate mapping.
- Keep the rule that deep raw-CSI networks need independent evidence over compact models.
- Keep train-only preprocessing, worst-group metrics, ECDF/error quantiles, and explicit failure conditions.

## Dev evidence level

S029 has full-text and full original-PDF visual review plus printed appendix static audit, which is **R2-equivalent descriptive evidence**. Because it is Dev, this does **not** become Train method evidence. R3 is not claimed because algorithm-defining imported modules are absent and no code execution was performed.
