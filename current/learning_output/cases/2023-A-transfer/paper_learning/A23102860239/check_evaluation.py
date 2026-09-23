"""Audit printed error claims and enrich existing results; no simulation reruns."""
from pathlib import Path
import json, math, statistics, hashlib

HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
ROOT=HERE.parents[4]


def normalized_error(reference, estimate):
    return ((estimate-reference)/reference)**2


def main():
    registry=json.loads((CASE/'PAPER_MARKDOWN_REGISTRY.json').read_text(encoding='utf-8'))
    paper=next(x for x in registry['papers'] if x['paper_id']=='A23102860239')
    hashes={}
    for kind in ('markdown','raw_layout'):
        path=ROOT/paper[kind+'_repo_path']
        value=hashlib.sha256(path.read_bytes()).hexdigest()
        assert value==paper[kind+'_sha256']
        hashes[kind]=value
    # NMSE formula is not visible in conversion. Evaluate an explicitly stated
    # candidate definition, inferred from Q1's printed MSE / theory^2.
    reported=[('Q1 throughput',67.174340,65.351722,.000912),
              ('Q1 collision',.104621,.108623,.002467),
              ('Q2 throughput',70.5586,68.9944,.000514),
              ('Q3 throughput p44',54.5733,54.7118,1.417e-7),
              ('Q3 collision p44',.296356,.271731,.0069),
              ('Q4 throughput p55',102.572708,103.236599,1.417e-7)]
    audit=[]
    for name,theory,simulation,nmse in reported:
        point=normalized_error(theory,simulation)
        audit.append(dict(name=name,theory=theory,simulation=simulation,
          signed_relative_error_percent=100*(simulation/theory-1),
          point_squared_relative_error=point,reported_nmse=nmse,
          point_error_divided_by_reported=point/nmse,
          violates_mean_sample_lower_bound_if_same_sample_mean=point>nmse*1.002))
    # Jensen: mean((Xi-a)^2)/a^2 >= ((mean(X)-a)/a)^2.
    values=[53.,54.,55.,56.];a=54.5733
    sample_nmse=statistics.mean((x-a)**2 for x in values)/a**2
    decomposition=normalized_error(a,statistics.mean(values))+statistics.pvariance(values)/a**2
    assert math.isclose(sample_nmse,decomposition,abs_tol=1e-14)
    assert audit[3]['point_error_divided_by_reported']>40
    assert audit[5]['point_error_divided_by_reported']>290

    scenarios=json.loads((CASE/'results/RESULTS.json').read_text(encoding='utf-8'))
    enriched=[]
    for scenario in scenarios:
        runs=scenario['runs']; n=len(runs[0]['attempts']); nodes=[]
        for node in range(n):
            rates=[];attempts=failures=0
            for run in runs:
                sent=run['attempts'][node];failed=run['failures'][node]
                assert sent==failed+run['successes'][node]
                assert math.isclose(run['mbps'][node],12000*run['successes'][node]/run['duration_us'],abs_tol=1e-10)
                rates.append(failed/sent);attempts+=sent;failures+=failed
            nodes.append(dict(node=node+1,pooled_failure_fraction=failures/attempts,
                seed_mean_failure_fraction=statistics.mean(rates),
                seed_min_failure_fraction=min(rates),seed_max_failure_fraction=max(rates),
                total_completed_attempts=attempts,total_failed_attempts=failures,
                mean_payload_mbps=scenario['per_node_mean'][node]))
        pooled=sum(x['total_failed_attempts'] for x in nodes)/sum(x['total_completed_attempts'] for x in nodes)
        assert min(x['pooled_failure_fraction'] for x in nodes)<=pooled<=max(x['pooled_failure_fraction'] for x in nodes)
        enriched.append(dict(id=scenario['id'],nodes=nodes,pooled_failure_fraction=pooled,
           total_payload_mbps=scenario['total_mean'],jain_mean=scenario['fairness_mean'],
           failure_semantics='Q3 includes overlap OR channel error; other scenarios Pe=0; not retry-limit drops'))

    # p49 / p59 rounds REMAINING time down. Partly completed slots must not
    # be silently credited as a full slot under our frozen model convention.
    floor_cases=[]
    for remaining_slots in (1,2,7):
        for elapsed in (0.,.1,4.5,8.9):
            residual=remaining_slots*9-elapsed
            author=int(residual/9)*9
            full_slots=remaining_slots*9
            expected=0 if elapsed==0 else 9
            assert math.isclose(full_slots-author,expected,abs_tol=1e-10)
            floor_cases.append(dict(slots=remaining_slots,elapsed_in_current_slot_us=elapsed,
              remaining_us=residual,paper_floor_remaining_us=author,
              frozen_full_slot_remaining_us=full_slots,advance_us=full_slots-author))
    result=dict(scope='partial review: Q3/Q4, evaluation and supplied appendix; no full author execution',
       source_sha256=hashes,nmse_definition='candidate mean squared error divided by squared fixed theory; original Eq3.23 absent in converted text',
       printed_error_audit=audit,jensen_identity_check='PASS',
       existing_scenarios=enriched,residual_slot_checks=floor_cases)
    (HERE/'EVALUATION_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(error_audit=audit,scenarios=len(enriched),runs=sum(len(x['runs']) for x in scenarios),
      q4_base=next(x for x in enriched if x['id']=='Q4_base'),residual_slot_cases=len(floor_cases)),ensure_ascii=False))


if __name__=='__main__':main()
