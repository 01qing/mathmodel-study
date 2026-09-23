from pathlib import Path
import tempfile,importlib.util,json,subprocess,sys,os
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
HOME_SKILLS=Path('C:/Users/lingyun/.codex/skills')
spec=importlib.util.spec_from_file_location('handoff',HOME_SKILLS/'mathmodel-evidence/scripts/handoff.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[]
def rejects(label,fn):
    try:fn()
    except ValueError:checks.append(label)
    else:raise AssertionError(label)
with tempfile.TemporaryDirectory(prefix='mathmodel_handoff_') as t:
    c=Path(t);(c/'answer.md').write_text('Synthetic fixture, not a contest solution',encoding='utf-8')
    m.snapshot(c,['answer.md']);m.check(c);checks.append('fresh snapshot accepted')
    (c/'answer.md').write_text('modified',encoding='utf-8')
    rejects('changed answer invalidates snapshot',lambda:m.check(c));m.snapshot(c,['answer.md'])
    assert (c/'review/history/v0001/handoff.json').is_file();checks.append('previous snapshot archived')
    snap=json.loads((c/'review/handoff.json').read_text())
    review=dict(snapshot_sha256=snap['snapshot_sha256'],decision='PASS',checks=['synthetic fixture inspected'],limitations=[],issues=[])
    m.dump(c/'review/review.json',review);m.check(c,True);checks.append('matching review accepted')
    review['issues']=[dict(id='Q1-1',question='Q1',severity='major',location='answer.md',evidence='synthetic failing constraint',impact='invalid result',action='correct and recheck',status='unresolved')]
    m.dump(c/'review/review.json',review);rejects('unresolved major blocks PASS',lambda:m.check(c,True))
    review['decision']='CHANGES_REQUIRED';m.dump(c/'review/review.json',review);m.check(c,True);checks.append('changes-required review recorded')
    review['snapshot_sha256']='incorrect';m.dump(c/'review/review.json',review);rejects('wrong review snapshot rejected',lambda:m.check(c,True))
    rejects('outside-case path rejected',lambda:m.snapshot(c,['../outside.md']))
    rejects('review file cannot review itself',lambda:m.snapshot(c,['review/handoff.json']))
env=os.environ.copy();env['PYTHONPATH']=str(HERE/'validation_dependencies');env['PYTHONUTF8']='1'
validations=[]
for name in ['mathmodel-evidence','mathmodel-architect','mathmodel-reviewer']:
    run=subprocess.run([sys.executable,str(HOME_SKILLS/'.system/skill-creator/scripts/quick_validate.py'),str(HOME_SKILLS/name)],env=env,capture_output=True,text=True,encoding='utf-8')
    validations.append(dict(skill=name,returncode=run.returncode,output=run.stdout.strip(),error=run.stderr.strip()))
    assert run.returncode==0,validations[-1]
run=subprocess.run([sys.executable,str(ROOT/'.agents/skills/graduate-mathmodel-learning/scripts/validate_learning_workspace.py')],cwd=ROOT,capture_output=True,text=True)
assert run.returncode==0,run.stderr
out=dict(status='PASS',scope='installed skill syntax and synthetic handoff integrity; no new contest problem run',checks=checks,skill_validation=validations,workspace=run.stdout.strip(),independent_agent_test=False)
(HERE/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
