# ROLE-P1-2022C-v0.2 — Execution / Failure Log

Status: `FROZEN`

| Stage | Event | Classification | Resolution |
|---|---|---|---|
| Identity gate | `release-v141.zip` SHA-256 matched required wrapper hash | PASS | Continued |
| Source gate | Five official files matched frozen size + Git-blob identity | PASS | Continued |
| Pass 1 simulation | Four selected schedules completed and were frozen | PASS | Preserved in `frozen_runs.pkl` |
| Candidate search | A broad return-lane search exceeded the execution window | Non-fatal execution limitation | Narrowed to staged deterministic candidate competition before freeze; selected headline schedules use zero returns |
| Spreadsheet export attempt | Large fully static workbook export through `artifact_tool` timed out / transport failed | First technical export failure | Original compact formula workbooks retained |
| Spreadsheet portability audit | Independent spreadsheet engine evaluated `Sheet1!B2` as `#VALUE!` for all four dynamic-formula XLSX files | **Pass-2 first material fail** | Single repair: static canonical matrices emitted as gzip CSV plus logs/sequences; XLSX portability downgraded to `NOT_VERIFIED` |
| Formula audit | Literal `S4` exceeded 100 for result12/result21 | Specification ambiguity, not silent code repair | Literal results preserved; capped-at-100 sensitivity added |
| Matrix semantic audit | Same-second duplicate parking codes observed at a few event boundaries | Warning | Event-level kinematic reconstruction used as authoritative collision check; ambiguity retained in claim limits |
| Event/score validation | Independent validator completed on all four frozen schedules | PASS | 0 hard failures |

## Stopping semantics

After the single Pass-3 provenance/portability repair, no second repair or model-search cycle was run. This satisfies the benchmark's one-repair ceiling.
