from pathlib import Path
import sys,json,zipfile,io,pickle,collections
OUT=Path(__file__).parent;sys.path.insert(0,str(OUT/'runtime_deps'));sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
ROOT=Path(r'D:\softdown\codex\mathmodel-study\current');SRC=Path(r'D:\数模\数模练习')
class Restricted(pickle.Unpickler):
    def find_class(self,m,n):
        if (m,n) in [('numpy','asarray'),('numpy','ndarray'),('numpy','dtype'),('numpy.core.multiarray','_reconstruct'),('numpy._core.multiarray','_reconstruct'),('numpy.core.multiarray','scalar'),('numpy._core.multiarray','scalar'),('numpy.core.numeric','_frombuffer'),('numpy._core.numeric','_frombuffer')]:return super().find_class(m,n)
        raise pickle.UnpicklingError(f'{m}.{n}')
out={}
with zipfile.ZipFile(next((SRC/'E题exp').glob('*.zip'))) as z:
    groups={}
    for n in z.namelist():
        if n.endswith('.pkl') and ('附件3-' in n or '附件4-' in n):
            group=('附件3' if '附件3-' in n else '附件4')+('未对齐' if '未对齐版本' in n else '对齐')
            try:
                a=Restricted(io.BytesIO(z.read(n))).load()
                if 'test' in a:a=a['test']
                d={'file':n,'keys':sorted(a.keys())}
                if 'text_bert' in a:
                    v=np.asarray(a['text_bert']);d['text_bert_integral']=bool(np.allclose(v,np.round(v)));d['text_bert_range']=[float(v.min()),float(v.max())]
                groups.setdefault(group,[]).append(d)
            except Exception as e:groups.setdefault(group,[]).append({'file':n,'error':str(e)})
    out['E_special_all']=groups
    print('E feature schema groups:')
    for k,v in groups.items():print(k,len(v),dict(collections.Counter(tuple(x.get('keys',[])) for x in v)))
assets=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
papers=json.loads((assets/'papers.json').read_text(encoding='utf-8'))
counts=collections.Counter((p['case_group'],p['split']) for p in papers)
out['training_group_counts']=[{'group':g,'split':s,'count':n} for (g,s),n in counts.items()]
selected={'S025':[9],'S026':[6],'S011':[25]}
texts=[]
for p in papers:
    if p['paper_id'] in selected:
        assert p['split']=='train'
        pages=json.loads((assets/p['text_pages_file']).read_text(encoding='utf-8'))
        for page in pages:
            if page['page'] in selected[p['paper_id']]:
                assert page['page'] in p['reviewed_pages']
                texts.append(f"## {p['paper_id']} {p['case_group']} 原PDF物理页{page['page']}\n{page['text']}")
(OUT/'training_pages_read.md').write_text('\n\n'.join(texts),encoding='utf-8')
smoke=json.loads((OUT/'A_smoke_results.json').read_text(encoding='utf-8'))
out['A_smoke_summary']=[{'question':r['question'],'exit_code':r.get('exit_code'),'makespan':r.get('result',{}).get('makespan'),'seconds':r.get('elapsed_seconds')} for r in smoke['runs']]
(OUT/'final_evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(out['training_group_counts']);print(out['A_smoke_summary'])
