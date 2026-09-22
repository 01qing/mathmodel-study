from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[4]
r=json.loads((ROOT/'knowledge_base/result_registry/S032.json').read_text(encoding='utf-8'))
q1=next(e for e in r['entries'] if e['id']=='Q1_METRIC_TABLE')['reported']
out=[]
for k,v in q1.items():
 iou=v['IoU_pct']/100
 exp=100*2*iou/(1+iou)
 out.append({'model':k,'reported_F1_pct':v['F1_pct'],'F1_from_reported_IoU_pct':round(exp,4),'difference_pct_point':round(v['F1_pct']-exp,4),'status':'PROVENANCE_REQUIRED_NOT_AUTOMATIC_ERROR'})
res={'paper_id':'S032','scope':'arithmetic replay only; not author reproduction','checks':out,'known_conflicts':['Q3 body JRC≈75 vs code clip 0..20','Q4 duplicate arithmetic-crossover children','Q4 density=True entropy misuse'],'pass_scope':'arithmetic replay completed'}
p=ROOT/'learning_output/analyses/S032_result_registry_replay.json'; p.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(res,ensure_ascii=False,indent=2))
