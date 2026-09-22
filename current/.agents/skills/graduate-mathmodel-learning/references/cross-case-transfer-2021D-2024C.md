# Cross-Case Transfer: 2021 D -> 2024 C

## Why a second case is necessary

2021 D mainly tests:
- high-dimensional tabular feature selection
- regression
- binary classification
- constrained optimization

2024 C adds structures that 2021 D does not adequately test:
- waveform/time-series shape representation
- classical physics equation calibration
- interpretable model correction
- factor interaction analysis
- mixed discrete/continuous engineering optimization

The purpose is not to collect another answer. It is to test whether the Skill can recognize a different mathematical structure and change its modeling behavior.

---

## Transfer rule 1: do not reuse "tabular ML first"

### 2021 D
A table-oriented pipeline is natural.

### 2024 C Q1
1024 magnetic-flux samples represent one waveform.

The first question is:

> What representation preserves waveform shape?

Candidate representations include:
- time-domain shape features
- slope / turning-point features
- Fourier harmonic ratios
- normalized waveform correlation/templates
- wavelet features
- raw-sequence models as an advanced alternative

Do not immediately treat 1024 positions as unrelated independent features.

---

## Transfer rule 2: Q2 is physics-model extension, not generic regression

Steinmetz baseline:

`P = k * f^alpha * Bm^beta`

The modeling question is:
- how temperature changes the relation,
- what functional correction is identifiable,
- whether the correction generalizes across temperature.

Candidate temperature terms:
- multiplicative polynomial
- exponential correction
- temperature-dependent k
- temperature-dependent exponents
- hierarchical / partially pooled parameters

Every added degree of freedom needs:
- physical or empirical rationale
- identifiability check
- out-of-temperature validation

A black-box model can be a benchmark but cannot replace the required Steinmetz correction explanation.

---

## Transfer rule 3: Q3 requires conditional effects

Raw loss depends strongly on:
- frequency
- peak flux density

Therefore simply comparing average losses across:
- temperatures
- waveforms
- materials

can confound the factors with operating conditions.

Preferred structure:
- transform loss if needed (often log loss)
- control frequency and Bm
- include main effects
- include only requested two-way interactions
- use robust inference where heteroscedasticity exists
- report effect size, not only p-value
- validate factor ranking with a predictive/perturbation method if useful

Possible frameworks:
- ANCOVA / regression with categorical interactions
- generalized additive / semiparametric effects
- mixed/hierarchical model if grouping structure requires it

---

## Transfer rule 4: Q4 generalization must match engineering deployment

Random K-fold can mix nearly identical operating regimes across folds.

The Skill should compare:
- random CV
- stratified CV by material/waveform/temperature
- leave-one-temperature-out
- leave-one-material-out if scientifically meaningful
- distribution shift diagnostics

Model candidates:
- physics baseline / corrected Steinmetz
- Ridge/ElasticNet on engineered features
- Random Forest / ExtraTrees
- HistGradientBoosting / XGBoost/LightGBM where available

The winner is conditional on the validation regime.

---

## Transfer rule 5: Q5 is multiobjective, not "run PSO"

Objectives:
- minimize predicted core loss
- maximize `f * Bm`

Before selecting an optimizer:
1. define feasible domains;
2. preserve discrete variables:
   - temperature levels if restricted
   - waveform category
   - material category
3. define continuous ranges:
   - frequency
   - Bm
4. prevent surrogate extrapolation outside the supported region;
5. produce Pareto trade-offs.

Weighted sum may be shown as one preference selection method, but not as the only definition of optimality.

---

## What should transfer from 2021 D

Good habits that transfer:
- test isolation
- fit preprocessing only on training folds
- model comparison under identical validation
- practical ties
- explicit switch conditions
- source/evidence governance
- code audit

What should not transfer mechanically:
- Top20 feature-selection workflow
- five independent binary classifiers
- pIC50-specific transformations
- descriptor-space feasibility logic
