from pathlib import Path
import json, hashlib, zipfile
import lxml.etree as ET
import openpyxl
ROOT=Path('D:/数模/数模练习/D题exp')
CASE=Path(__file__).resolve().parents[1]
out={}
for p in ROOT.rglob('*.xlsx'):
    w=openpyxl.load_workbook(p,data_only=True)
    out[p.stem]={s.title:list(s.values) for s in w}
(CASE/'results/input_tables.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'read_content':p.suffix.lower()!='.pdf'} for p in ROOT.rglob('*') if p.is_file()]
(CASE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
p=next(ROOT.glob('*.docx'))
r=ET.fromstring(zipfile.ZipFile(p).read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
txt='\n'.join(''.join(n.xpath('.//w:t/text() | .//m:t/text()',namespaces=ns)) for n in r.xpath('.//w:body/w:p | .//w:body/w:tbl',namespaces=ns))
(CASE/'PROBLEM_EXTRACT.txt').write_text(txt,encoding='utf-8')
print('Input hashes and text saved. PDF contents not parsed.')
