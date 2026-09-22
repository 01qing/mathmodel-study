"""Independent no-return route replay from unload/pickup actions; does not import solver."""
from pathlib import Path
import json, itertools, hashlib
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]

def score(ids, records,T):
    by={r['进车顺序']:r for r in records}
    h=[i for i,c in enumerate(ids) if by[c]['动力']=='混动']
    bad1=sum(b-a!=3 for a,b in zip(h,h[1:]))
    d=[by[c]['驱动'] for c in ids];first=d[0]
    cuts=[0]+[i for i in range(1,len(d)) if d[i]==first and d[i-1]!=first]+[len(d)]
    bad2=sum(Counter(d[a:b])['四驱']!=Counter(d[a:b])['两驱'] for a,b in zip(cuts,cuts[1:]))
    s4=100-.01*(T-9*len(ids)-72)
    total=.4*(100-bad1)+.3*(100-bad2)+.2*100+.1*s4
    return {'hbad':bad1,'dbad':bad2,'s4':s4,'total':total,'capped_s4_total':total-.1*max(0,s4-100)}

def validate(result,records,matrix):
    errors=[];counts=Counter()
    def check(name,cond,detail=None):
        counts[name]+=1
        if not cond:errors.append({'check':name,'detail':detail})
    ids=[r['进车顺序'] for r in records];C=len(ids)
    actions=result['actions'];rec=[a for a in actions if a['resource']=='receiver'];send=[a for a in actions if a['resource']=='sender']
    check('input_order',[a['car'] for a in rec]==ids)
    check('permutation',len(result['output_sequence'])==C and set(result['output_sequence'])==set(ids))
    check('no_return_subset',all(a['kind'] in ['paint_to_lane','lane_to_assembly'] for a in actions))
    times={1:18,2:12,3:6,4:0,5:12,6:18}
    for acts in [rec,send]:
        for i,a in enumerate(acts):
            d=times[a['lane']]
            check('machine_duration',a['done']-a['t']==d,a)
            check('pickup_time',a['pickup']==a['t']+(d//2 if a['resource']=='sender' else 0),a)
            check('unload_time',a['unload']==a['t']+(d if a['resource']=='sender' else d//2),a)
            if i:check('machine_nonoverlap',a['t']>=acts[i-1]['done'],a)
    check('completion',result['score']['T']==max(a['unload'] for a in send))
    check('sequence_from_actions',[a['car'] for a in send]==result['output_sequence'])
    picks={a['car']:a for a in send}
    movements={(m['car'],m['src']):m for m in result['movements']}
    check('nine_moves_each',len(result['movements'])==9*C and len(movements)==9*C)
    arrival={};depart={};lane_map={};entered={}
    for lane in range(1,7):
        visits=[a for a in rec if a['lane']==lane]
        check('lane_fifo',[a['car'] for a in visits]==[a['car'] for a in send if a['lane']==lane],lane)
        prev_dep={p:0 for p in range(1,11)};prev=None
        for a in visits:
            car=a['car'];lane_map[car]=lane;entered[car]=a['unload']
            arrival[car]={10:a['unload']};depart[car]={1:picks[car]['pickup']}
            if prev is not None:check('entry_timestamp_exclusive',a['unload']>depart[prev][10],car)
            for src in range(10,1,-1):
                expected_start=max(arrival[car][src],prev_dep[src-1])
                expected_end=expected_start+9
                m=movements[(car,src)]
                check('independent_fifo_recurrence',m=={'car':car,'lane':lane,'src':src,'dst':src-1,'start':expected_start,'end':expected_end},m)
                depart[car][src]=expected_start;arrival[car][src-1]=expected_end
            check('sender_only_parked',picks[car]['pickup']>=arrival[car][1],car)
            prev_dep=depart[car];prev=car
    sent=set()
    for a in send:
        heads=[c for c in ids if c not in sent and arrival[c][1]<=a['t']]
        check('chosen_head_present',a['car'] in heads,a['car'])
        if result['question']==1:
            check('q1_earliest_priority',arrival[a['car']][1]==min(arrival[c][1] for c in heads),a)
        sent.add(a['car'])
    # If a head is ready at an integer decision time, the sender must be active or act then.
    for t in range(result['score']['T']+1):
        busy=any(a['t']<=t<a['done'] for a in send)
        pending=[a for a in send if arrival[a['car']][1]<=t and a['t']>=t]
        check('sender_no_idle',busy or not pending or any(a['t']==t for a in send),t)
        for l in range(1,7):
            n=sum(entered[c]<=t<picks[c]['pickup'] for c in ids if lane_map[c]==l)
            check('lane_capacity',n<=10,[t,l,n])
    actual=score(result['output_sequence'],records,result['score']['T'])
    for k in ['hbad','dbad','s4','total']:check('independent_score',abs(actual[k]-result['score'][k])<1e-9,k)
    T=result['score']['T']
    check('matrix_shape',len(matrix)==C+1 and all(len(r)==T+2 for r in matrix))
    check('matrix_times',matrix[0]==[None]+list(range(T+1)))
    # Construct each trajectory independently from the inferred parking and shuttle timeline.
    for car,row in zip(ids,matrix[1:]):
        check('matrix_row_id',row[0]==car)
        expected=[None]*(T+1)
        a=next(x for x in rec if x['car']==car);b=picks[car];lane=lane_map[car]
        front=0 if car==ids[0] else rec[ids.index(car)-1]['t']
        for t in range(front,a['t']):expected[t]=0
        for t in range(a['t'],a['unload']):expected[t]=1
        for p in range(10,1,-1):
            for t in range(arrival[car][p],depart[car][p]+1):expected[t]=int(f'{lane}{p}')
        for t in range(arrival[car][1],b['pickup']):expected[t]=int(f'{lane}1')
        for t in range(b['pickup'],b['unload']):expected[t]=2
        expected[b['unload']]=3
        check('every_matrix_cell',row[1:]==expected,car)
        for m in [movements[(car,p)] for p in range(2,11)]:
            check('transit_blank',all(row[t+1] is None for t in range(m['start']+1,m['end'])),m)
    allowed={0,1,2,3}|{int(f'{l}{p}') for l in range(1,8) for p in range(1,11)}
    for t in range(T+1):
        codes=[r[t+1] for r in matrix[1:] if r[t+1] is not None]
        check('region_codes',all(c in allowed for c in codes),t)
        # Capacity-one is specified for parking positions and shuttles, not the assembly outlet.
        # Sequential zero-duration deliveries can legitimately share the sampled outlet code 3.
        counts_at=Counter(c for c in codes if c not in [0,3])
        check('no_duplicate_regions',all(v<=1 for v in counts_at.values()),[t,{k:v for k,v in counts_at.items() if v>1}])
    return {'status':'PASS' if not errors else 'FAIL','errors':errors[:30],'error_count':len(errors),'checks':dict(counts),
            'independent_score':actual,'scope':'No-return schedules under explicit endpoint and source-queue assumptions; not a proof of global optimality or validation of return-route dynamics.'}

def main():
    inputs=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'));reports={}
    for key in ['result11','result12','result21','result22']:
        r=json.loads((ROOT/'results'/f'{key}.json').read_text(encoding='utf-8'))
        m=json.loads((ROOT/'results'/f'{key}_matrix.json').read_text())
        report=validate(r,inputs[f'附件{r["dataset"]}'],m);reports[key]=report
        print(key,report['status'],report['error_count'],report['errors'][:2],flush=True)
    (ROOT/'results/INDEPENDENT_VALIDATION.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
    if any(r['status']!='PASS' for r in reports.values()):raise SystemExit(1)

if __name__=='__main__':main()
