# ROLE-P1-2022C-v0.2 — Validation Summary

Final validation status: **PASS with explicit deliverable/semantic limitations**.

- Core identity gate: PASS
- Official five-source identity: PASS
- Four run-object integrity checks: PASS
- Source-attribute preservation: PASS
- Region-code validity: PASS
- Painted-body input-order preservation: PASS
- Transverse-machine timing/non-overlap: PASS
- Incoming-lane FIFO: PASS
- Mandatory lane-motion reconstruction: PASS
- Constraint 8: PASS
- Q1 priority constraint 7: PASS
- Q1 priority constraint 6: vacuous because return lane unused
- Completion-time consistency: PASS
- Output/log order consistency: PASS
- Independent score recomputation: PASS
- Hard failures: **0**

Warnings/limitations:

1. literal time score >100 on result12/result21;
2. same-second sampled parking-code duplicates at a few event boundaries despite valid event-level kinematics;
3. dynamic-formula XLSX portability is `NOT_VERIFIED` (`#VALUE!` observed in independent engine);
4. original search-source reproducibility is incomplete.

Canonical final status string:

`RUN_A_FINAL_FROZEN / EVENT_AND_SCORE_VALIDATION_PASS / 0_HARD_FAILURES / XLSX_PORTABILITY_LIMITED / CLAIM_LIMITS_APPLY`
