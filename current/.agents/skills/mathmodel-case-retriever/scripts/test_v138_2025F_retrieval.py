from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[4]; A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
papers=json.loads((A/'papers.json').read_text(encoding='utf-8')); items=papers['papers'] if isinstance(papers,dict) else papers; P={p['paper_id']:p for p in items}
sp=Path(__file__).resolve().parent/'search_cases.py'; spec=importlib.util.spec_from_file_location('search_cases_v138',sp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
queries=['GMM MRF 开合节奏 寄畅园 灵敏度 Kendall 鹤园 相似度','园林 路线 骨架 异景 遗传算法 Dijkstra','余弦 Jaccard 鹤园 相似度 标准化']
found=False
for mode in ['evaluation','production']:
  for q in queries:
    out=mod.search(q,mode=mode,top=8); assert out['matches'],(mode,q)
    ids=[m['paper_id'] for m in out['matches']]
    if 'S045' in ids[:5]: found=True
    for x in out['matches']:
      p=P[x['paper_id']]; assert p['split']=='train',(mode,x['paper_id'],p['split']); assert x['page'] in p.get('reviewed_pages',[]),(mode,x['paper_id'],x['page'])
      assert x['paper_id'] not in {'S013','S014','S015','S016','S021','S022','S023','S024','S029','S030','S031','S037','S038'}
assert found
out=mod.search(queries[0],mode='production',top=10); m=next((x for x in out['matches'] if x['paper_id']=='S045'),None); assert m is not None
assert m['same_problem_cross_paper_map']['status']=='FINAL_FOUR_OF_FOUR_TRAIN_PAPERS_REVIEWED'
assert m['mathmodel_core_summary']['reproduction_level']=='R2'
print('PASS v1.38 2025-F retrieval: S045 found; evaluation/production reviewed-Train-only; final 4/4 map attached')
