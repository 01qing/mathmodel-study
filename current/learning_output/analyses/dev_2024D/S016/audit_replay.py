"""Transcribed values and explicit synthetic counterexamples; not model reproduction."""
from pathlib import Path
import json, hashlib, math
from datetime import datetime, timezone

P=Path(__file__).resolve().parent
checks=[]; records=[]
def ck(name, condition, detail):
    checks.append({'id':name,'passed':bool(condition),'detail':detail})

# p29, physically inspected. Three periods, five classes.
K=[[.017758,2.561795,-.336966,-.650894,-1.153579],
   [-.346666,2.105965,-.364588,-.432412,-1.323177],
   [.209042,1.040309,-.30412,-.427508,-.932658]]
D=[[.19089,2.623178,.029117,.017411,.024277],
   [.096746,.000951,.043703,.058419,.150114],
   [.100119,.000775,.045494,.061367,.175987]]
C=[[.173131,.061382,.366083,.668305,1.177856],
   [.106546,.153398,.014705,.010403,.003094],
   [.11026,.125137,.015308,.010928,.003627]]
for t in range(3):
    for j,cls in enumerate(['crop','forest','grass','shrub','wetland']):
        residual=K[t][j]-(D[t][j]-C[t][j])
        closes=abs(residual)<=2e-6
        records.append({'id':f'flow_{t}_{cls}','pdf_pages':[27,28,29,104],
                        'K':K[t][j],'LUD':D[t][j],'LUC':C[t][j],
                        'K_minus_LUD_plus_LUC':residual,'author_identity_holds':closes,
                        'scope':'printed values only, same-denominator/time contract'})
        ck(f'flow_diagnostic_{t}_{cls}',closes if t==0 else not closes,
           'First period closes within rounding; later periods fail printed identity.')

body=[262.84225,260.08557,270.5438,270.62848,273.0116,276.20404]
pred=[263.7575,260.5738,271.44904,271.3931,273.9359,277.6378]
truth=[273.74158,299.14838,269.47815,276.62497,264.9937,285.12454]
mae=sum(abs(a-b) for a,b in zip(pred,truth))/6
rmse=math.sqrt(sum((a-b)**2 for a,b in zip(pred,truth))/6)
records.append({'id':'lstm_2015_2020','pdf_pages':[22,87],
 'body_prediction_and_truth':body,'appendix_prediction':pred,'appendix_truth':truth,
 'appendix_mae_mm':mae,'appendix_rmse_mm':rmse,
 'scope':'table replay only; heldout membership and original preprocessing not established'})
ck('lstm_two_truth_sources_conflict',all(a!=b for a,b in zip(body,truth)), 'All six same-year truth entries differ.')
ck('appendix_lstm_not_zero_error',mae>0 and rmse>0,'Does not identify why body table duplicated values.')

# Independence is an exact arbiter: upper tails .1 each => joint .01.
# For marginalizing third Gaussian dimension, Z cutoff tends to +infinity.
upper=.1; correct=upper*upper; printed=(1-upper)*(1-upper)
records.append({'id':'upper_tail_counterexample','pdf_pages':[42],
 'fixture':'independent standardized variables, both upper-tail probabilities .1, Z marginalized',
 'correct_event_probability':correct,'printed_lower_cdf_probability':printed,
 'correct_return_observation_intervals':1/correct,'printed_return_observation_intervals':1/printed,
 'scope':'synthetic mathematical counterexample, not Chinese climate data'})
ck('upper_tail_probability_bound',correct<=upper and printed>upper,
   'Intersection cannot exceed either marginal; printed expression violates this fixture.')

# Marginals cannot identify physical cross-class flow.
a=[[.5,0],[0,.5]];b=[[0,.5],[.5,0]]
ck('fraction_marginals_do_not_identify_flow',
   [sum(r) for r in a]==[sum(r) for r in b] and
   [sum(r[j] for r in a) for j in range(2)]==[sum(r[j] for r in b) for j in range(2)] and a!=b,
   'Identical initial/final class totals permit no exchange or complete exchange; no unique flow without joint identity.')

out={'scope':'LOCAL_TABLE_AND_MATHEMATICAL_AUDIT_ONLY',
 'timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_sha256':hashlib.sha256((P/'source.pdf').read_bytes()).hexdigest(),
 'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,
 'core_gain':'NOT_ESTABLISHED','author_full_reproduction':'NOT_RUN',
 'history_note':'Designed contradiction checks; not alleged historical failed author runs.'}
(P/'audit_runs').mkdir(exist_ok=True)
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
(P/'audit_runs'/f'{stamp}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'AUDIT_REPLAY_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'RESULT_REGISTRY_PARTIAL.json').write_text(json.dumps({'status':'PARTIAL','records':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':out['passed'],'total':out['total'],'appendix_lstm_mae_mm':mae,'appendix_lstm_rmse_mm':rmse}))
raise SystemExit(0 if out['passed']==out['total'] else 1)
