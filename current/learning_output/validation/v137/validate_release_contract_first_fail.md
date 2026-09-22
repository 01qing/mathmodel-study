# v1.37 release-contract first FAIL

The first run failed inside the new release validator because it assumed `papers.json` had a top-level `{papers:[...]}` object, while the current library asset is a top-level list. This is a validator implementation bug, not a release-contract failure. The parser was corrected to accept the actual list shape; no release requirement was removed.
