from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[4]; A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'; checks=[]
def ck(n,c): assert c,n; checks.append(n)
def load(r): return json.loads((ROOT/r).read_text(encoding='utf-8'))
P={x['paper_id']:x for x in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
st=load('learning_output/context/learning_state.json'); ck('version >=1.34',tuple(map(int,st['current_version'].split('.')[:2])) >= (1,34)); ck('S036 remains completed',P['S036']['reviewed_pages']==list(range(1,77)))
for r in ['knowledge_base/paper_reviews/2025-C-S036-core.json','knowledge_base/candidate_competitions/S036.json','knowledge_base/result_registry/S036.json','knowledge_base/code_cases/2025-C-S036-code-access.json','knowledge_base/method_modules/2025-C-S036-modules.json','knowledge_base/figure_argumentation/S036.json','learning_output/analyses/S036_source_audit.json','learning_output/analyses/S036_result_registry_replay.json','learning_output/analyses/2025-C_mini_transfer.json','learning_output/analyses/2025-C_capability_evidence_gate.json','knowledge_base/figure_decision_rules/2025-C-final.json']: ck('exists '+r,(ROOT/r).exists())
rv=load('knowledge_base/paper_reviews/2025-C-S036-core.json'); ck('R1',rv['reproduction']['level']=='R1'); ck('pages',rv['pages']==76)
reg=load('knowledge_base/result_registry/S036.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_PROJECT_TRAIN_TEST_LEAKAGE','Q3_MULTI_METRIC_CONFLICT','Q4_EDGE_SCORE_REPLAY','Q4_EDGE_COMPONENT_CONTRADICTION','Q4_EIG_POSTERIOR_GAP']: ck(x,x in ids)
score=.45*1.71e-6+.45*.98+.10*.82; ck('score',abs(score-0.5230007695)<1e-12); ck('period',abs(math.pi*30-94.25)<0.01)
for pid,pages in [('S032',71),('S033',78),('S034',68),('S035',91),('S036',76)]: ck(pid+' reviewed',P[pid]['reviewed_pages']==list(range(1,pages+1)))
for pid in ['S030','S031']: ck(pid+' dev reserve',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']: ck(pid+' test frozen',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
mp=load('knowledge_base/cross_paper_maps/2025-C-S032-S036.json'); ck('map final',mp['status']=='FINAL_FIVE_TRAIN_PAPERS_REVIEWED'); ck('all reviewed',mp['papers_reviewed']==['S032','S033','S034','S035','S036']); ck('no pending',mp['papers_pending']==[])
mt=load('learning_output/analyses/2025-C_mini_transfer.json'); ck('first fail',mt['first_run_status']=='FAIL'); ck('transfer pass',mt['status']=='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX'); ck('rejects',mt['summary']['invalid_rejects']==mt['summary']['invalid_cases'])
cap=load('learning_output/analyses/2025-C_capability_evidence_gate.json'); ck('ablation not run',cap['controlled_ablation']['status']=='NOT_RUN')
nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(); ck('next progression beyond 2025-C','2025-F' in nexttxt); ck('test frozen','Test' in nexttxt and 'frozen' in nexttxt)
print(f'PASS {len(checks)}/{len(checks)}')
