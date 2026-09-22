"""Reproducible feasible-subset PBS search. No return-route use; not a global optimizer."""
from pathlib import Path
import json, random, time, argparse, csv
from collections import Counter
from historical_base import Sim, INOUT, POLICIES, score_sequence

ROOT = Path(__file__).resolve().parents[1]

class RevisedSim(Sim):
    def __init__(self, recs, q, prefs, arrival_interval=0, weights=None):
        super().__init__(recs, q, prefs, arrival_interval=arrival_interval, max_return_per_car=0)
        self.targets = set()
        self.movement_log = []
        self.instant_codes = {c:{} for c in self.ids}
        self.departed_at = {}
        self.now = 0
        self.weights = weights or [2.,1.,.02]

    def mark_paint(self,t):
        self.now=t
        super().mark_paint(t)

    def set_state(self,cid,st,t):
        super().set_state(cid,st,t)
        if st[0]!='transit':
            self.instant_codes[cid][t]=self.state_code(st)

    def start_moves(self,t):
        # Downstream first: a follower can start once its leader leaves the next slot.
        # The moving vehicle reserves its destination, but does not occupy its source.
        for lane in range(1,7):
            for src in range(2,11):
                cid=self.lanes[lane][src];dst=src-1
                if cid is not None and self.lanes[lane][dst] is None and (lane,dst) not in self.targets:
                    self.lanes[lane][src]=None
                    self.targets.add((lane,dst));self.moving.add(cid)
                    self.departed_at[(lane,src)]=t
                    self.instant_codes[cid][t]=int(f'{lane}{src}')
                    self.set_state(cid,('transit',lane,src,dst),t)
                    self.schedule(t+9,('lm',lane,src,dst,cid))
                    self.movement_log.append({'car':cid,'lane':lane,'src':src,'dst':dst,'start':t,'end':t+9})
        assert not any(self.ret[1:]), 'Return routes are outside this solver subset'

    def process(self,t,ev):
        if ev[0]=='lm':
            _,lane,src,dst,cid=ev
            assert self.lanes[lane][dst] is None
            assert (lane,dst) in self.targets
            self.targets.remove((lane,dst));self.moving.remove(cid)
            self.lanes[lane][dst]=cid
            self.set_state(cid,('lane',lane,dst),t)
            if dst==1:self.head_arrival[cid]=t
            self.event_log.append([t,list(ev)])
        else:
            super().process(t,ev)

    def lane_count(self,lane):
        return sum(c is not None for c in self.lanes[lane][1:])+sum(l==lane for l,_ in self.targets)

    def choose_lane(self,cid):
        feasible=[l for l in range(1,7) if self.lanes[l][10] is None and self.lane_count(l)<10
                  and self.departed_at.get((l,10),-1)!=self.now]
        if not feasible:return None
        pref=[self.prefs['route'][str(cid)]] if 'route' in self.prefs else self.prefs[self.cls(cid)]
        allowed=[l for l in feasible if l in pref]
        if not allowed:return None
        ranks={l:j for j,l in enumerate(pref)}
        a,b,c=self.weights
        return min(allowed,key=lambda l:(a*ranks[l]+b*self.lane_count(l)+c*INOUT[l],l))

    def invariant(self,t):
        super().invariant(t)
        for l in range(1,7):
            assert self.lane_count(l)<=10
        for l,p in self.targets:assert self.lanes[l][p] is None

    def matrix_rows(self,T):
        rows=super().matrix_rows(T)
        # Exact departure endpoint retains the last coded region reached at that second.
        # At interior transit samples the cell is blank. A just-departed lane-10 cannot
        # receive a new car at that same integer timestamp, preventing double codes.
        for row,cid in zip(rows,self.ids):
            for t,code in self.instant_codes[cid].items():
                if 0<=t<=T:row[t+1]=code
        return rows

def run(recs,q,prefs,arrival=0,weights=None):
    sim=RevisedSim(recs,q,prefs,arrival,weights)
    score=sim.run(max_t=20000)
    assert not sim.violations,sim.violations[:3]
    return sim,score

def candidates(dataset,q,budget):
    rng=random.Random(20220921+dataset*100+q)
    b=POLICIES[(f'附件{dataset}',q)]
    yield 'fifo_lane4',{k:[4] for k in ['H2','F2','F4']},[2,1,.02]
    yield 'historical_B_preferences',b,[2,1,.02]
    # Paper-motivated attribute partition; route parameters are chosen on this instance.
    yield 'fuel_central',{ 'H2':[1,2,5,6,3,4], 'F2':[4,3], 'F4':[4,3]},[2,1,.02]
    yield 'drive_partition',{'H2':[1,2,3,4],'F2':[4,3,2,1],'F4':[5,6]},[2,1,.02]
    for i in range(budget):
        p={k:rng.sample(range(1,7),6) for k in ['H2','F2','F4']}
        yield f'random_{i:03d}',p,[rng.choice([1,2,4,8]),rng.choice([0,.5,1,2]),rng.choice([0,.02,.1])]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--budget',type=int,default=40);ap.add_argument('--local',type=int,default=80);args=ap.parse_args()
    source=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
    out=ROOT/'results';out.mkdir(exist_ok=True)
    registry=[]
    for dataset in [1,2]:
        recs=source[f'附件{dataset}']
        for q in [1,2]:
            trace=[];best=None;started=time.monotonic()
            for name,prefs,weights in candidates(dataset,q,args.budget):
                sim,score=run(recs,q,prefs,weights=weights)
                trace.append({'name':name,'prefs':prefs,'weights':weights,'score':score})
                if best is None or score['total']>best[1]['total']:
                    best=(sim,score,name,prefs,weights)
            # A retained lane assignment is a warm start, not a reconstruction of A's search.
            historical=ROOT/'warmstarts'/f'result{q}{dataset}_action_log.csv'
            with historical.open(encoding='utf-8') as f: historical_rows=list(csv.DictReader(f))
            route={}
            for a in historical_rows:
                if a.get('action_type')=='recv_fresh':route[str(int(a['vehicle_id']))]=int(a['lane'])
            if len(route)==len(recs):
                sim,score=run(recs,q,{'route':route})
                trace.append({'name':'historical_A_route_new_decoder','prefs':{'route':route},'weights':[2,1,.02],'score':score})
                if score['total']>best[1]['total']:best=(sim,score,'historical_A_route_new_decoder',{'route':route},[2,1,.02])
            rng=random.Random(91021+dataset*100+q)
            route={str(a['car']):a['lane'] for a in best[0].actions if a['kind']=='paint_to_lane'}
            # Freeze the phenotype as a per-car lane vector, then search feasible decoded neighbors.
            sim,score=run(recs,q,{'route':route})
            trace.append({'name':'locked_route_seed','prefs':{'route':route},'weights':[2,1,.02],'score':score})
            local_best=(sim,score,'locked_route_seed',{'route':route},[2,1,.02])
            if score['total']>best[1]['total']:best=local_best
            for iteration in range(args.local):
                candidate=dict(local_best[3]['route'])
                for cid in rng.sample(list(candidate),rng.choice([1,2,4])):
                    candidate[cid]=rng.choice([l for l in range(1,7) if l!=candidate[cid]])
                sim,score=run(recs,q,{'route':candidate})
                name=f'local_{iteration:03d}'
                trace.append({'name':name,'prefs':{'route':candidate},'weights':[2,1,.02],'score':score})
                if score['total']>local_best[1]['total']:local_best=(sim,score,name,{'route':candidate},[2,1,.02])
                if score['total']>best[1]['total']:best=(sim,score,name,{'route':candidate},[2,1,.02])
            sim,score,name,prefs,weights=best
            cadence_sim,cadence_score=run(recs,q,prefs,arrival=9,weights=weights)
            key=f'result{q}{dataset}'
            result={'id':key,'dataset':dataset,'question':q,'score':score,'selected_candidate':name,
                'prefs':prefs,'weights':weights,'arrival_interval':0,'return_policy':'disabled feasible subset',
                'output_sequence':sim.output,'actions':sim.actions,'movements':sim.movement_log,
                'intervals':sim.intervals,'instant_codes':sim.instant_codes,
                'final_states':sim.states,'last_change':sim.last_change,
                'search_trace':trace,'baseline':trace[0]['score'],
                'cadence_9s_same_policy_sensitivity':cadence_score,
                'elapsed_seconds':time.monotonic()-started}
            (out/(key+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            (out/(key+'_matrix.json')).write_text(json.dumps([[None]+list(range(score['T']+1))]+sim.matrix_rows(score['T'])),encoding='utf-8')
            registry.append({k:result[k] for k in ['id','dataset','question','score','selected_candidate','baseline','cadence_9s_same_policy_sensitivity','elapsed_seconds']})
            print(key,score,'baseline',trace[0]['score']['total'],flush=True)
    (out/'RESULTS.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
