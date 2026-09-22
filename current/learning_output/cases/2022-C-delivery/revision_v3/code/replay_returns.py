from return_solver import ROOT,execute
from validate_returns import validate
import json

inputs=json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'));reports={}
for key in ['result11','result12','result21','result22']:
    saved=json.loads((ROOT/'results'/f'{key}.json').read_text(encoding='utf-8'))
    records=inputs[f"附件{saved['dataset']}"]
    result,matrix=execute(records,saved['question'],saved['prefs'],saved['return_policy'])
    assert result['score']==saved['score'] and result['output_sequence']==saved['output_sequence']
    assert matrix==json.loads((ROOT/'results'/f'{key}_matrix.json').read_text(encoding='utf-8'))
    report=validate(result,records,matrix)
    assert report['status']=='PASS',report['errors']
    reports[key]=report
    print(key,report['status'],'returns',result['score']['return_uses'],flush=True)
(ROOT/'results/SELECTED_RETURN_REPLAY.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
