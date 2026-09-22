from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'learning_output/analyses/dev_2024D'
checks=[]
def ck(name,cond,detail=''):
    checks.append({'name':name,'passed':bool(cond),'detail':detail})
    if not cond: print('FAIL',name,detail)

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

# S015/S016 closure
for pid,pages,audit in [('S015',96,17),('S016',114,19)]:
    d=A/pid
    led=json.loads((d/'PAGE_AUDIT_LEDGER.json').read_text(encoding='utf-8'))
    reg=json.loads((d/'RESULT_REGISTRY.json').read_text(encoding='utf-8'))
    # ledger shapes vary; rely on evidence file count plus status fields
    visual=list((d/'visual').glob('p*.png'))
    ck(pid+' source', (d/'source.pdf').exists())
    ck(pid+' final review', (d/f'{pid}_FINAL_REVIEW.md').exists())
    ck(pid+' registry final', reg.get('status')=='FINAL_R2_AUDIT_REGISTRY')
    ck(pid+' R2', reg.get('reproduction_level')=='R2')
    ck(pid+' visual count', len(visual)==pages, str(len(visual)))
    ck(pid+' text page claim', reg.get('text_pages_reviewed')==pages)
    ck(pid+' visual page claim', reg.get('visual_pages_reviewed')==pages)
    ck(pid+' audit count', reg.get('audit_replay',{}).get('passed')==audit)
    ck(pid+' source hash', reg.get('source_sha256')==sha(d/'source.pdf'))

# case-group map and composer
m=json.loads((A/'FINAL_METHOD_COMPETITION_MAP_V141.json').read_text(encoding='utf-8'))
ck('group final',m.get('status')=='FINAL_2024D_CASE_GROUP_REVIEW_COMPLETE')
ck('four papers',m.get('papers_reviewed')==['S013','S014','S015','S016'])
ck('four questions',set(m.get('questions',{}))=={'Q1','Q2','Q3','Q4'})
ck('all R2',all(x=='R2' for x in m.get('reproduction_levels',{}).values()))
ck('no capability overclaim','not controlled Core gain' in m.get('capability_evidence',''))
c=json.loads((A/'METHOD_COMPOSER_V141.json').read_text(encoding='utf-8'))
ck('seven gates',len(c.get('gates',[]))==7)
ck('composer rejects direct author pipelines','reject direct concatenation' in c.get('composition_decision',''))

# generic rule routing and errors
ref=ROOT/'.agents/skills/graduate-mathmodel-learning/references/dev-casegroup-contracts-v141.md'
skill=ROOT/'.agents/skills/graduate-mathmodel-learning/SKILL.md'
ck('v141 reference exists',ref.exists())
ck('v141 reference routed','dev-casegroup-contracts-v141.md' in skill.read_text(encoding='utf-8'))
err=json.loads((ROOT/'knowledge_base/error_patterns/2024-D-v141.json').read_text(encoding='utf-8'))
ck('error patterns',len(err.get('patterns',[]))>=8)

# mini transfer
mt=json.loads((ROOT/'learning_output/mini_transfer/2024D_v141/MINI_TRANSFER_RESULTS.json').read_text(encoding='utf-8'))
ck('mini transfer mechanism pass',mt.get('status')=='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX')
ck('mini transfer not capability',mt.get('core_gain')=='NOT_ESTABLISHED' and mt.get('controlled_ablation')=='NOT_RUN')

# frozen independent solution unchanged
PRES=ROOT/'learning_output/analyses/dev_2024D_presolution'
fm=PRES/'DEV_2024D_FREEZE_MANIFEST.json'
f=json.loads(fm.read_text(encoding='utf-8'))
bad=[]
for rel,meta in f.get('files',{}).items():
    q=PRES/rel
    if not q.exists() or sha(q)!=meta['sha256']: bad.append(rel)
ck('frozen independent files intact',not bad,','.join(bad[:5]))
ck('freeze status',f.get('status')=='INDEPENDENT_SOLUTION_FROZEN')

# Previous release identity verified
prev=json.loads((ROOT/'learning_output/validation/v141/PREVIOUS_RELEASE_V140_VERIFICATION.json').read_text(encoding='utf-8'))
ck('v140 release identity',prev.get('match') is True)

# one shared Core: no newly-created role skill directory names
names={x.name.lower() for x in (ROOT/'.agents/skills').iterdir() if x.is_dir()}
for n in ['mathmodel-master','mathmodel-architect','mathmodel-engineer','mathmodel-writer','mathmodel-reviewer']:
    ck('no role split '+n,n not in names)

passed=sum(x['passed'] for x in checks); total=len(checks)
out={'status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'checks':checks,'scope':'2024-D group closure/release-contract assets; not author end-to-end reproduction or Core capability gain'}
path=ROOT/'learning_output/validation/v141/test_v141_2024D_group.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'passed':passed,'total':total},ensure_ascii=False))
sys.exit(0 if passed==total else 1)
