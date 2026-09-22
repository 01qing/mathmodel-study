#!/usr/bin/env python3
# Synthetic mechanism transfer. Not a blind Dev/Test benchmark and not a paper reproduction.
import numpy as np, json
from scipy.optimize import least_squares
rng=np.random.default_rng(20250911)
P=94.25; w=2*np.pi/P

def huber_weights(r,delta=1.5):
    s=np.median(np.abs(r-np.median(r)))+1e-9
    u=np.abs(r)/(delta*1.4826*s+1e-9)
    return np.where(u<=1,1.0,1.0/u)

def fixed_linear_irls(x,y,it=15):
    X=np.c_[np.sin(w*x),np.cos(w*x),np.ones_like(x)]
    wt=np.ones(len(x))
    b=np.zeros(3)
    for _ in range(it):
        sw=np.sqrt(wt); b=np.linalg.lstsq(X*sw[:,None],y*sw,rcond=None)[0]
        wt=huber_weights(y-X@b)
    return X@b

def free_period_robust(x,y):
    def fun(p):
        A,P0,phi,C=p
        return A*np.sin(2*np.pi*x/P0+phi)+C-y
    # reasonable but still more nonlinear degrees of freedom
    p0=[(np.percentile(y,95)-np.percentile(y,5))/2,90,0,np.median(y)]
    z=least_squares(fun,p0,loss='huber',f_scale=1.0,bounds=([0,70,-4*np.pi,-np.inf],[200,120,4*np.pi,np.inf]),max_nfev=250)
    return y+z.fun

def fixed_nonlinear_bad_init(x,y):
    # intentionally represents the first implementation: correct P, but brittle amplitude/phase initialization/local search.
    def fun(p): return p[0]*np.sin(w*x+p[1])+p[2]-y
    z=least_squares(fun,[8,2.8,np.median(y)],loss='huber',f_scale=1.0,bounds=([0,-np.pi,-np.inf],[200,np.pi,np.inf]),max_nfev=22)
    return y+z.fun

def rmse(a,b): return float(np.sqrt(np.mean((a-b)**2)))
rows=[]
for i in range(18):
    x=np.linspace(0,188.5,140)
    A=12+2.3*i; phi=-2.6+0.31*i; C=80+17*i
    clean=A*np.sin(w*x+phi)+C
    y=clean+rng.normal(0,0.28,len(x))
    # sparse gross outliers/missing-like corruption
    ids=rng.choice(len(x),size=8,replace=False); y[ids]+=rng.normal(0,7.5,8)
    pred_free=free_period_robust(x,y)
    pred_bad=fixed_nonlinear_bad_init(x,y)
    pred_fix=fixed_linear_irls(x,y)
    rows.append({'case':i+1,'free_period_robust_rmse':rmse(pred_free,clean),'first_fixed_nonlinear_rmse':rmse(pred_bad,clean),'repaired_fixed_linear_irls_rmse':rmse(pred_fix,clean)})
# Explicit invalid composite-period fixtures for reject mechanism.
reject=[]
for i in range(12):
    x=np.linspace(0,188.5,140); clean=20*np.sin(w*x+0.2*i)+100
    y=clean+9*np.sin(2*np.pi*x/(55+2*i)+0.7)+rng.normal(0,.3,len(x))
    fit=fixed_linear_irls(x,y); e=rmse(fit,y)
    reject.append({'case':i+1,'residual_rmse':e,'reject':bool(e>3.0)})
first_mean=float(np.mean([r['first_fixed_nonlinear_rmse'] for r in rows])); free_mean=float(np.mean([r['free_period_robust_rmse'] for r in rows])); fix_mean=float(np.mean([r['repaired_fixed_linear_irls_rmse'] for r in rows]))
first_fail=first_mean>=free_mean or any(r['first_fixed_nonlinear_rmse']>3 for r in rows)
fix_wins=sum(r['repaired_fixed_linear_irls_rmse']<r['free_period_robust_rmse'] for r in rows)
status='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX' if first_fail and fix_mean<free_mean and fix_wins>=12 and all(r['reject'] for r in reject) else 'FAIL'
out={'scope':'synthetic non-paper mechanism transfer; not Dev/Test and not author reproduction','first_run_status':'FAIL' if first_fail else 'PASS','diagnosis':'fixed physical period was correct, but nonlinear amplitude/phase optimization remained brittle; with known frequency the model can be linearized as a*sin(wx)+b*cos(wx)+C','rule_fix':'solve fixed-frequency sinusoid in a linear basis with robust IRLS, then recover amplitude/phase; retain reject gate','status':status,'summary':{'free_period_robust_mean_clean_rmse':free_mean,'first_fixed_nonlinear_mean_clean_rmse':first_mean,'repaired_fixed_linear_irls_mean_clean_rmse':fix_mean,'repaired_wins_vs_free':fix_wins,'cases':18,'invalid_rejects':sum(r['reject'] for r in reject),'invalid_cases':12},'rows':rows,'reject_fixtures':reject}
print(json.dumps(out,ensure_ascii=False,indent=2))
