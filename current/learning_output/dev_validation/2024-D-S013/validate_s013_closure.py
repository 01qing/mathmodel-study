from pathlib import Path
import json,hashlib
from collections import Counter
P=Path(__file__).resolve().parent;R=P.parents[1];W=R/'v1.39-work'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(name,c):
    assert c,name
    checks.append(name)
ledger=load(P/'PAGE_AUDIT_LEDGER.json')
ck('113 unique reviewed pages',sorted(x['physical_page'] for x in ledger['pages'])==list(range(1,114)))
ck('render references resolve',all((P/x['visual_evidence']).is_file() for x in ledger['pages']))
ck('visual is separate evidence',ledger['visual_count']==113 and ledger['text_count']==113)
cards=load(P/'S013_QUESTION_CARDS.json')
ck('source hash unchanged',sha(Path(cards['source']))==cards['source_sha256']==ledger['source_sha256'])
schema=load(W/'knowledge_base/core_schema/mathmodel_core_question_schema_v1.json')
for q,c in cards['question_cards'].items():
    ck(q+' question contract complete',all(k in c for k in schema['question_card_fields']))
    ck(q+' competition contract',all(k in c['candidate_model_competition'] for k in schema['candidate_model_competition_required_roles']))
    ck(q+' operational six-hour plan',len(c['six_hour_baseline'])>=4)
ck('R2 only, Dev isolated',cards['reproduction_level']=='R2' and cards['split']=='dev' and not cards['core_promoted'])
reg=load(P/'S013_RESULT_REGISTRY.json');rs=load(W/'knowledge_base/core_schema/result_registry_schema_v1.json')
ck('registry IDs unique',len({x['result_id'] for x in reg['entries']})==len(reg['entries']))
ck('registry contracts valid',all(all(k in e for k in rs['required_metadata']) and e['status'] in rs['status_values'] for e in reg['entries']))
ck('registry evidence resolves',all((P/e['evidence_file']).is_file() for e in reg['entries']))
ck('contradictions and unresolved claims preserved',{'contradicted','not_reproducible_from_visible_evidence','author_reported'} <= {e['status'] for e in reg['entries']})
byid={e['result_id']:e for e in reg['entries']}
for rid in ['Q3-SVR-TRAIN','Q3-SVR-TEST']:
    v=byid[rid]['value_or_record'];ck(rid+' necessary metric consistency only',v['MSE']>=v['MAE']**2 and byid[rid]['status']=='author_reported')
agg=load(P/'Q1_AGGREGATION_RESULTS.json')
ck('5 reported rainfall values match alternate contract',len(agg['precipitation'])==5 and all(a['match_rounded_2dp'] for a in agg['precipitation']))
ck('annual support remains different',all(abs(a['annual_sum_valid_cell_unweighted_mean_mm']-a['paper_mm'])>100 for a in agg['precipitation']))
ck('cropland unresolved preserved',not all(round(a['positive_cell_mean_percent'],2)==a['paper_percent'] for a in agg['cropland']))
counter=load(P/'COUNTEREXAMPLE_RESULTS.json')
ck('ten mechanism first-fail histories',len(counter['tests'])==10 and all(t['first_state']=='FAIL' and t['diagnosis'] and t['repair'] and t['retest']=='PASS_MECHANISM_ONLY' for t in counter['tests']))
sp=load(P/'SPATIAL_PROVENANCE_RESULTS.json')
ck('spatial repair does not erase missing chain',sp['tests'][1]['repair_status'].startswith('NOT_IMPLEMENTED'))
supp=load(P/'FINAL_PRIMITIVE_RESULTS.json')
ck('six supplemental checks executed',supp['passed']==6 and not supp['author_pipeline_reproduced'])
comp=load(P/'S013_METHOD_MAP_AND_COMPOSER.json')
ck('seven gates reviewed without automatic promotion',len(comp['seven_gates'])==7 and comp['decision'].startswith('DO_NOT_IMPORT'))
ck('partial Dev group not closed',not comp['group_final'] and comp['papers_reviewed']==['S013'])
hist=load(P/'validation/RUNS.json');adapt=load(P/'validation/COMPATIBILITY_RETEST.json')
ck('four source-audit runners passed',all(r['exit_code']==0 for r in hist[:4]))
ck('original compatibility failures retained',{r['script'] for r in hist if r['exit_code']!=0}=={'test_v126_regressions.py','test_v138_s045_regressions.py'})
ck('external adaptations pass',len(adapt)==2 and all(a['original_status']=='FAIL_PRESERVED' and a['adapted_status']=='PASS' for a in adapt))
base=load(R/'FROZEN_CORE_V138_FILES.sha256.json');changed=[n for n,h in base.items() if not (W/n).is_file() or sha(W/n)!=h]
H=W/'learning_output/analyses/dev_2024D_presolution';mf=load(H/'DEV_2024D_FREEZE_MANIFEST.json')
changed_sol=[n for n,v in mf['files'].items() if not (H/n).is_file() or sha(H/n)!=v['sha256']]
ck('1470 frozen Core files unchanged',len(base)==1470 and not changed)
ck('55 frozen solution files unchanged',len(mf['files'])==55 and not changed_sol)
ck('independent freeze manifest unchanged',sha(H/'DEV_2024D_FREEZE_MANIFEST.json')=='ee139e2a7063fd6cb3a279ae5acba633f2e6784f8afa62d9e51fbc9a1db42a7e')
A=W/'.agents/skills/mathmodel-case-retriever/assets';papers=load(A/'papers.json')
ck('45 papers / 32-7-6 frozen split',len(papers)==45 and Counter(p['split'] for p in papers)==dict(train=32,dev=7,test=6))
ck('6752 chunk count retained',len(load(A/'chunks.json'))==6752)
ck('protected metadata remains unread',all(p.get('reviewed_pages',[])==[] for p in papers if p['paper_id'] in ['S014','S015','S016','S021','S022','S023','S024','S037','S038']))
ck('split manifest hash preserved',sha(A/'split_manifest.json')=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('intermediate recovery history preserved',(P/'RECOVERY_STATE_PRE_CLOSURE.json').is_file())
result={'status':'PASS','checks':len(checks),'names':checks,'scope':'S013 artifacts, named primitive evidence, frozen bytes and split metadata only',
        'not_claimed':['Author full reproduction','All original historical runners PASS','S014-S016 reviewed','Core v1.39 SEALED','Clean blind Core-level gain'],
        'historical_original':'21/22 historical scripts PASS; v1.26 FAIL retained; v1.38 additional script FAIL retained',
        'historical_adapted':'22/22 effective historical compatibility including one external adaptation; additional v1.38 adapted127/127',
        'author_result_registry_entries':len(reg['entries'])}
(P/'validation/S013_CLOSURE_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
