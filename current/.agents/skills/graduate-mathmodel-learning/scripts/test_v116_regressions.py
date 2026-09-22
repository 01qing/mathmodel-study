#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-B-S008-core.json').read_text(encoding='utf-8'))
ok('S008 full review status',rev['review_status'].startswith('FULL_TEXT'))
ok('S008 69 pages',rev['pages']==69)
ok('S008 Q1-Q3',set(rev['questions'])=={'Q1','Q2','Q3'})
ok('S008 T1 warning',any('one timestep' in x for x in rev['questions']['Q1']['risks']))
ok('S008 multi-interferer dBm warning',any('subtracts' in x and 'dBm' in x for x in rev['questions']['Q2']['risks']))
ok('S008 noninjective inverse warning',any('non-injective' in x for x in rev['questions']['Q2']['risks']))
ok('S008 metric algebra warning',any('MSE >= MAE^2' in x for x in rev['questions']['Q3']['risks']))
ok('S008 physics baseline recorded',any('physical baseline' in x for x in rev['questions']['Q3']['strengths']))
code=json.loads((R/'knowledge_base/code_cases/2024-B-S008-appendix-code.json').read_text(encoding='utf-8'))
ok('S008 not falsely reproduced',code['run_status'].startswith('NOT_RUN_AS_AUTHOR_PIPELINE'))
ok('S008 code Q1-Q3',set(code['questions'])=={'Q1','Q2','Q3'})
fig=json.loads((R/'knowledge_base/figure_argumentation/S008.json').read_text(encoding='utf-8'))
ok('S008 64 explicit figure captions',fig['explicit_caption_count']==64)
ok('S008 visual honesty',fig['pixel_level_audit'] is False)
for fn in ['single-timestep-rnn-pseudosequence.json','metric-algebra-sanity.json','physics-baseline-before-blackbox.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-B-S005-S008.json').read_text(encoding='utf-8'))
ok('2024-B four papers reviewed',cross['papers_reviewed']==['S005','S006','S007','S008'])
ok('2024-B no pending',cross['papers_pending']==[])
ok('2024-B final recommendation exists',set(cross['final_2024B_recommendation'])=={'Q1','Q2','Q3'})
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S008')
ok('S008 train retained',p['split']=='train')
ok('S008 all pages reviewed',p['reviewed_pages']==list(range(1,70)))
ok('S008 review linked',p['review_file']=='knowledge_base/paper_reviews/2024-B-S008-core.json')
ok('S008 code linked',p['code_audit_file']=='knowledge_base/code_cases/2024-B-S008-appendix-code.json')
ok('S008 figure linked',p['figure_argumentation_file']=='knowledge_base/figure_argumentation/S008.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-B-S008-paper-code-audit.md'
ok('S008 audit reference',ref.exists() and ref.stat().st_size>2500)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.16 gate in skill','v1.16：真实序列、指标代数与物理基线门禁' in skill)
sel=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('selector v1.16 gate','时序模型与指标代数闸门（v1.16）' in sel)
v=tuple(map(int,(R/'VERSION').read_text().strip().split('.')[:2])); ok('version at least 1.16',v>=(1,16))
print(json.dumps({'status':'PASS','scope':'v1.16 S008 full-text and printed appendix audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
