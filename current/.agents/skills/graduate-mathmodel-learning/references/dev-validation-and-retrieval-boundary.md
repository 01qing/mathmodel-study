# Dev validation and retrieval boundary

- Ordinary `evaluation` and `production` retrieval may search only pages that are both `split=train` and present in that paper's `reviewed_pages`.
- Dev/Test metadata, hashes, split membership and review-state may be integrity-checked without making their solution content retrievable.
- Dev transfer validation order: freeze Core → problem/data only → independent solution freeze → open Dev solution → gap analysis → generic rule updates only.
- Dev-specific solution details must not be written into Train paper reviews, Train same-problem maps, or ordinary retrieval summaries.
- Test solution content stays unopened until the independent Test answer is frozen.
