from return_solver import execute,ROOT
from validate_returns import validate
import json,copy

data=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
checks=[]
for q in [1,2]:
    for n in [1,2,20]:
        records=data['附件1'][:n]
        r,m=execute(records,q,{k:[4] for k in ['H2','F2','F4']},{'mode':'selected','cars':list(range(1,min(n,3)+1)),'max_per_car':2})
        report=validate(r,records,m)
        assert report['status']=='PASS',report['errors']
        assert r['score']['return_uses']==2*min(n,3)
        checks.append(dict(name=f'q{q}_{n}_cars_repeated_returns',passed=True,returns=r['score']['return_uses']))
# Intentionally corrupt return motion, score, and an actual return transit cell.
records=data['附件1'][:20]
r,m=execute(records,1,{k:[4] for k in ['H2','F2','F4']},{'mode':'selected','cars':[1,2,3]})
for kind in ['movement','matrix','count','flow']:
    rr=copy.deepcopy(r);mm=copy.deepcopy(m)
    move=next(x for x in rr['movements'] if x['lane']==7)
    if kind=='movement':move['end']+=1;expected='independent_motion_recurrence'
    elif kind=='matrix':mm[move['car']][move['start']+2]=71;expected='every_matrix_cell'
    elif kind=='count':rr['score']['return_uses']+=1;expected='return_count'
    else:
        # Mislabel a return pickup as fresh input: visit flow must reject.
        a=next(a for a in rr['actions'] if a['kind']=='return_to_lane')
        a['kind']='paint_to_lane';expected='fresh_input_order'
    report=validate(rr,records,mm)
    assert any(e['check']==expected for e in report['errors']),report
    checks.append(dict(name=f'reject_{kind}',passed=True))
for key in ['result11','result12','result21','result22']:
    old=json.loads((ROOT/'seed_inputs'/f'{key}.json').read_text(encoding='utf-8'))
    r,m=execute(data[f"附件{old['dataset']}"],old['question'],old['prefs'])
    assert r['score']==old['score'] and r['output_sequence']==old['output_sequence']
    report=validate(r,data[f"附件{old['dataset']}"],m)
    assert report['status']=='PASS',report['errors']
    checks.append(dict(name=f'{key}_no_return_backward_equivalence',passed=True))
stress=[]
records=data['附件1'][:40]
for q in [1,2]:
    prefs={'route':{str(c['进车顺序']):[1,3,4,5,6][i%5] for i,c in enumerate(records)}}
    r,m=execute(records,q,prefs,{'mode':'selected','cars':list(range(1,41)),'max_per_car':2,'return_lane':4})
    report=validate(r,records,m)
    assert report['status']=='PASS',report['errors']
    checks.append(dict(name=f'q{q}_40_cars_multilane_return_stress',passed=True,returns=r['score']['return_uses']))
    stress.append(dict(question=q,returns=r['score']['return_uses'],validation=report))
    if q==2:
        rr=copy.deepcopy(r);rr['question']=1
        wrong=validate(rr,records,m)
        assert any(e['check'] in ['q1_return_receiver_priority','q1_sender_priority'] for e in wrong['errors']),wrong
        checks.append(dict(name='reject_q2_schedule_under_q1_priority_rules',passed=True))
(ROOT/'results/RETURN_STRESS.json').write_text(json.dumps(stress,indent=2),encoding='utf-8')
(ROOT/'results/RETURN_REGRESSIONS.json').write_text(json.dumps(dict(status='PASS',checks=checks),indent=2),encoding='utf-8')
print('PASS',len(checks),'return and backward-compatibility checks')
