from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parents[4];S=Path(__file__).parent;V=R/'learning_output/validation/v139';V.mkdir(exist_ok=True,parents=True)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
names=(R/'learning_output/validation/v138/historical_22_files.txt').read_text(encoding='utf-8').splitlines()+['test_v138_s045_regressions.py']
rows=[]
for name in names:
    p=subprocess.run([sys.executable,'-X','utf8',str(S/name)],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',timeout=180)
    (V/(name+'.original.log')).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    rows.append(dict(script=name,exit_code=p.returncode,status='PASS' if p.returncode==0 else 'FAIL'))
    (V/'historical_original.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows[-1]),flush=True)
retr=R/'.agents/skills/mathmodel-case-retriever/scripts/test_v138_2025F_retrieval.py'
p=subprocess.run([sys.executable,'-X','utf8',str(retr)],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',timeout=240)
(V/'retrieval.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
(V/'retrieval.json').write_text(json.dumps(dict(exit_code=p.returncode,status='PASS' if p.returncode==0 else 'FAIL',scope='reviewed-Train-only evaluation/production')),encoding='utf-8')
print('retrieval exit '+str(p.returncode),flush=True)
