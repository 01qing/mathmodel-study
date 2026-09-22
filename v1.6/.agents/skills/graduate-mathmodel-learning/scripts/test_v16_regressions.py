"""Behavioral regression checks for local state and evidence guards, not blind capability evaluation."""
from pathlib import Path
import json,subprocess,sys,tempfile
import pymupdf
from validate_paper_inventory import validate
import hashlib

S=Path(__file__).parent
passed=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    passed.append(name)
def run(name,*args):return subprocess.run([sys.executable,'-X','utf8',str(S/name),*map(str,args)],capture_output=True,text=True,encoding='utf-8')
with tempfile.TemporaryDirectory() as temp:
    d=Path(temp); g=d/'gate.json';m=d/'matrix.json'
    def start(exposure,case='fixture',fingerprint='fixture-hash'):
        return run('start_blind_case.py','--case-id',case,'--problem-fingerprint',fingerprint,'--output',g,'--solution-exposure',exposure)
    check('initial contamination recorded',start('true').returncode==0)
    check('reinitialization cannot erase exposure',start('false').returncode==0 and not json.loads(g.read_text())['fresh_blind_eligible'])
    old=g.read_bytes();check('different fingerprint rejected without overwrite',start('false',fingerprint='different').returncode!=0 and old==g.read_bytes())
    m.write_text('{"questions":{"Q1":{"baseline":"fixture"}}}',encoding='utf-8')
    check('freeze contaminated matrix remains contaminated',run('freeze_blind_matrix.py','--gate',g,'--matrix',m).returncode==0 and not json.loads(g.read_text())['fresh_blind_eligible'])
    old=g.read_bytes();check('same freeze idempotent',run('freeze_blind_matrix.py','--gate',g,'--matrix',m).returncode==0 and old==g.read_bytes())
    m.write_text('{"different":true}',encoding='utf-8')
    check('different matrix rejected without overwrite',run('freeze_blind_matrix.py','--gate',g,'--matrix',m).returncode!=0 and old==g.read_bytes())
    g=d/'clean.json';check('fresh case allowed',start('false').returncode==0 and json.loads(g.read_text())['fresh_blind_eligible'])
    m.write_text('{}',encoding='utf-8');check('empty matrix rejected',run('freeze_blind_matrix.py','--gate',g,'--matrix',m).returncode!=0)
    g.write_text('broken',encoding='utf-8');check('corrupted gate fails closed',start('false').returncode!=0 and g.read_text()=='broken')
    pdf=d/'paper.pdf';doc=pymupdf.open();doc.new_page();doc.save(pdf);doc.close()
    item={'source_id':'fixture','path':str(pdf),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':1,'review_status':'not_reviewed','reviewed_pages':[]}
    check('zero papers valid',not validate([],d))
    check('real nonzero PDF count valid',not validate([item],d))
    check('wrong hash blocked',bool(validate([{**item,'sha256':'bad'}],d)))
    check('wrong page count blocked',bool(validate([{**item,'page_count':2}],d)))
    check('full review without coverage blocked',bool(validate([{**item,'review_status':'full'}],d)))
    check('full declared review with coverage accepted',not validate([{**item,'review_status':'full','reviewed_pages':[1],'review_evidence':'fixture note'}],d))
    check('missing PDF blocked',bool(validate([{**item,'path':str(d/'missing.pdf')}],d)))
    check('duplicate source blocked',bool(validate([item,item],d)))
    # Exercise the formerly hardcoded historical validator with a real nonzero inventory.
    base=d/'.agents/skills/graduate-mathmodel-learning/assets/cases';base.mkdir(parents=True)
    payloads={'2024_C_blind_contamination.json':{'fresh_blind_status':'CONTAMINATED'},
        '2024_C_independent_model_competition.json':{'analysis_status':'NOT_FRESH_BLIND','questions':{**{q:{} for q in ['Q1','Q2','Q3','Q4']},'Q5':{'objectives':{'minimize':'loss','maximize':'energy'}}}},
        '2024_C_paper_access_queue.json':{'full_paper_materialization':{'materialized_count':1},'materialized_papers':[item],'do_not_promote_profiles_to_papers':True}}
    for n,obj in payloads.items():(base/n).write_text(json.dumps(obj),encoding='utf-8')
    proc=subprocess.run([sys.executable,'-X','utf8',str(S/'validate_v15_case_logic.py')],cwd=d,capture_output=True)
    check('historical validator accepts evidenced nonzero inventory',proc.returncode==0)
print(json.dumps({'scope':'Known-defect regression checks','passed':len(passed),'tests':passed,'independent_modeling_evaluation':'NOT_RUN'},ensure_ascii=False,indent=2))
