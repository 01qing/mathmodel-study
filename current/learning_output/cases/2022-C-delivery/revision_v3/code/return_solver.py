"""Return-capable extension. Every lane entry is a distinct visit."""
from solve import RevisedSim, ROOT
from collections import Counter

class ReturnSim(RevisedSim):
    def __init__(self, records, q, prefs, policy=None, arrival_interval=0):
        super().__init__(records,q,prefs,arrival_interval)
        self.policy=policy or {'mode':'off'}
        self.max_return_per_car=self.policy.get('max_per_car',1)
        self.visits=Counter();self.return_visits=Counter();self.return_targets=set()

    def process(self,t,ev):
        kind=ev[0]
        if kind in ['riu','rru']:self.visits[ev[2]]+=1
        if kind=='sru':self.return_visits[ev[1]]+=1
        if kind=='rm':
            _,src,dst,cid=ev
            assert self.ret[dst] is None and dst in self.return_targets
            self.return_targets.remove(dst);self.moving.remove(cid)
            self.ret[dst]=cid;self.set_state(cid,('ret',dst),t)
            self.event_log.append([t,list(ev)])
        else:super().process(t,ev)

    def start_moves(self,t):
        for lane in range(1,7):
            for src in range(2,11):
                cid=self.lanes[lane][src];dst=src-1
                if cid is not None and self.lanes[lane][dst] is None and (lane,dst) not in self.targets:
                    self.lanes[lane][src]=None;self.targets.add((lane,dst));self.moving.add(cid)
                    self.departed_at[(lane,src)]=t;self.instant_codes[cid][t]=int(f'{lane}{src}')
                    self.set_state(cid,('transit',lane,src,dst),t)
                    self.schedule(t+9,('lm',lane,src,dst,cid))
                    self.movement_log.append(dict(car=cid,visit=self.visits[cid],lane=lane,src=src,dst=dst,start=t,end=t+9))
        for src in range(9,0,-1):
            cid=self.ret[src];dst=src+1
            if cid is not None and self.ret[dst] is None and dst not in self.return_targets:
                self.ret[src]=None;self.return_targets.add(dst);self.moving.add(cid)
                self.departed_at[(7,src)]=t;self.instant_codes[cid][t]=int(f'7{src}')
                self.set_state(cid,('transit',7,src,dst),t)
                self.schedule(t+9,('rm',src,dst,cid))
                self.movement_log.append(dict(car=cid,visit=self.return_visits[cid],lane=7,src=src,dst=dst,start=t,end=t+9))

    def invariant(self,t):
        super().invariant(t)
        assert sum(c is not None for c in self.ret[1:])+len(self.return_targets)<=10
        for p in self.return_targets:assert self.ret[p] is None

    def choose_lane(self,cid):
        if self.car_returns[cid] and self.policy.get('return_lane'):
            feasible=[l for l in range(1,7) if self.lanes[l][10] is None and self.lane_count(l)<10 and self.departed_at.get((l,10),-1)!=self.now]
            preferred=self.policy['return_lane']
            return min(feasible,key=lambda l:(l!=preferred,self.lane_count(l),abs(l-4),l)) if feasible else None
        return super().choose_lane(cid)

    def should_return(self,lane,cid):
        p=self.policy
        if p['mode']=='off' or self.car_returns[cid]>=self.max_return_per_car:return False
        if self.ret[1] is not None or sum(c is not None for c in self.ret[1:])+len(self.return_targets)>=10:return False
        if p['mode']=='selected':return cid in p.get('cars',[])
        if self.returns>=p.get('budget',8) or len(self.output)>self.C-8:return False
        if self.byid[cid]['动力']!='混动' or not self.seen_h:return False
        if self.fgap not in p.get('gaps',[1]):return False
        # Require at least one fuel car still inside the system or waiting outside.
        available=any(self.byid[c]['动力']!='混动' and c not in self.output for c in self.ids)
        return available

def execute(records,q,prefs,policy=None,arrival=0):
    sim=ReturnSim(records,q,prefs,policy,arrival)
    score=sim.run(max_t=20000)
    assert not sim.violations,sim.violations[:3]
    result=dict(question=q,prefs=prefs,return_policy=policy or {'mode':'off'},arrival_interval=arrival,
        score=score,output_sequence=sim.output,actions=sim.actions,movements=sim.movement_log,
        intervals=sim.intervals,instant_codes=sim.instant_codes,final_states=sim.states,last_change=sim.last_change)
    matrix=[[None]+list(range(score['T']+1))]+sim.matrix_rows(score['T'])
    return result,matrix
