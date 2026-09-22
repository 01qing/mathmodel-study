from pathlib import Path
import json,copy,statistics
from wlan import simulate,scenario
from analytic import bianchi,q2_exact,attempt_probability
from check_trace import check_trace
ROOT=Path(__file__).resolve().parents[1]
checks=[]
rate=455.8;single=12000/(13.6+1530*8/rate+48+43+7.5*9)
s=simulate(n=1,rate=rate,duration=5e6,seed=929)
assert abs(s['total_mbps']/single-1)<.01
checks.append(dict(name='single_node_renewal',pass_=True,exact=single,simulation=s['total_mbps']))
p=dict(n=2,hear=[[False]*2 for _ in range(2)],interfere=[[False]*2 for _ in range(2)])
s=simulate(**p,duration=5e6,seed=929)
assert abs(s['total_mbps']/(2*single)-1)<.01
checks.append(dict(name='two_independent_links',pass_=True,exact=2*single,simulation=s['total_mbps']))
s=simulate(n=1,pe=1,retries=2,duration=1e5,trace=True)
assert sum(s['successes'])==0 and sum(s['drops'])>0
assert check_trace(s,dict(n=1,pe=1,retries=2))['status']=='PASS'
checks.append(dict(name='certain_loss_retry_reset',pass_=True))
a=bianchi();assert abs(a['p']-(1-(1-a['tau'])**1))<1e-12
assert abs(attempt_probability(0)-2/17)<1e-14
checks.append(dict(name='finite_retry_fixed_point_limits',pass_=True))
a=q2_exact();assert a['stationary_residual']<1e-12 and abs(sum(a['stationary'])-1)<1e-12
checks.append(dict(name='q2_stationary_chain',pass_=True))
for q in [1,2,3,4]:
    p=scenario(q);s=simulate(**p,duration=100000,warmup=10000,trace=True)
    report=check_trace(s,p);assert report['status']=='PASS',report
    (ROOT/'results'/f'trace_Q{q}.json').write_text(json.dumps(dict(params=p,result=s,check=report),indent=2),encoding='utf-8')
    checks.append(dict(name=f'q{q}_independent_event_reconstruction',pass_=True,report=report))
for kind in ['backoff','outcome','stage']:
    x=copy.deepcopy(s)
    if kind=='backoff':x['trace'][5]['backoff']+=1;label='frozen_backoff'
    elif kind=='outcome':x['trace'][5]['success']=not x['trace'][5]['success'];label='collision_outcome'
    else:x['trace'][5]['stage']+=1;label='stage'
    report=check_trace(x,p);assert any(e['check']==label for e in report['errors']),report
    checks.append(dict(name='reject_tampered_'+kind,pass_=True))
p=scenario(4);p['sense_mode']='data_only';s=simulate(**p,duration=100000,warmup=10000,trace=True)
report=check_trace(s,p);assert report['status']=='PASS',report
checks.append(dict(name='data_only_sensing_alternative_trace',pass_=True,report=report))
(ROOT/'results/TESTS.json').write_text(json.dumps(dict(status='PASS',checks=checks),indent=2),encoding='utf-8')
print('PASS',len(checks),'model tests')
