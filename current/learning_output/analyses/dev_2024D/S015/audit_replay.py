"""Paper arithmetic and synthetic contract checks; not author reproduction."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
checks = []
registry = []

def record(key, pages, value, interpretation):
    registry.append(dict(id=key, pdf_pages=pages, replay=value,
                         interpretation=interpretation, source='transcribed paper values',
                         scope='arithmetic/static audit; original data not rerun'))

def check(key, condition, scope):
    checks.append(dict(id=key, passed=bool(condition), scope=scope))

counts = [2395914, 3313572, 214314, 54220, 10780, 1208, 92]
sampled = [6000, 5000, 4000, 3000, 1500, 1208, 92]
check('original_count_closure', sum(counts) == 5990100, 'table p35 arithmetic')
check('sample_count_closure', sum(sampled) == 20800, 'table p35 arithmetic')
rates = {'all_percent': 100*92/sum(counts),
         'wet_percent': 100*92/sum(counts[1:]),
         'sample_percent': 100*92/sum(sampled)}
record('rare_prevalence', [2,35], rates, 'Abstract all-data denominator does not match; wet-day possibility is not a correction of author contract.')
check('sampling_changes_prevalence', rates['sample_percent'] > 100*rates['all_percent'], 'detect changed statistical population')

for year, values in [(1990,[.288916,.32869,.420351,.371391,.325661]),
                     (2019,[.296083,.395821,.421159,.372098,.268423])]:
    total = sum(values)
    record(f'composition_{year}', [14,25,26], total, 'Contradicts sum-to-one printed definition; production origin unresolved.')
    check(f'detect_composition_nonclosure_{year}', abs(total-1) > .7, 'detect author contradiction, not endorse result')

record('variance_field', [14,88], {'RYs':9834605.71,'RYsd_squared':5.525**2}, 'Printed code uses sum for RYs.')
check('detect_sum_variance_mismatch', abs(9834605.71-5.525**2) > 1e6, 'table versus code identity')
x=[1.,2.,6.]; m=sum(x)/len(x)
bad=sum(v-m for v in x)/len(x)
good=sum((v-m)**2 for v in x)/len(x)
check('missing_square_counterexample', abs(bad)<1e-12 and good>0, 'synthetic formula witness, not author execution')
check('logvariance_direction', math.exp(.078)>1 and math.exp(-.074)<1, 'coefficient sign witness; arrow semantic issue')
check('median_not_necessary_threshold', 37.51 < 1084.11, 'table p39 falsifies all-cases-above-median interpretation')

for name, tn, fn, fp, tp in [('svm',4059,27,0,14),('rf',4058,0,1,41)]:
    n=tn+fn+fp+tp
    recall=tp/(tp+fn); specificity=tn/(tn+fp)
    metrics={'n':n,'accuracy':(tn+tp)/n,'recall':recall,
             'specificity':specificity,'hard_class_auc':(recall+specificity)/2,
             'majority_baseline_accuracy':(tn+fp)/n}
    record(name+'_confusion_replay', [61,93], metrics, 'Conditional on printed matrix; no model retraining and no matched evaluator claim.')
    check(name+'_matrix_count', n==4100 and tp+fn==41, 'printed matrix sample count')
    check(name+'_hard_auc_identity', 0 <= metrics['hard_class_auc'] <= 1, 'single operating-point interpolation')
    if name=='svm':
        check('svm_minority_weakness', recall<.35 and metrics['accuracy']>.99, 'accuracy can obscure low minority recall')
    else:
        check('rf_not_perfect', metrics['accuracy']<1 and fp==1, 'retain one error despite displayed rounding')

# Perfect score ordering still has bad operating thresholds.
scores=[.1,.2,.8,.9]; y=[0,0,1,1]
pair_auc=sum(scores[j]>scores[i] for i in [0,1] for j in [2,3])/4
threshold_predictions=[int(v>=0) for v in scores]
check('auc_one_not_every_threshold', pair_auc==1 and threshold_predictions!=y, 'synthetic counterexample, not paper predictions')
west={'grass':.259,'crop':.061,'forest':.068,'shrub':.079,'wetland':.010}
east={'grass':.085,'crop':.060,'forest':.084,'shrub':.036,'wetland':.002}
record('east_minus_west', [73,74,76], {k:east[k]-west[k] for k in west}, 'Three named types contradict east-higher summary.')
check('regional_sign_contract', all(west[k]>east[k] for k in ['grass','shrub','wetland']) and east['forest']>west['forest'], 'table/summary sign replay')

out={'scope':'LOCAL_ARITHMETIC_AND_SYNTHETIC_AUDIT_ONLY',
     'timestamp_utc':datetime.now(timezone.utc).isoformat(),
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'source_pdf_sha256':hashlib.sha256((ROOT/'source.pdf').read_bytes()).hexdigest(),
     'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),
     'author_end_to_end_reproduction':'NOT_RUN','core_gain':'NOT_ESTABLISHED',
     'history_note':'Synthetic fault witnesses are not claimed as historical first failed runs.'}
history=ROOT/'audit_runs';history.mkdir(exist_ok=True)
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
(history/(stamp+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'AUDIT_REPLAY_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'RESULT_REGISTRY_PARTIAL.json').write_text(json.dumps({'status':'PARTIAL','records':registry},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':out['passed'],'total':out['total'],'scope':out['scope']}))
raise SystemExit(0 if out['passed']==out['total'] else 1)
