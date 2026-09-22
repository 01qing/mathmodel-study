from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[4]
try:
 assert (ROOT/'VERSION').read_text().strip()=='1.36.0'
 st=json.loads((ROOT/'learning_output/context/learning_state.json').read_text()); assert st['current_version']=='1.36.0'; assert st['latest_completed_paper']=='S043'
 for f in ['PROGRESS_V136.md','VALIDATION_V136.md','S043_v1.36_训练摘要.md','knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/result_registry/S043.json','knowledge_base/code_cases/2025-F-S043-code-access.json']: assert (ROOT/f).exists() and (ROOT/f).stat().st_size>0
 p={x['paper_id']:x for x in json.loads((ROOT/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text())}; assert p['S043']['reviewed_pages']==list(range(1,72)); assert all(p[x]['reviewed_pages']==[] for x in ['S044','S045','S037','S038']); assert all(p[x]['reviewed_pages']==[] for x in ['S030','S031'])
 print('PASS v1.36 release contract')
except Exception as e:
 print('FAIL',e); sys.exit(1)
