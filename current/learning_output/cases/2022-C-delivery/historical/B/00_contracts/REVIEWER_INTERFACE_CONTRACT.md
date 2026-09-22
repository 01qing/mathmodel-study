# Reviewer Interface Contract v0.1

Mission: independently audit an already frozen mathematical-modeling artifact using MathModel-Core v1.41 read-only.

Freeze requirement before review:
- reviewed artifact/version
- source problem/data version
- existing code/figures/logs
- exposure boundary
No final PASS before artifact freeze.

Mandatory Reviewer Audit Record:
- reviewed_version
- scope
- first_fail: earliest material failure, recorded before repair
- formula_findings
- code_findings: actual primitives, solver identity, objective/constraint replay
- data_eval_findings: split, leakage, same-target, reference-vs-truth
- result_registry: headline provenance/recalculation status
- reproduction_level: R0-R7; no upgrade without evidence
- transferable_modules
- rejected_modules
- retest_plan
- decision: PASS / HOLD / FAIL
- pass_scope: exactly what the PASS proves

First-fail record must preserve severity, location, original claim, evidence, failure class, downstream consequence, minimal repair, retest required.
Do not silently repair formulas/code before recording the failure.

Required audit gates include constant-objective/conservation identity, denominator/domain, threshold exhaustiveness, monotonic direction, parameter drift, body-vs-code optimizer identity, objective/constraint replay, row-vs-column semantics, seed/hyperparameter provenance, post-decision leakage, same-target tuning/evaluation, reference agreement vs independent truth, and Result Registry consistency.

PASS must be scoped; no unqualified PASS.
