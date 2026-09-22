#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)

# identity + schemas
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('MathModel-Core identity','MathModel-Core' in skill)
ok('no role split current','不拆分' in skill and 'Method Composer' in skill)
for fn in ['mathmodel_core_question_schema_v1.json','reproduction_levels_v1.json','result_registry_schema_v1.json','method_composer_contract_v1.json','figure_decision_rule_schema_v1.json']:
    ok('schema '+fn,(R/'knowledge_base/core_schema'/fn).exists())

# S025 core card
rev=json.loads((R/'knowledge_base/paper_reviews/2025-A-S025-core.json').read_text(encoding='utf-8'))
ok('S025 core identity',rev['core_identity']=='MathModel-Core')
ok('S025 schema 1.0',rev['core_schema_version']=='1.0')
ok('S025 R2',rev['reproduction']['level']=='R2')
ok('visual separate',rev['reproduction']['visual_audit_separate']['does_not_raise_reproduction_level'] is True)
ok('independent unit graph','complete computation-graph workload instance' in rev['problem_data_contract']['independent_evaluation_unit'])
ok('not fake train test','NOT_APPLICABLE' in rev['problem_data_contract']['ml_split_status'])
for q in ['Q1','Q2','Q3']:
    c=rev['candidate_model_competition'][q]
    ok(q+' competition roles',all(k in c for k in ['author_route','baseline','major_alternatives','not_recommended','switch_conditions']))
    ok(q+' baseline nonempty',len(c['baseline']['six_hour_plan'])>=3)
    ok(q+' alternatives',len(c['major_alternatives'])>=2)
ok('Q1 no auto deep RL',any(x['model']=='deep RL' for x in rev['candidate_model_competition']['Q1']['not_recommended']))
ok('Q3 epsilon baseline','epsilon-constraint' in rev['candidate_model_competition']['Q3']['baseline']['name'])
ok('S025 result ref',rev['result_registry_ref']=='knowledge_base/result_registry/S025.json')
ok('S025 module ref',rev['transferable_modules_ref']=='knowledge_base/method_modules/2025-A-S025-modules.json')

# result registry
reg=json.loads((R/'knowledge_base/result_registry/S025.json').read_text(encoding='utf-8'))
ok('result registry schema',reg['schema_version']=='1.0')
ok('Q3 feasible 4/6',reg['Q3']['feasible_count']==4 and reg['Q3']['total_count']==6)
bad=[x['task'] for x in reg['Q3']['rows'] if not x['hard_cap_1p05_ok']]
ok('hard-cap bad cases',bad==['Conv_Case1','Matmul_Case1'])
ok('only Matmul0 time improves',reg['Q3']['only_time_improved_tasks']==['Matmul_Case0'])
val=json.loads((R/'learning_output/analyses/v125_core_protocol/S025_result_registry_validation.json').read_text(encoding='utf-8'))
ok('registry validator ran',val['status']=='PASS' and val['checks']>=12)
ok('known sign mismatch caught',any(x['type']=='REPORTED_PERCENT_MISMATCH' for x in val['issues']))

# Method Composer + figures
mods=json.loads((R/'knowledge_base/method_modules/2025-A-S025-modules.json').read_text(encoding='utf-8'))
ok('transfer modules >=4',len(mods['modules'])>=4)
comp=json.loads((R/'learning_output/analyses/v125_core_protocol/S025_composition_validation.json').read_text(encoding='utf-8'))
ok('composition 7 gates resolved',comp['status']=='PASS' and comp['mainline_recommendation_allowed'] is True)
fig=json.loads((R/'knowledge_base/figure_decision_rules/2025-A-provisional.json').read_text(encoding='utf-8'))
ok('S025 retained in figure-rule basis','S025' in fig.get('paper_basis',[]) and fig.get('status','').startswith('PROVISIONAL_AFTER_'))
ok('figure rules fields',all(all(k in r for k in ['figure_type','why_draw','supports_claim','cannot_prove','new_problem_use_conditions','result_registry_binding']) for r in fig['rules']))

# non-destructive legacy policy
cov=json.loads((R/'learning_output/analyses/v125_core_protocol/legacy_schema_coverage.json').read_text(encoding='utf-8'))
ok('legacy coverage keeps at least v125 cards',len(cov['cards'])>=20)
ok('S025 current schema',next(x for x in cov['cards'] if x['paper_id']=='S025')['missing_new_protocol_fields']==[])
ok('legacy not auto rewritten',any(x['paper_id']=='S020' and x['action'].startswith('NO_AUTO_REREAD') for x in cov['cards']))

# registry / frozen split
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p25=next(x for x in papers if x['paper_id']=='S025')
ok('S025 reviewed all pages',p25['reviewed_pages']==list(range(1,60)))
ok('S025 R2 registry',p25['reproduction_level']=='R2')
ok('45 papers',len(papers)==45)
ok('32/7/6',Counter(p['split'] for p in papers)=={'train':32,'dev':7,'test':6})
# ADAPTED v1.29+: S029 was intentionally opened only after a frozen Dev baseline. Preserve unread Test and unused Dev reserve.
for pid in ['S021','S022','S023','S024','S030','S031','S037','S038']:
    pp=next(x for x in papers if x['paper_id']==pid); ok(pid+' protected unread',pp.get('reviewed_pages',[])==[])
p29=next(x for x in papers if x['paper_id']=='S029'); ok('S029 documented Dev exposure',p29['split']=='dev' and bool(p29.get('reviewed_pages')) and p29.get('dev_boundary')=='DEV_ONLY_NOT_TRAIN_RETRIEVAL')
# No role skill creation
for name in ['mathmodel-master','mathmodel-architect','mathmodel-engineer','mathmodel-writer','mathmodel-reviewer']:
    ok('no role dir '+name,not (R/'.agents/skills'/name).exists())
ver=tuple(map(int,(R/'VERSION').read_text().strip().split('.'))); ok('version >=1.25',ver>=(1,25,0))

print(json.dumps({'status':'PASS','scope':'v1.25 MathModel-Core protocol + S025 first full-schema case','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
