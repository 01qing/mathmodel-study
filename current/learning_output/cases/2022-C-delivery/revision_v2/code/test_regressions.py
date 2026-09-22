from pathlib import Path
import json,copy
from solve import run
from validate import validate,score

ROOT=Path(__file__).resolve().parents[1]
inputs=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
checks=[]
for n in [1,2,10,30,318]:
    sim,s=run(inputs['附件1'][:n],1,{k:[4] for k in ['H2','F2','F4']})
    assert s['T']==9*n+72
    rows=sim.matrix_rows(s['T']);assert rows[0][1]==410 and rows[0][2] is None
    checks.append({'check':f'lane4_{n}_cars','T':s['T'],'passed':True})
ds='442242444224'
records=[{'进车顺序':i+1,'动力':'燃油','驱动':'四驱' if d=='4' else '两驱'} for i,d in enumerate(ds)]
assert score(list(range(1,len(ds)+1)),records,9*len(ds)+72)['dbad']==2
checks.append({'check':'official_drive_partition_example','passed':True})
r=json.loads((ROOT/'results/result11.json').read_text(encoding='utf-8'))
m=json.loads((ROOT/'results/result11_matrix.json').read_text())
for kind in ['score','movement','parking_duplicate']:
    rr=copy.deepcopy(r);mm=copy.deepcopy(m)
    if kind=='score':rr['score']['total']+=1
    elif kind=='movement':rr['movements'][0]['end']+=1
    else:mm[1][1]=410;mm[2][1]=410
    out=validate(rr,inputs['附件1'],mm)
    expected={'score':'independent_score','movement':'independent_fifo_recurrence','parking_duplicate':'no_duplicate_regions'}[kind]
    assert any(e['check']==expected for e in out['errors']),out
    checks.append({'check':'reject_tampered_'+kind,'passed':True,'detected':expected})
(ROOT/'results/REGRESSION_TESTS.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2),encoding='utf-8')
print('PASS',len(checks),'regressions including three deliberately corrupted results')
