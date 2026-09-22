# MathModel-Core v1.29 Validation

## Overall status

**PASS with explicit Dev-only boundary.**

## S029 specialist regression

- `test_v129_dev_regressions.py`: **67/67 PASS**
- verifies pre-solution freeze hash;
- verifies S029 remains Dev-only;
- verifies R2 descriptive ceiling;
- verifies headline metric drift records;
- verifies unlabeled-target and transductive-alignment gates;
- verifies S030/S031 remain unread Dev reserve;
- verifies all Test papers remain unread;
- verifies both ordinary retrieval modes exclude S029 and return only reviewed Train pages.

## Historical Core regressions

22 historical Core regression scripts were rerun after the v1.29 changes:

- v1.6;
- v1.10 through v1.28;
- v1.8 code-learning regression;
- v1.9 training regression.

Result: **22/22 PASS**.

An old v1.8 test was made cwd-independent by resolving the Skill root from `__file__`; the underlying GTeacher code cards were never missing.

## Retrieval regression

Representative learned case-group retrieval tests after the new hard boundary:

- 2024-A: PASS
- 2024-B: PASS
- 2024-C: PASS
- 2024-E: PASS
- 2025-A: PASS
- 2025-E supplemental code-link regression: PASS

A monolithic all-retrieval batch exceeded the execution time limit, so it is not reported as a complete rerun. The representative checks above were run individually.

## Library integrity

`validate_library.py`: PASS

- papers: **45**
- chunks: **6752**
- split: **32 Train / 7 Dev / 6 Test**
- frozen split SHA256 unchanged: `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`
- group isolation: PASS
- chunk/page round-trip: PASS
- review-page bounds: PASS
- train-only reviewed-page retrieval smoke: PASS

## Dev/Test protection

- S029: Dev, intentionally exposed only after baseline freeze; Dev-only evidence.
- S030/S031: Dev reserve, `reviewed_pages=[]`.
- all Test papers: `reviewed_pages=[]`.
- S029-specific solution content is not placed in Train paper reviews, Train Same-Problem Maps or Train retrieval summaries.

## Reproduction / visual status

S029:

- full-text review: complete;
- original PDF visual review: 57/57 pages;
- printed wrapper-code static audit: complete;
- reproduction level: **R2-equivalent Dev evidence**;
- R3+: NOT claimed.

## Next stage

Seal v1.29, keep S030/S031 reserved, resume Train with **S032 / 2025-C**.

