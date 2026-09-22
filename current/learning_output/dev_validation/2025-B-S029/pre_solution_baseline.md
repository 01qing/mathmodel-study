# S029 / 2025-B Dev — Pre-solution MathModel-Core Baseline Freeze

## Protocol

- Split: Dev.
- This document was frozen **before opening S029 excellent-paper solution, figures, code, parameter choices or conclusions**.
- Evidence used: public 2025-B problem description/mirror and metadata only.
- Purpose: evaluate whether MathModel-Core can independently decompose the task, choose models, reject unsuitable models, design validation and figures, then compare against Dev solution.
- This is Dev evidence, not Train evidence.

## Problem-only understanding

2025-B concerns MIMO-OFDM link-rate estimation from measured channel state information (CSI), with conventional physical-layer abstraction and TxBF/no-TxBF conditions. Public problem descriptions indicate three main tasks:

1. Fit/use an EESM-style model on complete dataset A to estimate actual link rate in a no-TxBF setting.
2. Build a new rate-estimation model for no-TxBF that may go beyond one-dimensional equivalent-SINR compression.
3. Build a model for TxBF-enabled conditions, where SVD/beamforming changes the effective channel.

The public descriptions indicate high-dimensional CSI per sample (reported as MIMO channel matrices across roughly 122 subcarriers), noise information, measured link rate, terminal/time/location-like acquisition metadata, and separate complete/validation data.

## Independent-sample unit and split rule

The **independent unit is not a CSI scalar/subcarrier row**. It is one measurement episode/sample associated with a terminal/position/time capture, containing the whole subcarrier-by-antenna CSI tensor plus metadata and one rate label.

Validation priority:

1. group/trajectory/location/terminal holdout when identifiers permit;
2. chronological block holdout within terminal trajectory;
3. only use random row split as a diagnostic, never as sole generalization evidence.

All fitted preprocessing (scalers, PCA, encoders, monotonic calibration) must be trained only on training folds.

## Q1 Candidate Model Competition

### 6-hour Baseline

**EESM + monotonic rate calibration**.

1. Parse complex CSI tensor and noise power.
2. Compute physically meaningful per-subcarrier post-detection SNR/SINR proxy using one explicitly declared receiver assumption.
3. Compress subcarrier quality with EESM using a small beta grid/1-D optimizer.
4. Map effective SINR to measured rate with isotonic regression or a small monotonic lookup/calibrator.
5. Evaluate grouped MAE/RMSE/R² plus error ECDF and worst-group error.

Why: transparent, physically interpretable, cheap, directly aligned with the stated baseline model.

### Main alternatives

- MIESM / mutual-information effective SNR: preferable if modulation/coding information is reliable and EESM residuals are strongly MCS-dependent.
- Logistic/ordinal mapping to MCS then table-rate conversion: preferable if observed rates are discrete MCS-derived plateaus.
- LightGBM/XGBoost on EESM + a few physical features: use only if it materially and stably improves grouped holdout over EESM calibration.

### Not recommended by default

- LSTM/RNN: no evidence that the required prediction target is inherently a long temporal sequence; individual samples already contain a frequency axis.
- large CNN/Transformer directly on CSI: data scale/generalization must justify it; otherwise overparameterized relative to tree/physics baselines.

## Q2 Candidate Model Competition

### 6-hour Baseline

**Physics-informed gradient boosting** on compact CSI features:

- EESM effective SINR;
- mean/std/quantiles/min of per-subcarrier SINR;
- outage fraction below thresholds;
- singular-value summaries per subcarrier;
- effective rank / condition-number summaries;
- receive/transmit antenna correlation summaries;
- noise level and permitted acquisition metadata.

Use LightGBM/XGBoost or HistGradientBoosting; grouped holdout; compare directly against Q1 EESM.

### Alternatives

- Random Forest / ExtraTrees: robust simple nonlinear baseline, good for feature-importance stability checks.
- small MLP: only if sample count is large after grouping and tree models saturate.
- 1-D CNN over subcarrier feature sequences: use only when frequency-local structure adds stable held-out gain.
- complex-valued NN: high-risk route; require much more data and stronger reproducibility.

### Abandon condition

If the learned model does not give stable, material grouped-holdout gain over EESM across terminals/locations, keep EESM or a small residual correction rather than the black-box model.

## Q3 Candidate Model Competition

### 6-hour Baseline

**SVD-derived TxBF physical features + the same calibrated/tree framework**.

For each subcarrier H_k:

- compute singular values;
- derive dominant-mode and/or multi-stream effective gain under an explicit beamforming/receiver assumption;
- summarize post-BF SNR/SINR, singular-value ratios, effective rank, condition number, gain relative to no-TxBF;
- apply EESM or grouped tree model.

### Alternatives

- capacity-inspired log-det feature / effective mutual information;
- per-stream EESM before aggregation;
- small 1-D CNN on singular-value/SINR sequences if frequency structure yields reproducible grouped gain.

### Not recommended by default

Directly feeding raw complex 2×4×K tensors into a deep network before establishing the SVD/EESM/tree baselines.

## Result Registry before Dev solution

Primary metrics:

- MAE, RMSE, R²;
- median/P90/P95 absolute and relative error;
- error ECDF;
- worst terminal/location/trajectory group metrics;
- calibration monotonicity vs effective SNR;
- runtime / parameter count for contest practicality.

If target rate contains zeros or near-zero values, MAPE is not a primary metric.

Consistency gates:

- RMSE² = MSE;
- RMSE >= MAE is not universally required, but RMSE should normally be >= MAE for the same errors;
- all headline metrics generated from one prediction registry keyed by sample id;
- no target-derived feature leakage;
- no whole-dataset scaler/PCA fitting;
- repeated samples from the same measurement episode cannot cross folds.

## Figure Decision Rules before Dev solution

Core figures expected:

1. rate/label distribution by scenario and TxBF state;
2. per-subcarrier SINR/CSI summary for representative samples;
3. EESM effective-SINR vs actual rate + monotonic calibration;
4. prediction-vs-actual scatter with grouped train/dev distinction;
5. error ECDF and worst-group bars;
6. residual vs effective SINR / rate / scenario;
7. Q2/Q3 feature-ablation chart showing whether extra physics features actually add value;
8. if using frequency-sequence model, ablation against a non-sequential model.

A correlation/SHAP/feature-importance plot can explain predictive association but cannot prove causality.

## Frozen independent recommendation

Start with a **physics-first EESM/SVD baseline plus monotonic calibration**, then allow compact tree models to learn residual structure. Deep sequence/complex models are promoted only after grouped independent validation shows stable, material improvement. Preserve the measurement episode as the atomic split unit and evaluate worst-group behavior, not only pooled random-split accuracy.

## Sources used before solution opening

- Public GitHub repository containing `B题.pdf` and original attachments, but **not** its `我的论文.pdf` solution: https://github.com/LongAoTianxia/Mathematical_modeling-2025B
- Public problem mirror describing MIMO-OFDM link-rate modeling and data acquisition: https://www.nsuidc.com/news/35_75501.html
- Public overview confirming the three task families (EESM / no-TxBF new model / TxBF model): https://damodev.csdn.net/6a431e77662f9a54cb85f4dc.html
