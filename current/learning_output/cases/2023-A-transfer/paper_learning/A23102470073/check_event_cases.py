"""Turn paper p32's six event cases into deterministic regressions of our model.
No changes to frozen simulator. Fixed backoff draws are synthetic test inputs.
"""
from pathlib import Path
import sys,json
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;CASE=HERE.parents[1]
sys.path.insert(0,str(CASE/'code'))
import wlan
from check_trace import check_trace

class Draws:
    def __init__(self,values):self.values=iter(values)
    def randrange(self,width):return min(next(self.values,15),width-1)
    def random(self):return .5

def main():
    cases=[('outer_first_separate',[0,5,15],{0:True}),
           ('outer_staggered_overlap',[0,5,2],{0:True,2:True}),
           ('center_first',[5,0,8],{1:True}),
           ('neighbor_simultaneous',[0,0,8],{0:False,1:False}),
           ('outers_simultaneous',[0,5,0],{0:True,2:True}),
           ('all_simultaneous',[0,0,0],{0:False,1:False,2:False})]
    results=[]
    for name,draws,expected in cases:
        with patch.object(wlan.random,'Random',return_value=Draws(draws)):
            p=wlan.scenario(4);r=wlan.simulate(**p,seed=0,warmup=0,duration=1000,trace=True)
        first={}
        for packet in r['trace']:first.setdefault(packet['node'],packet)
        assert all(first[i]['success']==value for i,value in expected.items()),name
        union_check=None
        if name=='outer_staggered_overlap':
            assert first[0]['start']<first[2]['start']<first[0]['end']
            assert first[1]['start']>=max(first[0]['release'],first[2]['release'])+43
            union_check='center waited until both outer exchanges ended plus DIFS'
        if name=='outer_first_separate':assert first[2]['start']>first[0]['release']
        checked=check_trace(r,p);assert checked['status']=='PASS',checked
        results.append(dict(name=name,initial_backoffs=draws,first_packets=first,
                            busy_union_check=union_check,independent_trace_check=checked))
    (HERE/'EVENT_CASE_REGRESSIONS.json').write_text(json.dumps(dict(scope='our model with synthetic fixed draws; no author-code replay',cases=results),ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS:',len(results),'event cases; independent trace assertions:',sum(r['independent_trace_check']['checks'] for r in results))

if __name__=='__main__':main()
