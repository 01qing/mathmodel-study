from pathlib import Path
import json,sys,subprocess,os,hashlib,datetime
P=Path(__file__).resolve().parent;R=P.parents[1];W=R/'v1.39-work';S=W/'.agents/skills/graduate-mathmodel-learning/scripts'
out=P/'validation';out.mkdir(exist_ok=True)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
rows=[]
def run(path,cwd,timeout=180):
    try:
        p=subprocess.run([sys.executable,'-X','utf8',str(path)],cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
        text=p.stdout+'\n'+p.stderr;code=p.returncode
    except subprocess.TimeoutExpired as e:
        text='TIMEOUT (not PASS)\n'+str(e.stdout)+str(e.stderr);code=-1
    (out/(path.stem+'.log')).write_text(text,encoding='utf-8')
    row={'script':path.name,'exit_code':code,'status':'PASS' if code==0 else 'FAIL','scope':'named audit/regression only'}
    rows.append(row);print(json.dumps(row),flush=True)
    (out/'RUNS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for name in ['audit_counterexamples.py','audit_spatial_provenance.py','audit_q1_units.py','audit_final_primitives.py']:
    run(P/name,P)
names=(W/'learning_output/validation/v138/historical_22_files.txt').read_text(encoding='utf-8').splitlines()
for name in names:
    if name.strip():run(S/name.strip(),W)
run(S/'test_v138_s045_regressions.py',W)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((R/'FROZEN_CORE_V138_FILES.sha256.json').read_text(encoding='utf-8'))
changes=[n for n,h in base.items() if not (W/n).is_file() or sha(W/n)!=h]
H=W/'learning_output/analyses/dev_2024D_presolution'
mf=json.loads((H/'DEV_2024D_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
changed=[n for n,v in mf['files'].items() if not (H/n).is_file() or sha(H/n)!=v['sha256']]
guard={'core_checked':len(base),'core_changed':changes,'solution_checked':len(mf['files']),'solution_changed':changed,
       'freeze_manifest_sha256':sha(H/'DEV_2024D_FREEZE_MANIFEST.json'),
       'status':'PASS' if not changes and not changed else 'FAIL',
       'scope':'Immutable bytes; does not establish ability gain or prove absence of historical exposure'}
(out/'FROZEN_GUARDS.json').write_text(json.dumps(guard,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(guard),flush=True)
assert all(r['exit_code']==0 for r in rows) and guard['status']=='PASS'
