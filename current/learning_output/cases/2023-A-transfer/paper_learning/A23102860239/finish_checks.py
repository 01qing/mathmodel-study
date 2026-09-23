"""Local formula/table checks for the fifth review; not author-code execution."""
from pathlib import Path
import json, statistics

HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]


def attempt(p,w=16,r=32):
    mass=sum(p**i for i in range(r+1))
    denominator=sum(p**i*(min(w*2**i,1024)+1)/2 for i in range(r+1))
    return mass/denominator,1/denominator


def bisect(f):
    lo,hi=0.,1.
    assert f(lo)*f(hi)<0
    for _ in range(100):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0:hi=mid
        else:lo=mid
    return (lo+hi)/2


def main():
    q2=[]
    t=2/17; ptr=1-(1-t)**2;single=2*t*(1-t);double=t*t
    for rate in (275.3,455.8):
        ts=13.6+12240/rate+91
        literal=(single+double)*12000/((1-ptr)*9+single*ts)
        corrected=(single+2*double)*12000/((1-ptr)*9+ptr*ts)
        q2.append(dict(rate=rate,literal_eq4_8_mbps=literal,
                       corrected_independent_mbps=corrected,
                       printed_table_mbps=70.5586))
    assert abs(q2[0]['corrected_independent_mbps']-70.5586)<.001
    assert abs(q2[0]['literal_eq4_8_mbps']-70.5586)>.1
    # Q4 equations 6.1-6.6 only; no reconstruction of missing throughput equations.
    t1=bisect(lambda x:attempt(attempt(1-(1-x)**2)[0])[0]-x)
    p2=1-(1-t1)**2;t2,b2=attempt(p2);p1=t2;_,b1=attempt(p1)
    residual=max(abs(t1-attempt(p1)[0]),abs(t2-attempt(p2)[0]))
    assert residual<1e-12
    q4=dict(tau1=t1,tau2=t2,p1=p1,p2=p2,b001=b1,b002=b2,residual=residual)
    for name,value in [('tau1',.106730),('tau2',.089277),('p2',.202069),('b001',.097202),('b002',.071237)]:
        assert abs(q4[name]-value)<1e-6,(name,q4[name])

    # Seven columns transcribed from p44 table5-4, in printed parameter order.
    theoretical=[46.986,40.161,45.9061,36.113,31.886,36.718,54.573]
    simulated=[45.557,37.533,45.510,35.126,28.234,36.495,54.576]
    nmse=[9.2497e-4,.0043,7.4451e-5,7.4698e-4,.0131,3.6885e-5,3.0219e-9]
    configs=list(zip([286.8]*3+[158.4]*3+[455.8],[16,32,16,16,32,16,16],[6,5,32,6,5,32,32]))
    frozen=json.loads((CASE/'results/RESULTS.json').read_text(encoding='utf-8'))
    rows=[]
    for i,((rate,w,r),a,s,n) in enumerate(zip(configs,theoretical,simulated,nmse),1):
        match=next(x for x in frozen if x['question']==3 and x['params']['rate']==rate and x['params'].get('cwmin',16)==w and x['params'].get('retries',32)==r)
        current=match['total_mean']
        rows.append(dict(column=i,rate=rate,cwmin=w,retries=r,author_theory=a,
             author_simulation=s,printed_nmse=n,point_squared_relative_error=((s-a)/a)**2,
             relative_theory_error_vs_author_sim_percent=100*(a/s-1),
             frozen_simulation=current,relative_theory_error_vs_frozen_percent=100*(a/current-1),
             author_sim_minus_frozen_mbps=s-current))
    grouped={str(w):dict(count=sum(x['cwmin']==w for x in rows),
       mape_vs_author_sim_percent=statistics.mean(abs(x['relative_theory_error_vs_author_sim_percent']) for x in rows if x['cwmin']==w),
       mape_vs_frozen_sim_percent=statistics.mean(abs(x['relative_theory_error_vs_frozen_percent']) for x in rows if x['cwmin']==w)) for w in (16,32)}
    result=dict(scope='local scalar reconstruction and seven printed parameter columns; author simulator not run',
         q2=q2,q4_attempt_closure=q4,q3_parameter_rows=rows,q3_window_groups=grouped,
         caution='Different simulator semantics; comparison with frozen simulation is diagnostic, not ground truth; missing formulas remain unreconstructed.')
    (HERE/'FINAL_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
