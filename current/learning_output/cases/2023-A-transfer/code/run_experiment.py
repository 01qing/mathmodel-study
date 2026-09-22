from pathlib import Path
import json,statistics,time
from wlan import simulate,scenario
from analytic import bianchi,q2_exact,hidden_poisson,ideal_chain_csma

ROOT=Path(__file__).resolve().parents[1]
SEEDS=[101,202,303,404,505]
def main():
    configs=[]
    for q in [1,2,3,4]:
        configs.append((f'Q{q}_base',q,scenario(q)))
        if q>=3:
            for rate in [286.8,158.4]:
                for w,r in [(16,6),(32,5),(16,32)]:
                    p=scenario(q);p.update(rate=rate,cwmin=w,retries=r)
                    configs.append((f'Q{q}_{rate}_W{w}_r{r}',q,p))
    summaries=[]
    for name,q,params in configs:
        runs=[simulate(**params,seed=s,duration=10_000_000,warmup=500_000) for s in SEEDS]
        vals=[x['total_mbps'] for x in runs];mean=statistics.mean(vals)
        ci=2.776445105*statistics.stdev(vals)/len(vals)**.5
        row=dict(id=name,question=q,params=params,total_mean=mean,ci95_halfwidth=ci,
                 per_node_mean=[statistics.mean(x['mbps'][i] for x in runs) for i in range(params['n'])],
                 fairness_mean=statistics.mean(x['fairness'] for x in runs),runs=runs)
        (ROOT/'results'/f'{name}.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        summaries.append(row)
        print(name,round(mean,4),'+/-',round(ci,4),row['per_node_mean'],flush=True)
    (ROOT/'results/RESULTS.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
    (ROOT/'results/ANALYTIC.json').write_text(json.dumps(dict(q1=bianchi(),q2=q2_exact(),q3=hidden_poisson(),q4=ideal_chain_csma()),indent=2),encoding='utf-8')

if __name__=='__main__':main()
