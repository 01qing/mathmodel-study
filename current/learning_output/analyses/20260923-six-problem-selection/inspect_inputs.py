from pathlib import Path
import json, zipfile, hashlib, collections, csv
from xml.etree import ElementTree as ET

ROOT=Path(r'D:\数模\数模练习')
OUT=Path(__file__).parent
OUT.mkdir(parents=True,exist_ok=True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
manifest=[]; inventories={}
for letter in 'ABCDEF':
    folder=ROOT/f'{letter}题exp'
    docs=list(folder.glob('*.docx'))
    for p in docs:
        with zipfile.ZipFile(p) as z:
            tree=ET.fromstring(z.read('word/document.xml'))
            lines=[]
            for i,para in enumerate(tree.findall('.//w:p',ns),1):
                text=''.join(el.text or '' for el in para.iter() if el.tag.endswith('}t'))
                if text.strip():lines.append(f'[{i:03d}] {text}')
            media=[e.filename for e in z.infolist() if e.filename.startswith('word/media/')]
        (OUT/f'{letter}_题面提取.txt').write_text('\n'.join(lines),encoding='utf-8')
        manifest.append({'id':letter,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'paragraphs':len(lines),'media_count':len(media),'note':'OOXML文字和公式文字提取；图像未读取，公式结构未完整渲染'})
    files=[p for p in folder.rglob('*') if p.is_file()]
    inv={'file_count':len(files),'bytes':sum(p.stat().st_size for p in files),'extensions':dict(collections.Counter(p.suffix.lower() for p in files)),'files':[{'path':str(p.relative_to(folder)),'bytes':p.stat().st_size} for p in files]}
    for zp in folder.glob('*.zip'):
        with zipfile.ZipFile(zp) as z:
            entries=[{'name':x.filename,'bytes':x.file_size,'compressed_bytes':x.compress_size} for x in z.infolist() if not x.is_dir()]
        inv.setdefault('archives',[]).append({'path':str(zp),'entries':entries,'count':len(entries),'uncompressed_bytes':sum(x['bytes'] for x in entries)})
    inventories[letter]=inv
(OUT/'input_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'attachment_inventory.json').write_text(json.dumps(inventories,ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in inventories.items():
    print(k, 'files=',v['file_count'],'bytes=',v['bytes'],'extensions=',v['extensions'])
    for a in v.get('archives',[]):
        print('ARCHIVE',a['path'],'count',a['count'],'bytes',a['uncompressed_bytes'])
        print(json.dumps(a['entries'][:18],ensure_ascii=False))
print('EXTRACTION_COMPLETE',OUT)
