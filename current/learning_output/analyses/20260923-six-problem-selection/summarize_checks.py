from pathlib import Path
import json,sys
import pypdfium2 as pdfium
OUT=Path(__file__).parent
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads((OUT/'data_inspection.json').read_text(encoding='utf-8'))
for group in ['B_excel','D_excel','E_labels']:
    print('\n',group)
    for k,v in d[group].items():
        print(k)
        for s in v: print(s['sheet'],s['rows'],s['cols'],json.dumps(s['sample'][:3],ensure_ascii=False,default=str))
print('\nE_nonvideo')
for f in d['E_nonvideo']:
    if not '/__MACOSX/' in f['name'] and not f['name'].endswith('.DS_Store'):print(f)
print('\nA graph count / total ops min max',len(d['A_graphs']),min(g['sizes']['ops'] for g in d['A_graphs']),max(g['sizes']['ops'] for g in d['A_graphs']))
print('\nF_csv')
for k,v in d['F_csv'].items(): print(k,v['rows'],v['columns'][:8])
pdf=pdfium.PdfDocument(r'D:\数模\数模练习\F题exp\数据说明.pdf')
pdf[1].render(scale=1.6).to_pil().save(OUT/'F_PDF_page2.png')
