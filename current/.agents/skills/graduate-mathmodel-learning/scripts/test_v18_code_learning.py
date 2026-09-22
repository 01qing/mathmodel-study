#!/usr/bin/env python3
from pathlib import Path
import importlib.util, json, tempfile

SCRIPT=Path(__file__).with_name('audit_code_bundle.py')
spec=importlib.util.spec_from_file_location('audit_code_bundle', SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
passed=[]

def ok(cond,name):
    if not cond: raise AssertionError(name)
    passed.append(name)

with tempfile.TemporaryDirectory() as td:
    r=Path(td)
    (r/'a.py').write_text('''import pandas as pd\nimport matplotlib.pyplot as plt\nfrom sklearn.model_selection import train_test_split\nP="E:/data/train.csv"\ndef main():\n    df=pd.read_csv("train.csv")\n    plt.plot(df.iloc[:,0]); plt.savefig("figure.png")\n''',encoding='utf-8')
    (r/'bad.py').write_text('def broken(:\n    pass\n',encoding='utf-8')
    rep=mod.audit(r)
    py={x['path']:x for x in rep['python']}
    ok(py['a.py']['syntax']=='PASS','valid python passes syntax')
    ok(py['bad.py']['syntax']=='FAIL','invalid python fails syntax')
    ok('train.csv' in rep['data_references'],'data dependency found')
    ok(any(x.startswith('E:/data') for x in rep['hardcoded_absolute_paths']),'windows absolute path found')
    ok('a.py' in rep['plotting_files'],'plotting file found')
    ok('a.py' in rep['split_related_files'],'split-related file found')

root=Path.cwd()
ok((root/'knowledge_base/code_cases/2025-E-GTeacher1-code.json').exists(),'GTeacher1 code card exists')
ok((root/'knowledge_base/code_cases/2025-E-GTeacher2-code.json').exists(),'GTeacher2 code card exists')
ok((root/'knowledge_base/figure_argumentation/2025-E-GTeacher2-code.json').exists(),'GTeacher2 figure card exists')
idx=json.loads((root/'learning_sources/source_index.json').read_text(encoding='utf-8'))
ids={x['source_id'] for x in idx['sources']}
ok({'GT2025E-G1-Q1-CODE','GT2025E-G1-Q2-CODE','GT2025E-G2-CODE','GT2025E-G2-RESULTS'} <= ids,'supplemental sources indexed')
print(json.dumps({'scope':'v1.8 code/paper/figure learning regressions','passed':len(passed),'tests':passed},ensure_ascii=False,indent=2))
