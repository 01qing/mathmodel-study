# Frozen independent solution

Status: INDEPENDENT_SOLUTION_FROZEN. This is the v1.39 pre-solution milestone, NOT a newly sealed Core version. Core VERSION remains1.38.0 intentionally. Read DEV_2024D_INDEPENDENT_SOLUTION.md and DEV_2024D_FREEZE_MANIFEST.json first. Do not reopen old handoff as latest status.

Reproduce prepared-array analysis: run solve_independent.py, then repair_figures.py and verify_independent.py from a COPY. Reports via write_reports.py; do not overwrite frozen originals. Full raw preparation: place selected raw datasets under root official-data/dataset1..6 and run prepare_features.py; external six RARs and exact hashes are in original-inputs/RAW_INPUT_MANIFEST.json. These large inputs are not inside the distribution ZIP. Source paths in the manifest refer to this PC; adjust on another machine with provenance notes.

The full workspace package preserves the original Core byte-for-byte, including quarantined libraries. Do not search unfiltered Dev/Test content. Freeze is an integrity checkpoint, not proof of scientific completeness. No S013 access until the user next directs the Dev comparison.
