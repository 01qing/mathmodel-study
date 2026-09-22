#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[4]
checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))
    if not cond: raise AssertionError(name)
def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
try:
    ok('version 1.32.0',(ROOT/'VERSION').read_text().strip()=='1.32.0')
    for rel in [
      'PROGRESS_V132.md','VALIDATION_V132.md','S034_v1.32_训练摘要.md',
      'knowledge_base/paper_reviews/2025-C-S034-core.json',
      'knowledge_base/candidate_competitions/S034.json',
      'knowledge_base/result_registry/S034.json',
      'knowledge_base/code_cases/2025-C-S034-code-access.json',
      'knowledge_base/method_modules/2025-C-S034-modules.json',
      'knowledge_base/figure_argumentation/S034.json',
      'learning_output/analyses/S034_source_audit.json',
      'learning_output/analyses/S034_result_registry_replay.json',
      'learning_output/analyses/v132_S034/historical_v126_first_failure.txt',
      'learning_output/analyses/v132_S034/historical_22_regressions_final.log',
      'learning_output/analyses/v132_S034/test_v132_s034_regressions_rerun.log',
      'learning_output/analyses/v132_S034/test_v132_2025C_retrieval_rerun.log',
      'learning_output/analyses/v132_S034/validate_library_rerun.log',
      'learning_output/analyses/v132_S034/validate_learning_workspace_rerun.log',
    ]: ok('exists '+rel,(ROOT/rel).is_file() and (ROOT/rel).stat().st_size>0)
    src=json.loads((ROOT/'learning_output/analyses/S034_source_audit.json').read_text())
    ok('S034 source sha',src['sha256']=='23dfbdeb5af6468a92428c0171ccfd569b6571066837df96b1960f47248b1d1f')
    ok('S034 68 pages',src['pages']==68)
    ok('S034 R1 source boundary',src['reproduction_level']=='R1')
    reg=json.loads((ROOT/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text())
    by={x['paper_id']:x for x in reg}
    ok('45 papers',len(reg)==45)
    s=by['S034']; ok('S034 Train',s['split']=='train'); ok('S034 all pages reviewed',s['reviewed_pages']==list(range(1,69))); ok('S034 R1 registry',s.get('reproduction_level')=='R1')
    for pid in ['S035','S036']:
        ok(pid+' future Train unread',by[pid]['split']=='train' and by[pid].get('reviewed_pages',[])==[])
    for pid in ['S030','S031']:
        ok(pid+' Dev reserve unread',by[pid]['split']=='dev' and by[pid].get('reviewed_pages',[])==[])
    for pid in ['S021','S022','S023','S024','S037','S038']:
        ok(pid+' Test unread',by[pid]['split']=='test' and by[pid].get('reviewed_pages',[])==[])
    sm=ROOT/'.agents/skills/mathmodel-case-retriever/assets/split_manifest.json'
    ok('frozen split sha',sha(sm)=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
    st=json.loads((ROOT/'learning_output/context/learning_state.json').read_text())
    ok('state version',st.get('current_version')=='1.32.0'); ok('state latest S034',st.get('latest_completed_paper')=='S034'); ok('state latest R1',st.get('reproduction_level_latest')=='S034:R1')
    nxt=(ROOT/'learning_output/context/next_learning.md').read_text()
    ok('next S035','S035 / 2025-C' in nxt); ok('Mini Transfer Test explicit','Mini Transfer Test' in nxt); ok('Dev reserve explicit','S030/S031 remain Dev reserve' in nxt); ok('Test frozen explicit','Test remains frozen' in nxt)
    hist=(ROOT/'learning_output/analyses/v132_S034/historical_22_regressions_final.log').read_text()
    ok('historical 22/22 strict','SUMMARY: 22/22 PASS, 0 FAIL' in hist)
    spec=(ROOT/'learning_output/analyses/v132_S034/test_v132_s034_regressions_rerun.log').read_text(); ok('specialist 163/163','PASS 163/163' in spec)
    ret=(ROOT/'learning_output/analyses/v132_S034/test_v132_2025C_retrieval_rerun.log').read_text(); ok('retrieval pass','PASS v1.32 2025-C retrieval' in ret)
    lib=(ROOT/'learning_output/analyses/v132_S034/validate_library_rerun.log').read_text(); ok('library pass','"status": "PASS"' in lib and '"train": 32' in lib and '"dev": 7' in lib and '"test": 6' in lib)
    ws=(ROOT/'learning_output/analyses/v132_S034/validate_learning_workspace_rerun.log').read_text(); ok('workspace pass','[PASS] learning workspace is valid' in ws)
    rr=json.loads((ROOT/'learning_output/analyses/S034_result_registry_replay.json').read_text()); ok('registry replay pass',rr.get('status')=='PASS' and rr.get('pass_count')==15 and rr.get('nonboolean_diagnostics')==1)
    mp=json.loads((ROOT/'knowledge_base/cross_paper_maps/2025-C-S032-S036.json').read_text()); ok('map 3/5',mp.get('status')=='PROVISIONAL_AFTER_THREE_TRAIN_PAPERS' and set(mp.get('papers_reviewed',[]))=={'S032','S033','S034'} and set(mp.get('papers_pending',[]))=={'S035','S036'})
    print(json.dumps({'status':'PASS','scope':'v1.32 release contract','passed':sum(v for _,v in checks),'checks':[n for n,v in checks if v]},ensure_ascii=False,indent=2))
except Exception as e:
    print(json.dumps({'status':'FAIL','scope':'v1.32 release contract','passed':sum(v for _,v in checks),'failed':str(e),'checks':[{'name':n,'pass':v} for n,v in checks]},ensure_ascii=False,indent=2))
    sys.exit(1)
