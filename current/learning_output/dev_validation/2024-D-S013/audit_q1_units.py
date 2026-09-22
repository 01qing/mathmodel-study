"""Compare explicit aggregation contracts; no author intermediate data available."""
from pathlib import Path
import os,json
import numpy as np
import netCDF4 as nc
import rasterio
H=Path(__file__).resolve().parent
R=H.parents[1]
f=next(p for p in (R/'official-data/dataset3').rglob('*.nc') if p.is_file())
os.chdir(f.parent)
out={'scope':'aggregation hypotheses, not full author reproduction','precipitation':[],'cropland':[]}
with nc.Dataset(f.name) as ds:
 print({k:(v.shape,getattr(v,'units','')) for k,v in ds.variables.items()},flush=True)
 t=ds.variables['time'];dates=nc.num2date(t[:],t.units);years=np.array([d.year for d in dates])
 v=ds.variables['pre']
 for year,reported in [(1990,166.62),(1998,178.08),(2011,142.51),(2016,186.32),(2020,177.59)]:
  ix=np.flatnonzero(years==year)
  a=np.ma.filled(v[ix],np.nan).astype(float);a[a<0]=np.nan
  valid=np.isfinite(a).any(axis=0);total=np.nansum(a,axis=0)
  daily100=float(np.nanmean(a)*100)
  row=dict(year=year,days=len(ix),paper_mm=reported,valid_cells=int(valid.sum()),annual_sum_valid_cell_unweighted_mean_mm=float(total[valid].mean()),daily_mean_times100=daily100,difference=daily100-reported,match_rounded_2dp=round(daily100,2)==reported)
  out['precipitation'].append(row);print(row,flush=True)
for year,reported in [(1990,21.51),(2006,20.51),(2019,21.04)]:
 f=next((R/'official-data/dataset4').rglob(f'cropland-{year}.tif'))
 with rasterio.open(f) as ds:
  a=ds.read(1).astype(float);a[(a<0)|(a>1)]=np.nan
  row=dict(year=year,paper_percent=reported,finite_cell_mean_percent=float(np.nanmean(a)*100),positive_cell_mean_percent=float(a[a>0].mean()*100),finite_cells=int(np.isfinite(a).sum()),positive_cells=int((a>0).sum()))
  out['cropland'].append(row);print(row,flush=True)
(H/'Q1_AGGREGATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
