"""Paper-inspired topology experiment and local formula/code probes.
Uses frozen simulator; does not execute author's MATLAB or reconstruct missing indices.
"""
from pathlib import Path
import sys, json, statistics, math, hashlib
HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
sys.path.insert(0,str(CASE/'code'))
from wlan import simulate, scenario
from check_trace import check_trace
from analytic import q2_exact

def topology(left,right):
    p=scenario(4)
    p['interfere']=[[False,left,False],[left,False,right],[False,right,False]]
    return p

def stats(values):
    return dict(mean=statistics.mean(values),ci95_halfwidth=2.776445105*statistics.stdev(values)/math.sqrt(len(values)))

def main():
    rows=[]; validations=[]
    for left,right in [(True,True),(True,False),(False,True),(False,False)]:
        p=topology(left,right)
        runs=[simulate(**p,seed=s,duration=5e6,warmup=.5e6) for s in [101,202,303,404,505]]
        row=dict(left_interference=left,right_interference=right,params=p,runs=runs,
                 total=stats([r['total_mbps'] for r in runs]),
                 per_node=[stats([r['mbps'][i] for r in runs]) for i in range(3)],
                 fairness=stats([r['fairness'] for r in runs]))
        rows.append(row)
        trace=simulate(**p,seed=71,duration=100000,warmup=10000,trace=True)
        checked=check_trace(trace,p)
        assert checked['status']=='PASS',checked
        name=f'{int(left)}{int(right)}'
        (HERE/f'TRACE_{name}.json').write_text(json.dumps(dict(params=p,result=trace),indent=2),encoding='utf-8')
        validations.append(dict(topology=name,**checked))
        print(name,row['total'],flush=True)
    # Re-labeling AP1<->AP3 maps the two mixed cases exactly at model level.
    a,b=rows[1],rows[2]
    permutation=[2,1,0]
    for key in ['hear','interfere']:
        assert [[a['params'][key][permutation[i]][permutation[j]] for j in range(3)] for i in range(3)]==b['params'][key]
    symmetry=dict(structural_relabeling='PASS',
        total_mean_difference=a['total']['mean']-b['total']['mean'],
        total_sum_of_ci_halfwidths=a['total']['ci95_halfwidth']+b['total']['ci95_halfwidth'],
        reversed_node_mean_differences=[a['per_node'][i]['mean']-b['per_node'][2-i]['mean'] for i in range(3)],
        scope='finite sample comparison, not equality of random trajectories; CI overlap is diagnostic only')
    tau=2/17; q2=q2_exact()
    formula=dict(tau=tau,idle_probability=(1-tau)**2,
        author_q2_numerator_2tau1minus_tau_mbps=q2['decoupled_mbps']*(1-tau),
        corrected_independence_reward_mbps=q2['decoupled_mbps'],
        residual_chain_mbps=q2['total_mbps'],
        omitted_expected_packets_per_virtual_slot=2*tau*tau)
    # Raw appendix uses inclusive endpoint overlap and Unhold without busy owners.
    def author_overlap(a,b):
        return a[0]<=b[0]<=a[1] or a[0]<=b[1]<=a[1]
    def positive_overlap(a,b):return max(a[0],b[0])<min(a[1],b[1])
    overlaps=[dict(local=a,interferer=b,author_branch=author_overlap(a,b),positive_overlap=positive_overlap(a,b))
              for a,b in [((10,20),(20,30)),((10,20),(5,25)),((10,20),(15,25)),((10,20),(0,10))]]
    # Constructed local branch input, not a replay of a complete author run.
    busy_owners={0,2}; busy_owners.remove(0)
    unhold=dict(author_unhold_after_first_neighbor_end='BACK_OFF',remaining_busy_neighbors=sorted(busy_owners),
                required_state_with_all_neighbor_sensing='HOLD',scope='constructed local state; not author trajectory reachability proof')
    result=dict(scope='our bounded numerical checks; author MATLAB NOT_RUN',
                topology_cases=rows,short_trace_validation=validations,symmetry=symmetry,q2_formula=formula,
                appendix_overlap_probes=overlaps,appendix_unhold_probe=unhold,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [CASE/'code/wlan.py',CASE/'code/check_trace.py',CASE/'code/analytic.py',Path(__file__)]})
    (HERE/'CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(symmetry=symmetry,q2_formula=formula),indent=2))

if __name__=='__main__':main()
