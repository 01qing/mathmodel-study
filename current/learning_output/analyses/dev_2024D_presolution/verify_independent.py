from pathlib import Path
import json,hashlib,os,calendar
import numpy as np
import netCDF4
H=Path(__file__).resolve().parent;R=H.parents[3];O=H/'results'
d=np.load(O/'climate_land.npz'); reg=json.loads((O/'RESULT_REGISTRY.json').read_text(encoding='utf-8'));audit=json.loads((O/'feature_audit.json').read_text(encoding='utf-8'))
checks=[]
def check(name,ok,scope):
 checks.append({'name':name,'pass':bool(ok),'scope':scope})
 if not ok: print('FAIL',name,flush=True)
frozen=json.loads((R/'FROZEN_CORE_V138_FILES.sha256.json').read_text(encoding='utf-8'))
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
check('frozen_core_1470_files',all(sha(R/'v1.39-work'/p)==h for p,h in frozen.items()),'original Core bytes unchanged; not historical regression rerun')
check('land_fraction_simplex',audit['land']['sum_above_1_001']==0,'five-type fraction sums <=1.001')
check('DEM_missing_sentinel_removed',np.nanmin(d['dem'])>=0 and np.nanmax(d['dem'])<=8848,'prepared DEM physical range for this source')
check('temperature_complete_years',all(v==365+calendar.isleap(int(y)) for y,v in audit['temperature']['annual_days'].items()),'1990–2018 daily file count')
check('socio_mass_conservation',all(c['relative_conservation_error']<1e-10 for c in audit['socio']['checks']),'eight anchor raster sums, within target rectangle')
check('annual_rain_ge_daily_max',np.all(d['pre'][:,d['mask']]+1e-5>=d['rx1'][:,d['mask']]),'physical precipitation aggregation inequality')
check('daily_max_nonnegative',np.all(d['rx1'][:,d['mask']]>=0),'negative sentinels excluded')
# Independent numeric arbiter: direct source-cell intersection loops, rather
# than the sparse matrix used in feature preparation, for three interior cells.
raw=next(f for f in (R/'official-data/dataset3').rglob('*.nc') if f.is_file());old=os.getcwd();os.chdir(raw.parent);nc=netCDF4.Dataset(raw.name);os.chdir(old)
times=netCDF4.num2date(nc['time'][:],nc['time'].units); ids=[i for i,t in enumerate(times) if t.year==1990]
sx=np.array(nc['longitude'][:]);sy=np.array(nc['latitude'][:]);pts=np.argwhere(d['mask']&(d['coverage']>.999))
errors=[]
for idx in [len(pts)//4,len(pts)//2,3*len(pts)//4]:
 i,j=pts[idx];x=float(d['lon'][j]);y=float(d['lat'][i]);num=np.zeros(len(ids));den=np.zeros(len(ids))
 for ri in np.where(np.abs(sy-y)<.375)[0]:
  for ci in np.where(np.abs(sx-x)<.375)[0]:
   left=max(x-.25,sx[ci]-.125);right=min(x+.25,sx[ci]+.125);bottom=max(y-.25,sy[ri]-.125);top=min(y+.25,sy[ri]+.125)
   w=max(right-left,0)*(np.sin(np.deg2rad(top))-np.sin(np.deg2rad(bottom)))
   a=np.array(nc['pre'][ids,ri,ci]);valid=np.isfinite(a)&(a>=0);num+=np.where(valid,a,0)*w;den+=valid*w
 z=num/den;errors.append({'row':int(i),'column':int(j),'annual_error':float(abs(z.sum()-d['pre'][0,i,j])),'Rx1_error':float(abs(z.max()-d['rx1'][0,i,j]))})
nc.close()
check('independent_precipitation_overlap_replay',all(e['annual_error']<1e-4 and e['Rx1_error']<1e-5 for e in errors),'direct source-cell spherical intersection, three interior cells,365days1990')
check('model_selection_gate',reg['claims']['Q2']['selected']=='climatology' or any(r['model']==reg['claims']['Q2']['selected'] and r['validation_gain_vs_climatology']>=.05 and r['spatial_wins']>=4 for r in reg['claims']['Q2']['models']),'predefined development and spatial promotion thresholds')
check('scenario_frequency_bounds',all(np.all((np.load(O/'Q3_scenarios.npz')[f'top_decile_frequency{y}'][d['mask']]>=0)&(np.load(O/'Q3_scenarios.npz')[f'top_decile_frequency{y}'][d['mask']]<=1)) for y in [2025,2030,2035]),'36 scenario frequency is a fraction, not disaster probability')
check('all_figures_exist',all((H/'figures'/n).stat().st_size>1000 for n in ['Q1_precipitation.png','Q1_landcover.png','Q2_validation.png','Q3_scenario_maps.png','Q4_regions.png']),'file existence, visual review separately')
result={'checks':checks,'independent_precipitation_errors':errors,'pass':all(c['pass'] for c in checks),'not_claimed':['Core capability gain','disaster forecast accuracy','causal terrain effect','historical pristine exposure','full historical Core test rerun']}
(O/'INDEPENDENT_VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
assert result['pass']
