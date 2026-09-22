# P1 2022-C COMMON FROZEN CONTRACT

Experiment ID: `ROLE-P1-2022C-v0.2`
Status: `REGISTERED / NOT_RUN`
Core: `MathModel-Core v1.41.0 SEALED / READ-ONLY`
Controlled Core Ablation: `NOT_RUN`
2025-D Test: untouched
2022-D: separate completed smoke fixture

## Isolation

Run A, Run B, and Blind Evaluator C must be executed in three fresh, separate chats.
A must never receive B output or B role prompt.
B must never receive A output or A prompt.
C starts only after A and B are frozen and receives anonymous X/Y bundles only.

## Shared runtime contract

- model/config: GPT-5.6 Sol / High
- max tool calls per condition: 40
- target wall-clock ceiling: 60 minutes
- input: attached official files + sealed v1.41 Core
- after run starts: no external web / Notion / GitHub solution search
- no answer/reference/excellent-paper retrieval
- user provides no modeling hints during a condition; bare `继续` is allowed only for technical continuation
- first complete frozen bundle or hard budget ceiling ends the condition
- same stopping semantics for A and B

## Required outputs

Each condition freezes:
- problem contract
- subproblem map
- Candidate Model Competition
- 6-hour robust baseline
- chosen mainline
- assumptions and data contract
- mathematical contract
- implementation/code where feasible
- validation design
- only actually reproduced headline results
- Result Registry
- unresolved risks
- execution/failure log

## Evaluation rubric

0-3 points each, evidence required:
1. problem-contract correctness
2. model-selection justification
3. six-hour baseline quality
4. assumption/constraint correctness
5. leakage prevention
6. mathematical validity
7. implementation feasibility
8. validation design
9. evidence provenance
10. error detection
11. repair quality
12. reproducibility

## Hard failures

- answer/reference contamination before blind freeze
- silent formula/code repair before first-fail is recorded
- fabricated execution/result
- test leakage
- unsupported optimum/best claim
- headline result without provenance
- model label inconsistent with actual primitive/code
- Core version substitution or mutation

## Claim gate

After a single clean paired benchmark, the strongest allowed conclusion is:

`ROLE_SPECIALIZATION_PILOT_EVIDENCE_{POSITIVE|NEUTRAL|MIXED|NEGATIVE}`

Do not claim `ROLE_SPECIALIZATION_IMPROVES_CAPABILITY` from one fixture.
