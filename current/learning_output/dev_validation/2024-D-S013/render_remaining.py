from pathlib import Path
import json
import pymupdf
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent
d=pymupdf.open(r'D:\BaiduNetdiskDownload\2024年研究生数学建模竞赛优秀论文选\2024年研究生数学建模竞赛优秀论文选\D\D24103850092.pdf')
s=json.loads((H/'RECOVERY_STATE.json').read_text(encoding='utf-8'))
remaining=[n for n in range(1,114) if n not in s['visual_reviewed_pages']]
out=H/'visual/sheets';out.mkdir(exist_ok=True)
groups=[]
for i in range(0,len(remaining),4):
 pages=remaining[i:i+4];sheet=Image.new('RGB',(1800,2600),'white');draw=ImageDraw.Draw(sheet)
 for j,n in enumerate(pages):
  p=d[n-1].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5));f=H/f'visual/p{n:03}.png';p.save(f)
  im=Image.open(f);im.thumbnail((900,1268));x=(j%2)*900;y=(j//2)*1300
  draw.text((x+12,y+5),f'PDF PAGE {n}',fill='black');sheet.paste(im,(x,y+25))
 f=out/f'batch{i//4+1:02}.png';sheet.save(f);groups.append({'sheet':f.name,'pages':pages})
(out/'index.json').write_text(json.dumps(groups,indent=2),encoding='utf-8');print(groups)
