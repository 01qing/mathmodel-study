#!/usr/bin/env python3
"""Non-destructive MathModel-Core schema coverage report for legacy review cards.
Default behavior does NOT rewrite S001-S020. Use the report to decide demand-driven backfill.
"""
from pathlib import Path
import json,argparse
R=Path(__file__).resolve().parents[4]
REQ=['candidate_model_competition','six_hour_baselines','result_registry_ref','transferable_modules_ref','reproduction']
def main():
 p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=R/'learning_output/analyses/core_schema_legacy_coverage.json'); a=p.parse_args()
 rows=[]
 for f in sorted((R/'knowledge_base/paper_reviews').glob('*-core.json')):
  o=json.loads(f.read_text(encoding='utf-8')); pid=o.get('paper_id',f.stem)
  missing=[k for k in REQ if k not in o]
  rows.append({'paper_id':pid,'file':str(f.relative_to(R)),'core_schema_version':o.get('core_schema_version'),'missing_new_protocol_fields':missing,'action':'NO_AUTO_REREAD; backfill on demand' if missing else 'CURRENT_SCHEMA'})
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps({'schema':'MathModel-Core v1','legacy_policy':'non-destructive','cards':rows},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'status':'PASS','cards':len(rows),'output':str(a.output)},ensure_ascii=False))
if __name__=='__main__': main()
