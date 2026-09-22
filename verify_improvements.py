"""Known-defect regression checks; not an independent modeling capability evaluation."""
from pathlib import Path
import ast, copy, importlib.util, json
import numpy as np

ROOT=Path(__file__).parent
SKILL=Path('C:/Users/lingyun/.codex/skills/mathmodel-evidence')
spec=importlib.util.spec_from_file_location('guard',SKILL/'scripts/check_experiment.py')
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
base={'samples':[
    {'id':'tr-a','group':'file-a','split':'train','label':'N','fs_hz':12000},
    {'id':'tr-b','group':'file-b','split':'train','label':'B','fs_hz':12000},
    {'id':'te-a','group':'file-c','split':'test','label':'N','fs_hz':12000},
    {'id':'te-b','group':'file-d','split':'test','label':'B','fs_hz':12000},
    {'id':'target','group':'file-e','split':'target','label':None,'fs_hz':32000}],
    'task_classes':['N','B'],'target_mode':'transductive',
    'fit_events':[{'name':'scaler','sample_ids':['tr-a','tr-b'],'purpose':'preprocessing','uses_labels':False},
                  {'name':'adapt','sample_ids':['target'],'purpose':'adaptation','uses_labels':False}],
    'metrics':[{'name':'accuracy','split':'test','truth':'independent_ground_truth','sample_ids':['te-a','te-b']}],
    'predictions':[{'id':'A','label':'B'}],'required_target_ids':['A']}
checks=[]
def expect(name,d,code=None):
    result=guard.check(d)
    ok=not result['errors'] if code is None else any(x.startswith(code) for x in result['errors'])
    if not ok: raise AssertionError((name,result))
    checks.append({'test':name,'pass':True,'errors':result['errors']})
expect('legitimate_unlabeled_target_adaptation_allowed',copy.deepcopy(base))
d=copy.deepcopy(base);d['samples'][2]['group']='file-a';expect('same_acquisition_across_split_blocked',d,'GROUP_CROSSES_SPLITS')
d=copy.deepcopy(base);d['fit_events'][0]['sample_ids'].append('te-a');expect('test_fitted_PCA_or_scaler_blocked',d,'FIT_BOUNDARY')
d=copy.deepcopy(base);d['metrics'].append({'name':'accuracy','split':'target','truth':'pseudo','sample_ids':['target']});expect('pseudo_label_accuracy_blocked',d,'UNSUPPORTED_ACCURACY')
d=copy.deepcopy(base);d['samples'][0]['fs_hz']=None;expect('unknown_sampling_rate_blocked',d,'UNKNOWN_SAMPLING_RATE')
d=copy.deepcopy(base);d['fit_events'][1]['uses_labels']=True;expect('target_labels_for_unsupervised_adaptation_blocked',d,'FIT_BOUNDARY')
d=copy.deepcopy(base);d['predictions']=[];expect('missing_target_predictions_blocked',d,'TARGET_OUTPUT_COVERAGE')
d=copy.deepcopy(base);d['samples'][2]['label']='B';expect('missing_test_class_blocked',d,'CLASS_COVERAGE')
d=copy.deepcopy(base);d.pop('metrics');expect('missing_record_field_blocked',d,'MISSING_FIELD')
d=copy.deepcopy(base);d['metrics'][0]['sample_ids']=['target'];expect('metric_on_wrong_population_blocked',d,'METRIC_POPULATION_MISMATCH')

# Reproduce only the inspected expressions, not third-party top-level programs.
source=ROOT/'evidence/S051-member-13.txt'
tree=ast.parse(source.read_text(encoding='utf-8'))
expr=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.value,ast.IfExp)
          and '48kHz' in ast.unparse(n.value))
path='source/48kHz_DE_data/IR014_1.mat'
observed=eval(compile(ast.Expression(expr),'<inspected-fs-expression>','eval'),{'__builtins__':{}},{'fpath':path})
fixed=48000 if '48khz' in path.lower() else 12000
assert observed==12000 and fixed==48000
checks.append({'test':'real_main8_sampling_fallback_case_bug','pass':True,'observed':observed,'expected':fixed})

source=ROOT/'evidence/notebook-92.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='maha_score')
namespace={'np':np,'mu_c':np.zeros((1,2)), 'cov_inv':np.linalg.inv(np.array([[2.,.5],[.5,1.]]))}
exec(compile(ast.Module(body=[fun],type_ignores=[]),'<inspected-maha-function>','exec'),namespace)
E=np.array([[1.,-.75]])
old_distance=float(-namespace['maha_score'](E)[0])
correct_distance=float(np.einsum('ncd,de,nce->nc',E[:,None,:],namespace['cov_inv'],E[:,None,:])[0,0])
assert old_distance<0 and correct_distance>0
checks.append({'test':'real_solve4_mahalanobis_nonnegative_invariant','pass':True,
               'reference_squared_distance':old_distance,'correct_squared_distance':correct_distance})

confidences=[.796,.699,.999,.968,.998,.997,.892,.998,.999,.868,.879,.897,.867,.999,.942,.997]
average=sum(confidences)/len(confidences)
assert abs(average-.9246875)<1e-12 and abs(average-.992)>.06
checks.append({'test':'S040_table_6_2_mean_recomputed','pass':True,'computed_mean':average,'prose_mean':.992,
               'scope':'Equal-file arithmetic mean of visually verified PDF pages 37-38; alternative weighting unspecified'})
(ROOT/'evidence/valid_experiment_example.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
result={'scope':'KNOWN_DEFECT_REGRESSION_AND_METADATA_TESTS','checks':checks,'count':len(checks),
        'not_proven':['Independent skill effectiveness','Real target accuracy','Full third-party pipeline reproducibility']}
(ROOT/'evidence/regression_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
