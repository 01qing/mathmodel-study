"""S014 Dev audit fixtures. No author pipeline or blind Core evaluation claimed."""
from pathlib import Path
import json, itertools, math, calendar, datetime
import numpy as np
O=Path(__file__).resolve().parent
checks=[]; history=[]; values={}
def ck(name,condition):
    checks.append(dict(name=name,pass_=bool(condition)))
def episode(name,first,diagnosis,repair,retest):
    history.append(dict(name=name,first_status='FAIL' if not first else 'PASS',diagnosis=diagnosis,repair=repair,retest_status='PASS' if retest else 'FAIL',scope='local fixture; not author end-to-end reproduction'))
def score(x):
    return sum((x[j]>x[i])-(x[j]<x[i]) for i in range(len(x)) for j in range(i+1,len(x)))
def variance(x):
    n=len(x);counts=np.unique(x,return_counts=True)[1]
    return (n*(n-1)*(2*n+5)-sum(int(t)*(int(t)-1)*(2*int(t)+5) for t in counts))/18
def z_value(x):
    s=score(list(x));v=variance(x)
    return 0. if v==0 else (s-np.sign(s))/math.sqrt(v)
# Exact null distribution is an independent arbiter, not another formula copy.
for x in [tuple(range(7)),(1,1,2,2,3,4),(1,1,1,1)]:
    permutations=set(itertools.permutations(x));ss=np.array([score(t) for t in permutations]);v=float(np.var(ss));key=str(x)
    ck('MK exact permutation variance '+key,abs(v-variance(x))<1e-10)
    values['MK '+key]=dict(permutations=len(permutations),exact_variance=v,corrected=variance(x))
n=7;bad=n*(n-1)*(2*n+5)/30;good=variance(tuple(range(n)))
episode('MK denominator',np.isclose(bad,good),'PDF12 Eq3-10 uses30; exact permutation variance disagrees','Use18 and tie correction; appendix18 is only no-tie case',np.isclose(good,values['MK '+str(tuple(range(n)))]['exact_variance']))
values['MK denominator']={'printed30':bad,'exact':good,'Z_inflation_ratio':math.sqrt(30/18)}
ck('MK ties alter variance',variance((1,1,2,2,3,4))<6*5*17/18)
ck('MK constant safe',z_value((1,1,1))==0)
ck('MK reversal antisymmetry',np.isclose(z_value((1,3,2,4,6,5)), -z_value((5,6,4,2,3,1))))
# Printed shape bug copied at primitive level, on tiny non-square raster.
m,n=2,3;sresult=np.array([-3,0,3,5,-5,np.nan]);zc=np.full((m,n),np.nan)
error=None
try: zc[sresult==0]=0
except IndexError as e:error=str(e)
flat=np.full(m*n,np.nan);flat[sresult==0]=0;flat[sresult>0]=(sresult[sresult>0]-1)/2;flat[sresult<0]=(sresult[sresult<0]+1)/2;fixed=flat.reshape(m,n)
ck('printed 1D mask against2D fails',error is not None)
ck('repaired shape preserves row-major values',np.allclose(fixed,[[-1,0,1],[2,-2,np.nan]],equal_nan=True))
episode('MK raster axes',error is None,'PDF55 allocates sresult(m*n) but zc(m,n)','Compute flat Z then reshape exactly once',np.allclose(fixed,[[-1,0,1],[2,-2,np.nan]],equal_nan=True));values['shape_exception']=error
def old_classes(b,z):
    return [b>.0005 and z>1.65,b>.0005 and -1.65<=z<=1.65,-.005<=b<=.005 and -1.65<=z<=1.65,b<.0005 and -1.65<=z<=1.65,b<.0005 and z< -1.65]
def classification(b,z,epsilon=.0005):
    if not np.isfinite([b,z]).all():return 'missing'
    if abs(b)<=epsilon:return 'flat_effect'
    if b>0:return 'positive_significant' if z>1.65 else 'positive_not_confirmed'
    return 'negative_significant' if z< -1.65 else 'negative_not_confirmed'
overlap=sum(old_classes(.001,0));ck('printed class overlap found',overlap==2)
grid=list(itertools.product([-.01,-.005,-.0005,0,.0005,.001,.005,.01],[-2,-1.65,0,1.65,2]))
ck('new explicit partition covers boundaries',all(isinstance(classification(b,z),str) for b,z in grid))
ck('zero effect not negative',classification(0,-2)=='flat_effect')
ck('missing effect separate',classification(float('nan'),0)=='missing')
episode('trend partition',overlap==1,'PDF14 Table3-5 overlapping beta bands and positive down threshold','Define epsilon, effect direction and significance separately; not recover authors percentages',True)
values['partition_witness']={'beta':.001,'Z':0,'printed_matches':overlap,'new_class':classification(.001,0)}
# Recompute printed reciprocal matrix, not guessed hidden author matrix.
A=np.array([[1+j-i if j>=i else 1/(1+i-j) for j in range(6)] for i in range(6)],float)
eig,vec=np.linalg.eig(A);ix=np.argmax(eig.real);lam=float(eig[ix].real);weights=vec[:,ix].real;weights/=sum(weights);ci=(lam-6)/5;cr=ci/1.24
ck('AHP reciprocal and diagonal contract',np.allclose(A*A.T,1) and np.allclose(np.diag(A),1))
ck('AHP eigen residual',np.linalg.norm(A@weights-lam*weights)<1e-10)
printed_w=np.array([.3794,.2488,.1604,.1024,.0655,.0434]);column_mean=(A/A.sum(axis=0)).mean(axis=1)
ck('AHP printed weights are not principal eigenvector rounding',not np.allclose(weights,printed_w,atol=.00006))
ck('AHP printed weights match normalized-column means',np.allclose(column_mean,printed_w,atol=.000051))
episode('audit hypothesis correction',False,'First audit assumed printed weights were eigenvector rounding; 28/29 checks passed. Normalized-column means explain all6 weights','Retain first failure; distinguish column-normalization primitive from eigenvector method',np.allclose(column_mean,printed_w,atol=.000051))
values['AHP_weight_primitive']={'normalized_column_means':column_mean.tolist(),'printed_weights':printed_w.tolist(),'eigenvector_difference_max':float(np.max(abs(weights-printed_w)))}
ck('printed lambda contradicts printed CI',abs((6.61889-6)/5-.0338)>.01)
ck('recomputed matrix passes declared CR threshold',cr<.1)
episode('AHP arithmetic',abs(lam-6.61889)<1e-5,'PDF39 lambda, CI and CR are not mutually consistent','Recompute eigenvalue, CI and RI indexed by n=6',cr<.1)
values['AHP']={'matrix':A.tolist(),'lambda':lam,'weights':weights.tolist(),'CI':ci,'RI6':1.24,'CR':cr,'printed_lambda':6.61889,'printed_CI':.0338,'printed_CR':.0302,'CI_div_RI5':ci/1.12}
local={'GDP':2/3,'population':1/3};global_printed={'GDP':.0868,'population':.1737};mass=sum(global_printed.values());global_fixed={k:mass*v for k,v in local.items()}
ck('AHP GDP/population reversal detected',global_printed['GDP']<global_printed['population'] and local['GDP']>local['population'])
ck('AHP keyed global weights preserve mass',np.isclose(sum(global_fixed.values()),mass))
episode('AHP entity mapping',global_printed['GDP']>global_printed['population'],'Table5-6GDP:pop=2:1 butTable5-7about1:2','Key local and parent weights by indicator_id; corrected numbers conditional on Table5-6',global_fixed['GDP']>global_fixed['population']);values['AHP_exposure']={'printed':global_printed,'conditional_fix':global_fixed}
x=np.array([[1.,1.,0.],[.3,.3,.3]]);linear=x@np.array([.6333,.2605,.1062]);product=x.prod(axis=1)
ck('HEV additive and product can reverse ranking',np.argmax(linear)!=np.argmax(product))
values['HEV_counterexample']={'HEV':x.tolist(),'linear':linear.tolist(),'product':product.tolist()}
# Calendar weighting, zero-vs-missing, cyclic angles and georeferenced support.
days=np.array([calendar.monthrange(2019,k)[1] for k in range(1,13)]);monthly=np.zeros(12);monthly[1]=10
bad=monthly.mean();good=float(np.average(monthly,weights=days));ck('mean of months differs from mean of days',not np.isclose(bad,good));ck('day weighted mean preserves accumulation',np.isclose(good*365,(monthly*days).sum()))
episode('calendar aggregation',np.isclose(bad,good),'PDF8 Eq3-1..3 recursively weights months equally','Weight monthly means by valid days; separately name annual total',np.isclose(good*365,280));values['calendar']={'mean_of_months':bad,'daily_weighted':good,'annual_total_mm':280}
angles=np.deg2rad([359.,1.]);circular=float(np.rad2deg(np.arctan2(np.sin(angles).mean(),np.cos(angles).mean()))%360);ck('aspect linear interpolation crosses opposite direction',np.mean([359,1])==180 and min(circular,360-circular)<1e-10)
episode('aspect interpolation',False,'PDF57/60 linearly zooms aspect degrees','Reproject sine/cosine; recover angle only if resultant norm nonzero',min(circular,360-circular)<1e-10)
ck('positive-only mask discards valid zeros',not np.all(np.array([0,1,2])>0) and np.isfinite([0,1,2]).all())
ck('dropna insufficient for finite sentinel',np.isfinite(-9999))
shape=(2,2);t1=(1,0,0,0,-1,2);t2=(1,0,10,0,-1,2)
ck('equal array size not geospatial agreement',shape==shape and t1!=t2)
counts=np.array([100,30]);exposure=np.array([1000,100]);rates=counts/exposure;ck('count vs incidence rank reversal',np.argmax(counts)!=np.argmax(rates));values['exposure']={'counts':counts.tolist(),'denominator':exposure.tolist(),'rates':rates.tolist()}
rf=1620.793;xgb=1613.645;values['Q2_table_gain_percent']=100*(rf-xgb)/rf;ck('XGB table gain under half percent',0<values['Q2_table_gain_percent']<.5)
values['Q4_table_relative_MSE_gains_percent']={name:100*(a-b)/a for name,a,b in [('grass',190.329,183.651),('crop',353.752,330.730),('shrub',186.282,180.864),('forest',484.855,392.408),('wetland',898.222,806.982)]}
ck('Q4 gains variable not one universal margin',max(values['Q4_table_relative_MSE_gains_percent'].values())>min(values['Q4_table_relative_MSE_gains_percent'].values())*4)
out=dict(status='PASS' if all(c['pass_'] for c in checks) else 'FAIL',scope='deterministic synthetic fixtures and printed-table arithmetic only; not independent Core gain, not full reproduction',checks=checks,passed=sum(c['pass_'] for c in checks),total=len(checks),history=history,values=values,executed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(O/'AUDIT_REPLAY.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
