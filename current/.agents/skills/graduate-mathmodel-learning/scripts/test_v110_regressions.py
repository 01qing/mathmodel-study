#!/usr/bin/env python3
from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name, cond):
    assert cond, name
    checks.append(name)

rev=json.loads((R/'knowledge_base/paper_reviews/2024-A-S002-core.json').read_text(encoding='utf-8'))
ok('S002 four questions', len(rev.get('questions',{}))==4)
fig=json.loads((R/'knowledge_base/figure_argumentation/S002.json').read_text(encoding='utf-8'))
# Allow either list or dict form while requiring substantial figure indexing.
figures=fig.get('figures', [])
ok('S002 figure index has 63 main-text figures', len(figures)==63)
ok('S002 argumentation roles recorded', len(fig.get('argumentation',[]))>=4)

cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-A-S001-S002.json').read_text(encoding='utf-8'))
qmap=cross.get('question_map', cross.get('questions', {}))
ok('S001-S002 cross map Q1-Q4', set(qmap.keys())=={'Q1','Q2','Q3','Q4'})

for fn in [
    'paper-code-evaluation-split-mismatch.json',
    'aggregate-feasibility-overclaim.json',
    'pareto-operating-point-selection.json',
    'metric-definition-code-mismatch.json',
    'arithmetic-sanity-check.json']:
    ok(fn, (R/'knowledge_base/error_patterns'/fn).exists())

spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('prediction evidence template', hasattr(mod,'prediction_curve_with_parity') or hasattr(mod,'prediction_curve_parity'))
ok('constraint validation template', hasattr(mod,'constraint_validation_dashboard') or hasattr(mod,'constraint_validation'))
smoke=R/'learning_output/analyses/v110_figure_template_smoke'
ok('two nonempty v110 smoke PNGs', len([p for p in smoke.glob('*.png') if p.stat().st_size>10000])==2)

papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S002')
ok('S002 metadata core reviewed', p.get('learning_status','').startswith('CORE_REVIEWED'))
ok('S002 all pages reviewed', len(p.get('reviewed_pages',[]))==79)

ref=(R/'.agents/skills/graduate-mathmodel-learning/references/2024-A-S001-S002-method-selection.md')
ok('method selection reference exists', ref.exists() and ref.stat().st_size>500)
print(json.dumps({'status':'PASS','scope':'v1.10 S002 learning regressions','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
