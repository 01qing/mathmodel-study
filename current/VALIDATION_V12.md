# v1.2 Validation

## Package

- Skill files: 104
- Python scripts: 26
- Python syntax errors: 0
- JSON parse errors: 0
- Source acquisition manifest version: `1.2`

## Source pipeline

- Remote XLSX metadata: **CONFIRMED**
- Remote participant CSV metadata: **CONFIRMED**
- Small real ADMET CSV text readability through GitHub connector: **CONFIRMED**
- Local acquisition script real-network behavior: **NETWORK_BLOCKED correctly reported**
- Verify-only with matching files: **PASS**
- CSV mirror audit: **PASS_WITH_WARNINGS on synthetic fixture**
- XLSX/CSV semantic cross-check, identical mirror: **CROSSCHECK_PASS**
- XLSX/CSV semantic cross-check, one altered label: **MIRROR_NOT_EQUIVALENT**
- CSV benchmark permission denied on mismatch: **PASS**

## Real-case status

- Case status: `V1_2_SOURCE_PIPELINE_READY_REAL_DATA_MATERIALIZATION_PENDING`
- Full real XLSX local materialization: **NOT_RUN**
- Full real participant CSV local materialization: **NOT_RUN**
- Real XLSX-vs-CSV cross-check: **NOT_RUN**
- Real Data Audit: **NOT_RUN**
- Fresh Blind Eval: **NOT_RUN**
- Real Standard Benchmark: **NOT_RUN**

## Interpretation

v1.2 closes the gap between “a remote file exists” and “the file is a trusted modeling input.”
The participant CSV can only replace the contest-attachment XLSX after hash verification, independent audits and semantic cross-check.
