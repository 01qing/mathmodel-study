"""Q3 selected-section reproduction from converted pp18-24 and47-48.
Eliminate b00 and tau analytically, then solve a scalar equation. This is our
Python implementation, not execution of the original MATLAB. No fitted values.
"""
from pathlib import Path
import math,json,sys,hashlib
HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
sys.path.insert(0,str(CASE/'code'))
from analytic import hidden_poisson

def state_terms(failure,rate=455.8,w=16,cap=1024,r=32):
    d=13.6+12240/rate;ts=d+91;tc=d+108;n=d/9
    widths=[min(cap,w*2**i) for i in range(r+1)]
    weights=[failure**i for i in range(r+1)]
    b00=1/sum(v*(width+3)/2 for v,width in zip(weights,widths))
    tau=b00*sum(weights)
    # Terms p1..p5 follow appendix main3. k=ceil(n) and fractional floor term.
    # Tested parameter grid has noninteger n and n<w. Generalization needs
    # piecewise clipping and separate integer-n treatment, not silently reused.
    assert n<w and abs(n-round(n))>1e-10 and ts>=2*d and tc>=2*d
    pieces=[0.]*5
    for v,width in zip(weights,widths):
        b=v*b00
        pieces[0]+=(1-failure)*b*(ts-2*d)/ts
        pieces[1]+=(1-failure)*b*d/ts*(1-n/(2*w))
        pieces[2]+=failure*b*(tc-2*d)/tc
        pieces[3]+=failure*b*d/tc*(1-n/(2*width))
        k=math.ceil(n);l=math.floor(n)
        pieces[4]+=b*((width-k+1)*(width-k)/(2*width)+(1-(n-l))*(width-l)/width)
    overlap=1-sum(pieces)
    return dict(b00=b00,tau=tau,overlap=overlap,no_overlap_terms=pieces,Ts=ts,Tc=tc,data_time=d)

def solve(rate=455.8,w=16,cap=1024,r=32,pe=.1,mode='body'):
    def residual(f):
        t=state_terms(f,rate,w,cap,r)
        return f-(pe+(1-pe)*t['overlap']) if mode=='body' else f-t['tau']
    # Scan all sign changes; do not assume the numerically found root is unique.
    roots=[];lo=0.;a=residual(lo)
    for i in range(1,1001):
        hi=i/1000;b=residual(hi)
        if a*b<0:
            left,right=lo,hi
            for _ in range(65):
                mid=(left+right)/2
                if residual(left)*residual(mid)<=0:right=mid
                else:left=mid
            roots.append((left+right)/2)
        lo=hi;a=b
    assert len(roots)==1,roots
    f=roots[0];t=state_terms(f,rate,w,cap,r)
    # Body equation (5.22) final line uses union probability of noise/overlap.
    effective=pe+(1-pe)*t['overlap'];tau=t['tau']
    s=2*tau*(1-effective)*12000/((1-tau)*9+tau*(1-effective)*t['Ts']+tau*effective*t['Tc'])
    assert 0<=t['overlap']<=1 and 0<=effective<=1
    return dict(mode=mode,stage_failure=f,effective_failure=effective,closure_residual=residual(f),
                body_failure_consistency=f-effective,total_mbps=s,roots_found_by_scan=len(roots),**t)

def main():
    baseline=json.loads((CASE/'results/RESULTS.json').read_text(encoding='utf-8'))
    rows=[]
    for row in baseline:
        if row['question']!=3:continue
        p=row['params'];params=dict(rate=p.get('rate',455.8),w=p.get('cwmin',16),cap=p.get('cwmax',1024),r=p.get('retries',32))
        body=solve(**params);active=solve(**params,mode='appendix_active');simple=hidden_poisson(**params)
        truth=row['total_mean']
        # Diagnostic only: reproduces commented solve3 expression that omits p*pe.
        additive_failure=body['overlap']+.1;t=body['tau']
        additive_s=2*t*(1-additive_failure)*12000/((1-t)*9+t*(1-additive_failure)*body['Ts']+t*additive_failure*body['Tc'])
        rows.append(dict(id=row['id'],params=params,simulation_reference_mbps=truth,
                    reference_ci_halfwidth=row['ci95_halfwidth'],body=body,appendix_active_plus_body_reward=active,
                    additive_noise_reward_diagnostic_mbps=additive_s,
                    poisson=simple,body_relative_error=(body['total_mbps']/truth-1),
                    poisson_relative_error=(simple['total_mbps']/truth-1)))
    summary=dict(body_mape=sum(abs(x['body_relative_error']) for x in rows)/len(rows),
                 poisson_mape=sum(abs(x['poisson_relative_error']) for x in rows)/len(rows),
                 body_worst_absolute_relative_error=max(abs(x['body_relative_error']) for x in rows))
    for w in [16,32]:
        subset=[x for x in rows if x['params']['w']==w]
        summary[f'W{w}']=dict(count=len(subset),body_mape=sum(abs(x['body_relative_error']) for x in subset)/len(subset),
                            poisson_mape=sum(abs(x['poisson_relative_error']) for x in subset)/len(subset))
    # Transcribed p28 Table5.2 values. Their labels differ from the six appendix6
    # parameter configurations that produce these values under additive noise.
    printed=[44.760,41.012,44.762,32.515,30.787,32.678]
    shifted=[]
    for row,value in zip(rows[1:],printed):
        shifted.append(dict(computed_configuration=row['id'],paper_printed_mbps=value,
                            diagnostic_minus_printed_mbps=row['additive_noise_reward_diagnostic_mbps']-value))
    assert all(abs(x['diagnostic_minus_printed_mbps'])<.0006 for x in shifted)
    out=dict(scope='selected Q3 sections; our reconstruction, not original MATLAB execution',
      sources={str(p.relative_to(CASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CASE/'results/RESULTS.json',CASE/'code/analytic.py',Path(__file__)]},
      clarification='Appendix active solve3 has no active throughput output; its model plus body reward is our diagnostic combination.',
      independent_new_simulations=0,comparison='same-problem retrospective; frozen existing event simulation is a model reference, not physical truth',
      table5_2_shifted_configuration_diagnostic=shifted,rows=rows,summary=summary)
    (HERE/'Q3_STATE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    for x in rows:print(x['id'],round(x['body']['total_mbps'],5),round(x['body_relative_error']*100,3))
    print(summary)

if __name__=='__main__':main()
