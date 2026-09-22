from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(name,cond):
    assert cond, name
    checks.append(name)
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
ck('version >=1.32',tuple(map(int,(ROOT/'VERSION').read_text().strip().split('.')[:2])) >= (1,32))
# assets
assets=[
 'knowledge_base/paper_reviews/2025-C-S034-core.json','knowledge_base/candidate_competitions/S034.json','knowledge_base/result_registry/S034.json',
 'knowledge_base/code_cases/2025-C-S034-code-access.json','knowledge_base/figure_argumentation/S034.json','knowledge_base/method_modules/2025-C-S034-modules.json',
 'knowledge_base/cross_paper_maps/2025-C-S032-S036.json','knowledge_base/figure_decision_rules/2025-C-provisional.json',
 'learning_output/analyses/S034_source_audit.json','learning_output/analyses/S034_result_registry_replay.json','S034_v1.32_训练摘要.md',
 'learning_output/analyses/v132_S034/S034_TRAINING_REPORT.md','learning_output/analyses/historical_test_adaptation_v132.md'
]
for f in assets: ck('asset '+f,(ROOT/f).exists())
# review/repro boundary
rv=load('knowledge_base/paper_reviews/2025-C-S034-core.json')
ck('review paper S034',rv['paper_id']=='S034')
ck('review train',rv['split']=='train')
ck('review pages68',rv['pages']==68)
ck('review R1',rv['reproduction']['level']=='R1')
ck('review code unavailable',any('Attachment 9' in x for x in rv['reproduction']['not_achieved']))
ck('review visual separate',rv['reproduction']['visual_audit_separate']['does_not_raise_reproduction_level'] is True)
# registry required findings
reg=load('knowledge_base/result_registry/S034.json'); ids={e['id'] for e in reg['entries']}
required=[
 'Q1_CONFUSION_METRIC_REPLAY','Q1_GROUND_TRUTH_PROVENANCE','Q2_RANSAC_PERIOD_PRIMITIVE_GAP','Q2_HORIZONTAL_BAND_AXIS_DRIFT','Q2_SIGNIFICANCE_PROVENANCE','Q2_PERIOD_GEOMETRY_CONTRACT',
 'Q3_BOOTSTRAP_ESTIMATOR_DRIFT','Q3_BOOTSTRAP_CI_ORDER','Q3_DENSE_REFERENCE_NOT_TRUTH','Q3_RAF_COEFFICIENT_PROVENANCE','Q3_Q4_JRC_RANGE_CONTRACT',
 'Q4_ISOLATION_RATE_DRIFT','Q4_CLUSTER_MEAN_THRESHOLD_SEMANTICS','Q4_PROBABILITY_CALIBRATION','Q4_UNCERTAINTY_SEMANTICS','Q4_INFORMATION_GAIN_SEMANTICS','Q4_SPACING_SET_CONTRACT','Q4_UNCERTAINTY_REDUCTION_REPLAY','CODE_ATTACHMENT_ACCESS_GAP']
for x in required: ck('registry '+x,x in ids)
ck('registry audit status',reg['status']=='AUDIT_REGISTRY_NOT_AUTHOR_REPRODUCTION')
ck('registry gates>=10',len(reg['global_gates'])>=10)
# code access boundary
ca=load('knowledge_base/code_cases/2025-C-S034-code-access.json')
ck('code access status',ca['status']=='CODE_REFERENCED_BUT_NOT_AVAILABLE')
ck('code R1',ca['consequence']['reproduction_level']=='R1')
ck('code no R2 claim','R2 or R3' in ca['do_not_claim'])
# generic gates
patterns=['metric-ground-truth-provenance-missing.json','pvalue-without-test-provenance.json','pseudocode-output-parameter-missing-primitive.json','bootstrap-estimator-ci-contract-drift.json','dense-reference-not-ground-truth.json','hard-constraint-set-coverage.json','referenced-code-artifact-unavailable.json']
for f in patterns: ck('pattern '+f,(ROOT/'knowledge_base/error_patterns'/f).exists())
# candidates
cc=load('knowledge_base/candidate_competitions/S034.json')
for q in ['Q1','Q2','Q3','Q4']:
    ck(q+' candidate',q in cc['questions'])
    ck(q+' baseline','baseline' in cc['questions'][q])
    ck(q+' author','author_route' in cc['questions'][q])
    ck(q+' alternatives',len(cc['questions'][q]['alternatives'])>=2)
    ck(q+' switch','switch_condition' in cc['questions'][q])
# modules
mods=load('knowledge_base/method_modules/2025-C-S034-modules.json')
ck('modules count',len(mods['modules'])==5)
for mid in ['S034_Q1_COARSE_TO_FINE_CLASSICAL_ENSEMBLE','S034_Q2_ROBUST_INSTANCE_THEN_GEOMETRY_FIT','S034_Q3_MULTISCALE_PROFILE_DIAGNOSTIC','S034_Q3_SAMPLING_CONVERGENCE','S034_Q4_FEASIBLE_COVERAGE_GREEDY']:
    ck('module '+mid,any(m['id']==mid for m in mods['modules']))
ck('blocked transfers>=8',len(mods['blocked_transfers'])>=8)
# cross-paper map / composer seven gates
mp=load('knowledge_base/cross_paper_maps/2025-C-S032-S036.json')
ck('map reviewed prefix3',mp['papers_reviewed'][:3]==['S032','S033','S034'])
ck('map later pending legal',set(mp['papers_pending']).issubset({'S035','S036'}))
ck('map status legal progression',mp['status'] in ['PROVISIONAL_AFTER_THREE_TRAIN_PAPERS','PROVISIONAL_AFTER_FOUR_TRAIN_PAPERS','FINAL_FIVE_TRAIN_PAPERS_REVIEWED'])
ck('map mini legal lifecycle',('NOT_DUE' in mp['mini_transfer']) or ('PASS_MECHANISM_TRANSFER' in mp['mini_transfer']))
for q in ['Q1','Q2','Q3','Q4']:
    ck('map '+q+' S034','S034' in mp['questions'][q])
sg=mp['method_composer_preliminary']['seven_gate_status']
for g in ['input_output_interface','variable_definitions','data_distribution','mathematical_assumptions','units','train_execution_stage','evaluation_metrics']:
    ck('composer gate '+g,g in sg)
ck('composer compat',len(mp['method_composer_preliminary']['compatible'])>=4)
ck('composer blocked',len(mp['method_composer_preliminary']['blocked'])>=6)
# figure rules/argumentation
fr=load('knowledge_base/figure_decision_rules/2025-C-provisional.json')
ck('figure rules preserve S032-S034 base',fr['status'].startswith('PROVISIONAL_AFTER_S032_S033_S034'))
ck('figure rules5',len(fr['rules'])>=5)
fa=load('knowledge_base/figure_argumentation/S034.json')
ck('figure visual68','68/68' in fa['visual_audit'])
ck('figure qcount4',len(fa['key_figures'])==4)
for q in ['Q1','Q2','Q3','Q4']: ck('figure '+q,any(x['question']==q for x in fa['key_figures']))
# source audit
sa=load('learning_output/analyses/S034_source_audit.json')
ck('source hash',sa['sha256']=='23dfbdeb5af6468a92428c0171ccfd569b6571066837df96b1960f47248b1d1f')
ck('source hash registry',sa['sha256']==P['S034']['sha256'])
ck('source pages68',sa['pages']==68)
ck('source visual68','68/68' in sa['visual_audit'])
ck('source R1',sa['reproduction_level']=='R1')
ck('source code unavailable','not available' in sa['available_collection_code'])
# result replay
rp=load('learning_output/analyses/S034_result_registry_replay.json')
ck('replay status',rp['status']=='PASS')
ck('replay boolean15',rp['boolean_check_count']==15)
ck('replay diagnostics1',rp['nonboolean_diagnostics']==1)
ck('replay scope','not author-code reproduction' in rp['scope'])
# independent arithmetic
rows=[(2908,348,254,325590),(3687,441,329,324643),(2563,284,198,326055)]
ps=[]; rs=[]; fs=[]
for tp,fp,fn,tn in rows:
    p=tp/(tp+fp); r=tp/(tp+fn); f=2*p*r/(p+r); ps.append(p);rs.append(r);fs.append(f)
ck('arith macro precision',abs(sum(ps)/3-0.8955116235400561)<1e-12)
ck('arith macro recall',abs(sum(rs)/3-0.9220118786922727)<1e-12)
ck('arith macro f1',abs(sum(fs)/3-0.9085681768101698)<1e-12)
ck('arith isolation64',abs(32/50-0.64)<1e-12)
ck('arith uncertainty reduction',abs(100*(0.523-0.395)/0.523-24.47418738049713)<1e-10)
new=[(800,1300),(2400,1500),(1600,1500)]; existing=[(500,2000),(1500,2000),(2500,2000),(500,1000),(1500,1000),(2500,1000)]
ck('arith new-new >=500',min(math.dist(new[i],new[j]) for i in range(3) for j in range(i+1,3))>=500)
ck('arith existing-new diagnostic',abs(min(math.dist(a,b) for a in existing for b in new)-424.26406871192853)<1e-10)
# paper metadata and retriever maps
ck('S034 reviewed68',P['S034'].get('reviewed_pages')==list(range(1,69)))
ck('S034 R1 meta',P['S034'].get('reproduction_level')=='R1')
ck('S034 review file',P['S034'].get('review_file')=='knowledge_base/paper_reviews/2025-C-S034-core.json')
for pid,pages in [('S035',91),('S036',76)]:
    ck(pid+' train',P[pid]['split']=='train'); ck(pid+' legal later review',P[pid].get('reviewed_pages',[]) in [[],list(range(1,pages+1))])
for pid in ['S030','S031']:
    ck(pid+' dev',P[pid]['split']=='dev'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test',P[pid]['split']=='test'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
cg=load('.agents/skills/mathmodel-case-retriever/assets/case_group_maps.json')['2025-C']
ck('retriever legal progression',cg['status'] in ['PROVISIONAL_3_OF_5_TRAIN_PAPERS','PROVISIONAL_4_OF_5_TRAIN_PAPERS','FINAL_5_OF_5_TRAIN_PAPERS'])
ck('retriever reviewed prefix3',cg['reviewed_papers'][:3]==['S032','S033','S034'])
ck('retriever later pending legal',set(cg['pending_papers']).issubset({'S035','S036'}))
core=load('.agents/skills/mathmodel-case-retriever/assets/core_retrieval_summaries.json')
ck('core S034 R1',core['S034']['reproduction_level']=='R1')
ck('core S034 files',core['S034']['candidate_competition_file']=='knowledge_base/candidate_competitions/S034.json')
# split/library frozen
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('papers45',len(P)==45)
ck('chunks6752',len(json.loads((A/'chunks.json').read_text(encoding='utf-8')))==6752)
ck('split counts',{s:sum(p['split']==s for p in P.values()) for s in ['train','dev','test']}=={'train':32,'dev':7,'test':6})
# skill/current pointer
skill=(ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
for term in ['v1.32 / S034','混淆矩阵先问真值从哪来','p 值必须可追溯','高分辨率收敛值不是物理真值','成对硬约束必须覆盖完整集合','代码见附件']:
    ck('skill '+term,term in skill)
nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8')
ck('next pointer advanced legally',('S035 / 2025-C' in nexttxt) or ('S036 / 2025-C' in nexttxt) or ('2025-F' in nexttxt) or ('2024-D' in nexttxt) or ('clean unseen' in nexttxt.lower()))
ck('next dev boundary',('S030/S031' in nexttxt) and ('Dev' in nexttxt))
ck('transfer lifecycle preserved',('due only after S036' in nexttxt) or ('2025-C' in nexttxt and ('PASS' in nexttxt or 'complete' in nexttxt.lower())) or ('2025-F' in nexttxt) or ('Mini Transfer' in nexttxt))
# historical adaptation evidence
ck('history snapshot',(ROOT/'.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v132_s034/test_v131_s033_regressions.py').exists())
ck('history note',(ROOT/'learning_output/analyses/historical_test_adaptation_v132.md').exists())
print(f'PASS {len(checks)}/{len(checks)}')
