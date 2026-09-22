# v1.2 Source Pipeline Smoke Test

## Acquisition verification

- Synthetic verified files: **10/10 PASS**
- `acquire_2021_D_sources.py --verify-only`: **READY_FOR_AUDIT**
- `verify_2021_D_sources.py`: **PASS**
- Git blob SHA algorithm exercised: **PASS**

## CSV audit

- CSV mirror audit execution: **PASS_WITH_WARNINGS**
- Expected warnings are present because the synthetic case has 4 train rows, 2 test rows and 3 descriptors instead of 1974/50/729.

## XLSX-vs-CSV cross-check

Matched mirror:
- status: **CROSSCHECK_PASS**
- CSV benchmark permission: `True`

Deliberately changed one `Caco-2` value in CSV:
- status: **MIRROR_NOT_EQUIVALENT**
- mismatches detected: **1**
- CSV benchmark permission: `False`

This confirms that a participant CSV is not silently trusted.

## Current-runtime network probe

A real acquisition attempt against the manifest returned:

`NETWORK_BLOCKED`

The captured reason is DNS/name-resolution failure in the container, not a missing GitHub source.

## Spreadsheet smoke note

The current spreadsheet RPC daemon was unavailable during this turn, so the mirror cross-check reused the already-created synthetic XLSX fixtures from the earlier v0.8 spreadsheet smoke test. No real-data claim depends on this fixture.
