#!/usr/bin/env python3
import json, os, collections, argparse

Y={1:0,2:3,3:6,4:9,5:15,6:18}; Y4=9; YR=12
INOUT={i:2*abs(Y[i]-Y4) for i in range(1,7)}
RET={i:abs(Y[i]-Y4)+abs(Y[i]-YR)+abs(YR-Y4) for i in range(1,7)}

POLICIES={
("附件1",1): {'H2':[4,3,6,1,2,5],'F2':[6,2,1,3,5,4],'F4':[3,5,2,1,4,6]},
("附件1",2): {'H2':[4,3,1,5,6,2],'F2':[1,6,3,5,4,2],'F4':[6,1,3,5,4,2]},
("附件2",1): {'H2':[3,6,4,5,1,2],'F2':[4,2,3,5,6,1],'F4':[3,1,4,5,2,6]},
("附件2",2): {'H2':[4,3,6,1,2,5],'F2':[1,5,3,6,4,2],'F4':[1,6,2,3,4,5]},
}

def score_sequence(output_ids,recs,return_uses,T):
    byid={r["进车顺序"]:r for r in recs}
    if len(output_ids)!=len(recs) or set(output_ids)!=set(byid):
        raise ValueError("output is not a permutation")
    prev_h=False; fuel_since=0; hbad=0
    for cid in output_ids:
        if byid[cid]["动力"]=="混动":
            if prev_h and fuel_since!=2: hbad+=1
            prev_h=True; fuel_since=0
        elif prev_h:
            fuel_since+=1
    drives=[4 if byid[c]["驱动"]=="四驱" else 2 for c in output_ids]
    start=drives[0]; blocks=[]; cur=[]
    for j,d in enumerate(drives):
        if j and ((start==4 and drives[j-1]==2 and d==4) or (start==2 and drives[j-1]==4 and d==2)):
            blocks.append(cur); cur=[]
        cur.append(d)
    blocks.append(cur)
    dbad=sum(1 for b in blocks if b.count(4)!=b.count(2))
    base=9*len(recs)+72
    total=100-.4*hbad-.3*dbad-.2*return_uses-.001*(T-base)
    return {"total":total,"s1":100-hbad,"s2":100-dbad,"s3":100-return_uses,
            "s4":100-.01*(T-base),"hbad":hbad,"dbad":dbad,
            "return_uses":return_uses,"T":T,"base":base,"deltaT":T-base,"blocks":len(blocks)}

class Sim:
    def __init__(self,recs,q,prefs,arrival_interval=9,max_return_per_car=1):
        self.recs=recs; self.byid={r["进车顺序"]:r for r in recs}; self.ids=[r["进车顺序"] for r in recs]
        self.C=len(recs); self.q=q; self.prefs=prefs; self.arrival_interval=arrival_interval
        self.in_idx=0; self.lanes={i:[None]*11 for i in range(1,7)}; self.ret=[None]*11
        self.moving=set(); self.res_s=set(); self.res_r=set()
        self.events=collections.defaultdict(list); self.rb=0; self.sb=0
        self.output=[]; self.out_time={}; self.returns=0; self.car_returns=collections.Counter()
        self.head_arrival={}
        self.states={cid:("outside",None) for cid in self.ids}; self.last_change={cid:0 for cid in self.ids}
        self.intervals={cid:[] for cid in self.ids}
        self.actions=[]; self.event_log=[]; self.violations=[]
        self.first_drive=None; self.prev_drive=None; self.b2=0; self.b4=0; self.seen_h=False; self.fgap=0
        self.max_return_per_car=max_return_per_car

    def cls(self,cid):
        r=self.byid[cid]
        return "F4" if r["驱动"]=="四驱" else ("H2" if r["动力"]=="混动" else "F2")

    def set_state(self,cid,st,t):
        old=self.states[cid]
        if old!=st:
            s=self.last_change[cid]
            if t>s and old[0]!="outside": self.intervals[cid].append([s,t,list(old)])
            self.states[cid]=st; self.last_change[cid]=t

    def schedule(self,t,ev): self.events[t].append(ev)

    def process(self,t,ev):
        k=ev[0]
        if k=="lm":
            _,lane,src,dst,cid=ev
            if self.lanes[lane][src]!=cid or self.lanes[lane][dst] is not None: self.violations.append(["lane_move_collision",t,ev])
            self.lanes[lane][src]=None; self.lanes[lane][dst]=cid; self.moving.discard(cid); self.set_state(cid,("lane",lane,dst),t)
            if dst==1:self.head_arrival[cid]=t
        elif k=="rm":
            _,src,dst,cid=ev
            if self.ret[src]!=cid or self.ret[dst] is not None:self.violations.append(["return_move_collision",t,ev])
            self.ret[src]=None; self.ret[dst]=cid; self.moving.discard(cid); self.set_state(cid,("ret",dst),t)
        elif k=="riu":
            _,lane,cid=ev
            if self.lanes[lane][10] is not None:self.violations.append(["recv_unload_occupied",t,ev])
            self.lanes[lane][10]=cid; self.set_state(cid,("lane",lane,10),t)
        elif k=="rrp":
            _,cid=ev
            if self.ret[10]!=cid:self.violations.append(["return_pickup_mismatch",t,ev])
            self.ret[10]=None; self.res_r.discard(cid); self.set_state(cid,("recv",None),t)
        elif k=="rru":
            _,lane,cid=ev
            if self.lanes[lane][10] is not None:self.violations.append(["return_unload_occupied",t,ev])
            self.lanes[lane][10]=cid; self.set_state(cid,("lane",lane,10),t)
        elif k=="sp":
            _,lane,cid,route=ev
            if self.lanes[lane][1]!=cid:self.violations.append(["sender_pickup_mismatch",t,ev])
            self.lanes[lane][1]=None; self.res_s.discard(cid); self.set_state(cid,("send",None),t)
        elif k=="soa":
            _,cid=ev
            self.set_state(cid,("assembly",None),t); self.output.append(cid); self.out_time[cid]=t; self.update_output(cid)
            self.schedule(t+1,("leave",cid))
        elif k=="leave":
            self.set_state(ev[1],("outside",None),t)
        elif k=="sru":
            _,cid=ev
            if self.ret[1] is not None:self.violations.append(["return1_occupied",t,ev])
            self.ret[1]=cid; self.set_state(cid,("ret",1),t)
        self.event_log.append([t,list(ev)])

    def start_moves(self,t):
        for lane in range(1,7):
            for src in range(2,11):
                cid=self.lanes[lane][src]
                if cid is not None and cid not in self.moving and self.lanes[lane][src-1] is None:
                    self.moving.add(cid); self.schedule(t+9,("lm",lane,src,src-1,cid))
        for src in range(9,0,-1):
            cid=self.ret[src]
            if cid is not None and cid not in self.moving and cid not in self.res_r and self.ret[src+1] is None:
                self.moving.add(cid); self.schedule(t+9,("rm",src,src+1,cid))

    def lane_count(self,lane): return sum(x is not None for x in self.lanes[lane])

    def choose_lane(self,cid):
        feas=[i for i in range(1,7) if self.lanes[i][10] is None]
        if not feas:return None
        pref=self.prefs[self.cls(cid)]; rank={x:j for j,x in enumerate(pref)}
        return min(feas,key=lambda i:(rank[i]*2+self.lane_count(i)+.02*INOUT[i],self.lane_count(i),INOUT[i],i))

    def heads(self):
        z=[]
        for lane in range(1,7):
            cid=self.lanes[lane][1]
            if cid is not None and cid not in self.res_s and cid not in self.moving:z.append((lane,cid))
        return z

    def cost(self,cid):
        r=self.byid[cid]; c=0.0
        if r["动力"]=="混动":
            if self.seen_h and self.fgap!=2:c+=.4
            if self.seen_h and self.fgap>2:c-=.12
            if not self.seen_h:c-=.15
            if self.seen_h and self.fgap==2:c-=.18
        else:
            if self.seen_h:
                if self.fgap<2:c-=.12
                elif self.fgap==2:c+=.12
                else:c+=.08
        d=4 if r["驱动"]=="四驱" else 2
        if self.first_drive is not None:
            bd=(self.first_drive==4 and self.prev_drive==2 and d==4) or (self.first_drive==2 and self.prev_drive==4 and d==2)
            if bd and self.b2!=self.b4:c+=.3
            elif bd:c-=.08
            if self.first_drive==2 and d==4 and self.b2>self.b4:c-=.04*min(3,self.b2-self.b4)
        return c

    def choose_head(self,t):
        h=self.heads()
        if not h:return None
        if self.q==1:
            m=min(self.head_arrival.get(cid,t) for lane,cid in h)
            e=[x for x in h if self.head_arrival.get(x[1],t)==m]
            return min(e,key=lambda x:(self.cost(x[1]),INOUT[x[0]],x[0]))
        return min(h,key=lambda x:(self.cost(x[1])+.001*INOUT[x[0]],self.head_arrival.get(x[1],t),x[0]))

    def should_return(self,lane,cid):
        if self.car_returns[cid]>=self.max_return_per_car or self.ret[1] is not None or len(self.output)>self.C-8:return False
        r=self.byid[cid]; h=self.heads()
        if self.q==2:
            return r["动力"]=="混动" and self.seen_h and self.fgap==1 and all(self.byid[c2]["动力"]=="混动" for _,c2 in h) and (self.in_idx<self.C or any(self.ret[1:]))
        return r["动力"]=="混动" and self.seen_h and self.fgap==1 and any(self.byid[c2]["动力"]!="混动" for _,c2 in h if c2!=cid)

    def update_output(self,cid):
        r=self.byid[cid]; d=4 if r["驱动"]=="四驱" else 2
        if self.first_drive is None:self.first_drive=d;self.prev_drive=d;self.b2=int(d==2);self.b4=int(d==4)
        else:
            bd=(self.first_drive==4 and self.prev_drive==2 and d==4) or (self.first_drive==2 and self.prev_drive==4 and d==2)
            if bd:self.b2=int(d==2);self.b4=int(d==4)
            else:self.b2+=int(d==2);self.b4+=int(d==4)
            self.prev_drive=d
        if r["动力"]=="混动":self.seen_h=True;self.fgap=0
        elif self.seen_h:self.fgap=min(3,self.fgap+1)

    def paint_ready(self,t):return self.in_idx<self.C and t>=self.in_idx*self.arrival_interval

    def mark_paint(self,t):
        if self.paint_ready(t):
            cid=self.ids[self.in_idx]
            if self.states[cid][0]=="outside":self.set_state(cid,("paint",None),t)

    def receiver(self,t):
        if t<self.rb:return False
        rc=self.ret[10]; rr=rc is not None and rc not in self.moving and rc not in self.res_r
        if rr and self.q==1:
            lane=self.choose_lane(rc)
            if lane is None:return False
            self.res_r.add(rc); pu=t+3; un=pu+abs(YR-Y[lane]); done=t+RET[lane]
            self.actions.append({"t":t,"resource":"receiver","kind":"return_to_lane","car":rc,"lane":lane,"return10_ready":True,"pickup":pu,"unload":un,"done":done})
            self.schedule(pu,("rrp",rc));self.schedule(un,("rru",lane,rc));self.rb=done;return True
        if self.q==2 and rr and (self.ret[9] is not None or self.in_idx>=self.C):
            lane=self.choose_lane(rc)
            if lane is not None:
                self.res_r.add(rc);pu=t+3;un=pu+abs(YR-Y[lane]);done=t+RET[lane]
                self.actions.append({"t":t,"resource":"receiver","kind":"return_to_lane","car":rc,"lane":lane,"return10_ready":True,"pickup":pu,"unload":un,"done":done})
                self.schedule(pu,("rrp",rc));self.schedule(un,("rru",lane,rc));self.rb=done;return True
        if self.paint_ready(t):
            cid=self.ids[self.in_idx];lane=self.choose_lane(cid)
            if lane is not None:
                self.in_idx+=1;d=abs(Y[lane]-Y4);self.set_state(cid,("recv",None),t)
                self.actions.append({"t":t,"resource":"receiver","kind":"paint_to_lane","car":cid,"lane":lane,"return10_ready":bool(rr),"pickup":t,"unload":t+d,"done":t+2*d})
                self.schedule(t+d,("riu",lane,cid));self.rb=t+2*d;return True
        if self.q==2 and rr:
            lane=self.choose_lane(rc)
            if lane is not None:
                self.res_r.add(rc);pu=t+3;un=pu+abs(YR-Y[lane]);done=t+RET[lane]
                self.actions.append({"t":t,"resource":"receiver","kind":"return_to_lane","car":rc,"lane":lane,"return10_ready":True,"pickup":pu,"unload":un,"done":done})
                self.schedule(pu,("rrp",rc));self.schedule(un,("rru",lane,rc));self.rb=done;return True
        return False

    def sender(self,t):
        if t<self.sb:return False
        h=self.heads()
        if not h:return False
        chosen=self.choose_head(t);lane,cid=chosen; route_ret=self.should_return(lane,cid)
        if route_ret and self.ret[1] is not None:route_ret=False
        arrs={str(c):self.head_arrival.get(c,t) for _,c in h}
        self.res_s.add(cid);d=abs(Y[lane]-Y4);pu=t+d
        if route_ret:
            un=pu+abs(Y[lane]-YR);done=un+abs(YR-Y4)
            self.actions.append({"t":t,"resource":"sender","kind":"lane_to_return","car":cid,"lane":lane,"eligible_heads":[c for _,c in h],"head_arrivals":arrs,"chosen_arrival":self.head_arrival.get(cid,t),"pickup":pu,"unload":un,"done":done})
            self.schedule(pu,("sp",lane,cid,"return"));self.schedule(un,("sru",cid));self.sb=done;self.returns+=1;self.car_returns[cid]+=1
        else:
            ar=pu+abs(Y[lane]-Y4)
            self.actions.append({"t":t,"resource":"sender","kind":"lane_to_assembly","car":cid,"lane":lane,"eligible_heads":[c for _,c in h],"head_arrivals":arrs,"chosen_arrival":self.head_arrival.get(cid,t),"pickup":pu,"unload":ar,"done":ar})
            self.schedule(pu,("sp",lane,cid,"out"));self.schedule(ar,("soa",cid));self.sb=ar
        return True

    def invariant(self,t):
        occ=[]
        for lane in range(1,7):occ += [x for x in self.lanes[lane][1:] if x is not None]
        occ += [x for x in self.ret[1:] if x is not None]
        if len(occ)!=len(set(occ)):self.violations.append(["duplicate_parking_occupancy",t])
        if any(sum(x is not None for x in self.lanes[l][1:])>10 for l in range(1,7)):self.violations.append(["lane_capacity",t])
        if sum(x is not None for x in self.ret[1:])>10:self.violations.append(["return_capacity",t])

    def run(self,max_t=12000):
        for t in range(max_t+1):
            self.mark_paint(t)
            while self.events.get(t):
                evs=self.events.pop(t)
                for ev in evs:self.process(t,ev)
            self.start_moves(t);self.invariant(t)
            changed=True;loop=0
            while changed and loop<20:
                loop+=1;changed=False;self.mark_paint(t)
                if t>=self.rb and self.receiver(t):changed=True
                if t>=self.sb and self.sender(t):changed=True
                if self.events.get(t):
                    evs=self.events.pop(t)
                    for ev in evs:self.process(t,ev)
                    self.start_moves(t);self.invariant(t);changed=True
            if len(self.output)==self.C:
                return score_sequence(self.output,self.recs,self.returns,t)
        raise RuntimeError("unfinished")

    def state_code(self,st):
        k=st[0]
        if k=="paint":return 0
        if k=="recv":return 1
        if k=="send":return 2
        if k=="assembly":return 3
        if k=="lane":return int(f"{st[1]}{st[2]}")
        if k=="ret":return int(f"7{st[1]}")
        return None

    def matrix_rows(self,T):
        rows=[]
        for cid in self.ids:
            row=[cid]+[None]*(T+1)
            for s,e,st in self.intervals[cid]:
                code=self.state_code(tuple(st))
                if code is not None:
                    for tt in range(max(0,s),min(T+1,e)):row[tt+1]=code
            st=self.states[cid];s=self.last_change[cid];code=self.state_code(st)
            if code is not None and s<=T:
                for tt in range(max(0,s),T+1):row[tt+1]=code
            rows.append(row)
        return rows

def run_case(snapshot_path,dataset,q):
    d=json.load(open(snapshot_path,encoding="utf-8"))
    sim=Sim(d[dataset],q,POLICIES[(dataset,q)])
    score=sim.run()
    return sim,score

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--snapshot",default="official_inputs_snapshot.json")
    ap.add_argument("--out",default="revised_execution.json")
    args=ap.parse_args()
    result={"runs":{}}
    for dataset in ["附件1","附件2"]:
        for q in [1,2]:
            sim,sc=run_case(args.snapshot,dataset,q)
            result["runs"][f"Q{q}_{dataset}"]={"score":sc,"output_sequence":sim.output,"actions":sim.actions,"violations":sim.violations,"return_counts_by_car":dict(sim.car_returns)}
    json.dump(result,open(args.out,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
if __name__=="__main__":main()
