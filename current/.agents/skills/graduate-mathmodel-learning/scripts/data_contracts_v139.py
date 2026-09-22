"""Small data-contract guards. They do not validate scientific claims or model quality."""
import math
import numpy as np

def require_unique(rows,keys):
    seen=set()
    for row in rows:
        key=tuple(row[k] for k in keys)
        if key in seen:raise ValueError('duplicate independent entity/time key')
        seen.add(key)
    return len(seen)

def names_for_classes(classes,decoder):
    result=[decoder[c] for c in classes]
    if len(set(result))!=len(result):raise ValueError('non-bijective class names')
    return result

def comparable_metrics(a,b):
    fields=('target','statistic','units','importance_type','normalization','evaluation_contract')
    if any(k not in a or k not in b for k in fields):raise ValueError('missing metric identity')
    if not a.get('run_id') or not b.get('run_id'):raise ValueError('missing run provenance')
    if any(a[k]!=b[k] for k in fields):raise ValueError('noncomparable metric contracts')
    return True

def weighted_spatial_summary(points,weights):
    x=np.asarray(points,dtype=float);w=np.asarray(weights,dtype=float)
    if x.ndim!=2 or x.shape[1]!=2 or len(x)!=len(w):raise ValueError('need Nx2 points and N weights')
    if not np.isfinite(x).all() or not np.isfinite(w).all() or (w<0).any() or w.sum()<=0:raise ValueError('invalid support/weights')
    center=np.average(x,axis=0,weights=w);z=x-center
    covariance=(z.T*w)@z/w.sum()
    eigenvalues,axes=np.linalg.eigh(covariance)
    return dict(total_weight=float(w.sum()),center=center,covariance=covariance,eigenvalues=eigenvalues,axes=axes)

def gaussian_2d_ellipse_mass(mahalanobis_radius):
    r=float(mahalanobis_radius)
    if not math.isfinite(r) or r<0:raise ValueError('radius must be finite and nonnegative')
    return -math.expm1(-r*r/2)
