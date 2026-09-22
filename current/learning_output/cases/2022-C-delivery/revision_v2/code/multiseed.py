"""Equal-budget independent continuations from the same saved v1 policy.
This measures local-search seed sensitivity, not end-to-end algorithm superiority.
"""
from solve import ROOT, run
from validate import validate
import json, random, statistics, time

SEEDS = [101, 202, 303, 404, 505]
STEPS = 60

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def main():
    inputs=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
    all_runs=[]; registry=[]; reports={}
    for key in ['result11','result12','result21','result22']:
        original=json.loads((ROOT/'seed_inputs'/f'{key}.json').read_text(encoding='utf-8'))
        records=inputs[f"附件{original['dataset']}"];q=original['question']
        global_best=original; case_runs=[]
        route0={str(a['car']):a['lane'] for a in original['actions'] if a['kind']=='paint_to_lane'}
        for seed in SEEDS:
            started=time.monotonic();rng=random.Random(seed)
            sim,score=run(records,q,{'route':route0})
            assert abs(score['total']-original['score']['total'])<1e-9
            route=dict(route0);trace=[]
            for iteration in range(STEPS):
                candidate=dict(route)
                for cid in rng.sample(list(candidate),rng.choice([1,2,4])):
                    candidate[cid]=rng.choice([l for l in range(1,7) if l!=candidate[cid]])
                cs,ss=run(records,q,{'route':candidate})
                accepted=ss['total']>score['total']
                trace.append({'iteration':iteration,'prefs':{'route':candidate},'score':ss,'accepted':accepted})
                if accepted:sim,score,route=cs,ss,candidate
            matrix=[[None]+list(range(score['T']+1))]+sim.matrix_rows(score['T'])
            result=dict(original)
            result.update(score=score,prefs={'route':route},weights=[2,1,.02],selected_candidate=f'continuation_seed_{seed}',
                output_sequence=sim.output,actions=sim.actions,movements=sim.movement_log,intervals=sim.intervals,
                instant_codes=sim.instant_codes,final_states=sim.states,last_change=sim.last_change,
                search_trace=trace,elapsed_seconds=time.monotonic()-started,search_seed=seed,continuation_steps=STEPS)
            check=validate(result,records,matrix)
            assert check['status']=='PASS',check['errors']
            item={'id':key,'seed':seed,'steps':STEPS,'start_score':original['score']['total'],'score':score,
                  'gain':score['total']-original['score']['total'],'validation':check,'trace':trace,'prefs':{'route':route},
                  'elapsed_seconds':result['elapsed_seconds']}
            save(ROOT/'results'/f'{key}_seed_{seed}.json',item)
            case_runs.append(item)
            if score['total']>global_best['score']['total']:global_best=result
            print(key,seed,round(score['total'],3),'gain',round(item['gain'],3),'PASS',flush=True)
        prefs=global_best['prefs'];weights=global_best['weights']
        sim,score=run(records,q,prefs,weights=weights)
        _,sensitivity=run(records,q,prefs,arrival=9,weights=weights)
        global_best['cadence_9s_same_policy_sensitivity']=sensitivity
        save(ROOT/'results'/f'{key}.json',global_best)
        matrix=[[None]+list(range(score['T']+1))]+sim.matrix_rows(score['T'])
        (ROOT/'results'/f'{key}_matrix.json').write_text(json.dumps(matrix),encoding='utf-8')
        reports[key]=validate(global_best,records,matrix)
        registry.append({k:global_best[k] for k in ['id','dataset','question','score','selected_candidate','baseline','cadence_9s_same_policy_sensitivity','elapsed_seconds']})
        scores=[x['score']['total'] for x in case_runs]
        all_runs.append({'id':key,'start_score':original['score']['total'],'seeds':SEEDS,'steps_per_seed':STEPS,
            'scores':scores,'min':min(scores),'mean':statistics.mean(scores),'median':statistics.median(scores),
            'max':max(scores),'sample_stdev':statistics.stdev(scores),'strict_improvements':sum(x['gain']>1e-9 for x in case_runs)})
    save(ROOT/'results/MULTISEED_SUMMARY.json',all_runs)
    save(ROOT/'results/RESULTS.json',registry)
    save(ROOT/'results/INDEPENDENT_VALIDATION.json',reports)

if __name__=='__main__':main()
