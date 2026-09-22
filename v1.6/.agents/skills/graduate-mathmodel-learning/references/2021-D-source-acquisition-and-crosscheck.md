# 2021 D Source Acquisition And Cross-Check

## Source roles

### Primary XLSX mirror
Repository: `zhanwen/MathModel`

Role:
`contest_attachment_mirror`

This is a public mirror of the contest attachments. It is **not** labeled as the official contest host.

### Participant CSV mirror
Repository: `Bureaux-Tao/modeling2021-D`

Role:
`participant_converted_mirror`

These CSV files are useful because they are plain-text and directly consumed by public participant code, but they are not automatically assumed to be byte/semantic equivalents of the XLSX files.

## Acquisition contract

The manifest stores for each file:
- repository
- ref
- repository path
- expected byte size
- Git blob SHA-1

Git blob SHA-1 is checked as:

`SHA1(b"blob " + str(len(content)) + b"\0" + content)`

This is **not** the same as ordinary file SHA-1.

## Preferred real-run order

1. acquire primary XLSX mirror
2. verify byte size + Git blob SHA
3. run XLSX data audit
4. optionally acquire participant CSV mirror
5. run CSV-mirror data audit
6. cross-check XLSX vs CSV:
   - train/test row counts
   - SMILES sets and order
   - descriptor column names
   - pIC50 / IC50 values
   - ADMET labels
   - descriptor numeric values within tolerance
7. only after cross-check passes may CSV replace XLSX as benchmark input

## Failure states

- `NETWORK_BLOCKED`: acquisition could not access source
- `HASH_MISMATCH`: downloaded bytes differ from manifest
- `MISSING`: required file absent
- `MIRROR_NOT_EQUIVALENT`: CSV differs materially from XLSX
- `READY_FOR_AUDIT`: files verified but data audit not yet run
- `CROSSCHECK_PASS`: mirrors are semantically equivalent within declared tolerance

## Important

A source existing on GitHub is not the same as that source being materialized and audited locally.

Never convert:
`remote metadata confirmed`
into:
`real data audit PASS`.
