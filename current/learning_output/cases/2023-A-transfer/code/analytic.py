"""Finite-retry fixed point, and an exact Q2 residual-counter renewal chain."""
import math

def attempt_probability(p,w=16,cap=1024,r=32):
    weights=[p**i for i in range(r+1)]
    return 2*sum(weights)/sum(v*(min(cap,w*2**i)+1) for i,v in enumerate(weights))

def bianchi(rate=455.8,w=16,cap=1024,r=32,n=2):
    lo,hi=0.,1.
    for _ in range(90):
        p=(lo+hi)/2;tau=attempt_probability(p,w,cap,r)
        if p>1-(1-tau)**(n-1):hi=p
        else:lo=p
    p=(lo+hi)/2;tau=attempt_probability(p,w,cap,r)
    p0=(1-tau)**n;ps=n*tau*(1-tau)**(n-1);pc=1-p0-ps
    d=13.6+1530*8/rate;ts=d+48+43;tc=d+65+43
    return dict(p=p,tau=tau,idle=p0,success=ps,collision=pc,total_mbps=ps*12000/(p0*9+ps*ts+pc*tc),Ts=ts,Tc=tc)

def q2_exact(w=16,rate=275.3):
    # State is absolute residual difference immediately after a successful busy epoch.
    # Equal counters produce two successes; otherwise the smaller counter wins.
    # Transition: draw fresh U in [0,w-1], then next residual is |U-d|.
    # d=0 means both redraw independently. Embedded epoch includes min backoff.
    P=[[0.]*w for _ in range(w)];reward=[0.]*w;idle=[0.]*w
    for d in range(w):
        pairs=[(a,b,1/w**2) for a in range(w) for b in range(w)] if d==0 else [(a,d,1/w) for a in range(w)]
        for a,b,prob in pairs:
            P[d][abs(a-b)]+=prob;reward[d]+=prob*(2 if a==b else 1);idle[d]+=prob*min(a,b)*9
    pi=[1/w]*w
    for iteration in range(100000):
        nxt=[sum(pi[i]*P[i][j] for i in range(w)) for j in range(w)]
        if max(abs(a-b) for a,b in zip(pi,nxt))<1e-15:pi=nxt;break
        pi=nxt
    ts=13.6+1530*8/rate+48+43
    throughput=12000*sum(a*b for a,b in zip(pi,reward))/(ts+sum(a*b for a,b in zip(pi,idle)))
    tau=2/(w+1);p0=(1-tau)**2
    approx=2*tau*12000/(p0*9+(1-p0)*ts)
    return dict(total_mbps=throughput,decoupled_mbps=approx,stationary=pi,iterations=iteration,
                stationary_residual=max(abs(sum(pi[i]*P[i][j] for i in range(w))-pi[j]) for j in range(w)),
                mean_payloads_per_epoch=sum(a*b for a,b in zip(pi,reward)),mean_idle_us=sum(a*b for a,b in zip(pi,idle)))

def hidden_poisson(rate=455.8,w=16,cap=1024,r=32,pe=.1):
    """Exploratory renewal/Poisson closure; not exact for coupled hidden senders."""
    d=13.6+1530*8/rate
    def cycle(p):
        weights=[p**i for i in range(r+1)]
        backoff=sum(v*(min(cap,w*2**i)-1)/2 for i,v in enumerate(weights))/sum(weights)
        return d+43+48*(1-p)+65*p+9*backoff
    lo,hi=0.,1.
    for _ in range(90):
        p=(lo+hi)/2
        residual=p-(1-(1-pe)*math.exp(-2*d/cycle(p)))
        if residual>0:hi=p
        else:lo=p
    p=(lo+hi)/2
    return dict(p=p,mean_attempt_cycle_us=cycle(p),total_mbps=2*12000*(1-p)/cycle(p),assumption='Poisson interfering starts; exploratory closure only')

def ideal_chain_csma(rate=455.8,w=16):
    """Ideal collision-free exponential activity-chain baseline for Q4."""
    exchange=13.6+1530*8/rate+48;idle=43+9*(w-1)/2
    rho=exchange/idle;z=1+3*rho+rho*rho
    per=[12000*(rho+rho*rho)/z/exchange,12000*rho/z/exchange,12000*(rho+rho*rho)/z/exchange]
    return dict(per_node_mbps=per,total_mbps=sum(per),rho=rho,assumption='Exponential backoff and holding times, no collisions, no retry stages; idealized baseline')

if __name__=='__main__':print(bianchi());print(q2_exact());print(hidden_poisson());print(ideal_chain_csma())
