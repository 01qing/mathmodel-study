# Architect Interface Contract v0.1

Mission: transform an unseen modeling problem into an implementable, verifiable, writable architecture using MathModel-Core v1.41 read-only.

Mandatory Architect Decision Record:
- artifact_id
- problem_contract: objective, sample unit, inputs, outputs, hard constraints, evaluation object
- subproblem_map: essence, dependencies, data dependencies, uncertainty
- candidate_model_competition: Baseline / Preferred / Serious Alternative / Not recommended now
- baseline_6h
- data_contract: features, units, missingness, split unit, leakage risk
- mathematical_contract: variables, assumptions, objective, constraints, identities, boundary cases
- validation_protocol: metrics, held-out, sensitivity, failure standard
- implementation_map: modules, data structures, solver/model primitives, minimum tests
- switch_conditions
- abandon_conditions
- evidence_plan for every headline result
- risks

Candidate Model Competition must state fit, extra assumptions, implementation cost, validation evidence, switch conditions and abandon conditions.

Hard gates:
- check whether objective is fixed by hard constraints before optimization
- no post-decision/post-review feature may support prospective decision
- same-target tuning/evaluation must be labeled in-sample
- reference-ranking agreement is not latent truth
- algorithm labels must be reduced to actual primitives
- Architect cannot issue Reviewer PASS
