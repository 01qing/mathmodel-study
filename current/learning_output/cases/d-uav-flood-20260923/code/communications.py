from model import *

GW=np.array([NODES['O01']['lon'],NODES['O01']['lat'],NODES['O01']['z']+20])
LIMITS={'direct':122.,'access':116.,'backhaul':126.}
RANGES={key:10**((val-32.45-20*math.log10(2400))/20)*1000 for key,val in LIMITS.items()}

def link(a,b,kind):
    d=math.hypot(GEOD.inv(a[0],a[1],b[0],b[1])[2],a[2]-b[2])
    free=32.45+20*math.log10(2400)+20*math.log10(max(d,1e-8)/1000)
    if free+10<=LIMITS[kind]:return True,LIMITS[kind]-free-10,True
    if free>LIMITS[kind]:return False,LIMITS[kind]-free,False
    rr,cc,t0,t1=cells_on_line(a,b)
    low=np.minimum(a[2]+(b[2]-a[2])*t0,a[2]+(b[2]-a[2])*t1)
    blocked=bool(np.any(DEM[rr,cc]>low+1e-8))
    return free+10*blocked<=LIMITS[kind],LIMITS[kind]-free-10*blocked,blocked

def route_segments(r):
    """Exact piecewise affine trajectory, relative seconds, including handoffs."""
    g=TYPES[r['g']]; seg=[]
    for h,L in enumerate(r['legs']):
        a,b=NODES[L['i']],NODES[L['j']]; t=L['t0']
        p0=[a['lon'],a['lat'],L['zi']]; p1=[a['lon'],a['lat'],L['H']]; p2=[b['lon'],b['lat'],L['H']]; p3=[b['lon'],b['lat'],L['zj']]
        for stage,pa,pb,dt in [('爬升',p0,p1,L['hu']/g['up']),('巡航',p1,p2,L['d']/g['v']),('下降',p2,p3,L['hd']/g['down'])]:
            if dt>1e-9:seg.append(dict(stage=stage,a=pa,b=pb,t0=t,t1=t+dt));t+=dt
        if L['j']!='O01':
            end=r['legs'][h+1]['t0']
            seg.append(dict(stage='投送',a=p3,b=p3,t0=t,t1=end))
    return seg

def relay_travel(p):
    o=NODES['O01']; a=[o['lon'],o['lat'],o['z']]
    rr,cc,_,_=cells_on_line(a,p); H=max(float(DEM[rr,cc].max())+50,a[2],p[2])
    d=GEOD.inv(a[0],a[1],p[0],p[1])[2]
    outbound=(H-a[2])/4+d/15+(H-p[2])/3
    inbound=(H-p[2])/4+d/15+(H-a[2])/3
    energy=1.15*2*d/15/3600+23.5*9.80665*(2*H-a[2]-p[2])/(3.6e6*.72)
    return dict(outbound=outbound,inbound=inbound,flight_energy=energy,H=H,d=d)

if __name__=='__main__':
    pts=[np.array([n['lon'],n['lat'],n['z']+30]) for k,n in NODES.items() if k!='O01']
    direct=[link(p,GW,'direct')[0] for p in pts]
    print('ranges',RANGES,'direct sites',direct,flush=True)
    candidates=[]
    for lon in np.linspace(109.175,109.28,27):
        for lat in np.linspace(23.015,23.075,21):
            p=[float(lon),float(lat),terrain(lon,lat)+300]
            if not link(p,GW,'backhaul')[0]:continue
            cover=[link(q,p,'access')[0] for q in pts]
            if sum(cover)>3:candidates.append(dict(p=p,cover=cover,travel=relay_travel(p)))
    best=[]
    for i,c in enumerate(candidates):
        for j in range(i+1,len(candidates)):
            v=candidates[j]
            if all(a or b or d for a,b,d in zip(c['cover'],v['cover'],direct)):
                score=sum(a and b and not d for a,b,d in zip(c['cover'],v['cover'],direct))*-100 + c['travel']['outbound']+v['travel']['outbound']
                best.append((score,i,j))
    best.sort(); print('candidates',len(candidates),'pairs',len(best),flush=True)
    save('relay_candidates.json',candidates);save('relay_pairs.json',best[:100])
    for score,i,j in best[:5]: print(score,candidates[i],candidates[j],flush=True)
