from pathlib import Path
import json, hashlib, sys
R=Path(__file__).resolve().parents[4]
checks=[]
def ck(name,cond,detail=''):
    checks.append({'name':name,'passed':bool(cond),'detail':detail})
    if not cond: print('FAIL',name,detail)
def load(rel): return json.loads((R/rel).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

ck('VERSION 1.41.0',(R/'VERSION').read_text().strip()=='1.41.0')
st=load('learning_output/context/learning_state.json')
ck('state version',st.get('current_version')=='1.41.0')
ck('latest S016',st.get('latest_completed_paper')=='S016')
ck('latest dev S016',st.get('latest_completed_dev_paper')=='S016')
ck('latest R2',st.get('reproduction_level_latest')=='S016:R2')
ck('core identity',st.get('core_identity')=='MathModel-Core')
ck('core gain bounded',st.get('core_gain')=='NOT_ESTABLISHED')
ck('ablation not run',st.get('core_ablation')=='NOT_RUN')

papers=load('.agents/skills/mathmodel-case-retriever/assets/papers.json')
items=papers['papers'] if isinstance(papers,dict) else papers
P={p['paper_id']:p for p in items}
ck('paper count',len(items)==45)
ck('train count',sum(p['split']=='train' for p in items)==32)
ck('dev count',sum(p['split']=='dev' for p in items)==7)
ck('test count',sum(p['split']=='test' for p in items)==6)
ck('all train reviewed',all(p.get('reviewed_pages') for p in items if p['split']=='train'))
for pid,n in [('S013',113),('S014',62),('S015',96),('S016',114)]:
    ck(pid+' dev split',P[pid]['split']=='dev')
    ck(pid+' reviewed pages',len(P[pid].get('reviewed_pages',[]))==n,str(len(P[pid].get('reviewed_pages',[]))))
    ck(pid+' R2',P[pid].get('reproduction_level')=='R2')
for pid in ['S030','S031']:
    ck(pid+' reserve unread',P[pid]['split']=='dev' and P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test unread',P[pid]['split']=='test' and P[pid].get('reviewed_pages',[])==[])

for rel in [
 'learning_output/analyses/dev_2024D/S015/S015_FINAL_REVIEW.md',
 'learning_output/analyses/dev_2024D/S016/S016_FINAL_REVIEW.md',
 'learning_output/analyses/dev_2024D/FINAL_METHOD_COMPETITION_MAP_V141.json',
 'learning_output/analyses/dev_2024D/METHOD_COMPOSER_V141.json',
 'learning_output/analyses/dev_2024D/DEV_2024D_GAP_ANALYSIS_V141.md',
 '.agents/skills/graduate-mathmodel-learning/references/dev-casegroup-contracts-v141.md',
 'knowledge_base/error_patterns/2024-D-v141.json',
 'learning_output/mini_transfer/2024D_v141/MINI_TRANSFER_FIRST_FAIL.json',
 'learning_output/mini_transfer/2024D_v141/MINI_TRANSFER_RESULTS.json',
 'PROGRESS_V141.md','VALIDATION_V141.md']:
    ck('exists '+rel,(R/rel).exists() and (R/rel).stat().st_size>0)

for pid,pages,aud in [('S015',96,17),('S016',114,19)]:
    d=R/f'learning_output/analyses/dev_2024D/{pid}'
    reg=load(f'learning_output/analyses/dev_2024D/{pid}/RESULT_REGISTRY.json')
    ck(pid+' registry final',reg.get('status')=='FINAL_R2_AUDIT_REGISTRY')
    ck(pid+' registry pages',reg.get('text_pages_reviewed')==pages and reg.get('visual_pages_reviewed')==pages)
    ck(pid+' audit count',reg.get('audit_replay',{}).get('passed')==aud)
    ck(pid+' source hash',reg.get('source_sha256')==sha(d/'source.pdf'))
    ck(pid+' visual files',len(list((d/'visual').glob('p*.png')))==pages)

mp=load('learning_output/analyses/dev_2024D/FINAL_METHOD_COMPETITION_MAP_V141.json')
ck('map final',mp.get('status')=='FINAL_2024D_CASE_GROUP_REVIEW_COMPLETE')
ck('map four papers',mp.get('papers_reviewed')==['S013','S014','S015','S016'])
ck('map four questions',set(mp.get('questions',{}))=={'Q1','Q2','Q3','Q4'})
ck('map evidence bounded','not controlled Core gain' in mp.get('capability_evidence',''))
comp=load('learning_output/analyses/dev_2024D/METHOD_COMPOSER_V141.json')
ck('seven composer gates',len(comp.get('gates',[]))==7)
ck('composer no pipeline copy','reject direct concatenation' in comp.get('composition_decision',''))
mt=load('learning_output/mini_transfer/2024D_v141/MINI_TRANSFER_RESULTS.json')
ck('mini transfer pass',mt.get('status')=='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX')
ck('mini six checks',len(mt.get('checks',[]))==6 and all(x.get('passed') for x in mt['checks']))
ck('mini bounded',mt.get('core_gain')=='NOT_ESTABLISHED' and mt.get('controlled_ablation')=='NOT_RUN')

prev=load('learning_output/validation/v141/PREVIOUS_RELEASE_V140_VERIFICATION.json')
ck('previous release verified',prev.get('match') is True)
ck('previous release hash',prev.get('sha256')=='beaa23ed9210be9c3075e13b84732598a27c25ed0f58ff0759e5b68f74da470c')

lib=(R/'learning_output/validation/v141/final_system/validate_library.log').read_text(encoding='utf-8',errors='ignore')
wrk=(R/'learning_output/validation/v141/final_system/validate_learning_workspace.log').read_text(encoding='utf-8',errors='ignore')
ck('library pass','"status": "PASS"' in lib or 'PASS' in lib)
ck('workspace pass','[PASS]' in wrk)
iso=load('learning_output/validation/v141/final_system/retrieval_isolation_check.json')
ck('production train-only',iso['production']['pass'] is True)
ck('evaluation train-only',iso['evaluation']['pass'] is True)

# 34 final regression logs must exist without traceback/FAIL markers.
O=R/'learning_output/validation/v141/final_regressions'
expected=['test_v16_regressions.py','test_v18_code_learning.py','test_v19_training_regressions.py']+[f'test_v1{i}_regressions.py' for i in range(10,29)]+['test_v129_dev_regressions.py','test_v130_s032_regressions.py','test_v131_s033_regressions.py','test_v132_s034_regressions.py','test_v133_s035_regressions.py','test_v134_s036_regressions.py','test_v135_s042_regressions.py','test_v136_s043_regressions.py','test_v137_s044_regressions.py','test_v138_s045_regressions.py','test_v139_contracts.py','test_v141_2024D_group.py']
seen=[]
for n in expected:
    if n not in seen and (R/'.agents/skills/graduate-mathmodel-learning/scripts'/n).exists(): seen.append(n)
ck('34 regression scripts',len(seen)==34,str(len(seen)))
bad=[]
for n in seen:
    p=O/(n+'.log')
    if not p.exists(): bad.append(n+':missing'); continue
    t=p.read_text(encoding='utf-8',errors='ignore')
    if 'Traceback' in t or t.startswith('FAIL ') or '\nFAIL ' in t: bad.append(n+':fail-marker')
ck('final regressions clean',not bad,','.join(bad[:5]))

grp=load('learning_output/validation/v141/test_v141_2024D_group.json')
ck('group 38/38',grp.get('status')=='PASS' and grp.get('passed')==38 and grp.get('total')==38)

# first-fail/adaptation evidence preserved
for rel in [
 'learning_output/validation/v141/test_v141_group_FIRST_FAIL.log',
 'learning_output/mini_transfer/2024D_v141/MINI_TRANSFER_FIRST_FAIL.json',
 'learning_output/validation/v141/historical_original/SUMMARY.json',
 'learning_output/validation/v141/recent_original/SUMMARY.json',
 'learning_output/validation/v141/historical_test_adaptation_v141/ORIGINAL_HASHES.json',
 'learning_output/validation/v141/historical_test_adaptation_v141/ADAPTATION_MANIFEST.json',
 'learning_output/validation/v141/final_system/validate_learning_workspace_FIRST_FAIL_WRONG_CWD.log',
 'learning_output/validation/v141/final_regressions/test_v18_code_learning_FIRST_FAIL_WRONG_CWD.log']:
    ck('preserved '+rel,(R/rel).exists() and (R/rel).stat().st_size>0)

skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ck('v141 reference routed','dev-casegroup-contracts-v141.md' in skill)
ck('v141 lean section','## 24. v1.41 / 2024-D Dev 题组闭环' in skill)
names={x.name.lower() for x in (R/'.agents/skills').iterdir() if x.is_dir()}
for n in ['mathmodel-master','mathmodel-architect','mathmodel-engineer','mathmodel-writer','mathmodel-reviewer']:
    ck('no role split '+n,n not in names)

passed=sum(x['passed'] for x in checks); total=len(checks)
out={'status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'checks':checks,'scope':'v1.41 release-candidate integrity/regression/retrieval/2024-D closure; not author end-to-end reproduction or causal Core capability gain'}
p=R/'learning_output/validation/v141/RELEASE_CONTRACT_V141.json'; p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'passed':passed,'total':total},ensure_ascii=False))
sys.exit(0 if passed==total else 1)
