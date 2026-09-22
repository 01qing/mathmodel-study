from pathlib import Path
import hashlib, json, zipfile
import xml.etree.ElementTree as ET
import pymupdf

BASE = Path('D:/BaiduNetdiskDownload')
OUT = Path(__file__).parent / 'evidence'
OUT.mkdir(exist_ok=True)
roots = [BASE/'2024年研究生数学建模竞赛优秀论文选', BASE/'2025年研究生数学建模竞赛优秀论文选']
code = BASE/'2025代码/0-2025 E题思路+参考文献+代码+成品论文'
roots += [code/n for n in ['G老师','G老师2','X老师']]
manifest=[]
for root in roots:
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        entry={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        idx=f'S{len(manifest)+1:03}'
        entry['id']=idx
        if p.suffix.lower()=='.pdf':
            try:
                with pymupdf.open(p) as doc:
                    entry['pages']=len(doc)
                    pages=[f'\n--- PAGE {i+1} ---\n'+page.get_text() for i,page in enumerate(doc)]
                target=OUT/(idx+'.txt'); target.write_text(''.join(pages),encoding='utf-8')
                entry['text_file']=str(target); entry['status']='TEXT_EXTRACTED_NOT_REVIEWED'
            except Exception as e: entry['error']=str(e)
        elif p.suffix.lower()=='.zip':
            with zipfile.ZipFile(p) as z:
                entry['members']=z.namelist()
                extracted=[]
                for i,n in enumerate(z.namelist()):
                    if Path(n).suffix.lower() in ['.py','.m','.ipynb','.md','.txt']:
                        b=z.read(n)
                        if len(b)>3000000: continue
                        t=OUT/f'{idx}-member-{i}.txt'
                        try: s=b.decode('utf-8-sig')
                        except UnicodeDecodeError: s=b.decode('gb18030',errors='replace')
                        t.write_text(s,encoding='utf-8'); extracted.append({'member':n,'text_file':str(t)})
                entry['code_texts']=extracted
        elif p.suffix.lower() in ['.py','.m','.ipynb']:
            entry['code_file']=str(p)
        manifest.append(entry)
for p in (BASE/'2025年中国研究生数学建模竞赛赛题').rglob('*.docx'):
    with zipfile.ZipFile(p) as z:
        xml=ET.fromstring(z.read('word/document.xml'))
        paragraphs=[''.join(n.itertext()) for n in xml.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')]
    (OUT/'official-problem.txt').write_text('\n'.join(paragraphs),encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(manifest),'pdfs':sum('pages' in x for x in manifest),'code_files':sum('code_file' in x for x in manifest)},ensure_ascii=False))
