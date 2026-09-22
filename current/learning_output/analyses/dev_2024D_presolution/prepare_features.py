"""Official-data-only geospatial aggregation. Run from any working directory."""
from pathlib import Path
import os,json,calendar,time,warnings
import numpy as np
import rasterio as rio
from rasterio.warp import reproject,Resampling
from rasterio.windows import Window
from pyproj import Transformer
import netCDF4
from scipy.sparse import csr_matrix

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
RAW=ROOT/'official-data'
OUT=HERE/'results'; OUT.mkdir(exist_ok=True)
audit={'failures_and_repairs':[
 {'first_fail':'inventory parser treated CRLF records as one record','diagnosis':'line endings not normalized before blank-line split','repair':'normalize CRLF; rerun six inventories','retest':'counts 71/29263/6/1204/133/109'},
 {'first_fail':'netCDF4 could not open Unicode full path','diagnosis':'native Windows path encoding; first lookup also selected .nc directory','repair':'require is_file; open ASCII basename from file parent','retest':'dimensions and variables loaded'},
 {'first_fail':'DEM nodata absent in metadata','diagnosis':'-32768 sentinel would bias mean elevation','repair':'explicitly mask -32768, record source CRS mismatch','retest':'physical-range and mask checks below'}]}

def dump(): (OUT/'feature_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
base=next((RAW/'dataset4').rglob('cropland-1990.tif'))
with rio.open(base) as d:
    shape=d.shape; trans=d.transform; crs=d.crs
ny,nx=shape
lon=trans.c+(np.arange(nx)+.5)*trans.a
lat=trans.f+(np.arange(ny)+.5)*trans.e
area=(6371.0088**2*np.deg2rad(.5)*(np.sin(np.deg2rad(lat+.25))-np.sin(np.deg2rad(lat-.25))))[:,None]*np.ones((1,nx))

def warp(arr,src_trans,src_crs,nodata=np.nan,method=Resampling.average):
    dst=np.full(shape,np.nan,dtype='float32')
    reproject(arr,dst,src_transform=src_trans,src_crs=src_crs,src_nodata=nodata,dst_transform=trans,dst_crs=crs,dst_nodata=np.nan,resampling=method)
    return dst

# Land fractions: preserve five types, unknown remainder; no fabricated transitions.
types=['cropland','forest','grass','shrub','wetland']
names={f.name.split('-')[0] for f in (RAW/'dataset4').rglob('*-1990.tif')}
if 'grassland' in names: types[2]='grassland'
if 'shrubland' in names: types[3]='shrubland'
land=[]
for y in range(1990,2020):
    rows=[]
    for typ in types:
        with rio.open(next((RAW/'dataset4').rglob(f'{typ}-{y}.tif'))) as d:
            assert d.shape==shape and d.transform==trans
            a=d.read(1).astype('float32'); a[(a<0)|(a>1.0001)]=np.nan; rows.append(a)
    land.append(rows)
land=np.array(land)
audit['land']={'types':types,'shape':list(land.shape),'years':[1990,2019],'sum_max':float(np.nanmax(land.sum(1))),'sum_above_1_001':int(np.sum(land.sum(1)>1.001)),'zero_is_not_automatically_missing':True}

# DEM: source is Krasovsky, despite WGS84 description. Transformation may use a
# ballpark datum operation; 0.5-degree grid does not support cadastral precision.
with rio.open(next((RAW/'dataset1').rglob('*.tif'))) as d:
    a=d.read(1).astype('float32'); bad=a==-32768; a[bad]=np.nan
    dem=warp(a,d.transform,d.crs)
    second=warp(a*a,d.transform,d.crs)
    relief=np.sqrt(np.maximum(second-dem*dem,0))
    audit['dem']={'crs':str(d.crs),'metadata_nodata':d.nodata,'masked_sentinel_count':int(bad.sum()),'valid_range_m':[float(np.nanmin(a)),float(np.nanmax(a))],'relief_definition':'within-cell elevation standard deviation; not hydrological slope'}
del a,second,bad

# Exact rectangular spherical overlap for precipitation -> common grid.
f=next(f for f in (RAW/'dataset3').rglob('*.nc') if f.is_file())
prev=os.getcwd(); os.chdir(f.parent); ds=netCDF4.Dataset(f.name); os.chdir(prev)
slon=np.array(ds['longitude'][:]); slat=np.array(ds['latitude'][:])
def overlap_matrix(dst,src,dh,sh,sine=False):
    lo=np.maximum(dst[:,None]-dh,src[None,:]-sh)
    hi=np.minimum(dst[:,None]+dh,src[None,:]+sh)
    v=np.maximum(hi-lo,0)
    if sine: v=np.where(hi>lo,np.sin(np.deg2rad(hi))-np.sin(np.deg2rad(lo)),0)
    return v
wx=overlap_matrix(lon,slon,.25,.125)
wy=overlap_matrix(lat,slat,.25,.125,True)
from scipy.sparse import kron
M=kron(csr_matrix(wy),csr_matrix(wx),format='csr')
first=np.array(ds['pre'][0]).ravel(); srcvalid=np.isfinite(first)&(first>=0)
den=np.asarray(M@srcvalid.astype(float)).ravel()
full=np.asarray(M@np.ones(first.size)).ravel()
coverage=(den/np.maximum(full,1e-30)).reshape(shape)
dates=netCDF4.num2date(ds['time'][:],ds['time'].units)
years=np.array([d.year for d in dates]); pre=[]; rx1=[]; rx5=[]; wet=[]
audit['precip']={'raw_shape':list(ds['pre'].shape),'units':ds['pre'].units,'missing_attr':str(ds['pre'].missing_value),'product':'IDW + PRISM; terrain-conditioned target, not independent causal evidence','annual_days':{}}
for y in range(1990,2023):
    a=np.array(ds['pre'][np.where(years==y)[0]],dtype='float32')
    valid=np.isfinite(a)&(a>=0)
    num=(M@np.where(valid,a,0).reshape(len(a),-1).T).T
    weight=(M@valid.reshape(len(a),-1).astype(float).T).T
    z=np.divide(num,weight,out=np.full(num.shape,np.nan),where=weight>0).reshape(-1,*shape)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        p=np.nansum(z,axis=0); p[np.all(~np.isfinite(z),axis=0)]=np.nan
        pre.append(p); rx1.append(np.nanmax(z,axis=0))
        # Five-day sums within each calendar year; no cross-year rolling windows.
        cs=np.concatenate([np.zeros((1,*shape)),np.cumsum(z,axis=0)])
        rx5.append(np.nanmax(cs[5:]-cs[:-5],axis=0)); wet.append(np.sum(z>=1,axis=0))
    audit['precip']['annual_days'][str(y)]=int(len(a))
    assert len(a)==365+calendar.isleap(y)
    print('precip',y,flush=True)
ds.close(); del a,z,cs,num,weight,valid
pre=np.array(pre); rx1=np.array(rx1); rx5=np.array(rx5); wet=np.array(wet)
mask=(coverage>=.5)&np.isfinite(dem)&np.all(np.isfinite(land),axis=(0,1))&np.isfinite(pre).all(0)
audit['common_support']={'cells':int(mask.sum()),'area_km2':float(area[mask].sum()),'boundary_rule':'precip coverage >=0.5, finite DEM and five cover fractions; analytical support, not administrative boundary','coverage_min':float(coverage[mask].min())}
np.savez_compressed(OUT/'climate_land.npz',lon=lon,lat=lat,area=area,land=land,dem=dem,relief=relief,pre=pre,rx1=rx1,rx5=rx5,wet=wet,mask=mask,coverage=coverage,types=types)
dump()

# Population/GDP count-preserving cell-centre assignment; checked against all
# input values whose centres fall inside the target rectangle (before mask).
socio={}; checks=[]
for dataset,prefix in [(5,'pop'),(6,'gdp')]:
    for year in [1990,2000,2010,2015]:
        f=next((RAW/f'dataset{dataset}').rglob(f'{prefix}{year}.tif'))
        sums=np.zeros(ny*nx); source_sum=0.; all_sum=0.
        with rio.open(f) as d:
            tr=Transformer.from_crs(d.crs,crs,always_xy=True)
            for row in range(0,d.height,256):
                h=min(256,d.height-row); a=d.read(1,window=Window(0,row,d.width,h))
                rr,cc=np.where(np.isfinite(a)&(a>=0)); vals=a[rr,cc].astype(float)
                xx=d.transform.c+(cc+.5)*d.transform.a; yy=d.transform.f+(row+rr+.5)*d.transform.e
                xx,yy=tr.transform(xx,yy)
                jj=np.floor((xx-trans.c)/trans.a).astype(int); ii=np.floor((yy-trans.f)/trans.e).astype(int)
                keep=(ii>=0)&(ii<ny)&(jj>=0)&(jj<nx)
                source_sum+=vals[keep].sum(); all_sum+=vals.sum()
                sums+=np.bincount(ii[keep]*nx+jj[keep],weights=vals[keep],minlength=ny*nx)
        err=abs(sums.sum()-source_sum)/max(source_sum,1)
        assert err<1e-10
        socio[f'{prefix}{year}']=sums.reshape(shape)
        checks.append({'variable':prefix,'year':year,'source_total':all_sum,'source_in_target_extent':source_sum,'aggregated_total':float(sums.sum()),'relative_conservation_error':err,'common_mask_total':float(sums.reshape(shape)[mask].sum())})
        print(prefix,year,'conservation',err,flush=True)
np.savez_compressed(OUT/'socio.npz',**socio)
audit['socio']={'method':'conservative by source-cell centre assignment; no fractional boundary overlap; ~1 km support uncertainty','checks':checks,'GDP_price_basis':'not established: do not interpret nominal GDP growth as real adaptive capacity growth'}
dump()

# Daily files are streamed to annual native-grid means, then average regridded.
temps=[]; days={}
for y in range(1990,2019):
    fs=sorted((RAW/'dataset2').rglob(f'{y}????_avg.tif'))
    assert len(fs)==365+calendar.isleap(y),(y,len(fs))
    total=None; count=None
    for f in fs:
        with rio.open(f) as d:
            a=d.read(1); good=np.isfinite(a)&(a>-100)&(a<70)
            if total is None: total=np.zeros(d.shape,dtype='float64'); count=np.zeros(d.shape,dtype='int32'); st=d.transform; sc=d.crs
            total+=np.where(good,a,0); count+=good
    mean=np.divide(total,count,out=np.full(total.shape,np.nan),where=count>=len(fs)*.95)
    temps.append(warp(mean,st,sc)); days[str(y)]=len(fs)
    print('temperature',y,flush=True)
np.savez_compressed(OUT/'temperature.npz',temperature=np.array(temps))
audit['temperature']={'annual_days':days,'missing_requirement':'native pixel >=95% daily validity before annual mean','units':'degrees C','regrid':'area-overlap average via GDAL; native 0.1-degree cells'}
audit['feature_preparation_completed']=True
dump()
