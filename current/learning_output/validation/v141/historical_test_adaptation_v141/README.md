# Historical test adaptation v1.41

Untouched historical/recent regression scripts were run first. First failures are preserved under `learning_output/validation/v141/historical_original/` and `recent_original/`.

The affected scripts failed on legal-timepoint assumptions only: S013-S016 were required to remain unread, version sets stopped at v1.38, or `next_learning.md` was required to point to 2025-F. v1.41 legally follows the frozen 2024-D independent solution and completes S013-S016 Dev review.

Adaptations therefore only widen version/latest/next-pointer or Dev lifecycle assertions. Paper-specific formulas, code findings, result registry assertions, Train split, and Test unread protections were not relaxed. Original byte snapshots and SHA256 values are stored in this directory.

This adaptation is regression-harness maintenance, not evidence of capability gain.
