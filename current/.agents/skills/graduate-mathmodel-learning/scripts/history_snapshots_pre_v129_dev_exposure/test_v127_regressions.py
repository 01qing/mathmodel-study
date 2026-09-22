#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)

ok('version >=1.27', tuple(map(int,(R/'VERSION').read_text().strip().split('.'))) >= (1,27,0))
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('MathModel-Core retained','MathModel-Core' in skill)
ok('v127 rules present','v1.27 / S027' in skill and 'macro' in skill and 'Result Registry' in skill)

rev=json.loads((R/'knowledge_base/paper_reviews/2025-A-S027-core.json').read_text(encoding='utf-8'))
ok('S027 train',rev['split']=='train')
ok('S027 120 pages',rev['pages']==120)
ok('S027 R2',rev['reproduction']['level']=='R2')
ok('S027 visual separate',rev['reproduction']['visual_audit_separate']['does_not_raise_reproduction_level'] is True)
ok('S027 combinatorial split N/A','NOT_APPLICABLE' in rev['problem_data_contract']['standard_ml_split'])

cc=json.loads((R/'knowledge_base/candidate_competitions/S027.json').read_text(encoding='utf-8'))
for q in ['Q1','Q2','Q3']:
    c=cc['questions'][q]
    ok(q+' competition roles',all(k in c for k in ['baseline','author_route','major_alternatives','not_recommended','switch_conditions']))
    ok(q+' six hour baseline',len(c['baseline']['six_hour_plan'])>=4)
    ok(q+' alternatives',len(c['major_alternatives'])>=3)
ok('Q1 Kahn baseline','Kahn' in cc['questions']['Q1']['baseline']['name'])
ok('Q2 lifetime baseline','lifetime' in cc['questions']['Q2']['baseline']['name'].lower())
ok('Q3 epsilon baseline','epsilon' in cc['questions']['Q3']['baseline']['name'].lower())

code=json.loads((R/'knowledge_base/code_cases/2025-A-S027-appendix-code.json').read_text(encoding='utf-8'))
ids={x['id'] for x in code['findings']}
for fid in ['Q1_CORE_HELPERS_MISSING','Q1_AVERAGE_SEMANTICS_DRIFT','Q2_ALLOCATOR_NAME_DRIFT','Q2_SPILL_DIRECTION_DRIFT','Q2_MAIN_MISSING','Q2_RESULT_AGGREGATION_PROVENANCE','Q3_CAP_PARAMETER_DRIFT','Q3_BASELINE_SOURCE_DRIFT','Q3_OPTIMIZER_CORE_MISSING','Q3_SIGN_CONVENTION_DRIFT','Q3_MULTI_SEQUENCE_LABEL_EVIDENCE_GAP']:
    ok('code finding '+fid,fid in ids)
ok('R3 blockers',len(code['r3_blockers'])>=4)

reg=json.loads((R/'knowledge_base/result_registry/S027.json').read_text(encoding='utf-8'))
ok('Q1 aggregate matches 89.2',abs(reg['Q1']['replay']['aggregate_sum_weighted_pct']['vs_random']-89.2)<0.1)
ok('Q1 macro is not 89.2',abs(reg['Q1']['replay']['mean_of_six_casewise_pct']['vs_random']-89.2)>10)
ok('Q1 S027 between S025 S026 Conv0',reg['Q1']['cross_paper_Cmax']['S025']['Conv_Case0'] < reg['Q1']['cross_paper_Cmax']['S027']['Conv_Case0'] < reg['Q1']['cross_paper_Cmax']['S026']['Conv_Case0'])
ok('Q2 six workload rows',len(reg['Q2']['table_5_12_rows'])==6)
ok('Q2 aggregation unresolved',reg['Q2']['aggregation_check']['status']=='UNRESOLVED')
ok('Q2 total traffic 206832',reg['Q2']['table_5_12_totals']['traffic']==206832)
ok('Q2 mean traffic 34472',reg['Q2']['table_5_12_means']['traffic']==34472)
ok('Q3 cycle replay',abs(reg['Q3']['aggregate_replay']['cycle_reduction_pct']-12.6197)<0.01)
ok('Q3 traffic replay',abs(reg['Q3']['aggregate_replay']['traffic_increase_pct']-7.1788)<0.01)
ok('Q3 15pct feasible',reg['Q3']['hard_cap_contract']['15pct_violation_tasks']==[])
ok('Q3 10pct violation',reg['Q3']['hard_cap_contract']['10pct_violation_tasks']==['FlashAttention_Case0'])
ok('Q3 sign drift caught',reg['Q3']['sign_check']['status']=='INCONSISTENT')
ok('Q3 Conv0 baseline drift',reg['Q3']['appendix_baseline_drift']['Conv_Case0']['code_traffic']==132096 and reg['Q3']['appendix_baseline_drift']['Conv_Case0']['paper_traffic']==99072)
val=json.loads((R/'learning_output/analyses/v127_S027/S027_result_registry_validation.json').read_text(encoding='utf-8'))
ok('registry validator',val['status']=='PASS' and val['checks']>=9)

mods=json.loads((R/'knowledge_base/method_modules/2025-A-S027-modules.json').read_text(encoding='utf-8'))
ok('transferable modules >=5',len(mods['modules'])>=5)
comp=json.loads((R/'learning_output/analyses/v127_S027/S025_S026_S027_composition_contract.json').read_text(encoding='utf-8'))
ok('composer retains 2025A contract',comp['case_group']=='2025-A' and len(comp['compatibility_checks'])==7)
ok('composer compatibility 7 dimensions',len(comp['compatibility_checks'])==7)
ok('composer blocks S027 spill',any('spill' in x['module'].lower() for x in comp['blocked_components']))

mp=json.loads((R/'knowledge_base/cross_paper_maps/2025-A-S025-S028.json').read_text(encoding='utf-8'))
ok('map preserves S025-S027',all(x in mp['papers_reviewed'] for x in ['S025','S026','S027']))
ok('S028 legal map transition',('S028' in mp['papers_pending']) or ('S028' in mp['papers_reviewed']))
ok('map status progresses',mp['current_status'] in ['PROVISIONAL_AFTER_THREE_TRAIN_PAPERS','FINAL_AFTER_FOUR_TRAIN_PAPERS'])
ok('S027 Q1 map present','S027' in mp['questions']['Q1'])
ok('S027 Q2 map present','S027' in mp['questions']['Q2'])
ok('S027 Q3 map present','S027' in mp['questions']['Q3'])

fig=json.loads((R/'knowledge_base/figure_decision_rules/2025-A-provisional.json').read_text(encoding='utf-8'))
ok('figure basis preserves S025-S027',all(x in fig.get('paper_basis',[]) for x in ['S025','S026','S027']))
ok('macro vs aggregate figure rule',any('macro' in r['figure_type'].lower() for r in fig['rules']))
ok('exact gap figure rule',any('exact-gap' in r['figure_type'].lower() for r in fig['rules']))

for fn in ['aggregate-vs-case-average-semantic-drift.json','allocator-name-bestfit-firstfit-drift.json','spill-victim-direction-paper-code-drift.json','optimizer-core-helper-missing.json','hard-cap-parameter-cross-section-drift.json','baseline-result-source-drift.json','reported-improvement-sign-convention-drift.json','multi-instance-coordination-label-with-single-instance-code.json']:
    ok('error '+fn,(R/'knowledge_base/error_patterns'/fn).exists())

papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
ok('45 papers',len(papers)==45)
ok('32 7 6 split',Counter(p['split'] for p in papers)=={'train':32,'dev':7,'test':6})
p27=next(x for x in papers if x['paper_id']=='S027')
ok('S027 all pages reviewed',p27['reviewed_pages']==list(range(1,121)))
ok('S027 R2 registry',p27['reproduction_level']=='R2')
p28=next(x for x in papers if x['paper_id']=='S028')
ok('S028 remains train',p28['split']=='train')
for pid in ['S029','S030']:
    p=next(x for x in papers if x['paper_id']==pid); ok(pid+' dev protected',p['split']=='dev' and p.get('reviewed_pages',[])==[])
for p in [x for x in papers if x['split']=='test']:
    ok(p['paper_id']+' test protected',p.get('reviewed_pages',[])==[])

state=json.loads((R/'learning_output/context/learning_state.json').read_text(encoding='utf-8'))
ok('state preserves S027-or-later',state['latest_completed_paper'] in ['S027','S028'] and tuple(map(int,state['current_version'].split('.'))) >= (1,27,0))
ok('next-learning protocol retained','Mini Transfer' in (R/'learning_output/context/next_learning.md').read_text(encoding='utf-8') or 'Dev' in (R/'learning_output/context/next_learning.md').read_text(encoding='utf-8'))

print(json.dumps({'status':'PASS','scope':'v1.27 MathModel-Core S027 upgraded protocol','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
