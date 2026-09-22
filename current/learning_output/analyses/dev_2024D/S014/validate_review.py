from pathlib import Path
import json,hashlib,subprocess,sys,datetime,concurrent.futures
O=Path(__file__).resolve().parent;W=O.parents[3];C=W.parent/'clean-dev-2024D';B=C/'v1.39-release-work';I=C/'v1.39-work/learning_output/analyses/dev_2024D_presolution'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
# Record Dev review only. Existing prior_exposure warning is deliberately preserved.
p=W/'.agents/skills/mathmodel-case-retriever/assets/papers.json';papers=json.loads(p.read_text(encoding='utf-8'))
for row in papers:
    if row['paper_id']=='S014':
        row.update(learning_status='CORE_REVIEWED_DEV_R2_CANDIDATES_NOT_RELEASED',reviewed_pages=list(range(1,63)),review_evidence='learning_output/analyses/dev_2024D/S014/S014_FINAL_REVIEW.md',reproduction_level='R2')
dump(p,papers)
p=W/'.agents/skills/graduate-mathmodel-learning/assets/catalog/local_papers_2024_2025.json';catalog=json.loads(p.read_text(encoding='utf-8'))
for row in catalog['papers']:
    if row['source_id']=='S014':row.update(reviewed_pages=list(range(1,63)),review_status='reviewed_dev_R2',review_evidence='learning_output/analyses/dev_2024D/S014/S014_FINAL_REVIEW.md')
dump(p,catalog)
checks=[]
def ck(n,b,scope):checks.append(dict(name=n,passed=bool(b),scope=scope))
base_list=[s.split('  ',1) for s in (B/'FILES_V139.sha256').read_text(encoding='utf-8').splitlines() if s.strip()]
bad=[r for h,r in base_list if not (B/r).is_file() or sha(B/r)!=h]
ck('sealed v139 content integrity',not bad,dict(files=len(base_list),changed=bad))
freeze=I/'DEV_2024D_FREEZE_MANIFEST.json';fm=json.loads(freeze.read_text(encoding='utf-8'));ibad=[r for r,d in fm['files'].items() if not (I/r).is_file() or sha(I/r)!=d['sha256']]
ck('independent frozen files unchanged',not ibad,dict(files=len(fm['files']),changed=ibad))
ck('independent manifest identity',sha(freeze)=='ee139e2a7063fd6cb3a279ae5acba633f2e6784f8afa62d9e51fbc9a1db42a7e','SHA256 exact')
allowed={'.agents/skills/mathmodel-case-retriever/assets/papers.json','.agents/skills/graduate-mathmodel-learning/assets/catalog/local_papers_2024_2025.json'}
core_changed=[r for h,r in base_list if r.startswith('.agents/') and r not in allowed and sha(W/r)!=h]
ck('inherited skill logic unchanged',not core_changed,dict(changed=core_changed,exceptions=sorted(allowed)))
pa={x['paper_id']:x for x in papers};expected={'train':32,'dev':7,'test':6}
ck('frozen45paper split counts',{s:sum(p['split']==s for p in papers) for s in expected}==expected,'metadata only; no protected answer text opened')
ck('S014 stays Dev',pa['S014']['split']=='dev','review metadata cannot promoteDevtoTrain')
ck('S015/S016 remain unread',all(not pa[s]['reviewed_pages'] for s in ['S015','S016']),'this review adds onlyS014')
for fn in ['split_manifest.json','chunks.json']:
    rel=Path('.agents/skills/mathmodel-case-retriever/assets')/fn
    ck(fn+' unchanged',sha(W/rel)==sha(B/rel),'bytehash comparison; chunk content not read for paper learning')
bp=json.loads((B/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
ck('all other paper metadata unchanged',all(row==pa[row['paper_id']] for row in bp if row['paper_id']!='S014'),'including protected Dev/Test records')
ledger=json.loads((O/'PAGE_AUDIT_LEDGER.json').read_text(encoding='utf-8'));ck('62pages audit ledger complete',len(ledger['pages'])==62 and all(x['text_reviewed'] and x['visual_reviewed'] and (O/x['image']).exists() for x in ledger['pages']),'coverage record, not automated visual quality certification')
reg=json.loads((O/'RESULT_REGISTRY.json').read_text(encoding='utf-8'))['results'];ck('registry has unique IDs and bounded pages',len(reg)==len({r['result_id'] for r in reg}) and all(all(1<=p<=62 for p in r['pdf_pages']) for r in reg),'schema and provenance only')
cards=json.loads((O/'QUESTION_CARDS.json').read_text(encoding='utf-8'))['cards'];ck('four complete model competitions',len(cards)==4 and all(all(c.get(k) for k in ['baseline','author','alternatives','not_recommended','why_select','why_not','switch_conditions','six_hour_baseline','transferable_modules','error_modes']) for c in cards),'content existence; not evidence of competence')
ck('all evidence levels cappedR2',all(c['reproduction_level']=='R2' for c in cards),'local fixture execution does not raise author reproduction')
mp=json.loads((O/'METHOD_MAP_AND_COMPOSER.json').read_text(encoding='utf-8'));ck('seven gates and pending group status',len(mp['seven_gates'])==7 and mp['not_final'],'do not mark2024-Dgroupcomplete')
ck('first audit failure retained',json.loads((O/'AUDIT_REPLAY_FIRST_FAIL.json').read_text(encoding='utf-8'))['status']=='FAIL','audit hypothesis failure28/29 preserved')
ap=json.loads((O/'AUDIT_REPLAY.json').read_text(encoding='utf-8'));ck('local numerical audit passes',ap['status']=='PASS',f"{ap['passed']}/{ap['total']} checks; deterministic local fixtures only")
S=W/'.agents/skills/graduate-mathmodel-learning/scripts';R=W/'.agents/skills/mathmodel-case-retriever/scripts'
jobs=[('v139_contracts',S/'test_v139_contracts.py'),('v19_historical',S/'test_v19_training_regressions.py'),('workspace',S/'validate_learning_workspace.py'),('retrieval_2025A',R/'test_v128_2025A_retrieval.py'),('retrieval_2025F',R/'test_v138_2025F_retrieval.py')]
def run(job):
    name,script=job
    try:
        p=subprocess.run([sys.executable,'-X','utf8',str(script)],cwd=W,capture_output=True,text=True,encoding='utf-8',timeout=90)
        (O/(name+'.log')).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8');return dict(name=name,exit_code=p.returncode,passed=p.returncode==0,log=name+'.log')
    except subprocess.TimeoutExpired as e:
        (O/(name+'.log')).write_text(str(e),encoding='utf-8');return dict(name=name,passed=False,error='TIMEOUT_NOT_PASS')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,jobs))
ck('selected inherited regressions and retrieval',all(r['passed'] for r in results),results)
out=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',scope='S014 review closure and selected compatibility checks; NOT full22suite rerun, NOT Core gain',checks=checks,inherited_runs=results,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(O/'VALIDATION_S014.json',out)
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
