#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations
import json, math

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'learning_output/mini_transfer/2025-A/mini_transfer_report.json'

# Frozen mini-instance. No S029-S031 Dev solution artifacts are used.
OPS={
 'A0':('ALLOC',6),'U0':('USE',0),'F0':('FREE',6),
 'A1':('ALLOC',7),'U1':('USE',0),'F1':('FREE',7),
 'A2':('ALLOC',7),'U2':('USE',0),'F2':('FREE',7),
 'A3':('ALLOC',6),'U3':('USE',0),'F3':('FREE',6),
}
NODES=list(OPS)
EDGES=[('A0','U0'),('U0','F0'),('A1','U1'),('U1','F1'),('A2','U2'),('U2','F2'),('A3','U3'),('U3','F3'),
       ('U0','U1'),('A0','U2'),('U0','U3'),('U1','U2'),('A1','U3'),('U2','U3')]

def topo_orders():
    succ={n:[] for n in NODES}; indeg={n:0 for n in NODES}
    for u,v in EDGES: succ[u].append(v); indeg[v]+=1
    out=[]
    def rec(order,d):
        if len(order)==len(NODES): out.append(order[:]); return
        ready=sorted(n for n in NODES if d[n]==0 and n not in order)
        for n in ready:
            d2=d.copy(); d2[n]=-1
            for v in succ[n]: d2[v]-=1
            rec(order+[n],d2)
    rec([],indeg)
    return out

def peak(order):
    cur=pk=0
    for n in order:
        typ,size=OPS[n]
        if typ=='ALLOC': cur+=size
        elif typ=='FREE': cur-=size
        pk=max(pk,cur)
    return pk

def cp_lengths():
    succ={n:[] for n in NODES}
    for u,v in EDGES: succ[u].append(v)
    memo={}
    def f(n):
        if n not in memo: memo[n]=1+(max((f(v) for v in succ[n]),default=0))
        return memo[n]
    return {n:f(n) for n in NODES}

def greedy(mode):
    succ={n:[] for n in NODES}; indeg={n:0 for n in NODES}
    for u,v in EDGES: succ[u].append(v); indeg[v]+=1
    cp=cp_lengths(); ready={n for n in NODES if indeg[n]==0}; order=[]
    while ready:
        def key(n):
            typ,size=OPS[n]
            free_first=0 if typ=='FREE' else 1
            delta=-size if typ=='FREE' else (size if typ=='ALLOC' else 0)
            # Historical failed ordering: memory-delta before critical-path urgency.
            if mode=='old': return (free_first,delta,-cp[n],n)
            # Revised frozen rule: legal FREE first, critical-path/slack urgency, then memory delta.
            return (free_first,-cp[n],delta,n)
        n=min(ready,key=key); ready.remove(n); order.append(n)
        for v in succ[n]:
            indeg[v]-=1
            if indeg[v]==0: ready.add(v)
    return order

orders=topo_orders(); exact=min(peak(o) for o in orders)
old_order=greedy('old'); new_order=greedy('new')
q1={'topological_orders':len(orders),'exact_peak':exact,'old_rule_peak':peak(old_order),'revised_rule_peak':peak(new_order),
    'old_gap_pct':(peak(old_order)/exact-1)*100,'revised_gap_pct':(peak(new_order)/exact-1)*100,
    'old_order':old_order,'revised_order':new_order,'status':'PASS_AFTER_RULE_REVISION' if peak(new_order)==exact and peak(old_order)>exact else 'FAIL'}

# Q2: deficit-aware spill subset. Capacity 10, A=6/cost12, B=4/cost4, request C=5 => deficit5.
victims=[('A',6,12),('B',4,4)]; deficit=5
naive_cost=0; freed=0; naive=[]
for name,size,cost in sorted(victims,key=lambda x:x[2]):
    naive.append(name); freed+=size; naive_cost+=cost
    if freed>=deficit: break
best=None
for r in range(1,len(victims)+1):
    for subset in combinations(victims,r):
        sf=sum(x[1] for x in subset); sc=sum(x[2] for x in subset)
        if sf>=deficit and (best is None or sc<best[0]): best=(sc,[x[0] for x in subset],sf)
q2={'capacity':10,'request_size':5,'deficit':deficit,'victims':[{'id':n,'size':s,'incremental_transfer_cost':c} for n,s,c in victims],
    'naive_cheapest_first':{'victims':naive,'cost':naive_cost},'exact_min_cost_subset':{'victims':best[1],'cost':best[0],'freed':best[2]},
    'status':'PASS' if best[0]==12 and naive_cost==16 else 'FAIL'}

# Q3: hard epsilon feasibility precedes any weighted/Pareto preference.
base_transfer=100; cap=1.10*base_transfer
cands=[{'id':'A','cycles':92,'transfer':109},{'id':'B','cycles':85,'transfer':116},{'id':'C','cycles':95,'transfer':104}]
for c in cands: c['feasible']=c['transfer']<=cap+1e-12
feasible=[c for c in cands if c['feasible']]; chosen=min(feasible,key=lambda c:c['cycles'])
q3={'baseline_transfer':base_transfer,'epsilon_cap':0.10,'hard_limit':cap,'candidates':cands,'selected':chosen['id'],
    'rejected_infeasible':[c['id'] for c in cands if not c['feasible']],
    'status':'PASS' if chosen['id']=='A' and 'B' in [c['id'] for c in cands if not c['feasible']] else 'FAIL'}

report={'schema_version':'1.0','case_group':'2025-A','test_type':'SELF_CONSTRUCTED_MINI_TRANSFER_NO_DEV_SOLUTION_EXPOSURE',
        'purpose':'Test whether MathModel-Core reselects/revises methods rather than memorizing S025-S028.',
        'history':{'initial_discovery':'The first Q1 transfer attempt exposed a priority-ordering flaw: memory delta was ranked before critical-path urgency.',
                   'action':'Rule revised before confirmatory frozen mini-test; failure history retained rather than overwritten.'},
        'q1_scheduling':q1,'q2_spill_selection':q2,'q3_epsilon_constraint':q3,
        'overall_status':'PASS_AFTER_RULE_REVISION' if q1['status'].startswith('PASS') and q2['status']=='PASS' and q3['status']=='PASS' else 'FAIL',
        'reproduction_note':'This is a Core transfer test, not evidence that S028 author code reaches R7. S028 remains R2.'}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
