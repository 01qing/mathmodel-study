#!/usr/bin/env python3
from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-B-S007-core.json').read_text(encoding='utf-8'))
ok('S007 full review status',rev['review_status'].startswith('FULL_TEXT'))
ok('S007 113 pages',rev['pages']==113)
ok('S007 Q1-Q3',set(rev['questions'])=={'Q1','Q2','Q3'})
ok('S007 dBm-to-mW strength recorded',any('mW' in x for x in rev['questions']['Q2']['strengths']))
ok('S007 imbalance warning recorded',any('0.98' in x for x in rev['questions']['Q2']['risks']))
ok('S007 cross-section drift recorded',any('copy' in x.lower() or 'contradict' in x.lower() for x in rev['questions']['Q3']['risks']))
code=json.loads((R/'knowledge_base/code_cases/2024-B-S007-appendix-code.json').read_text(encoding='utf-8'))
ok('S007 not falsely reproduced',code['run_status'].startswith('NOT_RUN_AS_AUTHOR_PIPELINE'))
ok('S007 code Q1-Q3',set(code['questions'])=={'Q1','Q2','Q3'})
fig=json.loads((R/'knowledge_base/figure_argumentation/S007.json').read_text(encoding='utf-8'))
ok('S007 68 explicit figure captions',fig['explicit_caption_count']==68)
ok('S007 visual honesty',fig['pixel_level_audit'] is False)
for fn in ['independent-structured-label-decoding.json','class-imbalance-accuracy-overclaim.json','log-domain-rssi-aggregation.json','cross-section-metric-drift.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-B-S005-S008.json').read_text(encoding='utf-8'))
ok('2024-B historical S005-S007 retained',set(['S005','S006','S007']).issubset(set(cross['papers_reviewed'])))
ok('2024-B group membership retained',cross['papers']==['S005','S006','S007','S008'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S007')
ok('S007 train retained',p['split']=='train')
ok('S007 all pages reviewed',p['reviewed_pages']==list(range(1,114)))
ok('S007 review linked',p['review_file']=='knowledge_base/paper_reviews/2024-B-S007-core.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-B-S007-paper-code-audit.md'
ok('S007 audit reference',ref.exists() and ref.stat().st_size>2200)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.15 gate in skill','v1.15：结构化标签、类别不平衡与跨章节指标一致性门禁' in skill)
sel=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('selector structured label gate','结构化分类与不平衡指标闸门（v1.15）' in sel)
spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('imbalance figure template',hasattr(mod,'imbalanced_classification_dashboard'))
ok('structured pair template',hasattr(mod,'structured_pair_validity'))
smoke=R/'learning_output/analyses/v115_figure_template_smoke'
ok('two v115 smoke figures',len([x for x in smoke.glob('*.png') if x.stat().st_size>20000])==2)
v=tuple(map(int,(R/'VERSION').read_text().strip().split('.')[:2])); ok('version at least 1.15',v>=(1,15))
print(json.dumps({'status':'PASS','scope':'v1.15 S007 full-text and printed appendix audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
