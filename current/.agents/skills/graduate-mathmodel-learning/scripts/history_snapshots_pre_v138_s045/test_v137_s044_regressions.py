from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(n,c):
    assert c,n; checks.append(n)
def load(r): return json.loads((ROOT/r).read_text(encoding='utf-8'))
P={x['paper_id']:x for x in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
st=load('learning_output/context/learning_state.json')
ck('version',st['current_version']=='1.37.0')
ck('latest',st['latest_completed_paper']=='S044')
ck('R2 latest',st['reproduction_level_latest']=='S044:R2')
req=[
 'knowledge_base/paper_reviews/2025-F-S044-core.json','knowledge_base/candidate_competitions/S044.json',
 'knowledge_base/result_registry/S044.json','knowledge_base/code_cases/2025-F-S044-printed-code-audit.json',
 'knowledge_base/method_modules/2025-F-S044-modules.json','knowledge_base/figure_argumentation/S044.json',
 'knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/figure_decision_rules/2025-F-provisional.json',
 'learning_output/analyses/S044_source_audit.json','learning_output/analyses/S044_result_registry_replay.json','S044_v1.37_训练摘要.md']
for r in req: ck('exists '+r,(ROOT/r).exists() and (ROOT/r).stat().st_size>0)
rv=load('knowledge_base/paper_reviews/2025-F-S044-core.json')
ck('pages 116',rv['pages']==116)
ck('R2',rv['reproduction']['level']=='R2')
ck('visual full','116-PAGE' in rv['visual_status'])
ck('printed audit evidence',any('printed Python appendix' in x for x in rv['reproduction']['evidence']))
ck('no R3',any('R3:' in x for x in rv['reproduction']['not_achieved']))
ck('reviewed 116',P['S044']['reviewed_pages']==list(range(1,117)))
ck('S044 train',P['S044']['split']=='train')
ck('S042 preserved',P['S042']['split']=='train' and len(P['S042']['reviewed_pages'])==182)
ck('S043 preserved',P['S043']['split']=='train' and len(P['S043']['reviewed_pages'])==71)
ck('S045 unread train',P['S045']['split']=='train' and P['S045']['reviewed_pages']==[])
for pid in ['S030','S031']: ck(pid+' dev reserve',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']: ck(pid+' test frozen',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
reg=load('knowledge_base/result_registry/S044.json'); ids={e['id'] for e in reg['entries']}
for x in ['Q1_PAPER_CODE_OPTIMIZER_DRIFT','Q1_WEIGHTED_SCALAR_VS_PARETO','Q2_FIXED_SCORE_INJECTION','Q2_RANDOM_REAL_FEATURES','Q2_WEIGHT_METHOD_DRIFT','Q2_KAPPA_THRESHOLD_STRICT','Q2_VALIDATION_PROVENANCE','Q3_PVALUE_SURFACE_SWAP','Q3_MULTIMODAL_CODE_COLLAPSE','Q3_PAIRWISE_ENTITY_SPLIT','Q3_R2_METRIC_CLAMP','Q3_FIXED_CV_METRICS','Q3_SELF_SIMILARITY_DIAGONAL']:
    ck(x,x in ids)
rep=load('learning_output/analyses/S044_result_registry_replay.json')['checks']
ck('Q2 sums exact',rep['Q2_table13_component_sum_exact_all_10'] is True)
ck('Q2 ten sums',len(rep['Q2_table13_component_sums'])==10)
ck('Q2 Jichang sum',abs(rep['Q2_table13_component_sums']['寄畅园']-100.0)<1e-12)
ck('Q2 Zhuozheng sum',abs(rep['Q2_table13_component_sums']['拙政园']-96.5)<1e-12)
ck('Q2 kappa exact',rep['Q2_kappa_reported']==0.833)
ck('Q2 strict fail',rep['Q2_kappa_strict_pass'] is False)
ck('Q3 p swap flag',rep['Q3_pvalue_labels_swapped'] is True)
ck('Q3 prose Pearson p',rep['Q3_prose_pvalues']['Pearson']==0.012)
ck('Q3 table Pearson p',rep['Q3_table17_pvalues']['Pearson']==0.018)
ck('Q3 cv constants match',rep['Q3_table19_equals_code_constants'] is True)
ck('Q3 R2 clamp',rep['Q3_printed_r2_clamp']==[0.75,0.95])
ca=load('knowledge_base/code_cases/2025-F-S044-printed-code-audit.json')
ck('code R2',ca['reproduction_level']=='R2')
ck('Q1 Dijkstra',any('Dijkstra' in x for x in ca['Q1']['printed_primitives']))
ck('Q1 no GA',any('no GA population loop' in x for x in ca['Q1']['missing_or_drift']))
ck('Q2 fixed output','score dictionaries' in ca['Q2']['hardcoded_outputs'] and 'inject' in ca['Q2']['hardcoded_outputs'])
ck('Q2 random placeholder',len(ca['Q2']['random_or_placeholder'])>=4)
ck('Q3 omitted training',any('training loop is omitted' in x for x in ca['Q3']['missing_or_drift']))
ck('Q3 hardcoded cv',any('30.0' in x and '0.78' in x for x in ca['Q3']['validation_fabrication_risk']))
mp=load('knowledge_base/cross_paper_maps/2025-F-S042-S045.json')
ck('map three reviewed',mp['status']=='PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED')
ck('reviewed 3',mp['papers_reviewed']==['S042','S043','S044'])
ck('pending S045',mp['papers_pending']==['S045'])
for rel in [
 'knowledge_base/error_patterns/paper-code-complex-method-collapse-to-baseline.json',
 'knowledge_base/error_patterns/random-placeholder-contamination.json',
 'knowledge_base/error_patterns/hardcoded-result-overrides-computation.json',
 'knowledge_base/error_patterns/validation-metric-clamp-or-constant.json',
 'knowledge_base/error_patterns/pairwise-entity-split-leakage.json',
 'knowledge_base/error_patterns/multimodal-label-shared-proxy-collapse.json']:
    ck('pattern '+rel,(ROOT/rel).exists())
summ=load('.agents/skills/mathmodel-case-retriever/assets/core_retrieval_summaries.json')
ck('summary S044','S044' in summ)
ck('summary R2',summ['S044']['reproduction_level']=='R2')
cgm=load('.agents/skills/mathmodel-case-retriever/assets/case_group_maps.json')
ck('case group 3/4',cgm['2025-F']['status']=='PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED')
skill=(ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ck('skill v137','## 20. v1.37 / S044' in skill)
ck('skill hardcoded','固定答案不能覆盖计算输出' in skill)
ck('skill pair group','先按 garden/entity 分组划分' in skill)
nexttxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8')
ck('next S045','S045 / 2025-F' in nexttxt)
ck('not due until S045','NOT_DUE until S045 is completed' in nexttxt)
ck('test frozen text','Test' in nexttxt and 'frozen' in nexttxt)
print(f'PASS {len(checks)}/{len(checks)}')
