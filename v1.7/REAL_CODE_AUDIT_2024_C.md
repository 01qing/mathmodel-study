# 2024 C Real Public Code Audit

Repository: `Tereaslle/2024-CPGMCM`

## Q1 Waveform classification

### Strength
The implementation explicitly derives waveform-level statistics:
- mean
- standard deviation
- max/min
- amplitude
- energy
- skewness
- kurtosis

and uses Random Forest classification.

### Risks
1. The feature dataframe is mutated sequentially. Later statistics are computed after earlier derived columns have already been appended, so they are not all pure functions of the original 1024 waveform samples.
2. Random 70/30 holdout reports perfect accuracy. This may mean the classes are easy, but does not establish cross-material/cross-temperature/cross-frequency robustness.
3. Notebook history contains an execution error due to mixed integer/string column names before later successful outputs; clean rerun is still needed.

## Q2 Steinmetz temperature correction

### Strength
The final notebook preserves an interpretable Steinmetz-style equation:

`P = k f^alpha Bm^beta log(T)^gamma`

rather than replacing the task with a generic black-box predictor.

### Risks
1. Temperature functional form is first selected from marginal `P vs T` fits. Since P also depends strongly on frequency and Bm, this can be confounded.
2. The inspected comparison evaluates fitted original/corrected equations on the same data used for fitting.
3. Bm is row-wise maximum; the physical definition should be checked against max-absolute or half peak-to-peak conventions.

## Q3 Factor interactions

Repository artifacts prove the authors produced:
- causal-model figure
- correlation/P-value figures
- material/waveform comparison figures

but the notebook content was not readable through the current connector. Therefore:
- frequency/Bm adjustment: unresolved
- two-way interaction implementation: unresolved
- effect-size reporting: unresolved

Do not infer these from image names.

## Q4 Prediction

### Strength
A physics-informed hybrid is used:
- temperature-corrected Steinmetz
- loss-separation model
- material × waveform specific parameters

### Risks
1. Missing physical quantities are collapsed into free calibration parameters, so predictive fit does not imply physical identifiability.
2. The inspected code sections do not show a declared group/random/out-of-condition validation protocol adequate for the question's generalization requirement.

## Q5 Optimization

### Strength
Material and waveform are explicitly enumerated as discrete groups.

### Critical issue
Verified objective:

```python
def objective_function(x):
    return a*steinmetz_eq_adjust(x) + b*separate(x)
```

This minimizes predicted core loss only.

The required second objective:

`maximize f * Bm`

is absent from the verified objective.

Therefore the implemented PSO does **not** solve the stated bi-objective problem.

### Additional risks
- Search uses a global min-max box only; sparse unsupported combinations remain possible.
- Markdown says genetic algorithm while executable code uses PSO.

## Learning conclusion

This repository is useful precisely because it contains both good ideas and important implementation gaps.

The Skill should learn:
- preserve physics-aware models,
- engineer waveform representations,
- validate under the deployment structure,
- distinguish calibration from physical identification,
- encode every stated optimization objective explicitly.
