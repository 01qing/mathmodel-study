# Case Knowledge Extraction Protocol

A case is not complete when predictions are produced.

After comparison/review, extract reusable knowledge into:

```text
knowledge_base/
├── methods/
├── problem_patterns/
├── paper_reviews/
├── competition_lessons/
└── error_patterns/
```

## Store a method card only when

At least one is true:
- method principle has reliable external support;
- method has been actually run in this case;
- method is explicitly stored as an unverified paper approach.

A method card must include:
- suitable structure
- unsuitable structure
- assumptions
- data requirements
- baseline
- alternatives
- switch conditions
- validation
- failure patterns
- learned examples

## Store a problem-pattern card when

The insight is broader than this case.

For 2021 D likely patterns:
- supervised high-dimensional feature selection
- small-sample tabular QSAR regression
- several related but non-identical binary tasks
- surrogate optimization under feasibility constraints

## Store an error pattern when

The mistake is reusable, e.g.:
- full-data feature selection before CV
- SMOTE before CV
- Accuracy-only evaluation under imbalance
- treating all binary label value 1 as favorable
- unconstrained descriptor optimization interpreted as realizable molecule

## Mastery update

Reading the case cannot by itself produce:
`can_apply_independently`.

Require practice evidence.
