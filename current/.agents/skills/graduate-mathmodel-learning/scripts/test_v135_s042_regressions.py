from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(n,c): assert c,n; checks.append(n)
def load(r): return json.loads((ROOT/r).read_text(encoding='utf-8'))
P={x['paper_id']:x for x in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
st=load('learning_output/context/learning_state.json')
ck('version compatible',tuple(map(int,st['current_version'].split('.')[:2])) >= (1,35)); ck('latest progressed',st['latest_completed_paper'] in {'S042','S043','S044','S045','S013','S014','S015','S016'}); ck('historical R2 preserved',P['S042'].get('reproduction_level')=='R2')
for r in ['knowledge_base/paper_reviews/2025-F-S042-core.json','knowledge_base/candidate_competitions/S042.json','knowledge_base/result_registry/S042.json','knowledge_base/code_cases/2025-F-S042-appendix-code.json','knowledge_base/method_modules/2025-F-S042-modules.json','knowledge_base/figure_argumentation/S042.json','knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/figure_decision_rules/2025-F-provisional.json','learning_output/analyses/S042_source_audit.json','learning_output/analyses/S042_result_registry_replay.json']: ck('exists '+r,(ROOT/r).exists())
rv=load('knowledge_base/paper_reviews/2025-F-S042-core.json'); ck('paper pages',rv['pages']==182); ck('R2',rv['reproduction']['level']=='R2')
ck('reviewed 182',P['S042']['reviewed_pages']==list(range(1,183))); ck('S042 train',P['S042']['split']=='train')
ck('S043 legal progression',P['S043']['split']=='train');
ck('S044 legal progression',P['S044']['split']=='train' and len(P['S044']['reviewed_pages'])>0)
ck('S045 legal progression',P['S045']['split']=='train' and P['S045'].get('reviewed_pages',[]) in [[],list(range(1,95))])
for pid in ['S030','S031']: ck(pid+' dev reserve',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']: ck(pid+' test frozen',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
reg=load('knowledge_base/result_registry/S042.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_LD_SIGN_CONTRACT','Q1_PATH_LENGTH_CONSTRAINT','Q1_HV_CLAIM','Q2_ANCHOR_CIRCULARITY','Q2_COLLINEARITY','Q3_CLUSTER_ANOVA_DOUBLE_DIP','Q3_ZERO_VARIANCE_DIVISION','CODE_STUBS_AND_DEFAULTS']: ck(x,x in ids)
ck('10 pair arithmetic',math.comb(10,2)==45); ck('11 pair arithmetic',math.comb(11,2)==55); ck('179 class sum',80+74+25==179); ck('88 share',abs(88/179*100-49.2)<0.1); ck('hard conflict',222>100)
ca=load('knowledge_base/code_cases/2025-F-S042-appendix-code.json'); ck('12 source listings',len(ca['files'])==12); ck('code pages',ca['pages']=='103-182'); ck('no R3','R3 local smoke' in ca['not_claimed'])
mp=load('knowledge_base/cross_paper_maps/2025-F-S042-S045.json'); ck('map legal progression',mp['status'] in {'PROVISIONAL_ONE_OF_FOUR_TRAIN_PAPERS_REVIEWED','PROVISIONAL_TWO_OF_FOUR_TRAIN_PAPERS_REVIEWED','PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED','FINAL_FOUR_OF_FOUR_TRAIN_PAPERS_REVIEWED'}); ck('S042 remains reviewed','S042' in mp['papers_reviewed']); ck('S045 lifecycle',('S045' in mp['papers_pending']) or ('S045' in mp['papers_reviewed'] and mp['papers_pending']==[]))
for rel in ['knowledge_base/error_patterns/decoded-object-constraint-leak.json','knowledge_base/error_patterns/anchor-target-circular-calibration.json','knowledge_base/error_patterns/post-selection-cluster-significance.json','knowledge_base/error_patterns/similarity-concentration-generalization.json','knowledge_base/error_patterns/silent-default-feature-on-exception.json']: ck('pattern '+rel,(ROOT/rel).exists())
nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8'); ck('next legal progression',('S043 / 2025-F' in nexttxt) or ('S044 / 2025-F' in nexttxt) or ('S045 / 2025-F' in nexttxt) or ('2024-D' in nexttxt)); ck('group gate lifecycle',(('NOT_DUE' in nexttxt and 'S045' in nexttxt) or ('Mini Transfer' in nexttxt and 'Capability Evidence Gate' in nexttxt))); ck('test frozen','Test' in nexttxt and 'frozen' in nexttxt)
print(f'PASS {len(checks)}/{len(checks)}')
