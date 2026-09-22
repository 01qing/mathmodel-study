#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import argparse, csv, json, math, sys

p=argparse.ArgumentParser()
p.add_argument('--csv-root', required=True, help='Root containing train/ and test/')
p.add_argument('--output-dir', default='learning_output/data_audit/gmcm-2021-D-csv-mirror')
p.add_argument('--tolerance', type=float, default=1e-6)
args=p.parse_args()
ROOT=Path(args.csv_root); OUT=Path(args.output_dir); OUT.mkdir(parents=True,exist_ok=True)
labels=['Caco-2','CYP3A4','hERG','HOB','MN']
favorable={'Caco-2':1,'CYP3A4':None,'hERG':0,'HOB':1,'MN':0}

def read_csv(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); rows=list(r); return r.fieldnames or [],rows

def norm(x): return str(x or '').strip().lower().replace(' ','').replace('_','').replace('-','')
def find_header(headers,candidates):
    for h in headers:
        for c in candidates:
            if norm(h)==norm(c): return h
    for h in headers:
        for c in candidates:
            if norm(c) in norm(h): return h
    return None

def compare(a,b):
    return {'same_length':len(a)==len(b),'same_order':a==b,'same_set':set(a)==set(b),
            'left_count':len(a),'right_count':len(b),'left_duplicates':len(a)-len(set(a)),
            'right_duplicates':len(b)-len(set(b)),'left_only_count':len(set(a)-set(b)),
            'right_only_count':len(set(b)-set(a))}

required=[ROOT/'train/ERα_activity.csv',ROOT/'train/Molecular_Descriptor.csv',ROOT/'train/ADMET.csv',
          ROOT/'test/ERα_activity.csv',ROOT/'test/Molecular_Descriptor.csv',ROOT/'test/ADMET.csv']
missing=[str(x) for x in required if not x.exists()]
report={'schema_version':'1.2','case_id':'gmcm-2021-D','source_role':'participant_converted_mirror',
        'status':'PENDING','checks':{},'warnings':[],'blockers':[], 'crosscheck_with_primary_xlsx':'NOT_RUN'}
if missing:
    report['status']='BLOCKED'; report['blockers'] += [f'missing: {x}' for x in missing]
    (OUT/'data_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('[BLOCKED] missing CSV files'); sys.exit(2)

ha,ra=read_csv(ROOT/'train/ERα_activity.csv'); hd,rd=read_csv(ROOT/'train/Molecular_Descriptor.csv'); hb,rb=read_csv(ROOT/'train/ADMET.csv')
hat,rat=read_csv(ROOT/'test/ERα_activity.csv'); hdt,rdt=read_csv(ROOT/'test/Molecular_Descriptor.csv'); hbt,rbt=read_csv(ROOT/'test/ADMET.csv')
asm=find_header(ha,['SMILES']); dsm=find_header(hd,['SMILES']); bsm=find_header(hb,['SMILES'])
asmt=find_header(hat,['SMILES']); dsmt=find_header(hdt,['SMILES']); bsmt=find_header(hbt,['SMILES'])
icol=find_header(ha,['IC50_nM','IC50']); pcol=find_header(ha,['pIC50'])

a=[str(r.get(asm) or '') for r in ra]; d=[str(r.get(dsm) or '') for r in rd]; b=[str(r.get(bsm) or '') for r in rb]
at=[str(r.get(asmt) or '') for r in rat]; dt=[str(r.get(dsmt) or '') for r in rdt]; bt=[str(r.get(bsmt) or '') for r in rbt]
align={'train_activity_vs_descriptor':compare(a,d),'train_activity_vs_admet':compare(a,b),'train_descriptor_vs_admet':compare(d,b),
       'test_activity_vs_descriptor':compare(at,dt),'test_activity_vs_admet':compare(at,bt)}
report['checks']['smiles_alignment']=align
for k,v in align.items():
    if not v['same_set']: report['blockers'].append(f'SMILES set mismatch: {k}')
    elif not v['same_order']: report['warnings'].append(f'SMILES order differs: {k}; reindex by SMILES')

errs=[]; bad=0; nonpos=0
if icol and pcol:
    for r in ra:
        try:
            ic=float(r[icol]); pc=float(r[pcol])
            if ic<=0: nonpos+=1
            else: errs.append(abs((9-math.log10(ic))-pc))
        except Exception: bad+=1
else: report['warnings'].append('IC50 or pIC50 column not found; relation not checked')
report['checks']['activity']={'train_rows':len(ra),'test_rows':len(rat),'smiles_column':asm,'ic50_column':icol,'pic50_column':pcol,
 'nonpositive_ic50':nonpos,'unparseable_pairs':bad,'formula_max_abs_error':max(errs) if errs else None,
 'formula_mean_abs_error':sum(errs)/len(errs) if errs else None,'formula_over_tolerance':sum(e>args.tolerance for e in errs)}

# descriptor audit
desc=[h for h in hd if h and h!=dsm]
stats={h:{'missing':0,'numeric':0,'nonnumeric':0,'min':None,'max':None} for h in desc}
for r in rd:
    for h in desc:
        v=r.get(h)
        if v in (None,''): stats[h]['missing']+=1; continue
        try:
            x=float(v); s=stats[h]; s['numeric']+=1; s['min']=x if s['min'] is None else min(s['min'],x); s['max']=x if s['max'] is None else max(s['max'],x)
        except Exception: stats[h]['nonnumeric']+=1
constants=[h for h,s in stats.items() if s['numeric'] and s['min']==s['max'] and not s['nonnumeric']]
allmissing=[h for h,s in stats.items() if s['numeric']==0 and s['nonnumeric']==0]
anymissing=[h for h,s in stats.items() if s['missing']]
nonnumeric=[h for h,s in stats.items() if s['nonnumeric']]
report['checks']['descriptors']={'train_rows':len(rd),'test_rows':len(rdt),'descriptor_count':len(desc),'constant_columns_count':len(constants),
 'constant_columns':constants[:100],'all_missing_columns_count':len(allmissing),'all_missing_columns':allmissing[:100],
 'columns_with_any_missing_count':len(anymissing),'nonnumeric_columns_count':len(nonnumeric),'nonnumeric_columns':nonnumeric[:100]}

# ADMET distributions
lcols={lab:find_header(hb,[lab]) for lab in labels}; dist={}
for lab,col in lcols.items():
    c=Counter()
    for r in rb:
        v=r.get(col) if col else None
        if v in (None,''): c['missing']+=1
        else:
            try: c[str(int(float(v)))]+=1
            except Exception: c['other']+=1
    n0,n1=c.get('0',0),c.get('1',0); valid=n0+n1
    dist[lab]={'0':n0,'1':n1,'missing':c.get('missing',0),'other':c.get('other',0),
               'minority_ratio':min(n0,n1)/valid if valid else None,'favorable_class':favorable[lab],
               'semantic_ambiguity':lab=='CYP3A4'}
report['checks']['admet']={'train_rows':len(rb),'test_rows':len(rbt),'label_columns':lcols,'distributions':dist}

for label,actual,expected in [('activity train rows',len(ra),1974),('descriptor train rows',len(rd),1974),('ADMET train rows',len(rb),1974),
                              ('descriptor count',len(desc),729),('activity test rows',len(rat),50),('descriptor test rows',len(rdt),50),('ADMET test rows',len(rbt),50)]:
    if actual!=expected: report['warnings'].append(f'{label}={actual}, problem statement expected {expected}')
if report['checks']['activity']['formula_over_tolerance']>0: report['warnings'].append('IC50/pIC50 relation exceeds tolerance')
if constants: report['warnings'].append('constant descriptor columns exist')
report['test_isolation_policy']={'used_for_modeling':False,'allowed':['cross-check and final prediction after route freeze'],
                                 'forbidden':['feature selection','model selection','hyperparameter tuning','threshold selection']}
report['status']='BLOCKED' if report['blockers'] else ('PASS_WITH_WARNINGS' if report['warnings'] else 'PASS')
(OUT/'data_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 2021 D CSV Mirror Data Audit','',f"Status: **{report['status']}**",'',
       f'- train rows: activity={len(ra)}, descriptor={len(rd)}, ADMET={len(rb)}',
       f'- test rows: activity={len(rat)}, descriptor={len(rdt)}, ADMET={len(rbt)}',f'- descriptor count: {len(desc)}','', '## ADMET']
for lab,x in dist.items(): lines.append(f"- {lab}: 0={x['0']}, 1={x['1']}, minority_ratio={x['minority_ratio']}, favorable={x['favorable_class']}")
lines += ['', '## Mirror status', '- This audit does not make the CSV equivalent to primary XLSX.', '- XLSX-vs-CSV cross-check is still required.']
(OUT/'data_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f"[{report['status']}] CSV audit written to {OUT}")
sys.exit(2 if report['status']=='BLOCKED' else 0)
