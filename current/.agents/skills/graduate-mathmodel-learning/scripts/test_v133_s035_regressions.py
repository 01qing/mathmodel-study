from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(n,c):
 assert c,n; checks.append(n)
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
P={x["paper_id"]:x for x in json.loads((A/'papers.json').read_text(encoding="utf-8"))}
ck("version >=1.33",(ROOT/'learning_output/context/learning_state.json').exists() and tuple(map(int,load('learning_output/context/learning_state.json')['current_version'].split('.')[:2])) >= (1,33))
for r in ['knowledge_base/paper_reviews/2025-C-S035-core.json','knowledge_base/candidate_competitions/S035.json','knowledge_base/result_registry/S035.json','knowledge_base/code_cases/2025-C-S035-code-access.json','knowledge_base/method_modules/2025-C-S035-modules.json','knowledge_base/figure_argumentation/S035.json','learning_output/analyses/S035_source_audit.json','learning_output/analyses/S035_result_registry_replay.json']: ck('exists '+r,(ROOT/r).exists())
rv=load('knowledge_base/paper_reviews/2025-C-S035-core.json'); ck('R1',rv['reproduction']['level']=='R1'); ck('visual',rv['pages']==91)
reg=load('knowledge_base/result_registry/S035.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_SOURCE_OVERLAP_LEAKAGE','Q2_FIXED_PERIOD_CONTRACT','Q2_POOR_FIT_REJECT_EXAMPLE','Q4_MC_ANGLE_MEAN_DIMENSION','Q4_SCORE_CALIBRATION','CODE_SOURCE_PATHS_UNAVAILABLE']: ck(x,x in ids)
ck('period',abs(math.pi*30-94.25)<0.01); ck('reviewed',P['S035']['reviewed_pages']==list(range(1,92))); ck('S036 legal later review',P['S036']['split']=='train' and P['S036']['reviewed_pages'] in [[],list(range(1,77))])
for pid in ['S030','S031']: ck(pid+' dev unread',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']: ck(pid+' test unread',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
mp=load('knowledge_base/cross_paper_maps/2025-C-S032-S036.json'); ck('map4-or-final',mp['status'] in ['PROVISIONAL_AFTER_FOUR_TRAIN_PAPERS','FINAL_FIVE_TRAIN_PAPERS_REVIEWED']); ck('pending legal',mp['papers_pending'] in [['S036'],[]])
print(f'PASS {len(checks)}/{len(checks)}')
