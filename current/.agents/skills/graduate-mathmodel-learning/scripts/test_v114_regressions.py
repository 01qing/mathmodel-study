#!/usr/bin/env python3
from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-B-S006-core.json').read_text(encoding='utf-8'))
ok('S006 full review status',rev['review_status'].startswith('FULL_TEXT'))
ok('S006 Q1-Q3',set(rev['questions'])=={'Q1','Q2','Q3'})
ok('S006 API smoke recorded','dim 3' in rev['api_smoke']['result'])
code=json.loads((R/'knowledge_base/code_cases/2024-B-S006-appendix-code.json').read_text(encoding='utf-8'))
ok('S006 not falsely reproduced',code['run_status'].startswith('NOT_RUN_AS_AUTHOR_PIPELINE'))
ok('S006 code audit Q1-Q3',set(code['questions'])=={'Q1','Q2','Q3'})
fig=json.loads((R/'knowledge_base/figure_argumentation/S006.json').read_text(encoding='utf-8'))
ok('S006 30 explicit figure captions',fig['explicit_caption_count']==30 and len(fig['figures'])==30)
ok('S006 visual honesty',fig['visual_review_status'].endswith('PENDING'))
for fn in ['target-encoding-before-split-leakage.json','oversampling-before-split-leakage.json','cascade-groundtruth-intermediate-mismatch.json','posthoc-output-noise-as-robustness.json','resampler-shape-contract.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-B-S005-S008.json').read_text(encoding='utf-8'))
ok('2024-B S005/S006 remain reviewed',all(x in cross['papers_reviewed'] for x in ['S005','S006']))
ok('2024-B Q1-Q3 map',set(cross['questions'])=={'Q1','Q2','Q3'})
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S006')
ok('S006 train retained',p['split']=='train')
ok('S006 all 104 pages reviewed',p['reviewed_pages']==list(range(1,105)))
ok('S006 review linked',p['review_file']=='knowledge_base/paper_reviews/2024-B-S006-core.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-B-S006-paper-code-audit.md'
ok('S006 audit reference',ref.exists() and ref.stat().st_size>1800)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.14 OOF gate in skill','v1.14：过采样、目标编码与级联模型 OOF 门禁' in skill)
ms=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('selector integrates cascade gate','级联/stacking 与不平衡分类的选择闸门' in ms)
spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('cascade figure template',hasattr(mod,'cascade_oof_validation'))
ok('resampling diagnostic template',hasattr(mod,'resampling_partition_diagnostic'))
smoke=R/'learning_output/analyses/v114_figure_template_smoke'
ok('two v114 smoke figures',len([x for x in smoke.glob('*.png') if x.stat().st_size>20000])==2)
ok('version at least 1.14',tuple(map(int,(R/'VERSION').read_text().strip().split('.'))) >= (1,14,0))
print(json.dumps({'status':'PASS','scope':'v1.14 S006 full-text and printed appendix audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
