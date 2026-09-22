from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[4]
try:
 assert (ROOT/'VERSION').read_text().strip()=='1.35.0'
 st=json.loads((ROOT/'learning_output/context/learning_state.json').read_text()); assert st['current_version']=='1.35.0'; assert st['latest_completed_paper']=='S042'
 for f in ['PROGRESS_V135.md','VALIDATION_V135.md','S042_v1.35_训练摘要.md','knowledge_base/cross_paper_maps/2025-F-S042-S045.json','knowledge_base/result_registry/S042.json','knowledge_base/code_cases/2025-F-S042-appendix-code.json']: assert (ROOT/f).exists() and (ROOT/f).stat().st_size>0
 p={x['paper_id']:x for x in json.loads((ROOT/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text())}; assert p['S042']['reviewed_pages']==list(range(1,183)); assert all(p[x]['reviewed_pages']==[] for x in ['S043','S044','S045','S037','S038'])
 print('PASS v1.35 release contract')
except Exception as e:
 print('FAIL',e); sys.exit(1)
