from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
sp=Path(__file__).resolve().parent/'search_cases.py'
spec=importlib.util.spec_from_file_location('search_cases_v137',sp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
q='多模态 AHP 熵权 改进遗传算法 园林 相似度'
for mode in ['evaluation','production']:
    out=mod.search(q,mode=mode,top=6)
    assert out['matches'], mode
    ids=[m['paper_id'] for m in out['matches']]
    assert 'S044' in ids[:4], (mode,ids)
    m=next(x for x in out['matches'] if x['paper_id']=='S044')
    assert m['same_problem_cross_paper_map']['status']=='PROVISIONAL_THREE_OF_FOUR_TRAIN_PAPERS_REVIEWED'
    assert m['mathmodel_core_summary']['reproduction_level']=='R2'
    for x in out['matches']:
        p=P[x['paper_id']]
        assert p['split']=='train', (mode,x['paper_id'],p['split'])
        assert x['page'] in p.get('reviewed_pages',[]), (mode,x['paper_id'],x['page'])
        assert x['paper_id'] not in {'S013','S014','S015','S016','S021','S022','S023','S024','S029','S030','S031','S037','S038'}
print('PASS v1.37 2025-F retrieval: S044 top-4; evaluation/production reviewed-Train-only')
