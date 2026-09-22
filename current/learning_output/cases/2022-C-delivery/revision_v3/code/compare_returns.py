"""24 evaluations per arm from fixed v2 routes; no-return arm also gets search budget."""
from return_solver import execute,ROOT
from validate_returns import validate
import json,random,itertools,time

def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    inputs=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
    registry=[];summaries=[];reports={}
    for key in ['result11','result12','result21','result22']:
        base=json.loads((ROOT/'seed_inputs'/f'{key}.json').read_text(encoding='utf-8'))
        recs=inputs[f"附件{base['dataset']}"];q=base['question'];prefs=base['prefs']
        by={x['进车顺序']:x for x in recs}
        hybrids=[c for c in base['output_sequence'] if by[c]['动力']=='混动']
        # Twelve explicit single-return probes plus twelve bounded reactive policies.
        picks=[hybrids[round(i*(len(hybrids)-1)/11)] for i in range(12)]
        policies=[dict(mode='selected',cars=[c]) for c in picks]
        policies += [dict(mode='gap',budget=b,gaps=g,return_lane=l) for b,g,l in itertools.product([1,3,8],[[1],[0,1]],[0,4])]
        original,original_matrix=execute(recs,q,prefs)
        assert original['score']==base['score']
        arm_best={};case_trace=[];started=time.monotonic()
        for arm in ['return','no_return']:
            best=original;bestmatrix=original_matrix;bestlabel='v2_base';trace=[]
            rng=random.Random(20220923+base['dataset']*10+q)
            route=dict(prefs['route'])
            for i in range(24):
                if arm=='return':candidate_prefs=prefs;policy=policies[i]
                else:
                    candidate=dict(route)
                    for c in rng.sample(list(candidate),rng.choice([1,2,4])):
                        candidate[c]=rng.choice([l for l in range(1,7) if l!=candidate[c]])
                    candidate_prefs={'route':candidate};policy={'mode':'off'}
                try:
                    r,m=execute(recs,q,candidate_prefs,policy)
                    item=dict(arm=arm,index=i,prefs=candidate_prefs,policy=policy,score=r['score'],status='SIMULATED')
                    if r['score']['total']>best['score']['total']:
                        # Every new incumbent must pass the independent visit checker.
                        check=validate(r,recs,m);item['validation']=check
                        if check['status']!='PASS':item['status']='REJECTED_BY_CHECKER'
                        else:
                            best,bestmatrix,bestlabel=r,m,f'{arm}_{i:02d}'
                            if arm=='no_return':route=dict(candidate_prefs['route'])
                except (RuntimeError,AssertionError) as e:
                    item=dict(arm=arm,index=i,prefs=candidate_prefs,policy=policy,status='FAILED',error=str(e))
                trace.append(item)
            check=validate(best,recs,bestmatrix)
            assert check['status']=='PASS',check['errors']
            arm_best[arm]=(best,bestmatrix,bestlabel,check)
            save(ROOT/'results'/f'{key}_{arm}_search.json',trace)
            save(ROOT/'results'/f'{key}_{arm}_best.json',best)
            case_trace+=trace
            print(key,arm,'best',round(best['score']['total'],3),'returns',best['score']['return_uses'],'PASS',flush=True)
        selected=max(arm_best,key=lambda arm:arm_best[arm][0]['score']['total'])
        result,matrix,label,check=arm_best[selected]
        sens,_=execute(recs,q,result['prefs'],result['return_policy'],arrival=9)
        result.update(id=key,dataset=base['dataset'],selected_candidate=label,baseline=base['baseline'],
            previous_score=base['score'],cadence_9s_same_policy_sensitivity=sens['score'],elapsed_seconds=time.monotonic()-started,
            weights=[2,1,.02],search_trace=case_trace)
        save(ROOT/'results'/f'{key}.json',result)
        (ROOT/'results'/f'{key}_matrix.json').write_text(json.dumps(matrix),encoding='utf-8')
        reports[key]=check
        summaries.append(dict(id=key,v2_score=base['score']['total'],selected_arm=selected,
            return_arm_score=arm_best['return'][0]['score']['total'],return_uses=arm_best['return'][0]['score']['return_uses'],
            no_return_arm_score=arm_best['no_return'][0]['score']['total'],evaluations_per_arm=24,
            failed_candidates=sum(x['status'] in ['FAILED','REJECTED_BY_CHECKER'] for x in case_trace)))
        registry.append({k:result[k] for k in ['id','dataset','question','score','selected_candidate','baseline','cadence_9s_same_policy_sensitivity','elapsed_seconds']})
    save(ROOT/'results/RESULTS.json',registry);save(ROOT/'results/RETURN_COMPARISON.json',summaries)
    save(ROOT/'results/INDEPENDENT_RETURN_VALIDATION.json',reports)

if __name__=='__main__':main()
