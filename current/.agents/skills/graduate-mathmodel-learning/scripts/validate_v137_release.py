from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
checks=[]
def ck(name, cond):
    assert cond, name; checks.append(name)
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
ck('VERSION 1.37.0',(ROOT/'VERSION').read_text().strip()=='1.37.0')
st=load('learning_output/context/learning_state.json')
ck('state version',st['current_version']=='1.37.0')
ck('latest S044',st['latest_completed_paper']=='S044')
ck('latest R2',st['reproduction_level_latest']=='S044:R2')
req=[
 'S044_v1.37_训练摘要.md',
 'learning_output/analyses/S044_source_audit.json',
 'learning_output/analyses/S044_result_registry_replay.json',
 'knowledge_base/paper_reviews/2025-F-S044-core.json',
 'knowledge_base/candidate_competitions/S044.json',
 'knowledge_base/result_registry/S044.json',
 'knowledge_base/code_cases/2025-F-S044-printed-code-audit.json',
 'knowledge_base/method_modules/2025-F-S044-modules.json',
 'knowledge_base/figure_argumentation/S044.json',
 'knowledge_base/cross_paper_maps/2025-F-S042-S045.json',
 'knowledge_base/figure_decision_rules/2025-F-provisional.json',
 'learning_output/analyses/v137_S044/test_v137_s044_regressions_first_fail.md',
 'learning_output/analyses/historical_test_adaptation_v137.md',
 'PROGRESS_V137.md','VALIDATION_V137.md']
for r in req: ck('exists '+r,(ROOT/r).exists())
papers=load('.agents/skills/mathmodel-case-retriever/assets/papers.json')
items = papers['papers'] if isinstance(papers, dict) else papers
P={p['paper_id']:p for p in items}
ck('S044 train',P['S044']['split']=='train')
ck('S044 reviewed 116',P['S044']['reviewed_pages']==list(range(1,117)))
ck('S044 R2',P['S044']['reproduction_level']=='R2')
ck('S045 unread train',P['S045']['split']=='train' and P['S045']['reviewed_pages']==[])
for pid in ['S030','S031']:
    ck(pid+' dev reserve',P[pid]['split']=='dev' and P[pid]['reviewed_pages']==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test frozen',P[pid]['split']=='test' and P[pid]['reviewed_pages']==[])
mp=load('knowledge_base/cross_paper_maps/2025-F-S042-S045.json')
ck('map 3/4',mp['status']=='PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED')
ck('map reviewed',mp['papers_reviewed']==['S042','S043','S044'])
ck('map pending S045',mp['papers_pending']==['S045'])
nxt=(ROOT/'learning_output/context/next_learning.md').read_text(encoding='utf-8')
ck('next S045','S045 / 2025-F' in nxt)
ck('group gates not due','NOT_DUE' in nxt and 'S045' in nxt)
ck('test frozen text','Test' in nxt and 'frozen' in nxt)
rv=load('learning_output/analyses/S044_result_registry_replay.json')
ck('registry audit replay pass',rv['status']=='PASS_AUDIT_REPLAY_WITH_IDENTIFIED_FAILURES')
ck('kappa strict fail preserved',rv['checks']['Q2_kappa_strict_pass'] is False)
ck('pvalue swap preserved',rv['checks']['Q3_pvalue_labels_swapped'] is True)
ck('fixed CV constants preserved',rv['checks']['Q3_table19_equals_code_constants'] is True)
print(json.dumps({'status':'PASS','checks':len(checks),'scope':'v1.37 release contract; does not claim author-code execution or independent capability gain'},ensure_ascii=False))
