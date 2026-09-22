"""Four-question independent analysis. No solution corpus retrieval."""
from pathlib import Path
import json,os,time,hashlib,warnings
os.environ['OMP_NUM_THREADS']='2'
import numpy as np
import pandas as pd
from scipy.stats import rankdata,spearmanr
from sklearn.preprocessing import SplineTransformer,StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from threadpoolctl import threadpool_limits
threadpool_limits(limits=2)
H=Path(__file__).resolve().parent; O=H/'results'; F=H/'figures'; F.mkdir(exist_ok=True)
d=np.load(O/'climate_land.npz'); s=np.load(O/'socio.npz'); temp=np.load(O/'temperature.npz')['temperature']
lon,lat=d['lon'],d['lat']; xx,yy=np.meshgrid(lon,lat); mask=d['mask']; ar=d['area']; land=d['land']; P=d['pre']; rx=d['rx1']; elev=d['dem']; relief=d['relief']
reg={'status':'INDEPENDENT_COMPUTATION','seed':20240920,'claims':{},'limits':['No disaster labels or drainage capacities supplied','No causal identification: precipitation product already terrain-adjusted','No Core ablation','Absolute historical pristine status unverified','2020 land cover not observed','Scenario maps are not validated disaster forecasts']}
def save(): (O/'RESULT_REGISTRY.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
def mean(a,m=mask): return np.sum(a[...,m]*ar[m],axis=-1)/ar[m].sum()
def slope(a,years):
    t=np.asarray(years,dtype=float); t-=t.mean();return np.tensordot(t,a,axes=(0,0))/np.dot(t,t)
def mapplot(ax,a,title,label,cmap='viridis'):
    from matplotlib.colors import ListedColormap,BoundaryNorm
    z=np.where(mask,a,np.nan); kw={};ticks=None
    if cmap=='RdBu':
        limit=float(np.nanmax(np.abs(z)));kw={'vmin':-limit,'vmax':limit}
    elif cmap=='tab10':
        k=int(np.nanmax(z)); cmap=ListedColormap(plt.get_cmap('tab10').colors[:k]);kw={'norm':BoundaryNorm(np.arange(.5,k+1.5),k)};ticks=np.arange(1,k+1)
    im=ax.pcolormesh(lon,lat,z,shading='nearest',cmap=cmap,**kw);ax.set(xlabel='Longitude (degrees E)',ylabel='Latitude (degrees N)',title=title);ax.set_aspect(1.2);plt.colorbar(im,ax=ax,label=label,shrink=.8,ticks=ticks)
def finish(fig,name):fig.savefig(F/name,dpi=160,bbox_inches='tight');plt.close(fig)

# Q1: descriptive outputs only, fixed observed intervals.
years=np.arange(1990,2021); nat=mean(P[:31]); pcv=np.sqrt(mean((P[:31]-nat[:,None,None])**2))/nat
cover=np.array([mean(x) for x in land]); trend=slope(P[:31],years)*10
pd.DataFrame({'year':years,'annual_precip_mm':nat,'spatial_CV':pcv}).to_csv(O/'Q1_precipitation.csv',index=False)
pd.DataFrame(cover,index=np.arange(1990,2020),columns=d['types']).rename_axis('year').to_csv(O/'Q1_cover_fraction.csv')
reg['claims']['Q1']={'support_cells':int(mask.sum()),'support_area_km2':float(ar[mask].sum()),'mean_annual_precip_1990_2020_mm':float(nat.mean()),'national_precip_trend_mm_decade':float(slope(nat,years)*10),'first_last_precip_mm':[float(nat[0]),float(nat[-1])],'land_net_percentage_points_1990_2019':dict(zip(d['types'].tolist(),((cover[-1]-cover[0])*100).tolist())),'observed_cover_end':2019,'area_note':'whole target cells meeting >=50% precipitation coverage; approximate analysis support'}
fig,axs=plt.subplots(1,3,figsize=(15,4));axs[0].plot(years,nat);axs[0].set(title='Area-weighted precipitation',xlabel='Year',ylabel='mm/year');mapplot(axs[1],trend,'Precipitation trend, 1990–2020','mm/decade','RdBu');axs[2].plot(years,pcv);axs[2].set(title='Spatial dispersion',xlabel='Year',ylabel='Area-weighted CV');fig.suptitle('Q1 | Official precipitation; fixed common support');fig.tight_layout();finish(fig,'Q1_precipitation.png')
fig,axs=plt.subplots(1,3,figsize=(15,4));
for j,name in enumerate(d['types']):axs[0].plot(np.arange(1990,2020),cover[:,j]*100,label=name)
axs[0].legend(fontsize=7);axs[0].set(title='Observed cover fractions',xlabel='Year',ylabel='Area-weighted %')
mapplot(axs[1],(land[-1,1]-land[0,1])*100,'Forest net change, 1990–2019','percentage points','RdBu')
mapplot(axs[2],np.abs(land[-1]-land[0]).sum(0)/2,'Half-L1 composition change','fraction; not actual transitions');fig.tight_layout();finish(fig,'Q1_landcover.png')

# Q2: temporal holdout and spatial transfer. No final-year tuning.
m=mask&np.all(np.isfinite(temp),0)&np.isfinite(relief)
cell=np.where(m.ravel())[0]; n=len(cell); groups=((np.floor(xx[m]/5)+37*np.floor(yy[m]/5))%5).astype(int)
yrs=np.arange(1990,2019); T=temp[:,m]; Y=rx[:29,m]
static=np.stack([xx[m],yy[m],elev[m]/1000,relief[m]/1000],1)
X=np.concatenate([np.broadcast_to(static,(29,n,4)),T[:,:,None],np.broadcast_to((yrs-1990)[:,None,None],(29,n,1))],2)
def features(a,interaction=False):
    if interaction:return np.column_stack([a,a[:,2]*a[:,4],a[:,3]*a[:,4]])
    return a
def model(name):
    if name=='boosting':return HistGradientBoostingRegressor(max_iter=60,max_leaf_nodes=15,min_samples_leaf=80,l2_regularization=10,random_state=20240920)
    return make_pipeline(SplineTransformer(n_knots=4,degree=2),StandardScaler(),Ridge(alpha=10))
names=['climatology','additive','interaction','boosting']
records=[]; preds={}; trained={}
for name in names:
    if name=='climatology': pred=np.broadcast_to(Y[:16].mean(0),Y[16:].shape)
    else:
        mod=model(name); mod.fit(features(X[:16].reshape(-1,6),name=='interaction'),Y[:16].ravel());pred=mod.predict(features(X[16:].reshape(-1,6),name=='interaction')).reshape(13,n);trained[name]=mod
    preds[name]=pred
    records.append({'model':name,'validation_MAE_mm':float(np.abs(pred[:5]-Y[16:21]).mean())})
    print('Q2 temporal validation',records[-1],flush=True)
# Spatial folds: baseline is global climatology because held cells unavailable.
fold_scores={name:[] for name in names}
for fold in range(5):
    tr=groups!=fold; va=groups==fold
    for name in names:
        if name=='climatology': pred=np.full((5,va.sum()),Y[:16,tr].mean())
        else:
            mod=model(name);mod.fit(features(X[:16,tr].reshape(-1,6),name=='interaction'),Y[:16,tr].ravel());pred=mod.predict(features(X[16:21,va].reshape(-1,6),name=='interaction')).reshape(5,-1)
        fold_scores[name].append(float(np.abs(pred-Y[16:21,va]).mean()))
    print('Q2 spatial fold',fold,flush=True)
lookup={r['model']:r for r in records}; base=lookup['climatology']['validation_MAE_mm']
eligible=[]
for name in names:
    gain=1-lookup[name]['validation_MAE_mm']/base
    wins=sum(a<b for a,b in zip(fold_scores[name],fold_scores['climatology']))
    lookup[name].update(spatial_MAE_mm=fold_scores[name],validation_gain_vs_climatology=gain,spatial_wins=wins)
    if name!='climatology' and gain>=.05 and wins>=4:eligible.append(name)
selected=min(eligible,key=lambda k:lookup[k]['validation_MAE_mm']) if eligible else 'climatology'
# Decision persisted before reporting final holdout. Protocol fixed complexity gate.
(O/'Q2_SELECTION_BEFORE_FINAL.json').write_text(json.dumps({'selected':selected,'validation_only':records},indent=2))
for name in names:
    error=preds[name][5:]-Y[21:];lookup[name]['final_MAE_mm']=float(np.abs(error).mean());lookup[name]['final_RMSE_mm']=float(np.sqrt((error**2).mean()))
reg['claims']['Q2']={'selected':selected,'cells':n,'target':'annual Rx1day of daily area-averaged 0.5-degree precipitation','train_years':[1990,2005],'validation_years':[2006,2010],'final_years':[2011,2018],'models':records,'causal_effect':'NOT_IDENTIFIED','temporal_and_spatial_baselines_differ':'temporal uses training climatology per seen cell; spatial uses global training mean for unseen cells'}
pd.DataFrame([{k:v for k,v in r.items() if k!='spatial_MAE_mm'} for r in records]).to_csv(O/'Q2_model_scores.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(11,4));axs[0].bar(names,[lookup[x]['validation_MAE_mm'] for x in names]);axs[0].set(title='Development years 2006–2010',ylabel='MAE (mm)',xlabel='Model');axs[1].bar(names,[lookup[x]['final_MAE_mm'] for x in names]);axs[1].set(title='Frozen final years 2011–2018',ylabel='MAE (mm)',xlabel='Model');fig.tight_layout();finish(fig,'Q2_validation.png');save()

# Q3: retrospective extrapolation checks and mechanistic scenarios, no labels.
back=[]
for end in [2004,2009,2014]:
    a=rx[:end-1990+1]; fit=a[-10:]; recent=fit.mean(0); sl=slope(fit,np.arange(end-9,end+1))
    target=rx[end-1990+1:end-1990+6].mean(0)
    predict=np.maximum(recent+sl*7.5,0) # centroid of fitting window=end-4.5; target=end+3
    back.append({'fit_end':end,'target_years':[end+1,end+5],'persistence_MAE_mm':float(mean(np.abs(recent-target))),'linear_MAE_mm':float(mean(np.abs(predict-target)))})
trend_supported=sum(b['linear_MAE_mm']<b['persistence_MAE_mm'] for b in back)>=2
central='trend' if trend_supported else 'no_trend'
recent=rx[-10:].mean(0); sl=slope(rx[-10:],np.arange(2013,2023)); L0=land[-1]; ls=slope(land[-10:],np.arange(2010,2020))
pop=s['pop2015']; gdp=s['gdp2015']; density=pop/ar
rank=lambda a: np.where(mask,np.nan,0) # assigned below, preserve common mask
def percentile(a):
    z=np.full(mask.shape,np.nan);z[mask]=rankdata(a[mask],method='average')/mask.sum();return z
# Adaptive-capacity proxy is GDP/person, fixed 2015, no measured drainage claim.
percap=np.divide(gdp,pop,out=np.zeros(mask.shape),where=pop>0)
exposure=percentile(np.log1p(density)); capacity=percentile(np.log1p(percap))
terrain=1+.25*percentile(relief)+.25*(1-percentile(elev))
coeff_sets=[np.array([.35,.15,.20,.20,.25]),np.array([.50,.25,.30,.30,.40]),np.array([.65,.35,.45,.40,.55])]
scenario_outputs={}; q3rows=[]; robustness=[]
for year in [2025,2030,2035]:
    maps=[]; descriptions=[]
    for climate in ['no_trend','trend']:
      rainfall=recent if climate=='no_trend' else np.clip(recent+sl*(year-2017.5),.5*recent,1.5*recent)
      for cover_trend in [False,True]:
        L=L0.copy() if not cover_trend else np.clip(L0+ls*(year-2019),0,1)
        L=L/np.maximum(L.sum(0),1)[None,:,:]
        residual=np.maximum(1-L.sum(0),0)
        for ci,coef in enumerate(coeff_sets):
          C=np.tensordot(coef,L,axes=(0,0))+residual*.35
          for K in [25.,50.,100.]:
            pressure=rainfall*C*terrain/K
            # Relative index, not probability. Terrain multipliers are scenarios.
            score=pressure*(.25+.75*exposure)/( .5+.5*capacity)
            maps.append(score);descriptions.append((climate,cover_trend,ci,K))
    arr=np.array(maps); central_i=descriptions.index((central,False,1,50.))
    score=arr[central_i]; top=np.array([a>=np.nanquantile(a[mask],.9) for a in arr]); freq=top.mean(0)
    scenario_outputs[f'score{year}']=score;scenario_outputs[f'top_decile_frequency{year}']=freq
    threshold=score>=np.nanquantile(score[mask],.9)
    q3rows.append({'year':year,'scenarios':len(maps),'central_climate':central,'top_decile_population_2015':float(pop[mask&threshold].sum()),'robust_top_decile_cells_at_least_80pct':int(np.sum(mask&(freq>=.8)))})
    for k in np.argsort(np.where(mask,score,-np.inf).ravel())[-20:][::-1]:
        r,c=np.unravel_index(k,mask.shape);robustness.append({'year':year,'longitude':lon[c],'latitude':lat[r],'relative_score':float(score[r,c]),'top_decile_scenario_frequency':float(freq[r,c])})
np.savez_compressed(O/'Q3_scenarios.npz',**scenario_outputs)
pd.DataFrame(robustness).to_csv(O/'Q3_top_cells.csv',index=False)
reg['claims']['Q3']={'backtests':back,'central_climate':central,'scenarios':q3rows,'critical_condition':'Pcrit=K/[C(L)*terrain_multiplier], assumed K=25/50/100 mm/day; not calibrated disaster threshold','coefficient_sets':[a.tolist() for a in coeff_sets],'residual_cover_coefficient':.35,'socio_year':2015,'index':'[P*C*terrain/K]*(0.25+0.75*population_density_percentile)/(0.5+0.5*GDP_per_person_percentile)','terrain_multiplier':'1+0.25*relief_percentile+0.25*(1-elevation_percentile), assumed, not derived hydrology','projection_contract':'2013–2022 Rx1 mean and OLS slope; no-trend versus bounded 0.5–1.5x trend; 2010–2019 cover trend clipped and normalized; socio fixed','validated_disaster_probability':'NOT_ESTABLISHED'}
fig,axs=plt.subplots(2,3,figsize=(15,8))
for j,y in enumerate([2025,2030,2035]):
    mapplot(axs[0,j],scenario_outputs[f'score{y}'],f'{y} relative scenario index','unitless index')
    mapplot(axs[1,j],scenario_outputs[f'top_decile_frequency{y}'],f'{y} top-decile robustness','fraction of 36 scenarios')
fig.suptitle('Q3 | Conditional scenarios; not calibrated disaster forecasts; 2015 socioeconomics');fig.tight_layout();finish(fig,'Q3_scenario_maps.png');save()

# Q4: geographic holdout selects representation complexity; independent test fold.
g=((np.floor(xx[mask]/5)+37*np.floor(yy[mask]/5))%5).astype(int)
Z=np.concatenate([land[:21].mean(0)[:,mask].T,(land[20]-land[0])[:,mask].T],axis=1)
train=g>=2;val=g==0;test=g==1
q4=[]; mods={}
global_mean=Z[train].mean(0)
for k in [1,2,3,4,5]:
    km=KMeans(n_clusters=k,n_init=10,random_state=20240920).fit(Z[train]);mods[k]=km
    prediction=km.cluster_centers_[km.predict(Z[val])]
    q4.append({'k':k,'development_RMSE_fraction':float(np.sqrt(np.mean((Z[val]-prediction)**2)))})
best=min(r['development_RMSE_fraction'] for r in q4 if r['k']>1)
chosen=min(r['k'] for r in q4 if r['development_RMSE_fraction']<=1.10*best)
for r in q4:
    km=mods[r['k']];prediction=km.cluster_centers_[km.predict(Z[test])];r['test_RMSE_fraction']=float(np.sqrt(np.mean((Z[test]-prediction)**2)))
km=mods[chosen];labels=km.predict(Z);pcs=PCA(n_components=2).fit(Z[train]);recon=pcs.inverse_transform(pcs.transform(Z[test]))
Zlate=np.concatenate([land[9:].mean(0)[:,mask].T,(land[-1]-land[9])[:,mask].T],axis=1)
stability=adjusted_rand_score(labels,km.predict(Zlate))
reg['claims']['Q4']={'selected_k':chosen,'selection':'smallest K within 10% of best development RMSE, before test evaluation','features':'five 1990–2010 mean fractions and five 1990–2010 net changes, unscaled fraction units','split':'5-degree blocks: train folds2/3/4, development0, final1','scores':q4,'PCA2_explained_variance':pcs.explained_variance_ratio_.tolist(),'PCA2_test_RMSE_fraction':float(np.sqrt(np.mean((Z[test]-recon)**2))),'window_shift_ARI':float(stability),'centroids':km.cluster_centers_.tolist(),'usefulness':'region prototypes compress composition/change; no external policy utility or causal validation'}
labelmap=np.full(mask.shape,np.nan);labelmap[mask]=labels+1
np.savez_compressed(O/'Q4_regions.npz',labels=labelmap,centroids=km.cluster_centers_)
fig,axs=plt.subplots(1,2,figsize=(12,4));mapplot(axs[0],labelmap,'Cover/change prototype regions','region id','tab10');axs[1].plot([r['k'] for r in q4],[r['development_RMSE_fraction'] for r in q4],label='development');axs[1].plot([r['k'] for r in q4],[r['test_RMSE_fraction'] for r in q4],label='spatial test');axs[1].set(xlabel='Number of regions',ylabel='RMSE (fraction units)',title='Spatial reconstruction');axs[1].legend();fig.tight_layout();finish(fig,'Q4_regions.png')
save();print('INDEPENDENT NUMERICAL RUN COMPLETE',flush=True)
