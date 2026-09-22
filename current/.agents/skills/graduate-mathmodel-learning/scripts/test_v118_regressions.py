#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name, cond):
    assert cond, name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-C-S010-core.json').read_text(encoding='utf-8'))
ok('S010 full review status', rev['review_status'].startswith('FULL_TEXT'))
ok('S010 82 pages', rev['pages']==82)
ok('S010 Q1-Q5', set(rev['questions'])=={'Q1','Q2','Q3','Q4','Q5'})
ok('S010 Q2 unseen-condition warning', any('unseen temperature' in x.lower() or 'leave-temperature' in x.lower() for x in rev['questions']['Q2']['risks']))
ok('S010 Q3 non-significance warning', any('nonsignificant' in x.lower() and 'independent' in x.lower() for x in rev['questions']['Q3']['risks']))
ok('S010 Q4 transform mismatch', any('raw maxb' in x.lower() or 'log(maxb)' in x.lower() for x in rev['questions']['Q4']['risks']))
ok('S010 Q4 final path gap', any('igse' in x.lower() and ('not reproduced' in x.lower() or 'no visible' in x.lower()) for x in rev['questions']['Q4']['risks']))
ok('S010 Q4 sum mean mismatch', any('true_mse' in x.lower() and 'dividing' in x.lower() for x in rev['questions']['Q4']['risks']))
ok('S010 Q5 scale warning', any('different units' in x.lower() or 'normalization' in x.lower() for x in rev['questions']['Q5']['risks']))
ok('S010 Q5 encoder bug', any('all zero' in x.lower() or 'all-zero' in x.lower() for x in rev['questions']['Q5']['risks']))
ok('S010 Q5 GWO implementation gap', any('gwo' in x.lower() and 'not' in x.lower() for x in rev['questions']['Q5']['risks']))
code=json.loads((R/'knowledge_base/code_cases/2024-C-S010-appendix-code.json').read_text(encoding='utf-8'))
ok('S010 partial smoke honest', code['run_status'].startswith('PARTIAL'))
ok('S010 code Q1-Q5', set(code['questions'])=={'Q1','Q2','Q3','Q4','Q5'})
ok('S010 smoke report linked', code['smoke_report']=='learning_output/analyses/v118_S010/q5_feature_contract_smoke.json')
smoke=json.loads((R/code['smoke_report']).read_text(encoding='utf-8'))
ok('S010 all 12 category pairs collapse', smoke['all_12_pairs_collapse_to_zero_category_vectors'] is True and len(smoke['examples'])==12)
fig=json.loads((R/'knowledge_base/figure_argumentation/S010.json').read_text(encoding='utf-8'))
ok('S010 figure captions indexed', fig['explicit_caption_count']==32)
ok('S010 table captions indexed', fig['table_caption_count']==33)
ok('S010 visual honesty', fig['pixel_level_audit'] is False)
for fn in [
    'metric-name-direction-mismatch.json',
    'unnormalized-weighted-objective-scale-dominance.json',
    'computed-feature-not-used.json',
    'categorical-encoding-type-mismatch.json',
    'mean-sum-metric-mislabel.json',
]: ok(fn, (R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-C-S009-S012.json').read_text(encoding='utf-8'))
ok('2024-C S009 S010 reviewed', {'S009','S010'}.issubset(set(cross['papers_reviewed'])))
ok('2024-C S009 S010 retained while S012 may progress', {'S009','S010'}.issubset(set(cross['papers_reviewed'])) and 'S012' in cross['papers'])
ok('2024-C all four declared', cross['papers']==['S009','S010','S011','S012'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S010')
ok('S010 train retained', p['split']=='train')
ok('S010 all pages reviewed', p['reviewed_pages']==list(range(1,83)))
ok('S010 review linked', p['review_file']=='knowledge_base/paper_reviews/2024-C-S010-core.json')
ok('S010 code linked', p['code_audit_file']=='knowledge_base/code_cases/2024-C-S010-appendix-code.json')
ok('S010 figure linked', p['figure_argumentation_file']=='knowledge_base/figure_argumentation/S010.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-C-S010-paper-code-audit.md'
ok('S010 audit reference', ref.exists() and ref.stat().st_size>2500)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.18 gate in skill', 'v1.18：泛化单位、类别编码与目标尺度门禁' in skill)
sel=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('selector v1.18 gate', '泛化单位与混合优化编码闸门（v1.18）' in sel)
for rel in [
    'learning_output/analyses/v118_figure_template_smoke/01_cv_generalization_units.png',
    'learning_output/analyses/v118_figure_template_smoke/02_objective_scale_audit.png',
    'learning_output/analyses/v118_figure_template_smoke/01_category_contract.png',
    'learning_output/analyses/v118_figure_template_smoke/02_scalarization_sensitivity.png',
]: ok(rel, (R/rel).exists() and (R/rel).stat().st_size>5000)
v=tuple(map(int,(R/'VERSION').read_text().strip().split('.')[:2])); ok('version at least 1.18',v>=(1,18))
print(json.dumps({'status':'PASS','scope':'v1.18 S010 full-text printed-appendix/category-contract audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
