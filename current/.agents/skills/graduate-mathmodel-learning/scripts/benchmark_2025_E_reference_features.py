"""Diagnostic comparison on an existing feature CSV, not a raw-signal reproduction."""
import argparse, csv, hashlib, json
from pathlib import Path
import numpy as np
import sklearn
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, confusion_matrix

def scores(y, p, classes):
    return {'accuracy':accuracy_score(y,p),'balanced_accuracy':balanced_accuracy_score(y,p),
            'macro_f1':f1_score(y,p,labels=classes,average='macro',zero_division=0),
            'confusion_matrix':confusion_matrix(y,p,labels=classes).tolist()}

def run(path, output, folds=3):
    rows=list(csv.DictReader(path.open(encoding='utf-8-sig',newline='')))
    if not rows: raise ValueError('Empty data')
    meta={'path','channel','label','fs_used','seg_idx'}
    if not meta.issubset(rows[0]): raise ValueError('Missing provenance columns')
    cols=[k for k in rows[0] if k not in meta]
    X=np.array([[float(r[k]) for k in cols] for r in rows])
    if not np.isfinite(X).all(): raise ValueError('Nonfinite features: audit first')
    y=np.array([r['label'] for r in rows]); groups=np.array([r['path'].replace('\\','/').lower() for r in rows])
    classes=np.unique(y); group_labels={}
    for g in np.unique(groups):
        labels=np.unique(y[groups==g])
        if len(labels)!=1: raise ValueError('Conflicting labels in group '+g)
        group_labels[g]=str(labels[0])
    group_counts={str(c):list(group_labels.values()).count(c) for c in classes}
    if min(group_counts.values())<folds: raise ValueError('Too few independent class groups for requested folds')
    configs={'random_rows':StratifiedKFold(folds,shuffle=True,random_state=42),
             'grouped_files':StratifiedGroupKFold(folds,shuffle=True,random_state=42)}
    out={'scope':'REFERENCE_DERIVED_FEATURE_DIAGNOSTIC_NOT_RAW_REPRODUCTION',
         'csv':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'rows':len(rows),'features':cols,'groups':len(group_labels),'class_group_counts':group_counts,
         'class_row_counts':{str(c):int(sum(y==c)) for c in classes},'sklearn':sklearn.__version__,
         'classes':classes.tolist(),'seed':42,'results':[]}
    for mode,splitter in configs.items():
        for fold,(tr,te) in enumerate(splitter.split(X,y,groups if mode=='grouped_files' else None)):
            if set(y[tr])!=set(classes) or set(y[te])!=set(classes):
                raise ValueError('A fold is missing classes; revise grouping protocol before comparison')
            overlap=sorted(set(groups[tr])&set(groups[te]))
            if mode=='grouped_files' and overlap: raise AssertionError('Group leakage')
            for name,model in [('ridge',make_pipeline(StandardScaler(),RidgeClassifier(class_weight='balanced'))),
                               ('random_forest',RandomForestClassifier(n_estimators=80,max_depth=14,
                                 class_weight='balanced',random_state=42,n_jobs=2))]:
                model.fit(X[tr],y[tr]); pred=model.predict(X[te])
                true_file=[]; pred_file=[]
                for g in sorted(set(groups[te])):
                    mask=groups[te]==g; labs,counts=np.unique(pred[mask],return_counts=True)
                    # Deterministic lexical tie break, reported rather than silently tuned.
                    pred_file.append(labs[np.argmax(counts)]); true_file.append(group_labels[g])
                out['results'].append({'mode':mode,'fold':fold,'model':name,
                    'shared_group_count':len(overlap),'test_groups':sorted(set(groups[te])),
                    'window':scores(y[te],pred,classes),'file':scores(true_file,pred_file,classes)})
    out['aggregation']='Majority vote per file; lexical tie break; random_rows votes only held-out windows of potentially seen files'
    out['limitations']=['Features supplied by reference author; upstream signal and preprocessing not reproduced',
        'Path groups are not a content-hash duplicate audit','No target-domain labels or target accuracy',
        'Fixed diagnostic candidates; folds descriptive, not independent significance tests']
    output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({mode:{name:{metric:float(np.mean([r['file'][metric] for r in out['results'] if r['mode']==mode and r['model']==name]))
            for metric in ['accuracy','balanced_accuracy','macro_f1']} for name in ['ridge','random_forest']} for mode in configs},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('csv',type=Path); p.add_argument('output',type=Path); p.add_argument('--folds',type=int,default=3)
    a=p.parse_args(); run(a.csv,a.output,a.folds)
