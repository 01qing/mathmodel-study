"""Visual-only repair after first visual inspection; no model refitting."""
from pathlib import Path
import ast,json,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;O=H/'results';F=H/'figures';hist=H/'history/first_visual_fail';hist.mkdir(exist_ok=True)
for n in ['Q1_precipitation.png','Q1_landcover.png','Q4_regions.png']:
 if not (hist/n).exists():shutil.copy2(F/n,hist/n)
d=np.load(O/'climate_land.npz');lon=d['lon'];lat=d['lat'];mask=d['mask'];ar=d['area'];land=d['land'];P=d['pre']
tree=ast.parse((H/'solve_independent.py').read_text(encoding='utf-8'))
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['mapplot','finish']:exec(compile(ast.Module(body=[node],type_ignores=[]),'plot_helpers','exec'))
def mean(a):return (a[...,mask]*ar[mask]).sum(-1)/ar[mask].sum()
years=np.arange(1990,2021);nat=mean(P[:31]);pcv=np.sqrt(mean((P[:31]-nat[:,None,None])**2))/nat;t=years-years.mean();trend=np.tensordot(t,P[:31],axes=(0,0))/np.dot(t,t)*10
fig,axs=plt.subplots(1,3,figsize=(15,4));axs[0].plot(years,nat);axs[0].set(title='Area-weighted precipitation',xlabel='Year',ylabel='mm/year');mapplot(axs[1],trend,'Precipitation trend, 1990–2020','mm/decade','RdBu');axs[2].plot(years,pcv);axs[2].set(title='Spatial dispersion',xlabel='Year',ylabel='Area-weighted CV');fig.suptitle('Q1 | Official precipitation; fixed common support');fig.tight_layout();finish(fig,'Q1_precipitation.png')
cover=np.array([mean(x) for x in land]);fig,axs=plt.subplots(1,3,figsize=(15,4))
for j,name in enumerate(d['types']):axs[0].plot(np.arange(1990,2020),cover[:,j]*100,label=name)
axs[0].legend(fontsize=7);axs[0].set(title='Observed cover fractions',xlabel='Year',ylabel='Area-weighted %');mapplot(axs[1],(land[-1,1]-land[0,1])*100,'Forest net change, 1990–2019','percentage points','RdBu');mapplot(axs[2],np.abs(land[-1]-land[0]).sum(0)/2,'Half-L1 composition change','fraction; not actual transitions');fig.tight_layout();finish(fig,'Q1_landcover.png')
q=json.loads((O/'RESULT_REGISTRY.json').read_text(encoding='utf-8'))['claims']['Q4'];fig,axs=plt.subplots(1,2,figsize=(12,4));mapplot(axs[0],np.load(O/'Q4_regions.npz')['labels'],'Cover/change prototype regions','region id','tab10');axs[1].plot([r['k'] for r in q['scores']],[r['development_RMSE_fraction'] for r in q['scores']],label='development');axs[1].plot([r['k'] for r in q['scores']],[r['test_RMSE_fraction'] for r in q['scores']],label='spatial test');axs[1].set(xlabel='Number of regions',ylabel='RMSE (fraction units)',title='Spatial reconstruction',xticks=[1,2,3,4,5]);axs[1].legend();fig.tight_layout();finish(fig,'Q4_regions.png')
print('Visual repairs applied; numeric registry untouched')
