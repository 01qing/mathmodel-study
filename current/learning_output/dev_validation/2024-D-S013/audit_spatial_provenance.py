from pathlib import Path
import json
import numpy as np
from sklearn.svm import SVR
H=Path(__file__).resolve().parent
# Literal Eq6-2 angle and Eq6-4 axes, tested against a valid covariance matrix.
C=np.array([[4.,1.],[1.,1.]])
theta=np.arctan((C[0,0]-C[1,1])/(2*C[0,1]))
printed=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),-np.cos(theta)]])
literal_cov=printed@C@printed.T
eigenvalues,V=np.linalg.eigh(C);repaired=V.T@C@V
assert abs(literal_cov[0,1])>1e-3 and abs(repaired[0,1])<1e-12
assert not np.allclose(printed@printed.T,np.eye(2))
# Same six country-level inputs repeated across locations cannot create a map
# with spatially varying deterministic SVR output if coordinates are excluded.
rng=np.random.default_rng(13);X=rng.normal(size=(80,6));y=X[:,0]+.2*X[:,1];mod=SVR().fit(X,y)
row=np.array([183.91,.045,.123,.046,.005,.022])
pred=mod.predict(np.repeat(row[None,:],20,axis=0));assert np.ptp(pred)==0
out={'scope':'literal formula and conditional dataflow counterexamples; not author GIS or SVR full reproduction','tests':[
 {'id':'S013-SP01','source_page':63,'first':'FAIL','printed_axis_dot_product':float((printed@printed.T)[0,1]),'printed_cross_covariance':float(literal_cov[0,1]),'diagnosis':'Eq6-2/6-4 literal angle/axis expressions do not produce orthogonal principal axes','repair':'symmetric covariance eigendecomposition with declared ordering','retest':'PASS','repaired_cross_covariance':float(repaired[0,1])},
 {'id':'S013-SP02','source_pages':[51,104,108],'first':'UNSUPPORTED_SPATIAL_OUTPUT','prediction_range_same_year_inputs':float(np.ptp(pred)),'diagnosis':'national annual six-feature forecasts plus no-coordinate predictor imply identical same-year predictions; spatial disaggregation primitive not supplied','retest':'PASS_CONDITIONAL_INVARIANT','repair_status':'NOT_IMPLEMENTED; needs original regional input or disaggregation chain'},
 {'id':'S013-SP03','source_pages':[51,52],'table2020_grass':.020,'table2020_forest':.003,'prose2020_grass':.003,'status':'CONTRADICTED_TABLE_VS_PROSE'},
 {'id':'S013-SP04','source_pages':[57,58],'prose_target':'SVR vulnerability index','figure5_24_title':'annual precipitation Getis-Ord Gi*','status':'RESULT_IDENTITY_MISMATCH_REQUIRES_SOURCE_TRACE'}]}
(H/'SPATIAL_PROVENANCE_RESULTS.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
