from pathlib import Path
import re,html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
body=ParagraphStyle('body',fontName='STSong-Light',fontSize=10.5,leading=17,spaceAfter=7,wordWrap='CJK')
h1=ParagraphStyle('title',parent=body,fontSize=18,leading=25,spaceAfter=15,textColor=HexColor('#173650'))
h2=ParagraphStyle('heading',parent=body,fontSize=13,leading=20,spaceBefore=13,spaceAfter=7,keepWithNext=True,textColor=HexColor('#173650'))
h3=ParagraphStyle('subheading',parent=h2,fontSize=11.5)
def formatted(s):
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'\1 (\2)',s)
    return html.escape(s.replace('`','').replace('**',''))
story=[]
for block in (ROOT/'REFERENCE_SOLUTION.md').read_text(encoding='utf-8').split('\n\n'):
    block=block.strip()
    if not block:continue
    if block.startswith('!['):
        match=re.match(r'!\[(.*?)\]\((.*?)\)',block)
        pic=Image(str(ROOT/match[2]));pic.drawHeight*=485/pic.drawWidth;pic.drawWidth=485
        story.append(KeepTogether([pic,Paragraph(formatted(match[1]),body)]));continue
    style=h3 if block.startswith('### ') else h2 if block.startswith('## ') else h1 if block.startswith('# ') else body
    block=re.sub(r'^#{1,3} ','',block)
    if block.startswith('- '):
        for line in block.splitlines():story.append(Paragraph(formatted(line),body))
    else:story.append(Paragraph(formatted(block).replace('\n','<br/>'),style))
def footer(c,doc):
    c.setFont('STSong-Light',9);c.setFillColor(HexColor('#657383'))
    c.drawString(50,27,'2023-A 跨题迁移参考解答 v1 · 条件性模型结果')
    c.drawRightString(545,27,str(doc.page))
doc=SimpleDocTemplate(str(ROOT/'deliverables/2023A_reference_v1.pdf'),pagesize=(595.28,841.89),
    rightMargin=50,leftMargin=50,topMargin=43,bottomMargin=48,title='2023-A WLAN参考解答 v1',author='MathModel local study')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF exported')
