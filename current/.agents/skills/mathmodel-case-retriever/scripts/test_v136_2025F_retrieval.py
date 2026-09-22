from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
sp=Path(__file__).resolve().parent/'search_cases.py'
spec=importlib.util.spec_from_file_location('search_cases_v136',sp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
q='寄畅园 幻境感 20维 Ward 0.847'
for mode in ['evaluation','production']:
    out=mod.search(q,mode=mode,top=4)
    assert out['matches'], mode
    assert any(m['paper_id']=='S043' for m in out['matches'][:3]), (mode,[m['paper_id'] for m in out['matches']])
    m43=next(m for m in out['matches'] if m['paper_id']=='S043')
    assert m43['same_problem_cross_paper_map']['status']=='PROVISIONAL_TWO_OF_FOUR_TRAIN_PAPERS_REVIEWED'
    assert m43['mathmodel_core_summary']['reproduction_level']=='R1'
    for m in out['matches']:
        p=P[m['paper_id']]
        assert p['split']=='train', (mode,m['paper_id'],p['split'])
        assert m['page'] in p.get('reviewed_pages',[]), (mode,m['paper_id'],m['page'])
        assert m['paper_id'] not in {'S013','S014','S015','S016','S021','S022','S023','S024','S029','S030','S031','S037','S038'}
print('PASS v1.36 2025-F retrieval: S043 top-3; evaluation/production reviewed-Train-only')
