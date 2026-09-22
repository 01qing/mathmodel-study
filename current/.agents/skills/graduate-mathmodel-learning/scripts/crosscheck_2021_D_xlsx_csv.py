#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, math, sys
from xlsx_stream_reader import XlsxBook

p=argparse.ArgumentParser(); p.add_argument('--xlsx-root',required=True); p.add_argument('--csv-root',required=True)
p.add_argument('--output',default='learning_output/source_crosscheck/gmcm-2021-D/crosscheck.json'); p.add_argument('--tolerance',type=float,default=1e-9)
args=p.parse_args(); XR=Path(args.xlsx_root); CR=Path(args.csv_root); OUT=Path(args.output); OUT.parent.mkdir(parents=True,exist_ok=True)

def norm(x): return str(x or '').strip().lower().replace(' ','').replace('_','').replace('-','')
def find_header(h,cands):
    for x in h:
        for c in cands:
            if norm(x)==norm(c): return x
    return None

def choose_sheet(book,kind):
    names=book.sheet_names()
    for n in names:
        if kind in norm(n): return n
    if kind=='train' and names:return names[0]
    if kind=='test' and len(names)>1:return names[1]
    return None

def read_xlsx(path,kind):
    b=XlsxBook(path); s=choose_sheet(b,kind); it=b.iter_rows(s); head=next(it); h=[str(x).strip() if x is not None else '' for x in head]; rows=[]
    for row in it:
        if len(row)<len(h): row=row+[None]*(len(h)-len(row))
        rows.append({h[i]:row[i] if i<len(row) else None for i in range(len(h))})
    return h,rows

def read_csv(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); return r.fieldnames or [],list(r)

def fnum(v):
    if v in (None,''): return None
    try:return float(v)
    except:return None

def value_equal(a,b,tol):
    fa,fb=fnum(a),fnum(b)
    if fa is not None and fb is not None:
        return math.isclose(fa,fb,rel_tol=tol,abs_tol=tol)
    return str(a or '').strip()==str(b or '').strip()

def compare_table(xh,xrows,ch,crows,kind,split):
    xsm=find_header(xh,['SMILES']); csm=find_header(ch,['SMILES']); out={'kind':kind,'split':split,'xlsx_rows':len(xrows),'csv_rows':len(crows),'status':'PASS','issues':[]}
    if len(xrows)!=len(crows): out['issues'].append('row_count_mismatch')
    if set(xh)!=set(ch):
        # tolerate same normalized names
        if {norm(x) for x in xh}!={norm(x) for x in ch}: out['issues'].append('column_set_mismatch')
    xd={str(r.get(xsm) or ''):r for r in xrows}; cd={str(r.get(csm) or ''):r for r in crows}
    if set(xd)!=set(cd): out['issues'].append('smiles_set_mismatch')
    shared=set(xd)&set(cd); mismatches=0; checked=0; examples=[]
    xmap={norm(x):x for x in xh}; cmap={norm(x):x for x in ch}
    for key in shared:
        for nk in set(xmap)&set(cmap):
            if nk==norm('SMILES'): continue
            checked+=1
            if not value_equal(xd[key].get(xmap[nk]),cd[key].get(cmap[nk]),args.tolerance):
                mismatches+=1
                if len(examples)<10: examples.append({'SMILES':key,'column':xmap[nk],'xlsx':xd[key].get(xmap[nk]),'csv':cd[key].get(cmap[nk])})
    out['cells_checked']=checked; out['numeric_or_text_mismatches']=mismatches; out['mismatch_examples']=examples
    if mismatches: out['issues'].append('value_mismatch')
    if out['issues']: out['status']='FAIL'
    return out

pairs=[
 ('activity','train','ERα_activity.xlsx','train/ERα_activity.csv'),('activity','test','ERα_activity.xlsx','test/ERα_activity.csv'),
 ('descriptor','train','Molecular_Descriptor.xlsx','train/Molecular_Descriptor.csv'),('descriptor','test','Molecular_Descriptor.xlsx','test/Molecular_Descriptor.csv'),
 ('admet','train','ADMET.xlsx','train/ADMET.csv'),('admet','test','ADMET.xlsx','test/ADMET.csv')]
results=[]; missing=[]
for kind,split,xf,cf in pairs:
    xp=XR/xf; cp=CR/cf
    if not xp.exists() or not cp.exists(): missing.append({'xlsx':str(xp),'csv':str(cp)}); continue
    xh,xr=read_xlsx(xp,split); ch,cr=read_csv(cp); results.append(compare_table(xh,xr,ch,cr,kind,split))
status='CROSSCHECK_PASS' if not missing and all(x['status']=='PASS' for x in results) else ('MISSING' if missing else 'MIRROR_NOT_EQUIVALENT')
out={'schema_version':'1.2','case_id':'gmcm-2021-D','status':status,'tolerance':args.tolerance,'results':results,'missing':missing,
     'permission':{'csv_can_replace_xlsx_for_benchmark':status=='CROSSCHECK_PASS'}}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print(f'[{status}] {OUT}'); sys.exit(0 if status=='CROSSCHECK_PASS' else 2)
