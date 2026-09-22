from pathlib import Path
import json
from decimal import Decimal, ROUND_HALF_UP
ROOT=Path(__file__).resolve().parents[4]
rows={
 '寄畅园':(100.0,100.0,100.0),'怡园':(93.0,89.0,90.8),'瞻园':(80.0,96.0,88.8),'沈园':(86.0,91.0,88.8),
 '拙政园':(80.0,76.0,77.8),'留园':(72.0,79.0,75.9),'耦园':(70.0,60.0,64.5),'秋霞圃':(55.0,63.0,59.4),'豫园':(62.0,44.0,52.1),'绮园':(35.0,38.0,36.7)}
calc={k:float((Decimal(str(a))*Decimal('0.45')+Decimal(str(b))*Decimal('0.55')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)) for k,(a,b,c) in rows.items()}
out={"paper_id":"S045","status":"PASS_AUDIT_REPLAY_WITH_IDENTIFIED_FAILURES","checks":{
 "Q2_table66_formula":"round(0.45*element+0.55*open_close,1)",
 "Q2_table66_calculated":calc,
 "Q2_table66_reported":{k:v[2] for k,v in rows.items()},
 "Q2_table66_exact_all_10":all(calc[k]==rows[k][2] for k in rows),
 "Q3_posthoc_adjustments":{"绮园":{"original":-0.791,"printed_adjusted":0.209,"delta":round(0.209-(-0.791),3)},"豫园":{"original":-0.857,"printed_adjusted":0.143,"delta":round(0.143-(-0.857),3)}},
 "Q3_two_adjustments_equal_plus_one":abs((.209+.791)-1)<1e-12 and abs((.143+.857)-1)<1e-12,
 "Q3_eq713_visual":"1 - abs(A_natural/A_total - A_artificial/A_total)",
 "Q3_eq713_text_extraction_lost_absolute_bars":True,
 "Q1_eq567_has_length_term":False,
 "Q2_sensitivity_axis_contract":"FAIL: scenario-indexed scores ranked as though garden-indexed",
 "scope_note":"Arithmetic/static-contract replay only; PASS does not validate author end-to-end model or aesthetic claims."
}}
p=ROOT/'learning_output/analyses/S045_result_registry_replay.json'; p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert out['checks']['Q2_table66_exact_all_10']
assert out['checks']['Q3_two_adjustments_equal_plus_one']
print('PASS S045 registry replay: 10/10 Table6.6 arithmetic; posthoc +1 edits preserved as provenance failures')
