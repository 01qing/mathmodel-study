#!/usr/bin/env python3
from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name, cond):
    assert cond, name
    checks.append(name)

rev=json.loads((R/'knowledge_base/paper_reviews/2024-A-S003-core.json').read_text(encoding='utf-8'))
qs=rev.get('questions',{})
ok('S003 four questions reviewed', len(qs)==4)
ok('S003 question ids 1-4', {str(q.get('question_id')) for q in qs}=={'1','2','3','4'})

fig=json.loads((R/'knowledge_base/figure_argumentation/S003.json').read_text(encoding='utf-8'))
ok('S003 42 caption occurrences indexed', fig.get('figure_count_main_text')==42 and len(fig.get('figures',[]))==42)
ok('S003 visual audit honestly pending source PDF', 'PENDING_ORIGINAL_PDF' in fig.get('visual_review_status',''))
ok('S003 numbering anomalies recorded', len(fig.get('numbering_issues',[]))>=3)

code=json.loads((R/'knowledge_base/code_cases/2024-A-S003-appendix-code.json').read_text(encoding='utf-8'))
ok('S003 appendix audit covers Q1-Q4', set(code.get('questions',{}).keys())=={'Q1','Q2','Q3','Q4'})
ok('S003 appendix not falsely marked reproduced', code.get('run_status','').startswith('NOT_RUN'))
ok('S003 Q3 major mismatch recorded', 'MAJOR_MISMATCH' in code['questions']['Q3']['status'])
ok('S003 Q4 major mismatch recorded', 'MAJOR_MISMATCH' in code['questions']['Q4']['status'])

for fn in [
    'declared-method-not-implemented.json',
    'scipy-ineq-sign-convention.json',
    'physical-feature-scaling-unit-break.json',
    'mpc-label-without-horizon.json',
    'robustness-single-severity-overclaim.json']:
    ok(fn, (R/'knowledge_base/error_patterns'/fn).exists())

cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-A-S001-S003.json').read_text(encoding='utf-8'))
ok('S001-S003 cross map has three same-problem papers', cross.get('papers')==['S001','S002','S003'])
qmap=cross.get('questions',cross.get('question_map',{}))
ok('S001-S003 cross map Q1-Q4', set(qmap.keys())=={'Q1','Q2','Q3','Q4'})

cg=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/case_group_maps.json').read_text(encoding='utf-8'))
ok('2024-A group map still represents reviewed S001-S003+', cg['2024-A']['cross_paper_map'].startswith('knowledge_base/cross_paper_maps/2024-A-S001-S00'))
ok('2024-A group map contains S001-S003', cg['2024-A']['papers'][:3]==['S001','S002','S003'])

spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('Pareto selected-point template available', hasattr(mod,'pareto_front_operating_point'))
ok('robustness severity template available', hasattr(mod,'robustness_severity_curve'))
smoke=R/'learning_output/analyses/v111_figure_template_smoke'
ok('two nonempty v111 smoke PNGs', len([p for p in smoke.glob('*.png') if p.stat().st_size>10000])==2)

papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S003')
ok('S003 train split retained', p.get('split')=='train')
ok('S003 metadata core reviewed', p.get('learning_status','').startswith('CORE_REVIEWED'))
ok('S003 all 73 pages reviewed', p.get('reviewed_pages')==list(range(1,74)))
ok('S003 review file linked', p.get('review_file')=='knowledge_base/paper_reviews/2024-A-S003-core.json')

ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-A-S003-paper-code-audit.md'
ok('S003 paper-code audit reference exists', ref.exists() and ref.stat().st_size>500)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.11 implementation-evidence gate in Skill', 'v1.11：复杂算法名称的实现证据门禁' in skill)

print(json.dumps({'status':'PASS','scope':'v1.11 S003 full-text and appendix audit regressions','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
