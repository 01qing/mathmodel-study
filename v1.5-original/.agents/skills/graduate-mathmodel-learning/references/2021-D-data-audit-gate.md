# 2021 D Data Audit Gate

## Purpose

Before any formal model competition, verify what the Excel files actually contain.

This gate checks:
- required files;
- train/test sheets and dimensions;
- cross-file SMILES alignment;
- IC50 ↔ pIC50 consistency;
- descriptor missing/constant/non-numeric columns;
- five ADMET label distributions;
- strict isolation of the 50-row test set.

## Required files

- `ERα_activity.xlsx`
- `Molecular_Descriptor.xlsx`
- `ADMET.xlsx`
- `分子描述符含义解释.xlsx`

## Hard rules

1. If train SMILES sets conflict across files, status is `BLOCKED`.
2. If order differs but sets match, reindex by SMILES and record a warning.
3. If IC50 is in nM, verify `pIC50 = 9 - log10(IC50_nM)`.
4. Feature selection, scaling, resampling and threshold selection must occur inside training folds.
5. The 50 test compounds are for final prediction only.
6. Do not replace actual-data statistics with problem-statement numbers.
7. Q4 favorable directions:
   - Caco-2: 1
   - HOB: 1
   - hERG: 0
   - MN: 0
   - CYP3A4: not silently assumed; explicit convention/sensitivity analysis required.

## Status

- `PASS`
- `PASS_WITH_WARNINGS`
- `BLOCKED`
