from pathlib import Path
import hashlib,json,zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent/'current'
SKILLS=Path('C:/Users/lingyun/.codex/skills')
selected={}
def add(p,name):selected[name]=p
def tree(base,prefix):
    for p in sorted(base.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(base)
        if any(x in {'.git','__pycache__','.venv','venv','node_modules','validation_dependencies'} for x in rel.parts):continue
        if p.suffix.lower() in {'.pyc','.pdf'}:continue
        add(p,prefix+'/'+rel.as_posix())
for name in ['00_交接说明.md','新Chat提示词.md','上述内容总结.md','build_package.py']:add(OUT/name,name)
for name in ['mathmodel-evidence','mathmodel-architect','mathmodel-reviewer','mathmodel-case-retriever']:tree(SKILLS/name,'installed_skills/'+name)
for name in ['.agents','knowledge_base','learning_sources','learning_output/context','learning_output/deployment','learning_output/cases/2023-A-transfer']:
    tree(ROOT/name,'project/'+name)
for name in ['PROJECT_STATE.json','START_HERE.md','HANDOFF_NEXT_CHAT.md','NEW_CHAT_PROMPT.md','VERSION','UPSTREAM_LICENSE','UPSTREAM_LOCK.json']:
    add(ROOT/name,'project/'+name)
manifest={'purpose':'continuation bundle, not a full project backup or sealed Core release','files':[]}
package=OUT/'MathModel_换Chat交接包_20260923.zip'
with zipfile.ZipFile(package,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,p in sorted(selected.items()):
        data=p.read_bytes();sha=hashlib.sha256(data).hexdigest()
        manifest['files'].append({'path':name,'bytes':len(data),'sha256':sha,'source':str(p)})
        z.writestr(name,data)
    z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(package) as z:
    assert z.testzip() is None
    for item in manifest['files']:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
    assert 'project/learning_output/cases/2023-A-transfer/revision_v9/REFERENCE_SOLUTION.md' in z.namelist()
    assert all(f'installed_skills/{s}/SKILL.md' in z.namelist() for s in ['mathmodel-evidence','mathmodel-architect','mathmodel-reviewer'])
report={'status':'PASS','file':str(package),'bytes':package.stat().st_size,'sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'files_checked':len(manifest['files']),'zip_crc':'PASS','per_file_sha256':'PASS','scope':'archive integrity, not model correctness'}
(OUT/'ZIP_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
