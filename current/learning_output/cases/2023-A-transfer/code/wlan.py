"""Event-driven saturated DCF under explicitly declared virtual exchange sensing.
Time unit: microsecond. Counts only full idle backoff slots; partial slots restart.
"""
import random, math

def simulate(n=2,rate=455.8,cwmin=16,cwmax=1024,retries=32,hear=None,interfere=None,
             pe=0.,seed=1,duration=2_000_000.,warmup=100_000.,trace=False,sense_mode='exchange'):
    hear=hear if hear is not None else [[i!=j for j in range(n)] for i in range(n)]
    interfere=interfere if interfere is not None else hear
    rng=random.Random(seed);data_time=13.6+8*1530/rate;inf=float('inf');eps=1e-7
    stage=[0]*n;bo=[rng.randrange(cwmin) for _ in range(n)]
    drawn=list(bo);countstart=[43.]*n;attempt=[43.+b*9 for b in bo]
    dataend=[inf]*n;release=[inf]*n;active=[False]*n
    bad=[False]*n;packet=[None]*n;sent=[0]*n;success=[0]*n;failed=[0]*n;drops=[0]*n
    assert sense_mode in ['exchange','data_only']
    def sensed(j):return active[j] and (sense_mode=='exchange' or dataend[j]<inf)
    log=[];t=0.;limit=warmup+duration;events=0
    while True:
        t=min(min(attempt),min(dataend),min(release))
        if t>limit:break
        events+=1
        # Data intervals are half-open; an arrival at their endpoint does not collide.
        for i in range(n):
            if abs(dataend[i]-t)<eps:
                dataend[i]=inf;release[i]=t+(65 if bad[i] else 48)
                packet[i]['success']=not bad[i];packet[i]['release']=release[i]
        for i in range(n):
            if abs(release[i]-t)<eps:
                active[i]=False;release[i]=inf
                if t>=warmup:
                    sent[i]+=1
                    if bad[i]:failed[i]+=1
                    else:success[i]+=1
                if bad[i] and stage[i]<retries:stage[i]+=1
                else:
                    if bad[i] and t>=warmup:drops[i]+=1
                    stage[i]=0
                width=min(cwmax,cwmin*2**stage[i]);bo[i]=rng.randrange(width);drawn[i]=bo[i]
                countstart[i]=None;attempt[i]=inf
        # Resume a frozen counter only after a fresh uninterrupted DIFS.
        for i in range(n):
            if not active[i] and countstart[i] is None and not any(sensed(j) and hear[i][j] for j in range(n)):
                countstart[i]=t+43;attempt[i]=countstart[i]+9*bo[i]
        starters=[i for i in range(n) if abs(attempt[i]-t)<eps]
        if not starters:continue
        # Determine all simultaneous starters before changing carrier state.
        for i in starters:
            assert not active[i]
            active[i]=True;attempt[i]=inf;countstart[i]=None
            bad[i]=rng.random()<pe;dataend[i]=t+data_time
            packet[i]=dict(node=i,start=t,end=t+data_time,stage=stage[i],cw=min(cwmax,cwmin*2**stage[i]),backoff=drawn[i],noise_bad=bad[i],success=None,release=None)
            if trace:log.append(packet[i])
        for i in starters:
            for j in range(n):
                if i!=j and active[j] and dataend[j]>t+eps and dataend[j]<inf and interfere[i][j]:
                    bad[i]=True;bad[j]=True
        # Freeze counters of listening nodes, preserving completed full slots.
        for i in range(n):
            if not active[i] and countstart[i] is not None and any(sensed(j) and hear[i][j] for j in range(n)):
                elapsed=max(0.,t-countstart[i]);decrement=math.floor(elapsed/9+1e-8)
                bo[i]=max(0,bo[i]-decrement);countstart[i]=None;attempt[i]=inf
    mbps=[s*12000/duration for s in success]
    return dict(mbps=mbps,total_mbps=sum(mbps),attempts=sent,successes=success,failures=failed,drops=drops,
                events=events,seed=seed,duration_us=duration,warmup_us=warmup,data_time_us=data_time,
                fairness=sum(mbps)**2/(n*sum(x*x for x in mbps)) if any(mbps) else 0,trace=log if trace else None)

def scenario(q):
    if q==1:return dict(n=2,rate=455.8)
    if q==2:return dict(n=2,rate=275.3,interfere=[[False]*2 for _ in range(2)])
    if q==3:return dict(n=2,rate=455.8,hear=[[False]*2 for _ in range(2)],interfere=[[False,True],[True,False]],pe=.1)
    if q==4:
        edges=[[False,True,False],[True,False,True],[False,True,False]]
        return dict(n=3,rate=455.8,hear=edges,interfere=edges)
    raise ValueError(q)
