from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(name,cond):
    assert cond,name
    checks.append(name)
def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

ck('VERSION 1.38.0',(ROOT/'VERSION').read_text().strip()=='1.38.0')
st=load('learning_output/context/learning_state.json')
ck('state version',st['current_version']=='1.38.0')
ck('latest S045',st['latest_completed_paper']=='S045')
ck('latest R2',st['reproduction_level_latest']=='S045:R2')

req=[
 'PROGRESS_V138.md','VALIDATION_V138.md','S045_v1.38_训练摘要.md',
 'learning_output/analyses/S045_source_audit.json','learning_output/analyses/S045_result_registry_replay.json',
 'knowledge_base/paper_reviews/2025-F-S045-core.json','knowledge_base/candidate_competitions/S045.json',
 'knowledge_base/result_registry/S045.json','knowledge_base/code_cases/2025-F-S045-printed-code-audit.json',
 'knowledge_base/method_modules/2025-F-S045-modules.json','knowledge_base/figure_argumentation/S045.json',
 'knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/figure_decision_rules/2025-F-final.json',
 'learning_output/mini_transfer/2025-F/first_fail.json','learning_output/mini_transfer/2025-F/repaired_pass.json',
 'learning_output/mini_transfer/2025-F/REPORT.md','learning_output/mini_transfer/2025-F/CAPABILITY_EVIDENCE_GATE.md',
 'learning_output/validation/v138/historical_22_final.json','learning_output/validation/v138/recent_and_current_final.json',
 'learning_output/analyses/historical_test_adaptation_v138.md'
]
for r in req: ck('exists '+r,(ROOT/r).exists() and (ROOT/r).stat().st_size>0)

papers=json.loads((A/'papers.json').read_text(encoding='utf-8')); items=papers['papers'] if isinstance(papers,dict) else papers
P={p['paper_id']:p for p in items}
ck('45 papers',len(P)==45)
ck('6752 chunks',len(json.loads((A/'chunks.json').read_text(encoding='utf-8')))==6752)
ck('split 32/7/6',{s:sum(p['split']==s for p in P.values()) for s in ['train','dev','test']}=={'train':32,'dev':7,'test':6})
ck('frozen split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('all train reviewed',all(p.get('reviewed_pages') for p in P.values() if p['split']=='train'))
ck('S045 reviewed 94',P['S045']['reviewed_pages']==list(range(1,95)))
ck('S045 R2',P['S045'].get('reproduction_level')=='R2')
ck('S029 dev exposed only',P['S029']['split']=='dev' and len(P['S029'].get('reviewed_pages',[]))>0)
for pid in ['S013','S014','S015','S016','S030','S031']:
    ck(pid+' dev unread',P[pid]['split']=='dev' and P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test frozen',P[pid]['split']=='test' and P[pid].get('reviewed_pages',[])==[])

rv=load('knowledge_base/paper_reviews/2025-F-S045-core.json')
ck('review pages 94',rv['pages']==94)
ck('review R2',rv['reproduction']['level']=='R2')
ck('visual separate',rv['reproduction']['visual_audit_separate']['does_not_raise_reproduction_level'] is True)
sa=load('learning_output/analyses/S045_source_audit.json')
ck('source hash',sa['source_sha256']=='0cd7b0001352da9a88dc4d70df750389eb7989d5d2520959e1222a3f05ba2e76')
ck('source pages',sa['pages']==94)
ck('source visual','94/94' in sa['visual_audit'])
ck('source R2',sa['reproduction_level']=='R2')

rr=load('learning_output/analyses/S045_result_registry_replay.json')
ck('registry scope pass',rr['status']=='PASS_AUDIT_REPLAY_WITH_IDENTIFIED_FAILURES')
rep=rr['checks']
ck('table66 10/10',rep['Q2_table66_exact_all_10'] is True and len(rep['Q2_table66_calculated'])==10)
ck('eq567 missing length',rep['Q1_eq567_has_length_term'] is False)
ck('sensitivity semantic fail','FAIL' in rep['Q2_sensitivity_axis_contract'])
ck('posthoc plus1 preserved',rep['Q3_two_adjustments_equal_plus_one'] is True)
ck('eq713 visual abs','abs(' in rep['Q3_eq713_visual'])

mp=load('knowledge_base/cross_paper_maps/2025-F-S042-S045.json')
ck('2025F map final',mp['status']=='FINAL_FOUR_OF_FOUR_TRAIN_PAPERS_REVIEWED')
ck('2025F reviewed all4',mp['papers_reviewed']==['S042','S043','S044','S045'])
ck('2025F pending none',mp['papers_pending']==[])
ck('method composer seven',len(mp['method_composer_final']['seven_gate_status'])==7)
ck('mini transfer in map','PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX' in mp['mini_transfer'])
ck('capability bounded','NOT_ESTABLISHED' in mp['capability_evidence_gate'] and 'NOT_RUN' in mp['capability_evidence_gate'])

mt1=load('learning_output/mini_transfer/2025-F/first_fail.json')
mt2=load('learning_output/mini_transfer/2025-F/repaired_pass.json')
ck('mini first fail',mt1['status']=='FAIL' and mt1['invalid_edges']==[['A','D']])
ck('mini repair pass',mt2['status']=='PASS' and mt2['overall']=='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX')
ck('similarity mechanism',mt2['similarity_scale_fixture']['raw_both_above_0_999'] is True and mt2['similarity_scale_fixture']['scaled_correct_separation'] is True)
cap=(ROOT/'learning_output/mini_transfer/2025-F/CAPABILITY_EVIDENCE_GATE.md').read_text(encoding='utf-8')
ck('clean gain not established','NOT ESTABLISHED' in cap)
ck('controlled ablation not run','NOT_RUN' in cap)

hist=load('learning_output/validation/v138/historical_22_final.json')
ck('historical 22/22',hist['status']=='PASS' and hist['count']==22 and hist['passed']==22)
rec=load('learning_output/validation/v138/recent_and_current_final.json')
ck('recent/current pass',rec['status']=='PASS')

nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8')
ck('next clean Dev 2024-D','2024-D' in nexttxt and 'problem/data' in nexttxt)
ck('S013-S016 unread protocol','S013-S016' in nexttxt and 'unread' in nexttxt)
ck('S030/S031 reserve','S030/S031' in nexttxt and 'Dev reserve' in nexttxt)
ck('Test frozen text','Test' in nexttxt and 'frozen' in nexttxt)
ck('no proxy ablation','Algorithm proxies must not be substituted' in nexttxt)

skill=(ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
for term in ['## 21. v1.38 / S045','灵敏度排序必须同一实体轴','异数量纲 cosine','禁止局部事后改相似度','32篇 Train 全部 reviewed']:
    ck('skill '+term,term in skill)

print(json.dumps({'status':'PASS','checks':len(checks),'scope':'v1.38 release contract; validates registered evidence/integrity boundaries, not author end-to-end execution or clean blind Core capability gain'},ensure_ascii=False))
