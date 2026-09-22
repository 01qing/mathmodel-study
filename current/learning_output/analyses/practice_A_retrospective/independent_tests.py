from pathlib import Path
import json, numpy as np
from scipy.integrate import solve_ivp
OUT=Path(__file__).parent
records=[]
def check(name,bug,fixed,expect,scope):
 records.append({'name':name,'first_result':bug,'expected':expect,'first_status':'FAIL' if bug!=expect else 'PASS','retest_result':fixed,'retest_status':'PASS' if fixed==expect else 'FAIL','scope':scope})
# Synthetic identifiers; not the original A workbook or runtime outputs.
routes={'仿真':'PDE','classification':'classifier'}
check('unrecognized-task-must-not-produce-generic-route',routes.get('mechanistic_simulation','generic'),routes.get({'mechanistic_simulation':'仿真'}['mechanistic_simulation'],'UNRESOLVED'),'PDE','schema routing only')
manifest=[{'path':'input.xlsx','role':'raw_data'},{'path':'result7.xlsx','role':'result_template'},{'path':'measured_result.xlsx','role':'raw_data'}]
check('manifest-authority-over-extension-or-name',[x['path'] for x in manifest if x['path'].endswith('.xlsx')],[x['path'] for x in manifest if x['role']=='raw_data'],['input.xlsx','measured_result.xlsx'],'includes measured_result legitimate data; templates excluded by role')
def compatible(a,b,semantic): return a['unit']==b['unit'] and (not semantic or a['denominator']==b['denominator'])
a={'unit':'kg/kg','denominator':'dry-solid'}; b={'unit':'kg/kg','denominator':'dry-air'}
check('equal-unit-string-does-not-imply-common-variable',compatible(a,b,False),compatible(a,b,True),False,'semantic denominator gate; no material parameter inference')
check('printed-decimals-do-not-certify-accuracy',len(f'{1.23456:.4f}'.split('.')[1])==4,2.3e-4<=.5e-4,False,'absolute error budget compared with half output rounding unit')
# New boundary layer function, domain and analytic oracle; not A PDE.
x=np.linspace(0,1,21); g=1-(1-x)**2; probe=np.linspace(0,1,2001); true=np.exp((probe-1)/.015)
eu=float(max(abs(np.interp(probe,x,np.exp((x-1)/.015))-true)))
eg=float(max(abs(np.interp(probe,g,np.exp((g-1)/.015))-true)))
check('boundary-layer-refinement',eu<.04,eg<.04,True,'independent analytic exponential field; interpolation only, not PDE reproduction')
# Same nonuniform mesh: stale constant spacing fails the manufactured linear derivative.
dr=np.diff(g); stale=np.diff(3*g+2)/(g[1]-g[0]); corrected=np.diff(3*g+2)/dr
check('nonuniform-mesh-requires-local-distance',bool(np.max(abs(stale-3))<1e-10),bool(np.max(abs(corrected-3))<1e-10),True,'exact linear gradient oracle on nonuniform mesh')
# Cross-domain PDE: 1D slab Dirichlet heat equation has an analytic sine solution.
errors=[]
for n in [20,40,80]:
 h=1/n; z=np.linspace(0,1,n+1); y=np.sin(np.pi*z[1:-1])
 def rhs(t,u): return np.diff(np.r_[0,u,0],n=2)/h**2
 s=solve_ivp(rhs,[0,.05],y,method='BDF',rtol=1e-9,atol=1e-11)
 errors.append(float(max(abs(s.y[:,-1]-y*np.exp(-np.pi*np.pi*.05)))))
records.append({'name':'new-slab-diffusion-analytic-oracle','status':'PASS' if errors[2]<errors[1]<errors[0] and errors[2]<.0001 else 'FAIL','errors':errors,'scope':'independent linear slab solver convergence; no sorption validation'})
records.append({'name':'boundary-refinement-measurements','uniform_max_error':eu,'graded_max_error':eg,'scope':'synthetic interpolation errors'})
tests=[r for r in records if 'retest_status' in r or 'status' in r]
out={'status':'PASS' if all(r.get('retest_status',r.get('status'))=='PASS' for r in tests) else 'FAIL','tests':records,'core_gain':'NOT_ESTABLISHED','not_core_ablation':True,'scope':'local defect-detection and synthetic mechanism transfer, no new full contest solution'}
(OUT/'INDEPENDENT_TEST_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
