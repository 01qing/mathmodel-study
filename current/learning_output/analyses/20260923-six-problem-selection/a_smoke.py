from pathlib import Path
import zipfile,json,sys,subprocess,time,hashlib
OUT=Path(__file__).parent; WORK=OUT/'A_evaluator_smoke';WORK.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
zp=next(Path(r'D:\数模\数模练习\A题exp').glob('*.zip'))
copies=[]
with zipfile.ZipFile(zp) as z:
    for name in z.namelist():
        if (name.startswith('code/') and name.endswith('.py')) or name in ['data/config.txt','data/case_001.json']:
            p=WORK/name;p.parent.mkdir(parents=True,exist_ok=True);data=z.read(name);p.write_bytes(data)
            copies.append({'archive_entry':name,'sha256':hashlib.sha256(data).hexdigest()})
g=json.loads((WORK/'data/case_001.json').read_text(encoding='utf-8'))
# Deliberately trivial legal plan: every compute op on one subgraph/core.
# This validates evaluator availability, NOT parallel algorithm quality.
plan={'node_to_subgraph':{str(o['id']):0 for o in g['ops'] if o['op'] not in ['COPY_IN','COPY_OUT']},'core_schedules':[[0],[]]}
(WORK/'single_task_plan.json').write_text(json.dumps(plan),encoding='utf-8')
r={'scope':'Interface smoke only: first supplied case, all compute operations on one core; no multi-core optimizer or full sweep','copies':copies,'runs':[]}
for q in range(1,4):
    args=[sys.executable,str(WORK/f'code/multicore_cut_evaluate_problem_{q}.py'),str(WORK/'data/case_001.json'),str(WORK/'single_task_plan.json'),'--config',str(WORK/'data/config.txt'),'-o',str(WORK/f'q{q}_result.json'),'--log-output',str(WORK/f'q{q}.log'),'--trace-output',str(WORK/f'q{q}_trace.json')]
    t=time.perf_counter()
    try:
        run=subprocess.run(args,cwd=WORK,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        rr={'question':q,'exit_code':run.returncode,'elapsed_seconds':time.perf_counter()-t,'stdout':run.stdout.decode('utf-8',errors='replace')[-1000:],'stderr':run.stderr.decode('utf-8',errors='replace')[-1500:]}
        if (WORK/f'q{q}_result.json').exists():rr['result']=json.loads((WORK/f'q{q}_result.json').read_text(encoding='utf-8'))
    except subprocess.TimeoutExpired:rr={'question':q,'timeout_seconds':60}
    r['runs'].append(rr)
    print('Q',q,{k:v for k,v in rr.items() if k not in ['result','stdout','stderr']}, flush=True)
    if rr.get('exit_code',1)!=0:print(rr,flush=True)
(OUT/'A_smoke_results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
