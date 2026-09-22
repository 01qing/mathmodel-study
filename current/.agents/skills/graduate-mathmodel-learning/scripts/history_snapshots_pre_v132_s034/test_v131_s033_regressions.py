from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(name,cond):
    if not cond: raise AssertionError(name)
    checks.append(name)
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
# identity and reviewed boundary
ck('S033 train',P['S033']['split']=='train')
ck('S033 pages78',P['S033']['pages']==78)
ck('S033 reviewed all',P['S033']['reviewed_pages']==list(range(1,79)))
ck('S033 R2',P['S033']['reproduction_level']=='R2')
ck('S033 review status', 'PRINTED_PYTHON_STATIC_AUDIT' in P['S033']['learning_status'])
# assets
assets=['knowledge_base/paper_reviews/2025-C-S033-core.json','knowledge_base/candidate_competitions/S033.json','knowledge_base/result_registry/S033.json','knowledge_base/code_cases/2025-C-S033-appendix-code.json','knowledge_base/figure_argumentation/S033.json','knowledge_base/method_modules/2025-C-S033-modules.json','knowledge_base/cross_paper_maps/2025-C-S032-S036.json','knowledge_base/figure_decision_rules/2025-C-provisional.json','learning_output/analyses/S033_source_audit.json','learning_output/analyses/S033_result_registry_replay.json','S033_v1.31_训练摘要.md']
for f in assets: ck('asset '+f,(ROOT/f).exists())
# registry findings
reg=load('knowledge_base/result_registry/S033.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_RECOMMENDATION_SEMANTICS','Q2_R2_TABLE_REPLAY','Q2_CLUSTER_COUNT_RESULT_CONTRACT','Q2_PERIOD_FIXED_VS_ESTIMATED','Q3_JRC_FORMULA_DRIFT','Q3_AREA_CORRECTION_CLAIM','Q4_SIMULATED_DATA_PROVENANCE','Q4_CONNECTIVITY_PROBABILITY_CALIBRATION','Q4_ENTROPY_CONTRACT','Q4_INFORMATION_GAIN_CONTRACT','Q4_SPACING_HARD_CONSTRAINT','Q4_DEPTH_RESULT_CODE_DRIFT','Q4_PRINTED_CHAIN_INCOMPLETE','Q4_JRC_RANGE_CONTRACT']:
    ck('registry '+x,x in ids)
# code audit findings
code=load('knowledge_base/code_cases/2025-C-S033-appendix-code.json'); cids={x['id'] for x in code['findings']}
for x in ['Q1_HEADLINE_METHODS_MISSING','Q1_CROSS_QUESTION_PATH','Q2_FIXED_GMM_COUNT_MISMATCH','Q2_DIRECTION_FEATURE_ABSENT','Q2_BIC_HELPER_INACTIVE','Q2_TOTAL_FRACTURES_MISLABEL','Q2_OPTIMIZERS_NOT_VISIBLE','Q3_HEADLINE_ADAPTIVE_Z3_ABSENT','Q3_CLOSED_CONTOUR_PROFILE_MISMATCH','Q3_MIN_ESTIMATOR_UNDOCUMENTED','Q4_SIMULATED_FIXED_INPUTS','Q4_DEPTH_FILTER_BODY_DRIFT','Q4_BINARY_ENTROPY_INCOMPLETE','Q4_UNCERTAINTY_STATE_NOT_ASSIGNED','Q4_SPACING_THRESHOLD_DRIFT','Q4_PSEUDO_INFORMATION_GAIN','Q4_MAIN_OMITS_OPTIMIZATION','Q4_JRC_RANGE_MISMATCH']:
    ck('code '+x,x in cids)
# generic gates learned from S033
for fn in ['fit-on-same-instance-not-generalization.json','cluster-count-contract-result-mismatch.json','closed-contour-not-profile-function.json','binary-event-entropy-missing-complement.json','information-gain-needs-posterior-update.json','synthetic-upstream-inputs-not-attachment-evidence.json','fixed-parameter-presented-as-estimated.json','bounded-similarity-needs-input-range-contract.json']:
    ck('generic '+fn,(ROOT/'knowledge_base/error_patterns'/fn).exists())
# candidate competitions all questions and baseline fields
cc=load('knowledge_base/candidate_competitions/S033.json')
for q in ['Q1','Q2','Q3','Q4']:
    ck(q+' candidate present',q in cc['questions'])
    ck(q+' baseline present','baseline' in cc['questions'][q])
    ck(q+' author route present','author_route' in cc['questions'][q])
# cross-paper map state
mp=load('knowledge_base/cross_paper_maps/2025-C-S032-S036.json')
ck('map reviewed S032 S033',mp['papers_reviewed']==['S032','S033'])
ck('map pending S034-36',mp['papers_pending']==['S034','S035','S036'])
ck('map provisional two',mp['status']=='PROVISIONAL_AFTER_TWO_TRAIN_PAPERS')
ck('mini transfer not due','NOT_DUE' in mp['mini_transfer'])
# retriever metadata aligned
cg=json.loads((A/'case_group_maps.json').read_text(encoding='utf-8'))
ck('retriever group status two',cg['2025-C']['status']=='PROVISIONAL_2_OF_5_TRAIN_PAPERS')
ck('retriever reviewed papers',cg['2025-C']['reviewed_papers']==['S032','S033'])
core=json.loads((A/'core_retrieval_summaries.json').read_text(encoding='utf-8'))
ck('S033 core summary present',core.get('S033',{}).get('reproduction_level')=='R2')
# source/hash visual audit
sa=load('learning_output/analyses/S033_source_audit.json')
ck('S033 source hash',sa['sha256']=='bc6529349c3a053b7774731f2fa3e383f6337807fd33954ee7726b04949878fd')
ck('S033 hash registry match',sa['sha256']==sa['expected_registry_sha256']==P['S033']['sha256'])
ck('visual 78','78/78' in sa['visual_audit'])
ck('appendix 52-78',sa['appendix_static_audit']=='pages 52-78')
# replay semantics
rp=load('learning_output/analyses/S033_result_registry_replay.json')
ck('replay pass',rp['status']=='PASS')
ck('replay count11',rp['pass_count']==11)
ck('replay R2 scope','not author-code reproduction' in rp['scope'])
# arithmetic repeat, independent of registry prose
a=[0.3810,0.5924,0.8129,0.7408,0.6472,0.8926,0.0462,0.6926,0.4720]
b=[0.4992,0.6938,0.9177,0.8826,0.8607,0.8915,0.8218,0.8137,0.7918]
ck('Q2 mean A',abs(sum(a)/9-0.5864111111111111)<1e-12)
ck('Q2 mean B',abs(sum(b)/9-0.7969777777777778)<1e-12)
ck('Q4 spacing violation detected',412.3105<500)
# skill generic rules
skill=(ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
for term in ['v1.31 / S033','同一对象自拟合不是学习泛化','Bernoulli','信息增益','模拟/手设上游输入只能作为情景证据','相似度归一化的上界必须与上游变量实际范围一致']:
    ck('skill '+term,term in skill)
# frozen split and unread reserves
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('papers45',len(P)==45)
ck('chunks6752',len(json.loads((A/'chunks.json').read_text(encoding='utf-8')))==6752)
ck('split counts', {s:sum(p['split']==s for p in P.values()) for s in ['train','dev','test']}=={'train':32,'dev':7,'test':6})
for pid in ['S030','S031']:
    ck(pid+' dev',P[pid]['split']=='dev'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
for pid in ['S034','S035','S036']:
    ck(pid+' train',P[pid]['split']=='train'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test',P[pid]['split']=='test'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
# history adaptation persisted
note=ROOT/'learning_output/analyses/historical_test_adaptation_v131.md'
ck('history adaptation note',note.exists())
ck('history snapshot exists',(ROOT/'.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v131_s033/test_v130_s032_regressions.py').exists())
assert len(checks)==119, len(checks)
print(f'PASS {len(checks)}/{len(checks)}')
