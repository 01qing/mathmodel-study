"""Deterministic source-branch probes. No full original simulator replay."""
from pathlib import Path
import json, math
HERE=Path(__file__).resolve().parent

def sequence(events,limit,reset_actual_counter):
    counter=0;rows=[]
    for event in events:
        dropped=False
        if event=='failure':
            counter+=1
            if counter==limit:counter=0;dropped=True
        else:
            unused_c=0 # Visible appendix success branch writes c, not c1/c2.
            if reset_actual_counter:counter=0
        rows.append(dict(event=event,counter=counter,dropped=dropped))
    return rows

def main():
    retry=[]
    for limit in (5,6,32):
        events=['failure']*(limit-1)+['success','failure']
        literal=sequence(events,limit,False);corrected=sequence(events,limit,True)
        assert literal[-1]['dropped'] and not corrected[-1]['dropped']
        assert corrected[-1]['counter']==1
        retry.append(dict(limit=limit,events=events,literal=literal,reset_counter=corrected))
    freezing=[]
    for rate in (455.8,286.8,158.4):
        ts=13.6+12240/rate+91
        for slots in (1,7,15,31):
            start=43.;deadline=start+9*slots
            appendix=deadline+ts if deadline<start+ts else deadline
            required=deadline+ts
            freezing.append(dict(rate=rate,remaining_slots=slots,Ts=ts,
              appendix_deadline=appendix,full_freeze_deadline=required,
              matches=math.isclose(appendix,required)))
    assert any(not row['matches'] for row in freezing)
    # Same denominator/attempt probabilities in p30 Eq5-38 versus p46 code:
    # numerator multipliers .9 and 1.8 give a factor two, irrespective of root.
    noise=[]
    for ptr,ps in ((.178,.859),(.22,.75),(.4,.6)):
        denominator=(1-ptr)*9+ptr*ps*.9*131.45+ptr*ps*.1*148.45+ptr*(1-ps)*148.45
        body=ptr*ps*.9*12000/denominator;code=ptr*ps*1.8*12000/denominator
        assert math.isclose(code,2*body)
        noise.append(dict(ptr=ptr,ps=ps,body_mbps=body,code_mbps=code,ratio=code/body,
                          scope='controlled inputs, not recovered published throughput'))
    # Ideal-channel MC p62-63 hardcodes the base data duration.
    hardcoded=14.126546731022378+26.32733655111891
    overlap=[]
    for rate in (455.8,286.8,158.4):
        duration=13.6+12240/rate
        gap=(duration+hardcoded)/2 if duration>hardcoded+1e-6 else duration
        literal=gap<hardcoded;parametric=gap<duration
        overlap.append(dict(rate=rate,start_gap=gap,hardcoded=hardcoded,actual_duration=duration,
                            literal_collision=literal,parametric_collision=parametric))
    assert all(x['parametric_collision'] and not x['literal_collision'] for x in overlap[1:])
    result=dict(scope='deterministic isolated branch reconstructions; original code not fully run',
      retry_history_cases=retry,freeze_cases=freezing,noise_reward_cases=noise,hardcoded_collision_cases=overlap)
    (HERE/'FINAL_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(retry_cases=len(retry),freeze_cases=len(freezing),freeze_mismatches=sum(not x['matches'] for x in freezing),noise_reward_ratio=2,hardcoded_rate_cases=len(overlap)),ensure_ascii=False))

if __name__=='__main__':main()
