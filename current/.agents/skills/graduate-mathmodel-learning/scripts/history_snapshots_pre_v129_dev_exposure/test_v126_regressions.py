#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)

ok('version >=1.26', tuple(map(int,(R/'VERSION').read_text().strip().split('.'))) >= (1,26,0))
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('MathModel-Core identity retained','MathModel-Core' in skill)
ok('role split still prohibited','不拆分' in skill and 'Method Composer' in skill)

rev=json.loads((R/'knowledge_base/paper_reviews/2025-A-S026-core.json').read_text(encoding='utf-8'))
ok('S026 train',rev['split']=='train')
ok('S026 98 pages',rev['pages']==98)
ok('S026 R2',rev['reproduction']['level']=='R2')
ok('S026 visual separate',rev['reproduction']['visual_audit_separate']['does_not_raise_reproduction_level'] is True)
ok('S026 combinatorial split N/A','NOT_APPLICABLE' in rev['problem_data_contract']['standard_ml_split'])
ok('S026 shared evaluator recommendation',any(('shared evaluator' in x.lower()) or ('common evaluator' in x.lower()) for x in rev['recommended_redo']))

cc=json.loads((R/'knowledge_base/candidate_competitions/S026.json').read_text(encoding='utf-8'))
for q in ['Q1','Q2','Q3']:
    c=cc['questions'][q]
    ok(q+' competition roles',all(k in c for k in ['baseline','author_route','major_alternatives','not_recommended','switch_conditions']))
    ok(q+' six-hour baseline',len(c['baseline']['six_hour_plan'])>=3)
    ok(q+' >=2 alternatives',len(c['major_alternatives'])>=2)
ok('Q1 deterministic baseline','Kahn' in cc['questions']['Q1']['baseline']['name'])
ok('Q2 lifecycle baseline','Best-Fit' in cc['questions']['Q2']['baseline']['name'])
ok('Q3 epsilon baseline','epsilon-constraint' in cc['questions']['Q3']['baseline']['name'])

code=json.loads((R/'knowledge_base/code_cases/2025-A-S026-appendix-code.json').read_text(encoding='utf-8'))
ids={x['id'] for x in code['findings']}
for fid in ['Q1_PRIORITY_FEATURE_DRIFT','Q1_TABU_TOKENIZATION','Q2_QUANTUM_PRIMITIVES_DEAD','Q2_UNNORMALIZED_MIXED_OBJECTIVE','Q2_GLOBALBEST_DESYNC','Q3_SPILL_COST_FORMULA_DRIFT','Q3_IMPLEMENTATION_ABSENT','Q3_HARD_CAP_NOT_FORMALIZED']:
    ok('code finding '+fid,fid in ids)
ok('R3 explicitly blocked',len(code['r3_blockers'])>=3)

reg=json.loads((R/'knowledge_base/result_registry/S026.json').read_text(encoding='utf-8'))
ok('Q1 six workloads',len(reg['Q1']['max_vstay_bytes'])==6)
ok('Q1 S026 never beats S025',not any(x['S026_better'] for x in reg['Q1']['cross_paper_vs_S025']))
ok('Q1 Conv0 worse by 6932',next(x for x in reg['Q1']['cross_paper_vs_S025'] if x['task']=='Conv_Case0')['delta_S026_minus_S025']==6932)
ok('Q2 six workloads',len(reg['Q2']['rows'])==6)
ok('Q2 S026 transfer higher all six',all(not x['S026_lower'] for x in reg['Q2']['cross_paper_vs_S025']))
ok('Q3 six rows',len(reg['Q3']['rows'])==6)
ok('Q3 transfer formula inconsistent',reg['Q3']['formula_contract']['status']=='INCONSISTENT')
val=json.loads((R/'learning_output/analyses/v126_S026/S026_result_registry_validation.json').read_text(encoding='utf-8'))
ok('S026 registry validator',val['status']=='PASS' and val['checks']>=12)

mods=json.loads((R/'knowledge_base/method_modules/2025-A-S026-modules.json').read_text(encoding='utf-8'))
ok('S026 transferable modules >=4',len(mods['modules'])>=4)
comp=json.loads((R/'learning_output/analyses/v126_S026/S025_S026_composition_contract.json').read_text(encoding='utf-8'))
ok('composer adapter decision',comp['decision']=='compatible_after_adapter' and comp['mainline_recommendation_allowed'] is True)
ok('composer blocks fake QPSO',any('ABQPSO' in x['module'] for x in comp['blocked_components']))
ok('composer blocks DPEA mainline',any('DPEA' in x['module'] for x in comp['blocked_components']))

fig=json.loads((R/'knowledge_base/figure_decision_rules/2025-A-provisional.json').read_text(encoding='utf-8'))
ok('figure rules preserve S025 S026',all(x in fig['paper_basis'] for x in ['S025','S026']))
ok('Pareto actual plot required',any('actual feasible Pareto' in r.get('better_alternative','') for r in fig['rules']))

mp=json.loads((R/'knowledge_base/cross_paper_maps/2025-A-S025-S028.json').read_text(encoding='utf-8'))
ok('2025A preserves reviewed S025 S026',all(x in mp['papers_reviewed'] for x in ['S025','S026']))
ok('2025A preserves S025-S026 knowledge',all(x in mp['papers_reviewed'] for x in ['S025','S026']))
ok('2025A map status valid',mp['current_status'].startswith('PROVISIONAL_') or mp['current_status'].startswith('FINAL_'))

for fn in ['priority-feature-paper-code-drift.json','algorithm-defining-primitives-dead-code.json','global-best-state-score-desynchronization.json','cross-question-objective-definition-drift.json','metaheuristic-without-matched-budget-baseline.json']:
    ok('error pattern '+fn,(R/'knowledge_base/error_patterns'/fn).exists())

papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
ok('45 papers',len(papers)==45)
ok('32/7/6 split',Counter(p['split'] for p in papers)=={'train':32,'dev':7,'test':6})
p26=next(x for x in papers if x['paper_id']=='S026')
ok('S026 all pages reviewed',p26['reviewed_pages']==list(range(1,99)))
ok('S026 registry R2',p26['reproduction_level']=='R2')
p27=next(x for x in papers if x['paper_id']=='S027'); ok('S027 remains train',p27['split']=='train')
p28=next(x for x in papers if x['paper_id']=='S028'); ok('S028 remains train',p28['split']=='train')
for pid in ['S029','S030']:
    pp=next(x for x in papers if x['paper_id']==pid); ok(pid+' dev protected unread',pp.get('reviewed_pages',[])==[] and pp['split']=='dev')
for pp in [x for x in papers if x['split']=='test']:
    ok(pp['paper_id']+' test protected unread',pp.get('reviewed_pages',[])==[])

state=json.loads((R/'learning_output/context/learning_state.json').read_text(encoding='utf-8'))
ok('state preserves S026-or-later',tuple(map(int,state['current_version'].split('.'))) >= (1,26,0) and state['latest_completed_paper'] in ['S026','S027','S028'])
ok('mini transfer protocol preserved','Mini Transfer Test' in (R/'learning_output/context/next_learning.md').read_text(encoding='utf-8'))

print(json.dumps({'status':'PASS','scope':'v1.26 MathModel-Core S026 full protocol','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
