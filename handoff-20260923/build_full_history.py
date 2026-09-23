from pathlib import Path
import os,json,hashlib,zipfile,time
OUT=Path(__file__).resolve().parent
STUDY=OUT.parent
RECOVERY=STUDY.parent/'mathmodel-recovery/2026-09-21'
SKILLS=Path('C:/Users/lingyun/.codex/skills')
SKIP={'.git','node_modules','__pycache__','.venv','venv','.pytest_cache','validation_dependencies'}
selected={};excluded=[]
def tree(base,prefix,extra=set()):
    for root,dirs,names in os.walk(base):
        root=Path(root)
        for d in dirs[:]:
            if d in SKIP or d in extra or (root/d).is_symlink():
                excluded.append(str(root/d));dirs.remove(d)
        for name in names:
            p=root/name
            if p.suffix=='.pyc' or p.is_symlink():continue
            selected[prefix+'/'+p.relative_to(base).as_posix()]=p
tree(STUDY,'mathmodel-study',{'handoff-20260923'})
tree(RECOVERY,'recovery-v1.41',{'sealed-v1.41'})
for name in ['mathmodel-evidence','mathmodel-architect','mathmodel-reviewer','mathmodel-case-retriever']:tree(SKILLS/name,'installed_skills/'+name)
for name in ['完整资料上传顺序.md','新Chat提示词.md','上述内容总结.md','build_full_history.py']:selected[name]=OUT/name
archive=OUT/'MathModel_完整历史资料包_20260923.zip'
manifest={'scope':'All existing project information except listed runtime/cache/git directories; original sealed v1.41 ZIP and installed entry skills included','excluded_directories':excluded,'files':[]}
print('Selected',len(selected),'files; packing now',flush=True)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for index,(name,p) in enumerate(sorted(selected.items()),1):
        data=p.read_bytes();manifest['files'].append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'source':str(p)})
        z.writestr(name,data)
        if index%500==0:print('Packed',index,flush=True)
    z.writestr('FULL_FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
print('Validating every archived file',flush=True)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for f in manifest['files']:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256'],f['path']
report={'status':'PASS','file':str(archive),'files_checked':len(manifest['files']),'uncompressed_bytes':sum(f['bytes'] for f in manifest['files']),'archive_bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'crc':'PASS','per_file_sha256':'PASS','excluded_directories':excluded,'known_missing':'Full historical ChatGPT transcripts and independently identified 2023-C final sealed ZIP are not guaranteed present; see upload guide.'}
(OUT/'FULL_ZIP_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='excluded_directories'},ensure_ascii=False,indent=2),flush=True)
