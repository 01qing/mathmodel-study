# 2024 C Learning Route

## L0 Source inventory
Read:
- `assets/cases/2024_C_problem_facts.json`
- `assets/cases/2024_C_case_manifest.json`

Do not read excellent-paper solutions during a claimed fresh blind run.

## Q1 Waveform classification

### First abstraction
Each sample contains a 1024-point waveform plus operating-condition fields.

Do not start with "which classifier?"

Start with:
1. phase/alignment consistency
2. amplitude normalization
3. shape descriptors
4. frequency-domain descriptors
5. class separation visualization

### Candidate model competition
Baseline:
- rule/template correlation using physically meaningful shape features

Classical:
- Logistic / LDA where suitable
- SVM
- Random Forest / ExtraTrees
- boosting

Advanced:
- 1D CNN / sequence representation only if justified by data volume and validation benefit

Validation:
- stratified CV
- confusion matrix
- macro F1 / balanced accuracy
- per-class recall
- robustness to scale/phase if relevant

## Q2 Steinmetz correction

### Baseline
Fit original Steinmetz model on the required material-1 sinusoidal subset.

### Candidate corrections
At least three:
1. coefficient k depends on T
2. multiplicative polynomial temperature factor
3. exponential temperature factor
4. optional temperature-dependent alpha/beta if identifiable

### Validation
Do not rely only on random CV.
Include:
- per-temperature error
- leave-one-temperature-out prediction
- residual-vs-temperature plot
- parameter uncertainty/stability

Reject a more complex correction if it only improves in-sample error.

## Q3 Factor and interaction analysis

Required main effects:
- temperature
- waveform
- material

Required two-way interactions:
- temperature × waveform
- temperature × material
- waveform × material

Control variables:
- frequency
- peak flux density Bm

Do not include a three-way interaction if the question only asks pairwise synergy unless it is a sensitivity analysis.

Report:
- effect estimate
- confidence/robust uncertainty
- effect size
- interaction interpretation
- lowest-loss supported condition

## Q4 General prediction

Feature groups:
- temperature/frequency/material
- waveform class
- Bm
- waveform statistics
- harmonic/spectral features

Target:
- consider log(core loss) because of dynamic range; verify empirically.

Validation regimes:
1. stratified random CV
2. grouped/leave-condition-out diagnostics
3. residuals by material/temperature/waveform

Candidate families:
- Ridge baseline
- ExtraTrees / RF
- HistGradientBoosting
- XGBoost/LightGBM if available
- corrected physics model as an interpretable comparator

## Q5 Multiobjective optimization

Primary output:
- Pareto set/front

Decision variables:
- discrete: material, waveform, possibly temperature levels
- continuous: frequency, Bm

Constraints:
- observed/support domain
- model applicability
- engineering bounds from data/problem statement

Do not output one "best point" without preference assumptions.

## Case completion gate

2024 C is not complete until:
- at least two excellent papers are materialized or otherwise sufficiently readable;
- one public codebase is audited;
- Q2 physics correction is compared with at least one black-box benchmark but remains interpretable;
- Q3 controls operating-condition confounders;
- Q4 evaluates cross-condition generalization;
- Q5 reports Pareto trade-offs.
