#!/usr/bin/env python3
from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-A-S004-core.json').read_text(encoding='utf-8'))
ok('S004 four questions reviewed',len(rev.get('questions',[]))==4)
ok('S004 ids 1-4',{str(x['question_id']) for x in rev['questions']}=={'1','2','3','4'})
fig=json.loads((R/'knowledge_base/figure_argumentation/S004.json').read_text(encoding='utf-8'))
ok('S004 41 caption-like occurrences indexed',fig.get('figure_count_caption_occurrences')==41 and len(fig.get('figures',[]))==41)
ok('S004 visual review honest pending',fig.get('visual_review_status','').startswith('PENDING_ORIGINAL_PDF'))
ok('S004 figure numbering/caption anomalies recorded',len(fig.get('numbering_issues',[]))>=5)
code=json.loads((R/'knowledge_base/code_cases/2024-A-S004-appendix-code.json').read_text(encoding='utf-8'))
ok('S004 appendix audit Q1-Q4',set(code.get('questions',{}))=={'Q1','Q2','Q3','Q4'})
ok('S004 not falsely reproduced',code.get('run_status','').startswith('NOT_RUN'))
ok('Q3 objective implementation missing recorded','objective/evaluation code absent' in ' '.join(code['questions']['Q3']['findings']))
ok('Q4 cross-turbine state leakage recorded','cross-turbine state leakage' in ' '.join(code['questions']['Q4']['findings']))
for fn in ['overlapping-window-cycle-double-counting.json','entity-state-not-reset.json','calibration-evaluation-same-data.json','multi-metric-overall-win-overclaim.json','unit-insensitive-event-threshold.json','physical-parameter-semantic-substitution.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-A-S001-S004.json').read_text(encoding='utf-8'))
ok('same problem map has four papers',cross.get('papers')==['S001','S002','S003','S004'])
ok('same problem map Q1-Q4',set(cross.get('questions',{}))=={'Q1','Q2','Q3','Q4'})
cg=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/case_group_maps.json').read_text(encoding='utf-8'))
ok('group map points S001-S004',cg['2024-A']['cross_paper_map']=='knowledge_base/cross_paper_maps/2024-A-S001-S004.json')
ok('group has 4 papers',cg['2024-A']['papers']==['S001','S002','S003','S004'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S004')
ok('S004 train split retained',p['split']=='train')
ok('S004 core reviewed metadata',p.get('learning_status','').startswith('CORE_REVIEWED'))
ok('S004 all 59 pages reviewed',p.get('reviewed_pages')==list(range(1,60)))
ok('S004 review linked',p.get('review_file')=='knowledge_base/paper_reviews/2024-A-S004-core.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-A-S004-paper-code-audit.md'
ok('S004 audit ref',ref.exists() and ref.stat().st_size>1000)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.12 state/metric gate in skill','v1.12：独立实体状态、多指标与校准证据门禁' in skill)
spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('runtime latency template',hasattr(mod,'runtime_latency_distribution'))
ok('multi-metric tradeoff template',hasattr(mod,'multi_metric_tradeoff'))
smoke=R/'learning_output/analyses/v112_figure_template_smoke'
ok('two nonempty v112 smoke PNGs',len([x for x in smoke.glob('*.png') if x.stat().st_size>10000])==2)
print(json.dumps({'status':'PASS','scope':'v1.12 S004 full-text and appendix audit regressions','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
