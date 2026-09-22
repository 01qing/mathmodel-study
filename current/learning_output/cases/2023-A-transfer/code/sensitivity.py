from pathlib import Path
import json,statistics
from wlan import simulate,scenario
ROOT=Path(__file__).resolve().parents[1]
configs=[]
p=scenario(3);p['pe']=0;configs.append(('Q3_no_channel_loss',p))
p=scenario(4);p['interfere']=[[False]*3 for _ in range(3)];configs.append(('Q4_all_concurrent_data_succeed',p))
for q in [1,2,4]:
    p=scenario(q);p['sense_mode']='data_only';configs.append((f'Q{q}_data_only_carrier',p))
results=[]
for name,p in configs:
    runs=[simulate(**p,seed=s,duration=5e6,warmup=5e5) for s in [101,202,303,404,505]]
    totals=[x['total_mbps'] for x in runs]
    results.append(dict(id=name,params=p,total_mean=statistics.mean(totals),
        ci95_halfwidth=2.776445105*statistics.stdev(totals)/5**.5,
        per_node_mean=[statistics.mean(x['mbps'][i] for x in runs) for i in range(p['n'])],runs=runs))
    print(name,results[-1]['total_mean'],flush=True)
(ROOT/'results/SENSITIVITY.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
