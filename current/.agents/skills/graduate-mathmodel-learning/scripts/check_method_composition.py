#!/usr/bin/env python3
from pathlib import Path
import argparse,json
GATES=['input_output_interface','variable_definition','data_distribution','mathematical_assumptions','units_and_dimensions','training_vs_execution_stage','evaluation_metric']
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('contract',type=Path); a=ap.parse_args(); o=json.loads(a.contract.read_text(encoding='utf-8'))
 c=o.get('compatibility',o); missing=[g for g in GATES if g not in c]; blocking=[g for g in GATES if c.get(g) in ['incompatible','unknown',None]]
 print(json.dumps({'status':'PASS' if not missing else 'INCOMPLETE','missing_gates':missing,'blocking_gates':blocking,'mainline_recommendation_allowed':not missing and not blocking},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
