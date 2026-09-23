from model import *
from functools import lru_cache

def solve_node(n,rho=.2,mode='flights'):
    kinds=sorted({b['kind'] for b in BOXES if b['node']==n})
    groups=[[i for i,b in enumerate(BOXES) if b['node']==n and b['kind']==k] for k in kinds]
    total=tuple(map(len,groups)); patterns=[]
    for counts in itertools.product(*(range(c+1) for c in total)):
        if not sum(counts):continue
        ids=tuple(i for gg,c in zip(groups,counts) for i in gg[:c])
        for g in TYPES:
            r=route(g,ids,rho=rho)
            if r and r['energy']<=(1-rho)*TYPES[g]['E']+1e-9:
                metric=(1,r['energy'],r['duration']) if mode=='flights' else (r['energy'],1,r['duration'])
                patterns.append((counts,g,metric))
    @lru_cache(None)
    def dp(state):
        if not any(state):return ((0.,0.,0.),[])
        best=None
        for c,g,val in patterns:
            if any(a>b for a,b in zip(c,state)):continue
            child=dp(tuple(b-a for a,b in zip(c,state)))
            if child is None:continue
            score=tuple(a+b for a,b in zip(val,child[0]))
            if best is None or score<best[0]:best=(score,child[1]+[(c,g)])
        return best
    sol=dp(total)
    if sol is None:return None
    ptr=[0]*len(groups); answer=[]
    for counts,g in sol[1]:
        ids=[]
        for h,c in enumerate(counts): ids+=groups[h][ptr[h]:ptr[h]+c];ptr[h]+=c
        answer.append(route(g,tuple(sorted(ids)),rho=rho))
    return answer

if __name__=='__main__':
    result=[]; sensitivity=[]
    for rho in [.1,.2,.3,.4]:
        for mode in (['flights','energy'] if rho==.2 else ['flights']):
            sol=[]
            impossible=[]
            for n in list(NODES)[1:]:
                local=solve_node(n,rho,mode)
                if local is None:impossible.append(n)
                else:sol.extend(local)
            record=dict(rho=rho,mode=mode,flights=len(sol),energy=sum(r['energy'] for r in sol),time=sum(r['duration'] for r in sol),types={g:sum(r['g']==g for r in sol) for g in TYPES},capacity={n:{g:capacity(g,n,rho) for g in TYPES} for n in list(NODES)[1:]})
            record['infeasible_nodes']=impossible
            sensitivity.append(record); print(record['rho'],mode,record['flights'],record['energy'],record['time'],record['types'],impossible,flush=True)
            if rho==.2 and mode=='flights':result=sol
    save('q1.json',result);save('q1_sensitivity.json',sensitivity)
