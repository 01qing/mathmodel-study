from pathlib import Path
import sys,json,zipfile,io,pickle,collections,time,subprocess,hashlib
OUT=Path(__file__).parent;sys.path.insert(0,str(OUT/'runtime_deps'));sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from scipy.io import loadmat
from openpyxl import load_workbook
import pandas as pd
ROOT=Path(r'D:\数模\数模练习');result={}
# Inspect spreadsheet unit contracts without fitting or changing source data.
with zipfile.ZipFile(next((ROOT/'B题exp').glob('*.zip'))) as z:
    wb=load_workbook(io.BytesIO(z.read('附件2.xlsx')),data_only=True,read_only=True)
    result['B_current_area']={}
    for s in wb:
        a=np.array([r[:5] for r in s.iter_rows(min_row=3,values_only=True) if isinstance(r[0],(int,float))],float)
        mask=(a[:,4]>0)&np.isfinite(a[:,4])
        area=a[mask,1]/a[mask,4]
        result['B_current_area'][s.title]={'rows':len(a),'time_range':a[[0,-1],0].tolist(),'implied_area_min_cm2':float(area.min()),'implied_area_max_cm2':float(area.max()),'first_row':a[0].tolist(),'stated_area_cm2':25,'matches_stated_area':bool(np.allclose(area,25))}
    wb.close()
# MAT data structure and actual event changes.
result['C_events']={}
for p in (ROOT/'C题exp').glob('*.mat'):
    m=loadmat(p);a=m['data'];labels=[str(x[0]) for x in m['DataLabel'].ravel()]
    ev={}
    for i in [7,8]:
        v=a[i]; onset=(v!=0)&np.r_[True,v[1:]!=v[:-1]]
        vals,counts=np.unique(v[onset],return_counts=True)
        ev[labels[i]]={'nonzero_run_start_counts':dict(zip(vals.tolist(),counts.tolist())),'all_values':np.unique(v).tolist()}
    result['C_events'][p.name]={'labels':labels,'sampling_rate':float(m['SampleRate'].item()),'events':ev}
# D coordinate coverage. DEM is available in scipy-readable MAT, so GIS runtime is not a blocker.
demfile=next((ROOT/'D题exp').rglob('*30米DEM.mat'));m=loadmat(demfile)
lat=m['latitude'].ravel();lon=m['longitude'].ravel();dem=m['dem'];nd=float(m['nodata'].item())
valid=np.isfinite(dem)&(dem!=nd)
wb=load_workbook(next((ROOT/'D题exp').rglob('调度中心与服务区.xlsx')),read_only=True,data_only=True)
nodes=[]
for row in wb.active.iter_rows(values_only=True):
    if isinstance(row[0],str) and (row[0]=='O01' or (row[0].startswith('S') and row[0][1:].isdigit())):
        x,y=float(row[2]),float(row[3]);r=int(np.argmin(abs(lat-y)));c=int(np.argmin(abs(lon-x)))
        nodes.append({'id':row[0],'in_bbox':bool(lon.min()<=x<=lon.max() and lat.min()<=y<=lat.max()),'nearest_dem_valid':bool(valid[r,c]),'given_elevation':row[4],'nearest_dem':float(dem[r,c])})
wb.close()
result['D_DEM']={'shape':list(dem.shape),'epsg':float(m['epsg_code'].item()),'nodata_fraction':float(1-valid.mean()),'elevation_range':[float(dem[valid].min()),float(dem[valid].max())],'nodes':nodes}
wb=load_workbook(next((ROOT/'D题exp').rglob('物资需求与配送时限.xlsx')),read_only=True,data_only=True)
rows=list(wb['逐箱货箱清单'].iter_rows(min_row=2,values_only=True));rows=[r for r in rows if r[0]]
result['D_cargo']={'boxes':len(rows),'unique_ids':len(set(r[0] for r in rows)),'service_count':len(set(r[1] for r in rows)),'total_kg':sum(float(r[3]) for r in rows)};wb.close()
# Safe, restricted unpickling of small supplied feature examples only, no arbitrary globals.
class FeatureUnpickler(pickle.Unpickler):
    def find_class(self,module,name):
        if (module,name) in [('numpy','asarray'),('numpy','ndarray'),('numpy','dtype'),('numpy.core.multiarray','_reconstruct'),('numpy._core.multiarray','_reconstruct'),('numpy.core.multiarray','scalar'),('numpy._core.multiarray','scalar'),('numpy.core.numeric','_frombuffer'),('numpy._core.numeric','_frombuffer')]: return super().find_class(module,name)
        raise pickle.UnpicklingError(f'Unapproved global {module}.{name}')
def describe(o,level=0):
    if isinstance(o,np.ndarray):return {'shape':list(o.shape),'dtype':str(o.dtype),'finite_fraction':float(np.isfinite(o).mean()) if o.dtype.kind in 'fiu' and o.size else None}
    if isinstance(o,dict):return {str(k):describe(v,level+1) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return {'type':type(o).__name__,'len':len(o),'first':describe(o[0],level+1) if len(o) and level<3 else None}
    return str(o)[:90]
with zipfile.ZipFile(next((ROOT/'E题exp').glob('*.zip'))) as z:
    targets=[]
    for prefix in ['附件3-','附件4-']:
        for ver in ['对齐版本/','未对齐版本/']:
            names=[n for n in z.namelist() if prefix in n and '/'+ver in n and n.endswith('.pkl')]
            if names:targets.append(names[0])
    result['E_feature_samples']={}
    for name in targets:
        try:result['E_feature_samples'][name]=describe(FeatureUnpickler(io.BytesIO(z.read(name))).load())
        except Exception as e:result['E_feature_samples'][name]={'error':str(e)}
    name=next(n for n in z.namelist() if '附件2-' in n and n.endswith('label.xlsx'))
    wb=load_workbook(io.BytesIO(z.read(name)),read_only=True,data_only=True)
    rows=list(wb['label'].iter_rows(min_row=2,values_only=True));wb.close()
    modes=collections.Counter(str(r[5]) for r in rows)
    ids=[(str(r[0]),str(r[1])) for r in rows]
    result['E_labels']={'samples':len(rows),'unique_clip_ids':len(set(ids)),'splits':dict(modes),'class_counts':dict(collections.Counter(str(r[4]) for r in rows))}
for name in ['loss_benchmark_bridge_expanded.csv','leaderboard_extended_timeseries.csv']:
    p=ROOT/'F题exp/real_attachments/C_efficiency_evolution'/name;df=pd.read_csv(p)
    info={'rows':len(df),'columns':list(df.columns),'null_counts':df.isna().sum().to_dict()}
    for col in df:
        if any(k in col.lower() for k in ['source','type','compar','quality','confidence','synthe']):info[col+'_counts']=df[col].value_counts(dropna=False).head(20).to_dict()
    result.setdefault('F_provenance',{})[name]=info
pdffile=ROOT/'F题exp/数据说明.pdf'
import pdfplumber,logging
logging.getLogger('pdfminer').setLevel(logging.ERROR)
with pdfplumber.open(pdffile) as pdf:
    page=pdf.pages[1]
    def faint(ch):
        color=ch.get('non_stroking_color')
        return isinstance(color,(list,tuple)) and len(color) in (1,3) and min(color)>.98
    hidden=[ch for ch in page.chars if faint(ch)]
    result['F_pdf_small_text']={'page':2,'small_char_count':len(hidden),'normal_char_count':len(page.chars)-len(hidden),'sizes':collections.Counter(round(ch['size'],2) for ch in hidden),'sample':''.join(ch['text'] for ch in hidden)[:350]}
    visible=[]
    for i,p in enumerate(pdf.pages):
        filtered=p.filter(lambda o:o.get('object_type')!='char' or not faint(o))
        visible.append(f'=== PAGE {i+1} ===\n{filtered.extract_text()}')
    (OUT/'F_数据说明_可见字号文本.txt').write_text('\n\n'.join(visible),encoding='utf-8')
(OUT/'readiness_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
