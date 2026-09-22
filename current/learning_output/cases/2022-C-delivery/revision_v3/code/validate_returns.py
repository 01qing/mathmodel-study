"""Independent reconstruction from shuttle actions and per-car visit order.
No simulator import. Reconstruct FIFO motion in both directions, including re-entry.
"""
from collections import Counter, defaultdict
from validate import score as output_score

def validate(result,records,matrix):
    errors=[];counts=Counter()
    def check(name,ok,detail=None):
        counts[name]+=1
        if not ok:errors.append({'check':name,'detail':detail})
    ids=[r['进车顺序'] for r in records];T=result['score']['T']
    actions=result['actions'];recv=[a for a in actions if a['resource']=='receiver'];send=[a for a in actions if a['resource']=='sender']
    fresh=[a for a in recv if a['kind']=='paint_to_lane']
    check('fresh_input_order',[a['car'] for a in fresh]==ids)
    outs=[a for a in send if a['kind']=='lane_to_assembly'];returns=[a for a in send if a['kind']=='lane_to_return']
    check('output_permutation',len(outs)==len(ids) and {a['car'] for a in outs}==set(ids))
    check('output_sequence',[a['car'] for a in outs]==result['output_sequence'])
    check('completion',max(a['unload'] for a in outs)==T)
    Y={1:0,2:3,3:6,4:9,5:15,6:18}
    for acts in [recv,send]:
        for i,a in enumerate(acts):
            lane=a['lane'];y=Y[lane];t=a['t'];kind=a['kind']
            if kind=='paint_to_lane':pu=t;un=t+abs(y-9);done=t+2*abs(y-9)
            elif kind=='return_to_lane':pu=t+3;un=pu+abs(y-12);done=un+abs(y-9)
            elif kind=='lane_to_assembly':pu=t+abs(y-9);un=pu+abs(y-9);done=un
            elif kind=='lane_to_return':pu=t+abs(y-9);un=pu+abs(y-12);done=un+3
            else:check('known_action',False,kind);continue
            check('machine_geometry',(a['pickup'],a['unload'],a['done'])==(pu,un,done),a)
            if i:check('machine_nonoverlap',a['t']>=acts[i-1]['done'],a)
    visits=[];rvisits=[]
    send_index={id(a):i for i,a in enumerate(send)}
    for cid in ids:
        ra=[a for a in recv if a['car']==cid];sa=[a for a in send if a['car']==cid]
        check('visit_counts',len(ra)==len(sa) and len(ra)>0,cid)
        check('car_flow',ra[0]['kind']=='paint_to_lane' and all(a['kind']=='return_to_lane' for a in ra[1:]) and sa[-1]['kind']=='lane_to_assembly' and all(a['kind']=='lane_to_return' for a in sa[:-1]),cid)
        for j,(a,b) in enumerate(zip(ra,sa),1):
            check('same_visit_lane',a['lane']==b['lane'],cid)
            v=dict(car=cid,visit=j,lane=a['lane'],entry=a,exit=b,index=send_index[id(b)])
            visits.append(v)
            if j<len(ra):rvisits.append(dict(car=cid,visit=j,lane=7,entry=b,exit=ra[j]))
    moves={(m['car'],m['visit'],m['lane'],m['src']):m for m in result['movements']}
    check('move_count',len(moves)==len(result['movements'])==9*(len(visits)+len(rvisits)))
    for lane in range(1,8):
        vv=sorted([v for v in (visits if lane<7 else rvisits) if v['lane']==lane],key=lambda v:v['entry']['unload'])
        check('fifo_pickups',[v['exit']['pickup'] for v in vv]==sorted(v['exit']['pickup'] for v in vv),lane)
        prevdep={p:0 for p in range(1,11)};previous=None
        begin,end,step=(10,1,-1) if lane<7 else (1,10,1)
        for v in vv:
            arr={begin:v['entry']['unload']};dep={end:v['exit']['pickup']}
            if previous:check('entry_endpoint_exclusive',arr[begin]>prevdep[begin],(lane,v['car']))
            for src in range(begin,end,step):
                dst=src+step;start=max(arr[src],prevdep[dst]);finish=start+9
                expected=dict(car=v['car'],visit=v['visit'],lane=lane,src=src,dst=dst,start=start,end=finish)
                check('independent_motion_recurrence',moves.get((v['car'],v['visit'],lane,src))==expected,expected)
                dep[src]=start;arr[dst]=finish
            check('dispatch_only_after_arrival',v['exit']['t']>=arr[end],(lane,v['car']))
            v['arrival']=arr;v['departure']=dep;prevdep=dep;previous=v
    for v in sorted(visits,key=lambda v:v['index']):
        t=v['exit']['t'];pending=[w for w in visits if w['index']>=v['index'] and w['arrival'][1]<=t]
        check('head_available',v in pending,v['car'])
        if result['question']==1 and pending:check('q1_sender_priority',v['arrival'][1]==min(w['arrival'][1] for w in pending),v['car'])
    if result['question']==1:
        for a in fresh:
            check('q1_return_receiver_priority',not any(v['arrival'][10]<=a['t']<=v['exit']['t'] for v in rvisits),a['car'])
    for t in range(T+1):
        busy=any(a['t']<=t<a['done'] for a in send)
        pending=any(v['arrival'][1]<=t<=v['exit']['t'] for v in visits)
        check('sender_no_idle',busy or not pending or any(a['t']==t for a in send),t)
        for lane in range(1,8):
            n=sum(v['entry']['unload']<=t<v['exit']['pickup'] for v in (visits if lane<7 else rvisits) if v['lane']==lane)
            check('capacity',n<=10,(t,lane,n))
    actual=output_score(result['output_sequence'],records,T);actual['total']-=.2*len(returns)
    actual['capped_s4_total']-=.2*len(returns)
    actual.update(s1=100-actual['hbad'],s2=100-actual['dbad'],s3=100-len(returns))
    check('return_count',result['score']['return_uses']==len(returns)==len(rvisits))
    for k in ['hbad','dbad','s1','s2','s3','s4','total']:check('independent_score',abs(actual[k]-result['score'][k])<1e-9,k)
    check('matrix_shape',len(matrix)==len(ids)+1 and all(len(row)==T+2 for row in matrix))
    check('matrix_times',matrix[0]==[None]+list(range(T+1)))
    if not all(len(row)==T+2 for row in matrix):return {'status':'FAIL','errors':errors,'error_count':len(errors)}
    fresh_by={a['car']:a for a in fresh}
    for i,cid in enumerate(ids):
        expected=[None]*(T+1);first=fresh_by[cid]
        front=max(i*result.get('arrival_interval',0),0 if i==0 else fresh[i-1]['t'])
        for t in range(front,first['t']):expected[t]=0
        for v in sorted([v for v in visits if v['car']==cid],key=lambda v:v['visit']):
            a,b=v['entry'],v['exit'];lane=v['lane']
            for t in range(a['pickup'],a['unload']):expected[t]=1
            for pos in range(10,1,-1):
                for t in range(v['arrival'][pos],v['departure'][pos]+1):expected[t]=int(f'{lane}{pos}')
            for t in range(v['arrival'][1],b['pickup']):expected[t]=int(f'{lane}1')
            for t in range(b['pickup'],b['unload']):expected[t]=2
            if b['kind']=='lane_to_assembly':expected[b['unload']]=3
            else:
                rv=next(w for w in rvisits if w['car']==cid and w['visit']==v['visit'])
                for pos in range(1,10):
                    for t in range(rv['arrival'][pos],rv['departure'][pos]+1):expected[t]=int(f'7{pos}')
                for t in range(rv['arrival'][10],rv['exit']['pickup']):expected[t]=710
        row=matrix[i+1];check('matrix_row_id',row[0]==cid)
        check('every_matrix_cell',row[1:]==expected,{'car':cid,'first_mismatches':[t for t in range(T+1) if row[t+1]!=expected[t]][:5]})
    allowed={0,1,2,3}|{int(f'{l}{p}') for l in range(1,8) for p in range(1,11)}
    for t in range(T+1):
        codes=[row[t+1] for row in matrix[1:] if row[t+1] is not None]
        check('region_codes',all(c in allowed for c in codes),t)
        occ=Counter(c for c in codes if c not in [0,3])
        check('sampled_region_exclusivity',all(n<=1 for n in occ.values()),t)
    return dict(status='PASS' if not errors else 'FAIL',error_count=len(errors),errors=errors[:30],checks=dict(counts),
        visits=len(visits),return_visits=len(rvisits),independent_score=actual,
        scope='Action-derived visit replay with forced FIFO motion, capacity, priorities, shuttle geometry, scores and full sampled trajectories; conditional on explicit endpoint and arrival assumptions.')
