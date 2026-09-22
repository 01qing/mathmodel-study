from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(n,c): assert c,n; checks.append(n)
def load(r): return json.loads((ROOT/r).read_text(encoding='utf-8'))
P={x['paper_id']:x for x in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
st=load('learning_output/context/learning_state.json')
ck('version',st['current_version'] in {'1.36.0','1.37.0','1.38.0'}); ck('latest',st['latest_completed_paper'] in {'S043','S044','S045'}); ck('R1 latest',st['reproduction_level_latest'] in {'S043:R1','S044:R2','S045:R2'})
req=['knowledge_base/paper_reviews/2025-F-S043-core.json','knowledge_base/candidate_competitions/S043.json','knowledge_base/result_registry/S043.json','knowledge_base/code_cases/2025-F-S043-code-access.json','knowledge_base/method_modules/2025-F-S043-modules.json','knowledge_base/figure_argumentation/S043.json','knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/figure_decision_rules/2025-F-provisional.json','learning_output/analyses/S043_source_audit.json','learning_output/analyses/S043_result_registry_replay.json','S043_v1.36_训练摘要.md']
for r in req: ck('exists '+r,(ROOT/r).exists() and (ROOT/r).stat().st_size>0)
rv=load('knowledge_base/paper_reviews/2025-F-S043-core.json'); ck('pages 71',rv['pages']==71); ck('R1',rv['reproduction']['level']=='R1'); ck('code unavailable','R2:' in rv['reproduction']['not_achieved'][0])
ck('reviewed 71',P['S043']['reviewed_pages']==list(range(1,72))); ck('S043 train',P['S043']['split']=='train')
ck('S042 preserved',P['S042']['split']=='train' and len(P['S042']['reviewed_pages'])==182)
ck('S044 legal progression',P['S044']['split']=='train' and len(P['S044']['reviewed_pages'])>0)
ck('S045 legal progression',P['S045']['split']=='train' and P['S045'].get('reviewed_pages',[]) in [[],list(range(1,95))])
for pid in ['S030','S031']: ck(pid+' dev reserve',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']: ck(pid+' test frozen',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
reg=load('knowledge_base/result_registry/S043.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_GLOBAL_OPTIMUM_GAP0','Q1_ADAPTIVE_MUTATION_DIRECTION','Q1_FITNESS_CORRELATION_REPLAY','Q2_LAYOUT_SCORE_RANGE','Q2_THEME_ENTROPY_NORMALIZER','Q2_100_MAX_CONTRADICTION','Q3_AHP_CIRCULAR_MATRIX','Q3_NONSIGNIFICANCE_COMMONALITY','Q3_ALL_GT_093_CONTRADICTION','Q3_MATRIX_SUMMARY_REPLAY','Q3_CLUSTER_MEAN_REPLAY','Q3_ABSTRACT_TOP_RANK_DRIFT','Q3_EXTERNAL_ACCURACY_PROVENANCE']: ck(x,x in ids)
rep=load('learning_output/analyses/S043_result_registry_replay.json')['checks']
ck('Q1 r replay',abs(rep['Q1_fitness_scenic_pearson_replayed']-0.9897137821)<1e-9); ck('reported r 0.89',rep['Q1_reported_r']==0.89)
ck('Q2 weight sum',abs(rep['Q2_weight_sum_layout']-1.0)<1e-12); ck('Q2 scale impossible',rep['Q2_reported_layout_max']>rep['Q2_if_component_bounds_hold_formula_max'])
ck('45 pairs',rep['Q3_pair_count']==45); ck('matrix range',abs(rep['Q3_matrix_min']-0.523)<1e-12 and abs(rep['Q3_matrix_max']-0.847)<1e-12)
ck('matrix mean replay',abs(rep['Q3_matrix_mean']-0.6642666666666667)<1e-12); ck('mean mismatch',abs(rep['Q3_matrix_mean']-rep['Q3_reported_mean'])>0.03)
ck('matrix sd mismatch',abs(rep['Q3_matrix_sample_sd']-rep['Q3_reported_sd'])>0.015)
ck('large group mismatch',abs(rep['Q3_group_means_replayed']['large']-0.721)>0.05); ck('medium group near',abs(rep['Q3_group_means_replayed']['medium']-0.741)<0.002); ck('small group mismatch',abs(rep['Q3_group_means_replayed']['small']-0.735)>0.05)
ck('2/3 arithmetic',abs(rep['Q3_external_accuracy_arithmetic']-2/3)<1e-12)
ca=load('knowledge_base/code_cases/2025-F-S043-code-access.json'); ck('code unavailable status',ca['status']=='CODE_REFERENCED_BUT_NOT_AVAILABLE'); ck('code R1',ca['consequence']['reproduction_level']=='R1')
mp=load('knowledge_base/cross_paper_maps/2025-F-S042-S045.json'); ck('map legal progression',mp['status'] in {'PROVISIONAL_TWO_OF_FOUR_TRAIN_PAPERS_REVIEWED','PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED','FINAL_FOUR_OF_FOUR_TRAIN_PAPERS_REVIEWED'}); ck('reviewed S042 S043',mp['papers_reviewed'][:2]==['S042','S043']); ck('S045 lifecycle',('S045' in mp['papers_pending']) or ('S045' in mp['papers_reviewed'] and mp['papers_pending']==[]))
for rel in ['knowledge_base/error_patterns/adaptive-control-formula-direction-drift.json','knowledge_base/error_patterns/population-dependent-objective-normalization.json','knowledge_base/error_patterns/constructed-score-range-contract-break.json','knowledge_base/error_patterns/cluster-taxonomy-cross-surface-drift.json']: ck('pattern '+rel,(ROOT/rel).exists())
skill=(ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8'); ck('skill v136','## 19. v1.36 / S043' in skill); ck('skill gap rule','启发式算法不能自行证明 Gap=0' in skill); ck('skill ward','Ward 需要欧氏合同' in skill)
nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8'); ck('next legal progression',('S044 / 2025-F' in nexttxt) or ('S045 / 2025-F' in nexttxt) or ('2024-D' in nexttxt)); ck('group gate lifecycle',(('NOT_DUE' in nexttxt and 'S045' in nexttxt) or ('Mini Transfer' in nexttxt and 'Capability Evidence Gate' in nexttxt))); ck('test frozen text','Test' in nexttxt and 'frozen' in nexttxt)
print(f'PASS {len(checks)}/{len(checks)}')
