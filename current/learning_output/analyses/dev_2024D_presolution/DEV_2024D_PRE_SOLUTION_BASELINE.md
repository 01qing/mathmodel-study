# 2024-D independent baseline — protocol before numerical fitting

Status: PRE_SOLUTION_PROTOCOL_FIXED; independent answer NOT YET FROZEN.
Source: official D problem and six official datasets only. Frozen solver: MathModel-Core v1.38.0. No S013–S016 or Test answers accessed in this run. Historical all-paper prior_exposure was generated as a blanket flag; absolute historical pristine status is unverified.

## Six-hour route and limits
1. Audit input dates, missing values, CRS and aggregation semantics; common 0.5-degree landcover grid. Preserve original archive SHA256 and exact selection lists.
2. Q1: area-weighted annual precipitation mean/time series, spatial trend map, interannual spatial dispersion; cover-type area trajectories, net fraction-change maps, composition-change magnitude. Precipitation 1990–2020, observed landcover 1990–2019; 2020 cannot be supplied as observation. Fraction grids do not identify actual transition matrices.
3. Q2: predict annual maximum daily precipitation (Rx1day), using location, terrain elevation/relief, year and annual temperature. Compare climatology, additive spline Ridge, explicit terrain × temperature interaction Ridge, and shallow histogram gradient boosting. Predictive association only: precipitation product itself uses PRISM terrain adjustment. No causal terrain effect or real-time forecast claim.
4. Q3: a transparent runoff-pressure scenario. Effective storm runoff C(L)·P compared with an explicitly assumed drainage/infiltration capacity K; Pcrit=K/C(L). Vary coefficients and K, never fit disaster thresholds to invented labels. Relative exposure and pressure maps for 2025/2030/2035 with frozen socioeconomics versus explicitly stated extrapolated climate/cover scenarios. No supplied disaster outcomes or drainage network: calibrated disaster probability and validated disaster threshold are NOT_ESTABLISHED.
5. Q4: summarize five cover fractions and their net changes with interpretable low-dimensional PCA and clustering. Compare global mean, K=2/3/4/5 centroid reconstructions using deterministic spatial blocks; choose the smallest K attaining useful improvement. PCA fit on training cells only. Explain stable regions and heterogeneity; do not force a famous dividing line.

## Validation fixed before fitting
Q2 train years 1990–2005, development 2006–2010, final holdout 2011–2018. Tune only on development; retain frozen final results regardless of success. Also use five deterministic 5° spatial block folds (block id = floor(lon/5)+37*floor(lat/5), mod 5). Train-fitted imputation/scaling/bases only. MAE in mm and spatial-fold errors; secondary RMSE. Complex mainline requires >=5% development MAE improvement and improvement in at least 4/5 spatial folds; otherwise prefer simpler route. Do not interpret fold variability as a rigorous confidence interval.
Climate extrapolation evaluated against persistence using historical pseudo-future blocks available before projections. Include a no-trend scenario even if trend improves. Future weather realization is unknown.
Q4 spatial holdout reconstruction RMSE in fraction units and label stability under year-window perturbation; no unsupervised silhouette alone as accuracy truth.

## Contracts and stopping point
All transformations specify cell support, units, year, missing mask and aggregation. Extensive population/GDP are summed conservatively; fractions and climate are averaged. Preserve genuine failed checks and repair history. Run reproducibility replay and manifest checks. Freeze code, parameters, numerical outputs, figures and limitations together; then STOP before opening Dev papers. This is an agent-produced practice solution, not a human competition submission or a No-Core/Previous-Core/New-Core capability experiment.
