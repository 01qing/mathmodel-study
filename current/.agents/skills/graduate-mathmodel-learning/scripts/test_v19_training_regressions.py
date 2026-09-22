from pathlib import Path
import json, importlib.util
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name,cond):
    assert cond,name; checks.append(name)
# cards exist and parse
for sid in ['S039','S040','S041']:
    rev=json.loads((R/f'knowledge_base/paper_reviews/2025-E-{sid}-core.json').read_text(encoding='utf-8'))
    ok(f'{sid} four questions',len(rev['questions'])==4)
    fig=json.loads((R/f'knowledge_base/figure_argumentation/2025-E-{sid}.json').read_text(encoding='utf-8'))
    ok(f'{sid} figure argumentation',len(fig['argumentation'])>=4)
# cross map and code boundaries
cross=json.loads((R/'knowledge_base/cross_paper_maps/2025-E-S039-S041-with-code.json').read_text(encoding='utf-8'))
ok('cross map Q1-Q4',set(cross['question_map'])=={'Q1','Q2','Q3','Q4'})
ok('teacher code identity boundary','不表示教师代码是对应论文官方附录实现' in cross['identity_boundary'])
links=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/code_case_links.json').read_text(encoding='utf-8'))['2025-E']
ok('two supplemental code cases',len(links)==2)
ok('GTeacher2 Q3 CORAL',any('CORAL' in x for x in links[1]['question_links']['Q3']))
# learned error patterns
for fn in ['overlapping-window-split-leakage.json','unlabeled-target-metric-overclaim.json','preprocessing-before-split-leakage.json']:
    ok(fn,(R/'knowledge_base/error_patterns'/fn).exists())
# figure templates and smoke images
spec=importlib.util.spec_from_file_location('eft',R/'.agents/skills/data-cleaning-and-visualization/scripts/evidence_figure_templates.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ok('five evidence figure templates',all(hasattr(mod,n) for n in ['paired_embedding','confusion_grid','repeated_metric_boxplot','target_probability_heatmap','signal_mechanism_four_panel']))
smoke=R/'learning_output/analyses/v19_figure_template_smoke'
ok('five nonempty smoke PNGs',len([p for p in smoke.glob('*.png') if p.stat().st_size>10000])==5)
# status metadata
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
sel={p['paper_id']:p for p in papers if p['paper_id'] in {'S039','S040','S041'}}
ok('2025E papers core-reviewed metadata',all(p['learning_status'].startswith('CORE_REVIEWED') for p in sel.values()))
print(json.dumps({'status':'PASS','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
