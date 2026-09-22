#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[4]
checks=[]
def ok(name, cond):
    assert cond, name; checks.append(name)
rev=json.loads((R/'knowledge_base/paper_reviews/2024-C-S009-core.json').read_text(encoding='utf-8'))
ok('S009 full review status', rev['review_status'].startswith('FULL_TEXT'))
ok('S009 71 pages', rev['pages']==71)
ok('S009 Q1-Q5', set(rev['questions'])=={'Q1','Q2','Q3','Q4','Q5'})
ok('S009 feature contract warning', any('feature contract' in x.lower() for x in rev['questions']['Q1']['risks']))
ok('S009 held-out temperature warning', any('held-out-temperature' in x.lower() or 'held-out temperature' in x.lower() for x in rev['questions']['Q2']['risks']))
ok('S009 covariate confounding warning', any('confound' in x.lower() and ('frequency' in x.lower() or 'bm' in x.lower()) for x in rev['questions']['Q3']['risks']))
ok('S009 parameter drift warning', any('transcription' in x.lower() or 'mismatch' in x.lower() for x in rev['questions']['Q4']['risks']))
ok('S009 claimed PSO mismatch', any('scipy.optimize.minimize' in x and 'PSO' in x for x in rev['questions']['Q5']['risks']))
ok('S009 reported optimum outside domain', any('exceed' in x.lower() or 'below printed' in x.lower() for x in rev['questions']['Q5']['risks']))
code=json.loads((R/'knowledge_base/code_cases/2024-C-S009-appendix-code.json').read_text(encoding='utf-8'))
ok('S009 partial smoke honest', code['run_status'].startswith('PARTIAL'))
ok('S009 code Q1-Q5', set(code['questions'])=={'Q1','Q2','Q3','Q4','Q5'})
ok('S009 Q5 smoke link', code['smoke_report']=='learning_output/analyses/v117_S009/q5_printed_code_smoke.json')
smoke=json.loads((R/code['smoke_report']).read_text(encoding='utf-8'))
ok('S009 Q5 printed fragment smoke has result', any(k in smoke for k in ['x','result','solution','optimum','x_opt']))
fig=json.loads((R/'knowledge_base/figure_argumentation/S009.json').read_text(encoding='utf-8'))
ok('S009 figure captions indexed', fig['explicit_caption_count']==22)
ok('S009 table captions indexed', fig['table_caption_count']==32)
ok('S009 visual honesty', fig['pixel_level_audit'] is False)
for fn in [
    'feature-contract-train-inference-drift.json',
    'factor-analysis-covariate-confounding.json',
    'parameter-registry-transcription-drift.json',
    'optimization-result-outside-feasible-domain.json',
    'declared-method-not-implemented.json',
]:
    ok(fn, (R/'knowledge_base/error_patterns'/fn).exists())
cross=json.loads((R/'knowledge_base/cross_paper_maps/2024-C-S009-S012.json').read_text(encoding='utf-8'))
ok('2024-C S009 reviewed', 'S009' in cross['papers_reviewed'])
ok('2024-C S009 retained while later papers may progress', 'S009' in cross['papers_reviewed'] and 'S012' in cross['papers'])
ok('2024-C all four declared', cross['papers']==['S009','S010','S011','S012'])
papers=json.loads((R/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
p=next(x for x in papers if x['paper_id']=='S009')
ok('S009 train retained', p['split']=='train')
ok('S009 all pages reviewed', p['reviewed_pages']==list(range(1,72)))
ok('S009 review linked', p['review_file']=='knowledge_base/paper_reviews/2024-C-S009-core.json')
ok('S009 code linked', p['code_audit_file']=='knowledge_base/code_cases/2024-C-S009-appendix-code.json')
ok('S009 figure linked', p['figure_argumentation_file']=='knowledge_base/figure_argumentation/S009.json')
ref=R/'.agents/skills/graduate-mathmodel-learning/references/2024-C-S009-paper-code-audit.md'
ok('S009 audit reference', ref.exists() and ref.stat().st_size>3000)
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ok('v1.17 gate in skill', 'v1.17：特征契约、协变量调整、参数注册与优化可行性门禁' in skill)
sel=(R/'.agents/skills/modeling-paper-rubric-and-model-selector/SKILL.md').read_text(encoding='utf-8')
ok('selector v1.17 gate', '物理-数据混合与优化可行性闸门（v1.17）' in sel)
for rel in ['learning_output/analyses/v117_figure_template_smoke/01_adjusted_interaction.png','learning_output/analyses/v117_figure_template_smoke/02_feasibility_replay.png']:
    ok(rel, (R/rel).exists() and (R/rel).stat().st_size>10000)
v=tuple(map(int,(R/'VERSION').read_text().strip().split('.')[:2])); ok('version at least 1.17',v>=(1,17))
print(json.dumps({'status':'PASS','scope':'v1.17 S009 full-text printed-appendix and Q5 fragment audit','passed':len(checks),'tests':checks},ensure_ascii=False,indent=2))
