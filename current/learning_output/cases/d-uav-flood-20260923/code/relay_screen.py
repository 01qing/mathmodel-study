from communications import *
import time

def path_samples(i,j,step=50):
    L=leg(i,j);a=NODES[i];b=NODES[j]
    p0=np.array([a['lon'],a['lat'],L['zi']]);p1=np.array([a['lon'],a['lat'],L['H']]);p2=np.array([b['lon'],b['lat'],L['H']]);p3=np.array([b['lon'],b['lat'],L['zj']])
    pts=[]
    for x,y,d in [(p0,p1,L['hu']),(p1,p2,L['d']),(p2,p3,L['hd'])]:
        for t in np.linspace(0,1,max(2,math.ceil(d/step)+1)):pts.append(x+(y-x)*t)
    return pts

if __name__=='__main__':
    cand=json.loads((CASE/'results/relay_candidates.json').read_text());nodes=list(NODES)[1:]
    needed={n:[p for p in path_samples('O01',n,40)+path_samples(n,'O01',40) if not link(p,GW,'direct')[0]] for n in nodes}
    result=[]
    for ix,c in enumerate(cand):
        cover=[]
        for k,n in enumerate(nodes):cover.append(c['cover'][k] and all(link(p,c['p'],'access')[0] for p in needed[n]))
        result.append(dict(**c,index=ix,path_cover=cover))
        if ix%100==0:print(ix,flush=True)
    save('relay_screen.json',result)
    for n in nodes:
        k=nodes.index(n);r=max(result,key=lambda c:sum(c['path_cover'])*c['path_cover'][k]);print(n,r['index'],[nodes[j] for j,v in enumerate(r['path_cover']) if v],flush=True)
