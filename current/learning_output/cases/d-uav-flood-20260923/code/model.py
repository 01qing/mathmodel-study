"""Common deterministic physical model. Seconds, metres, kilograms, kWh."""
from pathlib import Path
import json, itertools, math
from functools import lru_cache
import numpy as np
import rasterio
from pyproj import Geod
from scipy.optimize import brentq

CASE=Path(__file__).resolve().parents[1]
ROOT=Path('D:/数模/数模练习/D题exp')
DATA=json.loads((CASE/'results/input_tables.json').read_text(encoding='utf-8'))
rows=DATA['调度中心与服务区']['数据']
NODES={r[0]:dict(id=r[0],name=r[1],lon=r[2],lat=r[3],z=r[4],pop=r[5] or 0) for r in rows if r[0] and (r[0]=='O01' or r[0].startswith('S0'))}
tr=DATA['运输无人机数据']['数据']
keys=['id','name','m0','Q','V','v','L0','LF','E','rho','prep','load','handoff','perbox','up','down','eta','downeta']
TYPES={r[0]:dict(zip(keys,r)) for r in tr[2:5]}
for g in TYPES.values(): g['rho']/=100
DRONES={g:[r[0] for r in tr if isinstance(r[0],str) and r[0].startswith('U') and r[1]==g] for g in TYPES}
BAT={r[0]:int(r[1]) for r in tr if r[0] in TYPES and isinstance(r[1],int)}
FULL={r[0]:r[2] for r in tr if r[0] in TYPES and isinstance(r[1],int)}
boxes=DATA['物资需求与配送时限']['逐箱货箱清单'][1:]
BOXES=[dict(id=r[0],node=r[1],kind=r[2],m=r[3],v=r[4],first=r[5]=='是',deadline=min([x for x in [r[6],r[7] if r[2]=='医疗物资' else None] if x is not None],default=1e9),due=r[7],weight=r[8]) for r in boxes]
GEOD=Geod(ellps='WGS84')
DS=rasterio.open(next(ROOT.rglob('*DEM.tif')))
DEM=DS.read(1); TF=DS.transform

def grid(lon,lat): return (lon-TF.c)/TF.a,(lat-TF.f)/TF.e
def terrain(lon,lat):
    x,y=grid(lon,lat); return float(DEM[min(max(int(y),0),DEM.shape[0]-1),min(max(int(x),0),DEM.shape[1]-1)])

def cells_on_line(a,b):
    """All intersected raster cells, including boundaries; each with entry/exit t."""
    x0,y0=grid(a[0],a[1]); x1,y1=grid(b[0],b[1]); dx=x1-x0; dy=y1-y0
    ts=[0.,1.]
    if abs(dx)>1e-12: ts.extend((np.arange(math.floor(min(x0,x1))+1,math.ceil(max(x0,x1)))-x0)/dx)
    if abs(dy)>1e-12: ts.extend((np.arange(math.floor(min(y0,y1))+1,math.ceil(max(y0,y1)))-y0)/dy)
    ts=np.unique(np.clip(ts,0,1)); tm=(ts[:-1]+ts[1:])/2
    cols=np.floor(x0+tm*dx).astype(int); rows=np.floor(y0+tm*dy).astype(int)
    if np.any(rows<0) or np.any(rows>=DEM.shape[0]) or np.any(cols<0) or np.any(cols>=DEM.shape[1]): raise ValueError('Outside DEM')
    return rows,cols,ts[:-1],ts[1:]

@lru_cache(None)
def leg(i,j):
    a,b=NODES[i],NODES[j]
    rows,cols,_,_=cells_on_line((a['lon'],a['lat']),(b['lon'],b['lat']))
    H=float(DEM[rows,cols].max())+50
    zi=a['z']+(30 if i!='O01' else 0); zj=b['z']+(30 if j!='O01' else 0)
    H=max(H,zi,zj)
    d=GEOD.inv(a['lon'],a['lat'],b['lon'],b['lat'])[2]
    return dict(i=i,j=j,d=d,H=H,hu=H-zi,hd=H-zj,zi=zi,zj=zj)

def leg_energy(g,L,q):
    t=TYPES[g]; ran=t['L0']-(t['L0']-t['LF'])*(q/t['Q'])**1.5
    return t['E']*L['d']/ran+(t['m0']+q)*9.80665*L['hu']/(3.6e6*t['eta'])
def leg_time(g,L):
    t=TYPES[g]; return L['hu']/t['up']+L['d']/t['v']+L['hd']/t['down']
def charge(g,e):
    use=TYPES[g]['E'] if g in TYPES else 3.2; full=FULL[g] if g in TYPES else 1800
    s=1-e/use
    return full*(.65*(.9-s)/.9+.35) if s<.9 else full*.35*(1-s)/.1
def capacity(g,node,rho=None):
    t=TYPES[g]; limit=(1-(rho if rho is not None else t['rho']))*t['E']
    f=lambda q:leg_energy(g,leg('O01',node),q)+leg_energy(g,leg(node,'O01'),0)-limit
    if f(0)>0:return -1.
    return t['Q'] if f(t['Q'])<=0 else brentq(f,0,t['Q'])

@lru_cache(maxsize=200000)
def route(g,ids,order=None,rho=None):
    ids=tuple(sorted(ids)); t=TYPES[g]; mass=sum(BOXES[k]['m'] for k in ids); volume=sum(BOXES[k]['v'] for k in ids)
    if mass>t['Q']+1e-8 or volume>t['V']+1e-8:return None
    nodes=sorted({BOXES[k]['node'] for k in ids})
    if len(nodes)>3:return None
    best=None
    for visit in ([tuple(order)] if order is not None else itertools.permutations(nodes)):
        elapsed=t['prep']+len(ids)*t['load']; energy=0.; load=mass; prev='O01'; delivery={}; legs=[]
        for n in (*visit,'O01'):
            L=leg(prev,n); e=leg_energy(g,L,load); ft=leg_time(g,L)
            legs.append(dict(**L,load=load,energy=e,t0=elapsed,t1=elapsed+ft))
            elapsed+=ft; energy+=e
            if n!='O01':
                unload=[k for k in ids if BOXES[k]['node']==n]
                elapsed+=t['handoff']+len(unload)*t['perbox']
                for k in unload: delivery[k]=elapsed
                load-=sum(BOXES[k]['m'] for k in unload)
            prev=n
        if energy>(1-(t['rho'] if rho is None else rho))*t['E']+1e-9:continue
        cand=dict(g=g,boxes=ids,order=visit,mass=mass,volume=volume,duration=elapsed,energy=energy,deliveries=delivery,legs=legs)
        key=(sum(BOXES[k]['weight']*delivery[k] for k in ids),energy,elapsed)
        if best is None or key<best[0]:best=(key,cand)
    return best[1] if best else None

def save(name,obj):
    (CASE/'results'/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda x:x.item() if hasattr(x,'item') else list(x)),encoding='utf-8')

if __name__=='__main__':
    print('types',TYPES,'drones',DRONES,'batteries',BAT)
    print('Total boxes,mass,volume',len(BOXES),sum(b['m'] for b in BOXES),sum(b['v'] for b in BOXES))
    print('Node terrain versus supplied altitude')
    for n,a in NODES.items():print(n,round(terrain(a['lon'],a['lat']),2),a['z'])
    print('Maximum payload')
    for n in list(NODES)[1:]:print(n,*(round(capacity(g,n),4) for g in TYPES))
    save('geometry.json',{f'{i}-{j}':leg(i,j) for i in NODES for j in NODES if i!=j})
