from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[4]
try:
 st=json.loads((ROOT/'learning_output/context/learning_state.json').read_text()); assert st['current_version']=='1.33.0'; assert st['latest_completed_paper']=='S035'; assert (ROOT/'VERSION').read_text().strip()=='1.33.0'
 for f in ['PROGRESS_V133.md','VALIDATION_V133.md','S035_v1.33_训练摘要.md','knowledge_base/paper_reviews/2025-C-S035-core.json','learning_output/analyses/S035_source_audit.json']: assert (ROOT/f).exists()
 print('PASS v1.33 release contract')
except Exception as e:
 print('FAIL',e); sys.exit(1)
