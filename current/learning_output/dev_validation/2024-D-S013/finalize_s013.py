from pathlib import Path
import json,hashlib,datetime,zipfile
P=Path(__file__).resolve().parent;R=P.parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=load(P/'validation/S013_CLOSURE_VALIDATION.json');assert v['status']=='PASS'
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
state={'status':'S013_DEV_REVIEW_COMPLETE','updated':now,'paper_id':'S013','case_group':'2024-D','split':'dev',
       'S013_total_pages':113,'full_text_review_completed':True,'text_reviewed_pages':list(range(1,114)),
       'visual_reviewed_pages':list(range(1,114)),'printed_code_static_pages':list(range(82,114)),
       'reproduction_level':'R2','full_reproduction':False,'independent_solution':'FROZEN_UNCHANGED_55_FILES',
       'core':'v1.38_UNCHANGED_1470_FILES','core_v139':'NOT_SEALED','closure_checks':42,
       'rule_updates':'DEV_CANDIDATES_ONLY_NOT_PROMOTED','historical_original':'21/22; v126 FAIL retained',
       'historical_adapted':'22/22 compatibility incl one external adaptation; v138 additional adapted127/127',
       'S014_S016':'NOT_OPENED_THIS_SESSION','Test':'NOT_OPENED_THIS_SESSION','core_gain':'NOT_ESTABLISHED',
       'historical_pristine':'UNVERIFIED','next':'Stop at S013 completion as requested; remaining Dev review and integrated tuning require subsequent continuation.',
       'report':'S013_FINAL_REVIEW.md','validation':'VALIDATION_S013.md','previous_state':'RECOVERY_STATE_PRE_CLOSURE.json'}
save(P/'RECOVERY_STATE.json',state)
save(P/'DEV_EXPOSURE_OVERLAY.json',{'base_index':'Frozen v1.38 snapshot is not modified','current_reviewed_dev_this_cycle':['S013'],
     'historically_exposed_dev':['S029'],'still_unopened_this_cycle':['S014','S015','S016','S030','S031'],
     'protected_test':['S021','S022','S023','S024','S037','S038'],'train_retrieval_eligible_additions':[],
     'historical_pristine':'UNVERIFIED','independent_freeze_manifest_sha256':'ee139e2a7063fd6cb3a279ae5acba633f2e6784f8afa62d9e51fbc9a1db42a7e'})
current=load(R/'CURRENT_STATE.json');current['dev_comparison']=state
current['dev_comparison_report']=str(P/'S013_FINAL_REVIEW.md')
current['status_scope_note']='status is historical independent-freeze snapshot; dev_comparison is current. S013 is now completed R2 in Dev isolation after authorized access; v1.39 Core NOT SEALED.'
save(R/'CURRENT_STATE.json',current)
if (P/'FILES.sha256').exists() and not (P/'FILES_PRE_CLOSURE.sha256').exists():
    (P/'FILES_PRE_CLOSURE.sha256').write_bytes((P/'FILES.sha256').read_bytes())
files=sorted(x for x in P.rglob('*') if x.is_file() and x.name!='FILES.sha256' and '__pycache__' not in x.parts)
(P/'FILES.sha256').write_text(''.join(f'{sha(f)}  {f.relative_to(P).as_posix()}\n' for f in files),encoding='utf-8')
dest=R/'release-s013-dev-review';dest.mkdir(exist_ok=True)
z=dest/'MathModel-Core-v1.39-S013-Dev-Review-Complete.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for f in files+[P/'FILES.sha256']:archive.write(f,Path('S013')/f.relative_to(P))
    source=Path(load(P/'S013_QUESTION_CARDS.json')['source']);archive.write(source,'S013_SOURCE/D24103850092.pdf')
with zipfile.ZipFile(z) as archive:
    assert archive.testzip() is None
    for f in files:
        assert hashlib.sha256(archive.read('S013/'+f.relative_to(P).as_posix())).hexdigest()==sha(f)
digest=sha(z)
(dest/(z.stem+'.sha256')).write_text(f'{digest}  {z.name}\n',encoding='utf-8')
save(dest/'PACKAGE_MANIFEST.json',{'status':'S013_DEV_REVIEW_COMPLETE_NOT_CORE_RELEASE','created_at':now,
     'zip':str(z),'zip_sha256':digest,'zip_integrity':'PASS','file_hashes_checked':len(files),
     'source_pdf_included':'S013 only','official_datasets_included':False,'frozen_core_included':False,
     'requires_existing_baseline':'v1.38 + frozen v1.39 independent solution for full reruns','core_v139':'NOT_SEALED'})
print(json.dumps({'zip':str(z),'sha256':digest,'files_checked':len(files),'status':state['status']},ensure_ascii=False),flush=True)
