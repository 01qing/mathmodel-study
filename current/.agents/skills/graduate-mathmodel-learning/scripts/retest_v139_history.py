"""Versioned compatibility adapters; original tests and original FAIL logs are retained."""
from pathlib import Path
import json,contextlib,io,traceback,os,sys,hashlib
S=Path(__file__).parent;R=S.resolve().parents[3];V=R/'learning_output/validation/v139'
os.chdir(R);sys.dont_write_bytecode=True;sys.path.insert(0,str(S))
old=json.loads((V/'historical_original.json').read_text());rows=[]
previous={}
if (V/'historical_effective.json').exists():
    previous={x['script']:x for x in json.loads((V/'historical_effective.json').read_text(encoding='utf-8'))}
    if not (V/'historical_effective_first_attempt.json').exists():
        (V/'historical_effective_first_attempt.json').write_bytes((V/'historical_effective.json').read_bytes())
for item in old:
    if previous.get(item['script'],{}).get('effective_status') in ['PASS_UNMODIFIED','PASS_ADAPTED']:
        rows.append(previous[item['script']]);continue
    if item['exit_code']==0:
        rows.append({**item,'effective_status':'PASS_UNMODIFIED'});continue
    path=S/item['script'];src=path.read_text(encoding='utf-8');edits=[];lines=[]
    for line in src.splitlines(keepends=True):
        new=line
        if "for pid in ['S013','S014'" in line:
            new=line.replace("['S013','S014'","['S014'")
        if "ok('dev S013-S016 held'" in line:
            new="ok('remaining Dev held after S013',any('S014-S016' in x and '未读' in x for x in state['pending_replications']))\n"
        if path.name=='test_v138_s045_regressions.py' and "ck('version',st['current_version']" in line:
            new=new.replace("st['current_version']=='1.38.0'","st['current_version']=='1.39.0'")
            new=new.replace("st['latest_completed_paper']=='S045'","st['latest_completed_train_paper']=='S045' and st['latest_completed_dev_paper']=='S013'")
            new=new.replace("st['reproduction_level_latest']=='S045:R2'","st['reproduction_level_latest']=='S013:R2'")
        if new!=line:edits.append({'old':line.strip(),'new':new.strip()})
        lines.append(new)
    assert edits,('Unrecognized failure; must investigate',item)
    extra="\n_current_papers=json.loads((Path(__file__).resolve().parents[4]/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))\n_current_s013=next(x for x in _current_papers if x['paper_id']=='S013')\nassert _current_s013['split']=='dev' and _current_s013['reviewed_pages']==list(range(1,114)) and _current_s013['dev_boundary']=='DEV_ONLY_NOT_TRAIN_RETRIEVAL'\n"
    adapted=''.join(lines)+extra;out=io.StringIO();status='PASS_ADAPTED'
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
        try:exec(compile(adapted,str(path),'exec'),{'__name__':'__main__','__file__':str(path)})
        except Exception:status='FAIL';traceback.print_exc()
    log=V/(path.name+'.adapted.log')
    if log.exists() and not (V/(path.name+'.adapted-first-fail.log')).exists():
        (V/(path.name+'.adapted-first-fail.log')).write_bytes(log.read_bytes())
    log.write_text(out.getvalue(),encoding='utf-8')
    rows.append({**item,'effective_status':status,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'edits':edits,
                 'added_assertion':'S013 must now be completed113-page Dev-only; not simply exempted from protection',
                 'reason':'Current version legitimately changes S013 exposure and latest version; other unread Dev/Test checks unchanged.'})
    print(path.name+' '+status,flush=True)
(V/'historical_effective.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(x['effective_status'] in ['PASS_UNMODIFIED','PASS_ADAPTED'] for x in rows)
