# Final Fit And Test Prediction Protocol

## Purpose

After the leakage-safe benchmark has frozen the recommended model family, fit final models on all training compounds and predict the official test compounds.

This stage must not reopen model selection using the test set.

## Preconditions

Required:
1. data audit = `PASS` or `PASS_WITH_WARNINGS`
2. model benchmark contract exists and validates
3. recommended Q2 pipeline exists
4. each usable Q3 label has a recommended pipeline
5. official test rows were not used in benchmark

## Q1/Q2 final fitting

Use the benchmark-recommended:
- selector family
- regressor family

Then perform one final training-only CV on all training rows to choose hyperparameters.

Pipeline order remains:

`imputer -> scaler -> selector -> regressor`

After fitting:
- save final selected features
- save selector/model hyperparameters
- predict pIC50 for test
- convert to IC50_nM using `10^(9-pIC50)`

Do not use test predictions to revise the model.

## Q3 final fitting

For each ADMET label:
- use its benchmark-recommended feature mode and classifier
- tune only on training data
- fit all available labeled training rows
- predict class for test
- save probability when available

Different labels may use different models.

## Prediction contracts

Outputs:

```text
learning_output/final_fit/gmcm-2021-D/
├── final_fit.json
├── q2_test_predictions.csv
├── q3_test_predictions.csv
└── final_fit.md
```

The JSON must record:
- benchmark source
- frozen route
- best hyperparameters
- final selected descriptors
- test isolation statement
- pIC50/IC50 predictions
- five ADMET predictions/probabilities

## Critical rules

1. Do not call the test set a validation set.
2. Do not select the final model by inspecting test predictions.
3. Do not compare test predictions against hidden answers unless an official answer source exists and is explicitly introduced later.
4. Final-fit predictions are model outputs, not proof that the model is scientifically correct.
