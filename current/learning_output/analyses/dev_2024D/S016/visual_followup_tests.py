"""Small audit witnesses after PDF inspection; never an author model reproduction."""
from pathlib import Path
from datetime import datetime, timezone
import csv, io, json, math, hashlib, statistics
import pandas as pd

P = Path(__file__).resolve().parent
checks, histories, registry = [], [], []
def check(name, passed, detail):
    checks.append(dict(id=name, passed=bool(passed), detail=detail))
def witness(name, first, diagnosis, repair, retest, scope):
    histories.append(dict(id=name, origin='DESIGNED_MICRO_FIXTURE_NOT_HISTORICAL_AUTHOR_RUN',
                          first_fail=first, diagnosis=diagnosis, repair=repair,
                          retest=retest, scope=scope))

# A real pandas writer feeds a semantic transcription of the printed line reader.
# No original C++ binary is claimed; float conversion matches these finite numeric tokens.
original = [[.2, .8], [.7, .3]]
def numeric_lines(text):
    return [[float(x) for x in row] for row in csv.reader(io.StringIO(text))]
bad = numeric_lines(pd.DataFrame(original).to_csv(index=False))
good = numeric_lines(pd.DataFrame(original).to_csv(index=False, header=False))
check('csv_numeric_header_detected', len(bad)==3 and bad[0]==[0.,1.], bad)
check('csv_roundtrip_shape_and_values', good==original, good)
witness('numeric_header_becomes_pixel', {'status':'FAIL','expected_rows':2,'actual_rows':len(bad)},
        'p92 writer retains numeric column header; p93 reader parses every numeric line as a pixel row.',
        'Declare header contract; this fixture writes header=False and asserts original shape and values.',
        {'status':'PASS' if good==original else 'FAIL','rows':len(good)},
        'Local pandas CSV path plus Python transcription; actual author files/compiled chain not available.')

# Matching dimensions cannot establish geographic identity.
rain = [('g1',10),('g2',20),('g3',30)]
height = [('g3',300),('g1',100),('g2',200)]
positional = [(r[0],r[1],h[1]) for r,h in zip(rain,height)]
lookup = dict(height)
joined = [(key,value,lookup[key]) for key,value in rain]
oracle = [('g1',10,100),('g2',20,200),('g3',30,300)]
check('same_length_can_misalign', positional!=oracle and len(rain)==len(height), positional)
check('coordinate_join_restores_identity', joined==oracle, joined)
witness('same_length_is_not_same_pixel', {'status':'FAIL','joined':positional},
        'Equal-length arrays can have different coordinate order, as allowed by p45 min_length pseudocode.',
        'Join validated unique coordinate/time keys and assert support equality; never truncate to minimum length.',
        {'status':'PASS' if joined==oracle else 'FAIL','joined':joined}, 'Synthetic three-cell dataset.')

# Range and semantic output validation; do not guess the link function of the paper.
def accept_probability(values):
    return all(math.isfinite(v) and 0 <= v <= 1 for v in values)
check('shap_output_not_probability', not accept_probability([4.67]),
      'p79 f(x)=4.67 and p80 roughly 1–7 cannot directly be probabilities.')
margin=4.67
linked=1/(1+math.exp(-margin))
check('known_binary_link_probability_control', accept_probability([linked]),
      {'synthetic_binary_margin':margin,'linked_probability':linked,'paper_link':'UNRESOLVED'})
base, contributions = .2, {'a':.5,'b':-.1}
output=base+sum(contributions.values())
check('contribution_direction_and_sum', output==.6 or math.isclose(output,.6),
      {'base':base,'contributions':contributions,'output':output})
check('positive_contribution_cannot_mean_decrease', not(contributions['a']<0),
      'Reject a verbal decrease for a positive additive contribution in the same declared output space.')
witness('shap_probability_semantics', {'status':'FAIL','claimed':'probability','value':4.67},
        'A plot output was called a probability without an output/link/class contract.',
        'Reject the probability claim; leave author output space UNRESOLVED. Link only a separately declared binary-logit control.',
        {'status':'PASS','author_probability_claim':'REJECTED','author_output_space':'UNRESOLVED'},
        'Range audit and independent known-link control; no author probability reconstructed.')

# Formula audit: p16 displays n/(n-1) rather than 1/(n-1).
x=[1.,2.,3.,4.]; n=len(x); ss=sum((v-statistics.mean(x))**2 for v in x)
printed_sd=math.sqrt(n/(n-1)*ss); reference_sd=statistics.stdev(x)
check('sd_normalizer_counterexample', math.isclose(printed_sd/reference_sd,math.sqrt(n)),
      {'printed':printed_sd,'sample_stdev':reference_sd,'ratio':printed_sd/reference_sd})

# p64: rows=true, columns=predicted, class order=[no storm, storm].
tn,fp,fn,tp=9733,1944,2177,5137
N=tn+fp+fn+tp
metrics={'n':N,'accuracy':(tn+tp)/N,'precision':tp/(tp+fp),
         'recall':tp/(tp+fn),'specificity':tn/(tn+fp),
         'f1':2*tp/(2*tp+fp+fn),'majority_accuracy':max(tn+fp,fn+tp)/N}
y_true=[0]*(tn+fp)+[1]*(fn+tp)
y_pred=[0]*tn+[1]*fp+[0]*fn+[1]*tp
check('confusion_matrix_arithmetic', sum(a==b for a,b in zip(y_true,y_pred))/N==metrics['accuracy']
      and N==18991, metrics)
check('regression_and_classification_runs_not_mergeable', N!=501301,
      {'classification_n':N,'p63_OLS_n':501301,'link':'UNRESOLVED; could be different sampling, not automatically an error'})
registry.append({'id':'S016_Q3_FIG537','pdf_pages':[63,64],'source':'Figure 5.37',
                 'matrix':[[tn,fp],[fn,tp]],'row_axis':'true_label','column_axis':'predicted_label',
                 'positive_class':'storm','metrics':metrics,
                 'model_id':'UNRESOLVED: RF heading but preceding numerical output is OLS',
                 'split_id':'UNRESOLVED','scope':'PRINTED_CONFUSION_MATRIX_ARITHMETIC_ONLY',
                 'forbidden_inference':'Does not validate future disaster prediction or matching frozen Rx1day task.'})
registry.append({'id':'S016_Q4_SHAP_OUTPUT','pdf_pages':[78,79,80],
                 'force_output':4.67,'decision_axis_approx':[1,7],
                 'author_claim':'probability','status':'PROBABILITY_SEMANTICS_CONTRADICTED',
                 'actual_output_space':'UNRESOLVED','class_id':'UNRESOLVED',
                 'feature_map':'UNRESOLVED: NDVI not in earlier list; QW label differs from prose',
                 'scope':'VISUAL_RANGE_AND_LABEL_AUDIT_ONLY'})

out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
     'scope':'LOCAL_ARITHMETIC_AND_SYNTHETIC_MECHANISMS_ONLY',
     'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,
     'first_fail_diagnosis_repair_retest':histories,'result_registry':registry,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'source_sha256':hashlib.sha256((P/'source.pdf').read_bytes()).hexdigest(),
     'pandas_version':pd.__version__,'author_reproduction':'NOT_RUN','core_gain':'NOT_ESTABLISHED'}
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
(P/'audit_runs').mkdir(exist_ok=True)
payload=json.dumps(out,ensure_ascii=False,indent=2)
(P/'audit_runs'/f'visual_followup_{stamp}.json').write_text(payload,encoding='utf-8')
(P/'VISUAL_FOLLOWUP_TEST_RESULTS.json').write_text(payload,encoding='utf-8')
print(json.dumps({'passed':out['passed'],'total':out['total'],'confusion_metrics':metrics}))
raise SystemExit(0 if out['passed']==out['total'] else 1)
