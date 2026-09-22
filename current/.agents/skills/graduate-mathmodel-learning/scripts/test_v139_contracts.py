from pathlib import Path
import json,math
import numpy as np
from data_contracts_v139 import require_unique,names_for_classes,comparable_metrics,weighted_spatial_summary,gaussian_2d_ellipse_mass
R=Path(__file__).resolve().parents[4];checks=[];history=[]
def ck(n,c):assert c,n;checks.append(n)
def rejects(n,f):
    try:f()
    except (ValueError,KeyError):checks.append(n);return
    raise AssertionError(n)
panel=[dict(site='A',year=y,cover=c) for y in [2000,2001] for c in ['crop','forest']]
rejects('pseudo-replicated cell-year blocked',lambda:require_unique(panel,['site','year']))
ck('unique entity-year after aggregation',require_unique([dict(site='A',year=y) for y in [2000,2001]],['site','year'])==2)
history.append(dict(first='FAIL_DUPLICATE_CELL_YEAR',diagnosis='cover rows share independent unit',repair='aggregate before calendar window',retest='PASS_CONTRACT_ONLY'))
ck('label order follows actual classes',names_for_classes([1,0],{0:'High',1:'Low'})==['Low','High'])
rejects('unknown class fails',lambda:names_for_classes([2],{0:'High',1:'Low'}))
rejects('duplicate semantic classes fail',lambda:names_for_classes([0,1],{0:'Low',1:'Low'}))
base=dict(target='loss',statistic='importance',units='1',importance_type='gain',normalization='sum1',evaluation_contract='heldout-spatial-v1',run_id='A')
rejects('gain and split weight incomparable',lambda:comparable_metrics(base,{**base,'run_id':'B','importance_type':'weight'}))
ck('same metric different documented run comparable',comparable_metrics(base,{**base,'run_id':'B'}))
rejects('missing provenance fails',lambda:comparable_metrics(base,{**base,'run_id':''}))
x=np.array([[0,0],[2,1],[1,3],[4,2]],float);w=np.array([1,2,3,4.])
a=weighted_spatial_summary(x,w);b=weighted_spatial_summary(x,2*w)
ck('total doubles',b['total_weight']==2*a['total_weight'])
ck('center unchanged under common weight scaling',np.allclose(a['center'],b['center']))
ck('covariance unchanged under common weight scaling',np.allclose(a['covariance'],b['covariance']))
ck('principal axes orthogonal',np.allclose(a['axes'].T@a['axes'],np.eye(2)))
ck('principal frame covariance diagonal',np.allclose(a['axes'].T@a['covariance']@a['axes'],np.diag(a['eigenvalues'])))
rejects('negative weights fail',lambda:weighted_spatial_summary(x,[-1,2,3,4]))
rejects('zero total support fails',lambda:weighted_spatial_summary(x,[0,0,0,0]))
ck('2D unit radius not68percent',abs(gaussian_2d_ellipse_mass(1)-.3934693402873666)<1e-12)
ck('2D calibrated68percent radius',abs(gaussian_2d_ellipse_mass(math.sqrt(-2*math.log(.32)))-.68)<1e-12)
rejects('negative radius fails',lambda:gaussian_2d_ellipse_mass(-1))
history.append(dict(first='FAIL_1D_COVERAGE_ASSUMPTION',diagnosis='wrong dimension',repair='2D radial CDF with declared Gaussian assumption',retest='PASS_CONDITIONAL_MATH_ONLY'))
out=dict(status='PASS',checks=len(checks),names=checks,history=history,scope='local deterministic contracts, not author reproduction or Core gain')
dest=R/'learning_output/validation/v139';dest.mkdir(parents=True,exist_ok=True)
(dest/'contracts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
