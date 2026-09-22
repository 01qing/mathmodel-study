#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-B-S005-core.json').read_text(encoding='utf-8'))
ok('S005 reviewed',rev['review_status'].startswith('FULL_TEXT'))
ok('S005 Q1-Q3',set(rev['questions'])=={'Q1','Q2','Q3'})
code=json.loads((R/'knowledge_base/code_cases/2024-B-S005-appendix-code.json').read_text(encoding='utf-8'))
ok('S005 not falsely reproduced',code['execution_status'].startswith('NOT_EXECUTED'))
ok('S005 four code audit findings',len(code['audit_findings'])>=4)
fig=json.loads((R/'knowledge_base/figure_argumentation/S005.json').read_text(encoding='utf-8'))
ok('S005 16 unique figures indexed',fig['figure_count_unique']==16 and len(fig['figures'])==16)
for fn in ['grouped-experiment-split-leakage.json','dbm-linear-power-domain.json','noninjective-target-reconstruction.json','regression-accuracy-pseudometric.json','loss-input-contract-mismatch.json','predictive-importance-causal-overclaim.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-B-S005-S008.json').read_text(encoding='utf-8'))
ok('2024-B map retains S005','S005' in cross['papers_reviewed'])
cg=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/case_group_maps.json').read_text(encoding='utf-8'))
ok('2024-B group map linked',cg['2024-B']['papers']==['S005','S006','S007','S008'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S005')
ok('S005 train retained',p['split']=='train')
ok('S005 all 90 pages reviewed',p['reviewed_pages']==list(range(1,91)))
ok('S005 review link',p['review_file']=='knowledge_base/paper_reviews/2024-B-S005-core.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-B-S005-paper-code-audit.md'
ok('S005 audit reference',ref.exists() and ref.stat().st_size>1000)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.13 WLAN gate in skill','v1.13：WLAN实验组、功率量纲与回归指标门禁' in skill)
ok('version at least 1.13',tuple(map(int,(R/'VERSION').read_text().strip().split('.'))) >= (1,13,0))
print(json.dumps({'status':'PASS','scope':'v1.13 S005 full-text and printed appendix audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
