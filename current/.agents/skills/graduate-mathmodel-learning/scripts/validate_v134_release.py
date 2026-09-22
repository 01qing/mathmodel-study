from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[4]
try:
 st=json.loads((ROOT/'learning_output/context/learning_state.json').read_text()); assert st['current_version']=='1.34.0'; assert st['latest_completed_paper']=='S036'; assert (ROOT/'VERSION').read_text().strip()=='1.34.0'
 for f in ['PROGRESS_V134.md','VALIDATION_V134.md','S036_v1.34_训练摘要.md','knowledge_base/cross_paper_maps/2025-C-S032-S036.json','learning_output/analyses/2025-C_mini_transfer.json','learning_output/analyses/2025-C_capability_evidence_gate.json']: assert (ROOT/f).exists() and (ROOT/f).stat().st_size>0
 mt=json.loads((ROOT/'learning_output/analyses/2025-C_mini_transfer.json').read_text()); assert mt['first_run_status']=='FAIL'; assert mt['status']=='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX'
 print('PASS v1.34 release contract')
except Exception as e:
 print('FAIL',e); sys.exit(1)
