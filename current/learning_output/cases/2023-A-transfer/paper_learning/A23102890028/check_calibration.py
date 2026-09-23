"""Q4 scalar reconstruction and printed calibration audit; no author simulation."""
from pathlib import Path
import math,json,hashlib,statistics
HERE=Path(__file__).resolve().parent;CASE=HERE.parents[1];ROOT=HERE.parents[4]

def reconstruct(rate,w,r,k=1.76855):
    d=13.6+12240/rate; m=int(math.log2(1024/w));v=round((9+d)/36)
    def values(p):
        b=1/sum(p**i*(min(w*2**i,1024)+1)/2 for i in range(r+1))
        t1=b*sum(p**i for i in range(r+1))
        # As printed on p44: second sum ends at m, not r.
        t2=b*((v+1)*sum(p**i for i in range(m+1))-v*(v+1)/(2*w)*sum((p/2)**i for i in range(m+1)))
        return t1,t2
    def f(p):
        t1,t2=values(p)
        assert 0<=t1<=1 and 0<=t2<=1
        return 1-(1-t1)**1.8*(1-t2)**.8-p
    lo,hi=0.,1.;assert f(lo)*f(hi)<0
    for _ in range(90):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0:hi=mid
        else:lo=mid
    p=(lo+hi)/2;t1,t2=values(p);ptr=1-(1-t1)**3
    ps=3*t1*(1-t1)**1.5*(1-t2)**.5/ptr
    ts=d+91;tc=(9/2+d+65)/2+(d/2+d+65)/2
    s=ptr*ps*k*12000/((1-ptr)*9+ptr*ps*ts+ptr*(1-ps)*tc)
    assert abs(f(p))<1e-12 and 0<=ps<=1
    return dict(rate=rate,cwmin=w,retries=r,V=v,p=p,tau1=t1,tau2=t2,ps=ps,k=k,mbps=s,residual=abs(f(p)))

def main():
    reg=json.loads((CASE/'PAPER_MARKDOWN_REGISTRY.json').read_text(encoding='utf-8'))
    paper=next(x for x in reg['papers'] if x['paper_id']=='A23102890028'); hashes={}
    for kind in ('markdown','raw_layout'):
        digest=hashlib.sha256((ROOT/paper[kind+'_repo_path']).read_bytes()).hexdigest()
        assert digest==paper[kind+'_sha256'];hashes[kind]=digest
    params=[(455.8,16,32),(286.8,16,6),(286.8,32,5),(286.8,16,32),(158.4,16,6),(158.4,32,5),(158.4,16,32)]
    predictions=[116.54,105.60,98.66,105.60,87.61,83.76,87.61]
    simulations=[116.54,107.86,87.45,107.87,93.12,74.75,93.14]
    rows=[]
    for i,(config,pred,sim) in enumerate(zip(params,predictions,simulations)):
        result=reconstruct(*config)
        result.update(printed_prediction=pred,printed_simulation=sim,
          printed_simulation_rate=268.8 if i in (1,2,3) else config[0],
          parameter_identity_status='RATE_MISMATCH_UNRESOLVED' if i in (1,2,3) else 'MATCHED_PRINTED',
          role='CALIBRATION_NOT_VALIDATION' if i==0 else 'TRANSFER_CHECK',
          printed_signed_error_percent=100*(pred/sim-1),
          code_minus_printed_prediction=result['mbps']-pred,
          implied_k_from_printed_ratio=1.76855*sim/pred)
        if i in (1,2,3):result['alternative_268_8_code']=reconstruct(268.8,config[1],config[2])
        rows.append(result)
    eligible=[x for x in rows if x['role']=='TRANSFER_CHECK' and x['parameter_identity_status']=='MATCHED_PRINTED']
    # Shares explicitly chosen in text p35; verify weighted counts without fixing source.
    shares=[.25,.5,.25];nc=sum(a*b for a,b in zip(shares,[2,3,2]));nh=sum(a*b for a,b in zip(shares,[1,0,1]))
    assert nc==2.5 and nh==.5
    # Terminal-time branch counterexample only; max planned times is itself not
    # a general estimator of completed-event observation time.
    terminal=dict(planned_times=[100.,110.,200.],credited_bits=24000,
                  printed_denominator=max(100.,110.),three_clock_max=200.,
                  printed_ratio=24000/110,three_clock_ratio=24000/200,
                  status='synthetic branch input, not an observed simulation state')
    result=dict(scope='Q4 partial reading; local appendix formula reconstruction, no original author run',
      source_sha256=hashes,rows=rows,
      strict_transfer_mape_percent=statistics.mean(abs(x['printed_signed_error_percent']) for x in eligible),
      strict_transfer_count=len(eligible),excluded_transfer_rows_due_to_rate_conflict=3,
      weighted_node_counts=dict(text_weights=shares,calculated_nc=nc,calculated_nh=nh,
           converted_text_nc=2/3,converted_text_nh=7/3,code_failure_exponents=[1.8,.8],code_success_exponents=[1.5,.5]),
      terminal_time_probe=terminal,
      caution='Printed min/max simulation intervals are not confidence intervals; calibrated-point agreement is not independent validation.')
    (HERE/'CALIBRATION_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(rows=rows,strict_transfer_mape_percent=result['strict_transfer_mape_percent'],weighted_node_counts=result['weighted_node_counts']),ensure_ascii=False))

if __name__=='__main__':main()
