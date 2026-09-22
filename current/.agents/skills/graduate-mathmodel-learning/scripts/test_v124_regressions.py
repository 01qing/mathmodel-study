#!/usr/bin/env python3
from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond): assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-E-S020-core.json').read_text(encoding='utf-8'))
ok('S020 full review',rev['review_status'].startswith('FULL_TEXT'))
ok('S020 78 pages',rev['pages']==78)
ok('S020 train split',rev['split']=='train')
ok('S020 Q1-Q4',set(rev['questions'])=={'Q1','Q2','Q3','Q4'})
ok('target leakage risk',any('target variable is directly included' in x for x in rev['questions']['Q1']['risks']))
ok('global scaler leakage risk',any('MinMaxScaler' in x and 'before' in x for x in rev['questions']['Q1']['risks']))
ok('T1 risk',any('T=1' in x for x in rev['questions']['Q1']['risks']))
ok('SKNet drift',any('Split/Fuse/Select' in x for x in rev['questions']['Q1']['risks']))
ok('worst group negative R2',any('-0.81001' in x for x in rev['questions']['Q1']['risks']))
ok('shockwave time sign',any('nonnegative' in x or 'negative' in x for x in rev['questions']['Q2']['risks']))
ok('Greenshields replay',any('42.265' in x and '78.868' in x for x in rev['questions']['Q3']['risks']))
ok('79.72 claim replay',any('79.72' in x for x in rev['questions']['Q3']['risks']))
ok('utilization claim replay',any('69.44' in x and '90.28' in x for x in rev['questions']['Q3']['risks']))
ok('layout heuristic boundary',any('optimization' in x.lower() for x in rev['questions']['Q4']['risks']))
code=json.loads((R/'knowledge_base/code_cases/2024-E-S020-appendix-code.json').read_text(encoding='utf-8'))
ok('printed appendix boundary',code['run_status'].startswith('PRINTED_PYTHON_STATIC_AUDIT'))
ok('Q2 no state machine',any('No executable' in x for x in code['questions']['Q2']['findings']))
ok('Q3 no sim code',any('No executable' in x for x in code['questions']['Q3']['findings']))
ok('Q4 no optimizer code',any('No camera-placement optimization' in x for x in code['questions']['Q4']['findings']))
fig=json.loads((R/'knowledge_base/figure_argumentation/S020.json').read_text(encoding='utf-8'))
ok('S020 curated 43 figures',fig['figure_count_indexed']==43)
ok('S020 28 table labels',fig['table_count_indexed']==28)
ok('S020 no pixel overclaim','not mounted original S020 PDF pixels' in fig['style_learning_boundary'])
for rel in fig['derived_template_smoke']: ok(rel,(R/rel).exists() and (R/rel).stat().st_size>5000)
for fn in ['target-feature-identity-leakage.json','single-timestep-sequence-model.json','architecture-name-implementation-drift.json','worst-group-metric-ignored.json','model-state-counterfactual-inconsistency.json','cross-domain-template-contamination.json','heuristic-layout-presented-as-optimization.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-E-S017-S020.json').read_text(encoding='utf-8'))
ok('2024E all four reviewed',cross['papers_reviewed']==['S017','S018','S019','S020'])
ok('2024E none pending',cross['papers_pending']==[])
ok('2024E final route', 'target-leakage' in cross['current_recommendation'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p20=next(x for x in papers if x['paper_id']=='S020')
ok('S020 registry reviewed',p20['reviewed_pages']==list(range(1,79)))
for pid in ['S013','S014','S015','S016']:
    pp=next(x for x in papers if x['paper_id']==pid); ok(pid+' remains dev split',pp.get('split')=='dev')
for pid in ['S021','S022','S023','S024','S037','S038']:
    pp=next(x for x in papers if x['paper_id']==pid); ok(pid+' test remains unread',pp.get('split')=='test' and pp.get('reviewed_pages',[])==[])
ok('45 paper inventory',len(papers)==45)
from collections import Counter
ok('32/7/6 split',Counter(p['split'] for p in papers)=={'train':32,'dev':7,'test':6})
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-E-S020-paper-code-audit.md'
ok('S020 audit reference',ref.exists() and ref.stat().st_size>1800)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.24 gates in skill','v1.24：目标泄漏、模型自洽反事实与最差组门禁' in skill)
sel=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('v1.24 selector gates','目标泄漏、最差组与反事实自洽闸门（v1.24）' in sel)
state=json.loads((R/'learning_output/context/learning_state.json').read_text(encoding='utf-8'))
ok('S025 next', 'S025' in json.dumps(state,ensure_ascii=False))
from packaging.version import Version
ok('version >=1.24',Version((R/'VERSION').read_text().strip())>=Version('1.24.0'))
print(json.dumps({'status':'PASS','scope':'v1.24 S020 target leakage / counterfactual / worst-group / layout audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
