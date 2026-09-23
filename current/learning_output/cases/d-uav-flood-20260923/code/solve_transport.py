from model import *
from ortools.sat.python import cp_model
import random,time,copy

def allocate(schedule):
    avail_u={u:0. for us in DRONES.values() for u in us}
    avail_b={f'{g}{j+1:02d}':0. for g in TYPES for j in range(BAT[g])}
    ans=[]
    for ix,(start,r) in enumerate(sorted(schedule,key=lambda x:x[0])):
        g=r['g']; u=min(DRONES[g],key=lambda u:avail_u[u]); b=min([b for b in avail_b if b.startswith(g)],key=lambda b:avail_b[b])
        assert max(avail_u[u],avail_b[b])<=start+1e-7
        end=start+r['duration']; avail_u[u]=end; avail_b[b]=end+charge(g,r['energy'])
        ans.append({**r,'id':f'T{ix+1:03d}','start':start,'end':end,'drone':u,'battery':b,'battery_ready':avail_b[b]})
    return ans

def metrics(s):
    return dict(flights=len(s),energy=sum(r['energy'] for r in s),makespan=max(r['end'] for r in s),weighted_tardiness=sum(BOXES[int(k)]['weight']*max(0,r['start']+t-BOXES[int(k)]['due']) for r in s for k,t in r['deliveries'].items()),weighted_arrival=sum(BOXES[int(k)]['weight']*(r['start']+t) for r in s for k,t in r['deliveries'].items()),hard_late=max([0]+[r['start']+t-BOXES[int(k)]['deadline'] for r in s for k,t in r['deliveries'].items()]),types={g:sum(r['g']==g for r in s) for g in TYPES})

def schedule_cp(routes,limit=1.,release=None,windows=None):
    m=cp_model.CpModel(); horizon=30000; starts=[]; ends=[]; ts=[]; energyints={g:[] for g in TYPES}; droneints={g:[] for g in TYPES}
    for i,r in enumerate(routes):
        lo=int(math.ceil(release[i])) if release else 0
        latest=min(int(math.floor(BOXES[k]['deadline']-t)) for k,t in r['deliveries'].items())
        latest=min(latest,horizon)
        if latest<lo:return None
        s=m.new_int_var(lo,latest,f's{i}'); dur=math.ceil(r['duration']); e=m.new_int_var(0,horizon+dur,f'e{i}'); m.add(e==s+dur)
        starts.append(s);ends.append(e)
        droneints[r['g']].append(m.new_interval_var(s,dur,e,f'd{i}'))
        bd=math.ceil(r['duration']+charge(r['g'],r['energy'])); be=m.new_int_var(0,horizon+bd,f'be{i}');m.add(be==s+bd)
        energyints[r['g']].append(m.new_interval_var(s,bd,be,f'b{i}'))
        for k,t in r['deliveries'].items():
            v=m.new_int_var(0,horizon,f'tard{i}_{k}');m.add(v>=s+math.ceil(t)-BOXES[k]['due']);ts.append(BOXES[k]['weight']*v)
        if windows:
            for offset0,offset1,w0,w1 in windows[i]:m.add(s+math.floor(offset0)>=math.ceil(w0));m.add(s+math.ceil(offset1)<=math.floor(w1))
    for g in TYPES:
        m.add_cumulative(droneints[g],[1]*len(droneints[g]),len(DRONES[g]));m.add_cumulative(energyints[g],[1]*len(energyints[g]),BAT[g])
    cmax=m.new_int_var(0,horizon,'cmax');m.add_max_equality(cmax,ends)
    m.minimize(100000*sum(ts)+100*cmax+sum(starts))
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=limit;solver.parameters.num_search_workers=4;solver.parameters.random_seed=20260923
    status=solver.solve(m)
    if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):return None
    return allocate([(float(solver.value(s)),r) for s,r in zip(starts,routes)])

def greedy(seed):
    rng=random.Random(seed);remain=set(range(len(BOXES)));routes=[];work={g:0. for g in TYPES}
    while remain:
        urgent=min(remain,key=lambda k:(BOXES[k]['deadline'],BOXES[k]['due'],rng.random()))
        choices=[]
        for g in TYPES:
            ids=[urgent];r=route(g,tuple(ids))
            if r is None:continue
            others=sorted(remain-{urgent},key=lambda k:(BOXES[k]['node']!=BOXES[urgent]['node'], GEOD.inv(NODES[BOXES[k]['node']]['lon'],NODES[BOXES[k]['node']]['lat'],NODES[BOXES[urgent]['node']]['lon'],NODES[BOXES[urgent]['node']]['lat'])[2]+rng.random()*3000))
            for k in others:
                rr=route(g,tuple(sorted(ids+[k])))
                if rr is not None:ids.append(k);r=rr
            urgency=sum(BOXES[k]['weight']*(2 if BOXES[k]['deadline']<1e8 else .4) for k in ids)
            efficiency=(r['duration']+work[g]/len(DRONES[g])*.8)/max(urgency,1)
            choices.append((efficiency*rng.uniform(.7,1.3),r))
        r=min(choices,key=lambda z:z[0])[1];routes.append(r);remain.difference_update(r['boxes']);work[r['g']]+=r['duration']
    return routes

def mutate(routes,rng):
    rs=list(routes);i=rng.randrange(len(rs));r=rs[i];op=rng.randrange(4)
    if op==0:
        rr=route(rng.choice(list(TYPES)),tuple(r['boxes']))
        if rr:rs[i]=rr
    elif op==1 and len(r['boxes'])>1:
        k=rng.choice(r['boxes']);left=tuple(x for x in r['boxes'] if x!=k)
        a=route(r['g'],left);b=route(rng.choice(list(TYPES)),(k,))
        if a and b:rs[i]=a;rs.append(b)
    else:
        j=rng.randrange(len(rs))
        if i==j:return rs
        other=rs[j];transfer=list(r['boxes']) if op==3 else [rng.choice(r['boxes'])]
        b=route(rng.choice([other['g'],other['g'],*TYPES]),tuple(sorted(set(other['boxes'])|set(transfer))))
        left=tuple(k for k in r['boxes'] if k not in transfer);a=route(r['g'],left) if left else None
        if b and (a or not left):
            rs[j]=b
            if a:rs[i]=a
            else:rs.pop(i)
    return rs

def score(s):
    m=metrics(s)
    return m['weighted_tardiness']*10000+m['makespan']+m['energy']*8+m['flights']*12+m['weighted_arrival']*.0001

if __name__=='__main__':
    start=time.time();best=None;records=[]
    for seed in range(35):
        rs=greedy(seed);s=schedule_cp(rs,.3)
        if s:
            records.append(dict(seed=seed,**metrics(s)))
            if best is None or score(s)<score(best):best=s;print('seed',seed,metrics(best),flush=True);save('q2_best.json',best)
    if best is None:raise RuntimeError('No feasible initial schedule')
    baseline=copy.deepcopy(best);current=best;rng=random.Random(84217)
    for it in range(400):
        rs=mutate(current,rng);s=schedule_cp(rs,.15)
        if not s:continue
        delta=score(s)-score(current);temperature=60*(1-it/400)+1
        if delta<0 or rng.random()<math.exp(-min(700,delta/temperature)):current=s
        if score(s)<score(best):best=s;print('iteration',it,metrics(best),flush=True);save('q2_best.json',best)
    refined=schedule_cp(best,8)
    if refined and score(refined)<score(best):best=refined
    save('q2.json',best);save('q2_search.json',dict(elapsed=time.time()-start,seeds=records,iterations=400,baseline=metrics(baseline),final=metrics(best),seed=84217,global_optimal=False))
    print('FINAL',metrics(best),flush=True)
