"""Keep completed payload rewards and wall-clock data occupancy separate."""
from pathlib import Path
import json
import math


def audit(result, payload_bytes=1500):
    lo=result['warmup_us']; hi=lo+result['duration_us']
    counts=[0]*len(result['mbps']); events={lo:0,hi:0}
    for packet in result['trace']:
        release=packet.get('release')
        if packet.get('success') is True and release is not None and lo<=release<=hi:
            counts[packet['node']]+=1
        start=max(lo,packet['start']); end=min(hi,packet['end'])
        if start<end:
            events[start]=events.get(start,0)+1
            events[end]=events.get(end,0)-1
    active=0; last=lo; durations={}
    for t,delta in sorted(events.items()):
        durations[active]=durations.get(active,0)+(t-last)
        active+=delta; last=t
        assert active>=0
    assert active==0
    assert math.isclose(sum(durations.values()),hi-lo,abs_tol=1e-7)
    mbps=[count*payload_bytes*8/(hi-lo) for count in counts]
    assert counts==result['successes']
    assert all(math.isclose(a,b,abs_tol=1e-10) for a,b in zip(mbps,result['mbps']))
    assert math.isclose(sum(mbps),result['total_mbps'],abs_tol=1e-10)
    union=sum(t for n,t in durations.items() if n>0)
    sum_node=sum(n*t for n,t in durations.items())
    assert sum_node>=union-1e-8
    return dict(completed_successes=counts,completed_payload_mbps=mbps,
                total_payload_mbps=sum(mbps),data_occupancy_by_concurrency_us=durations,
                data_busy_union_us=union,sum_node_data_airtime_us=sum_node,
                overlap_extra_airtime_us=sum_node-union,
                boundary='completion counted by release in [warmup,warmup+duration]; occupancy clipped to window',
                note='occupancy includes failed data, excludes ACK/DIFS; cannot substitute for successful bits')


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    results={}
    for file in sorted((here.parent/'A23100070049').glob('TRACE_*.json')):
        results[file.name]=audit(json.loads(file.read_text(encoding='utf-8'))['result'])
    assert len(results)==4
    (here/'REWARD_LEDGER_CHECKS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS: four existing traces, exact packet rewards and concurrency-duration conservation; no rerun')
