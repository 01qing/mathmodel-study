from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
sp=Path(__file__).resolve().parent/'search_cases.py'
spec=importlib.util.spec_from_file_location('search_cases_v131',sp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
q='Canny GMM 神经网络 二阶导数 信息熵 补充钻孔'
for mode in ['evaluation','production']:
    out=mod.search(q,mode=mode,top=6)
    assert out['matches'], mode
    top=out['matches'][0]
    assert top['paper_id']=='S033', (mode,top['paper_id'],top['page'])
    assert top['same_problem_cross_paper_map']['status']=='PROVISIONAL_2_OF_5_TRAIN_PAPERS'
    assert top['mathmodel_core_summary']['reproduction_level']=='R2'
    for m in out['matches']:
        p=P[m['paper_id']]
        assert p['split']=='train', (mode,m['paper_id'],p['split'])
        assert m['page'] in p.get('reviewed_pages',[]), (mode,m['paper_id'],m['page'])
        assert m['paper_id'] not in {'S013','S014','S015','S016','S021','S022','S023','S024','S029','S030','S031','S037','S038'}
print('PASS v1.31 2025-C retrieval: S033 top; evaluation/production reviewed-Train-only')
