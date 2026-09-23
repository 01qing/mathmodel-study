"""Scoped reconstructions; never a full original author-program replay."""
from pathlib import Path
import json, math
BASE=Path(__file__).resolve().parent
CONFIGS=[(455.8,16,32),(286.8,16,6),(286.8,32,5),(286.8,16,32),(158.4,16,6),(158.4,32,5),(158.4,16,32)]
def tau(p,w,r):
    return 2*sum(p**i for i in range(r+1))/sum(p**i*(min(w*2**i,1024)+1) for i in range(r+1))
def root(f,a=0.,b=.49):
    assert f(a)*f(b)<0
    for _ in range(100):
        c=(a+b)/2
        if f(a)*f(c)<=0:b=c
        else:a=c
    return (a+b)/2
def timing(rate):
    d=13.6+12240/rate
    return d,d+91,d+108
def save(pid,data):
    d=BASE/pid;d.mkdir(exist_ok=True)
    (d/'CHECKS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def seventh():
    t=root(lambda x:tau(x,16,32)-x)
    _,ts,tc=timing(275.3)
    q2=dict(tau=t,body=2*t*12000/((1-t)**2*9+(2*t-t*t)*ts),appendix=2*t*12000/((1-t)**2*9+t*t*tc+(2*t-2*t*t)*ts),no_failure_independent=2*(2/17)*12000/((1-2/17)**2*9+(4/17-(2/17)**2)*ts))
    q3=[];q4=[]
    for rate,w,r in CONFIGS:
        d,ts,tc=timing(rate);n=math.ceil(d/9);t=tau(.1,w,r)
        q3.append(dict(rate=rate,w=w,r=r,tau=t,n=n,appendix=2*t*(1-t)**n*.9*12000/((1-t)*9+t*(1-t)**n*.9*ts+t*(1-(1-t)**n)*.9*tc+t*.1*tc)))
        a=root(lambda x:tau(x,w,r)-x);b=root(lambda x:1-(1-tau(x,w,r))**2-x);b=tau(b,w,r)
        def calc(code):
            z=(1-a)**n
            p=[a*(1-b)*z,a*(1-b)*(1-z),a*b*(z if code else 1-a),a*b*((1-z) if code else a),(1-a)*(1-b)*(1-a),(1-a)*(1-b)*a,(1-a)*b*(z if code else 1-a),(1-a)*b*((1-z) if code else a)]
            den=sum(pi*di for pi,di in zip(p,[ts,ts,tc,tc,9,ts,ts,tc]))
            return 12000*(p[0]+2*p[1]+p[5]+p[6])/den
        q4.append(dict(rate=rate,w=w,r=r,body=calc(False),appendix_without_ta=calc(True),appendix_ta_1_55=calc(True)*1.55))
    rounding=[]
    for rate in [455.8,286.8,158.4]:
        h=math.floor(240/rate+13.6*100+.5)/100
        rounding.append(dict(rate=rate,literal_H=h,correct_H=13.6+240/rate))
    rmse=[dict(question=1,prediction=67.174,reported_mean=65.530,rmse_lower_bound_if_same_mean=1.644,reported_rmse=.266),dict(question=2,prediction=67.936,reported_mean=67.250,rmse_lower_bound_if_same_mean=.686,reported_rmse=.010)]
    save('A23103360079',dict(scope='local scalar and isolated operator reconstruction; no full MATLAB/App replay',q2=q2,q3=q3,q4=q4,rounding=rounding,rmse=rmse,backoff=[dict(stage=i,literal_upper=2*i*15,required_upper=min(16*2**i,1024)-1) for i in range(1,7)]))
def eighth():
    t=(-7.5+math.sqrt(7.5**2+4))/2;_,ts,_=timing(275.3)
    q2=dict(tau=t,throughput=2*t*12000/((1-t)**2*9+(2*t-t*t)*ts),initial_backoff_support=list(range(0,15)),required_support=list(range(16)))
    q4=[]
    for rate,w,r in CONFIGS:
        a=.1;b=.1
        for _ in range(1000):a,b=tau(b,w,r),tau(1-(1-a)**2,w,r)
        ptr=1-(1-a)*(1-b);ps=(2*(1-b)*a+(1-a)*b)/ptr
        _,ts,tc=timing(rate)
        assert ps>1
        q4.append(dict(rate=rate,w=w,r=r,tau_outer=a,tau_center=b,Ps=ps,collision_weight=ptr*(1-ps),scope='finite-sum closure; appendix parenthesis drift not silently adopted'))
    pf=[.2291,.2558,.1963,.2502,.2770,.2343,.2961]
    probability=[dict(table_pf=p,table_tau2=p,required_pf=.1+.9*p,residual=p-(.1+.9*p)) for p in pf]
    # Deterministic data overlap with an interferer ending before source completes.
    collision=dict(source_interval=[0,41],interferer_interval=[0,20],noise=False,positive_overlap=True,source_completion_time=89,appendix_current_channel_success=True,required_sticky_failure=True)
    save('A23103840031',dict(scope='local scalar and isolated event probes; no original full Python simulation',q2=q2,q3_table_probability=probability,q4=q4,collision_latch_probe=collision))
def ninth():
    t=2/17;_,ts,_=timing(275.3)
    a=.1046;b=.0934;q=.9326
    s1=b*(1-a)**2;s2=a*a*(1-b);s3=2*a*(1-a)*(1-b)*(1-q);s4=2*a*(1-a)*(1-b)*q
    q4=dict(center_only=s1,outer_simultaneous=s2,outer_single=s3,outer_overlap=s4,
            printed_reward=2*s1+s2+s3+2*s4,event_count_reward=s1+2*s2+s3+2*s4)
    touching=dict(interval1=[0,41],interval2=[41,82],positive_overlap=False,literal_strict_separation_branch_collision=True)
    wake=dict(initial=[200,200],horizon=100,literal_if_elseif_updated_nodes=1,independent_conditions_updated_nodes=2,reachability='isolated branch probe, not full trajectory')
    assert q4['printed_reward']!=q4['event_count_reward']
    save('A23104860166',dict(scope='scalar and isolated boundary checks; no original MATLAB replay',q2=dict(literal_tau=2/16+1,required_tau=t,independent_throughput=2*t*12000/((1-t)**2*9+(2*t-t*t)*ts)),q3_vulnerability=dict(data_slots=math.ceil(timing(455.8)[0]/9),exchange_slots=math.ceil(timing(455.8)[1]/9),printed_exchange_slots=7),q4_reward=q4,touching_probe=touching,wakeup_probe=wake))

def tenth():
    def poly(x):return 2050*x**35-1029*x**34+2*x**33-1024*x**8-18*x*x+21*x-2
    roots=[dict(p=p,cleared_polynomial=poly(p),finite_sum_tau=tau(p,16,32),original_residual=tau(p,16,32)-p) for p in [.10462063228196894,.5,1.]]
    assert abs(roots[0]['original_residual'])<1e-12
    assert all(abs(x['original_residual'])>.1 for x in roots[1:])
    pairs=[(67.174,62.389,455.8),(70.562,66.139,275.3),(31.269,45.283,455.8),(98.567,110.627,455.8)]
    metrics=[dict(question=i+1,theory=a,simulation=b,efficiency_difference_percentage_points=abs(a-b)/rate*100,relative_error_percent=abs(a-b)/b*100) for i,(a,b,rate) in enumerate(pairs)]
    pf=.46479313254;t=.057893
    save('A23105330383',dict(scope='scalar consistency checks; no original C++ or optimization replay',root_checks=roots,q3=dict(reported_pf=pf,reported_tau=t,finite_sum_tau=tau(pf,16,32),reported_Ptr=.0845,Ptr_from_reported_tau=1-(1-t)**2),error_metrics=metrics,backoff=dict(standard_mean_us=7.5*9,plus_one_mean_us=8.5*9),payload=dict(required_bits=12000,q3_code_bits=10000,reward_ratio=10/12),export=dict(counter_kilobits=12,literal_times_100_bits=1200,correct_times_1000_bits=12000)))

if __name__=='__main__':
    seventh();eighth();ninth();tenth();print('Saved scoped checks for remaining four papers')
