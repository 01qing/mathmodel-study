"""Q1 effective-concentration baseline, not a calibrated sorption model."""
from pathlib import Path
import json, csv, hashlib, time, sys, platform
import numpy as np
from scipy.integrate import solve_ivp, trapezoid
from scipy.sparse import diags, block_diag
from scipy.special import j0,j1
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[3]; O=R/'paper_output'
for d in ['results','tables','figures','data_cleaned']: (O/d).mkdir(exist_ok=True)
def writej(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def grid(n):
 r=.02*(1-(1-np.linspace(0,1,n+1))**2); faces=np.r_[0,(r[1:]+r[:-1])/2,.02]
 return r,faces,np.diff(faces**2)/2
def solve(n,env,rtol=1e-8,constant=False):
 r,f,v=grid(n); m=n+1; dr=np.diff(r)
 def rhs(t,y):
  T,C=y[:m],y[m:]; Ta,Ca=(50.,.05) if constant else (np.interp(t,env[:,0],env[:,1]),np.interp(t,env[:,0],env[:,2]))
  D=7e-9*np.exp(-.89/np.maximum(C,1e-10)); df=2*D[1:]*D[:-1]/(D[1:]+D[:-1])
  qt=np.r_[0,f[1:-1]*.36*np.diff(T)/dr,.02*25*(Ta-T[-1])]
  qc=np.r_[0,f[1:-1]*df*np.diff(C)/dr,.02*8e-7*(Ca-C[-1])]
  return np.r_[np.diff(qt)/v/(820*2600),np.diff(qc)/v]
 spars=block_diag([diags([np.ones(m-1),np.ones(m),np.ones(m-1)],[-1,0,1])]*2).tocsc()
 sol=solve_ivp(rhs,(0,1800),np.r_[np.full(m,28.),np.full(m,2.55)],method='BDF',t_eval=np.arange(1801),rtol=rtol,atol=rtol*.01,jac_sparsity=spars,max_step=10)
 if not sol.success: raise RuntimeError(sol.message)
 return sol,r,v
def savecsv(path,rows):
 with path.open('w',newline='',encoding='utf-8-sig') as f: csv.writer(f).writerows(rows)
def main():
 t0=time.time()
 env=np.loadtxt(O/'data_cleaned/environment.csv',delimiter=',',skiprows=1,encoding='utf-8-sig')
 assert np.isfinite(env).all() and np.all(np.diff(env[:,0])>0)
 savecsv(O/'data_cleaned/environment.csv',[['time_s','temperature_C','effective_boundary_concentration_kgkg'],*env.tolist()])
 outputs={}; raw={}
 for n in [40,80,160]:
  s,r,v=solve(n,env); m=len(r); raw[n]=(s,r,v)
  targets=np.arange(21)*.001
  outputs[n]=np.array([[np.interp(targets,r,s.y[j*m:(j+1)*m,k]) for k in range(1801)] for j in [0,1]])
 fine=outputs[160]; comp={}
 for a,b in [(40,80),(80,160)]:
  diff=np.abs(outputs[a]-outputs[b]); comp[f'{a}_vs_{b}']={'max_T_C':float(diff[0].max()),'max_C_kgkg':float(diff[1].max())}
 s,r,v=raw[160]; tight,_,_=solve(160,env,rtol=1e-9)
 temporal={'max_T_C':float(np.max(abs(s.y[:161]-tight.y[:161]))),'max_C_kgkg':float(np.max(abs(s.y[161:]-tight.y[161:])))}
 # Independent analytical constant-ambient Robin cylinder heat solution.
 test,rr,_=solve(80,env,constant=True); Bi=25*.02/.36
 fun=lambda z:z*j1(z)-Bi*j0(z)
 xs=np.linspace(.00001,120,10000); roots=[]
 for a,b in zip(xs[:-1],xs[1:]):
  if fun(a)*fun(b)<0: roots.append(brentq(fun,a,b))
 exact=np.zeros(len(rr)); Fo=.36/(820*2600)*1800/.02**2
 for z in roots:
  A=2*j1(z)/(z*(j0(z)**2+j1(z)**2)); exact+=A*j0(z*rr/.02)*np.exp(-z*z*Fo)
 exact=50+(28-50)*exact
 analytic_error=float(max(abs(test.y[:81,-1]-exact)))
 # Independently quadrature-integrated boundary flux vs state inventory.
 T,C=s.y[:161],s.y[161:]; ta=np.interp(s.t,env[:,0],env[:,1]); ca=np.interp(s.t,env[:,0],env[:,2])
 heat_change=float(np.dot(v,T[:,-1]-28)*820*2600); heat_flux=float(trapezoid(.02*25*(ta-T[-1]),s.t))
 mass_change=float(np.dot(v,C[:,-1]-2.55)); mass_flux=float(trapezoid(.02*8e-7*(ca-C[-1]),s.t))
 balance={'heat_relative_residual':abs(heat_change-heat_flux)/max(abs(heat_change),1e-15),'effective_moisture_relative_residual':abs(mass_change-mass_flux)/max(abs(mass_change),1e-15),'meaning':'effective-concentration inventory; not calibrated physical water mass'}
 for j,name in enumerate(['temperature','moisture']):
  savecsv(O/f'tables/q1_{name}_full.csv',[['time_s',*list(np.round(np.arange(21)*.1,1))],*[[t,*fine[j,t].tolist()] for t in range(1,1801)]])
  savecsv(O/f'tables/q1_{name}_requested.csv',[['time_s','r0cm','r0.5cm','r1cm','r1.5cm','r2cm'],*[[t,*[f'{x:.4f}' for x in fine[j,t,::5]]] for t in [100,300,600,900,1200,1500,1800]]])
 fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
 for j,ax in enumerate(axs):
  for t in [100,600,1200,1800]: ax.plot(np.arange(21)*.1,fine[j,t],label=f'{t} s')
  ax.set(xlabel='Radius (cm)',ylabel=['Temperature (deg C)','Dry-basis moisture (kg/kg)'][j],title=['Q1 temperature','Q1 effective moisture model'][j]); ax.legend(); ax.grid(alpha=.25)
 fig.savefig(O/'figures/q1_profiles.png',dpi=170); plt.close(fig)
 metrics={'question_id':'Q1','status':'NUMERICAL_BASELINE_ONLY','grid_comparison':comp,'time_tolerance_comparison':temporal,'analytic_robin_heat_max_error_C':analytic_error,'balance':balance,'minimum_moisture':float(C.min()),'finite':bool(np.isfinite(s.y).all()),'at_1800s':{'T_center_C':float(fine[0,-1,0]),'T_surface_C':float(fine[0,-1,-1]),'C_center_kgkg':float(fine[1,-1,0]),'C_surface_kgkg':float(fine[1,-1,-1])},'validation_thresholds':{'grid_T_C':.01,'grid_C_kgkg':.001,'analytic_T_C':.005,'balance_relative':.001},'four_decimal_accuracy_established':False,'physical_accuracy_established':False,'Q2_Q3_Q4':'NOT_RUN','elapsed_s':time.time()-t0}
 metrics['numerical_checks_pass']=bool(comp['80_vs_160']['max_T_C']<.01 and comp['80_vs_160']['max_C_kgkg']<.001 and analytic_error<.005 and balance['heat_relative_residual']<.001 and balance['effective_moisture_relative_residual']<.001 and metrics['finite'] and metrics['minimum_moisture']>=0)
 writej(O/'results/q1_baseline_metrics.json',metrics)
 def rec(p):return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 writej(O/'results/q1_run_manifest.json',{'scope':'Q1 only; not official complete workflow run','exit_code':0,'python':sys.version,'platform':platform.platform(),'code':rec(Path(__file__)),'inputs':[rec(R/'problem_files/附件1.xlsx')],'outputs':[rec(p) for p in [O/'results/q1_baseline_metrics.json',O/'figures/q1_profiles.png',*list((O/'tables').glob('q1*.csv'))]]})
 print(json.dumps(metrics,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
