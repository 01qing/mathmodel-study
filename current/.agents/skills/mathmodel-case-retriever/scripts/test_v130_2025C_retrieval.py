from pathlib import Path
import importlib.util, json
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
spec=importlib.util.spec_from_file_location('sc',Path(__file__).with_name('search_cases.py'))
sc=importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
for mode in ['evaluation','production']:
    r=sc.search('围岩裂隙 JRC 正弦拟合 三维重构',mode=mode,top=4)
    assert r['matches'], mode
    assert r['matches'][0]['paper_id']=='S032', (mode,[m['paper_id'] for m in r['matches']])
    for m in r['matches']:
        p=P[m['paper_id']]
        assert p['split']=='train'
        assert m['page'] in p.get('reviewed_pages',[])
        assert m['paper_id'] not in {'S029','S030','S031','S021','S022','S023','S024','S037','S038'}
print('v1.30 2025-C S032 retrieval regression PASS')
