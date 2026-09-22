"""Bounded primitive audits. Not a reproduction of the author's full run."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import reproject,Resampling
from sklearn.model_selection import train_test_split,GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'v1.39-work/learning_output/analyses/dev_2024D_presolution/results'
cases=[]
def record(name,first,diagnosis,repair,retest,**evidence):
 assert retest
 cases.append(dict(name=name,first_state='FAIL',first_evidence=first,diagnosis=diagnosis,repair=repair,retest='PASS_MECHANISM_ONLY',evidence=evidence))
df=pd.DataFrame({'longitude':[110.,110.],'latitude':[30.,30.],'Year':[1990,1991],'Rain':[10.,20.]})
terrain=pd.DataFrame({'longitude':[110.]*30,'latitude':[30.]*30,'year':range(1990,2020),'altitude':[100.]*30})
bad=df.merge(terrain,on=['longitude','latitude']);fixed=df.merge(terrain.rename(columns={'year':'Year'}),on=['longitude','latitude','Year'],validate='many_to_one')
record('join_multiplicity_p98',{'input_rows':len(df),'output_rows':len(bad)},'30-year terrain expansion merged without year duplicates each observation30times','include year, validate cardinality; or keep terrain static and unique',len(bad)==60 and len(fixed)==2,repaired_rows=len(fixed))
long=pd.DataFrame({'Region':['A']*15,'Year':np.repeat([2000,2001,2002],5),'Rain':np.repeat([10.,20.,30.],5)})
badroll=long.groupby('Region')['Rain'].transform(lambda x:x.rolling(3,min_periods=1).mean()).iloc[-1]
annual=long.groupby(['Region','Year'],as_index=False)['Rain'].mean();goodroll=annual.groupby('Region')['Rain'].transform(lambda x:x.rolling(3,min_periods=1).mean()).iloc[-1]
record('row_window_not_year_window_p96',float(badroll),'five cover-type rows per year make window3 span rows not3years','aggregate unique Region-Year then calendar-aware rolling',badroll==30 and goodroll==20,repaired_value=float(goodroll))
g=np.repeat(np.arange(1000),5);ids=np.arange(len(g));tr,te=train_test_split(ids,test_size=.3,random_state=42);overlap=len(set(g[tr])&set(g[te]));tr2,te2=next(GroupShuffleSplit(n_splits=1,test_size=.3,random_state=42).split(ids,groups=g))
record('row_split_entity_leakage',overlap,'replicated cell-year rows straddle train/evaluation','split independent cell-year or spatial/temporal blocks',overlap>0 and not(set(g[tr2])&set(g[te2])),fixed_overlap=0)
record('annual_total_not_daily_extreme',{'annual_total_mm':365,'daily_max_mm':1,'annual_gt300':True},'annual accumulation threshold does not identify a daily extreme','declare temporal support; derive daily extreme from daily data',365>300 and 1<300)
rounds=pd.Series([72.47499999,72.97599999]).round(0).tolist()
record('coordinate_contract_p24_p86',rounds,'paper truncation example disagrees with round; integer bins are not0.5degree grids','declare grid edges/resolution and use explicit overlap mapping',rounds==[72.,73.],coordinate_center_offset_degrees=.04)
m,n=10,3;badentropy=np.log(m)/np.log(n);goodentropy=np.log(m)/np.log(m)
record('entropy_sample_axis_p45',float(badentropy),'if m is sample count, normalization by log(n criteria) can exceed1','normalize entropy by log(number of samples)',badentropy>1 and goodentropy==1)
rng=np.random.default_rng(20240920);X=rng.random((4000,3));pseudo=(X.mean(1)>.5).astype(int);external=rng.integers(0,2,len(X));tr,te=train_test_split(np.arange(len(X)),test_size=.3,random_state=42);model=DecisionTreeClassifier(max_depth=8,random_state=42).fit(X[tr],pseudo[tr]);pred=model.predict(X[te]);pa=accuracy_score(pseudo[te],pred);ea=accuracy_score(external[te],pred)
record('synthetic_index_not_external_disaster_truth',{'pseudo_accuracy':float(pa),'independent_random_outcome_accuracy':float(ea)},'high index-label accuracy measures imitation of index, not disaster calibration','retain label provenance and require observed independent outcomes',pa>.85 and .4<ea<.6,scope='synthetic counterexample, not author accuracy')
d=np.load(P/'climate_land.npz');annualtemp=np.load(P/'temperature.npz')['temperature'][0];base=next((R/'official-data/dataset4').rglob('cropland-1990.tif'))
with rasterio.open(base) as dst:dt,dc,shape=dst.transform,dst.crs,dst.shape
f=next((R/'official-data/dataset2').rglob('19900101_avg.tif'))
with rasterio.open(f) as src:
 a=src.read(1);a[a<-100]=np.nan;jan=np.full(shape,np.nan,dtype='float32');reproject(a,jan,src_transform=src.transform,src_crs=src.crs,src_nodata=np.nan,dst_transform=dt,dst_crs=dc,dst_nodata=np.nan,resampling=Resampling.average)
mask=d['mask']&np.isfinite(jan)&np.isfinite(annualtemp);weights=d['area'][mask];jmean=np.average(jan[mask],weights=weights);amean=np.average(annualtemp[mask],weights=weights);mae=np.average(np.abs(jan[mask]-annualtemp[mask]),weights=weights)
record('January1_not_annual_temperature_p85',{'1990_Jan1_area_mean_C':float(jmean),'1990_annual_area_mean_C':float(amean),'spatial_MAE_C':float(mae)},'printed code reads Jan1 then drops date; cannot relabel as annual mean','aggregate all365days before spatial comparison',mae>1,source='official data, frozen annual features; not author merged spreadsheet reproduction')
r68=float(np.sqrt(-2*np.log(1-.68)));cdf1=float(1-np.exp(-.5));cdfsqrt2=float(1-np.exp(-1))
record('ellipse_dimension_coverage_p71',{'Mahalanobis_radius1_mass':cdf1,'radius_sqrt2_mass':cdfsqrt2},'one-dimensional 68percent rule cannot define two-dimensional ellipse coverage','declare ellipse scale and use dimension-specific Gaussian radial CDF or empirical held-out coverage',abs((1-np.exp(-r68*r68/2))-.68)<1e-12,radius_for_68percent=r68,scope='conditional Gaussian math, not measured author ellipse coverage')
points=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
c1=np.cov(points.T,aweights=np.ones(4),ddof=0);c2=np.cov(points.T,aweights=np.ones(4)*2,ddof=0)
record('ellipse_footprint_not_land_area_p67',{'total_weight_first':4,'total_weight_second':8,'same_covariance':bool(np.allclose(c1,c2))},'covariance ellipse area is distribution extent, not total occupied land area','compute total area separately as sum(cell_area*fraction)',np.allclose(c1,c2),scope='counterexample to equating ellipse extent and occupied area')
out={'source':'S013 Dev','status':f'{len(cases)} bounded mechanism checks completed','tests':cases,'full_paper_reproduction':False,'frozen_solution_mutated':False,'retest_scope_note':'PASS confirms named mechanism/correction only; synthetic-index and ellipse tests are counterexamples, not an end-to-end repaired author pipeline'}
(H/'COUNTEREXAMPLE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False),flush=True)
