"""Fast replay of saved selected policies, independent of archived directories."""
from solve import ROOT, run
import json

inputs = json.loads((ROOT/'inputs.json').read_text(encoding='utf-8'))
checks = []
for key in ['result11', 'result12', 'result21', 'result22']:
    saved = json.loads((ROOT/'results'/f'{key}.json').read_text(encoding='utf-8'))
    sim, score = run(inputs[f"附件{saved['dataset']}"], saved['question'], saved['prefs'], weights=saved['weights'])
    assert score == saved['score']
    assert sim.output == saved['output_sequence']
    matrix = [[None]+list(range(score['T']+1))]+sim.matrix_rows(score['T'])
    assert matrix == json.loads((ROOT/'results'/f'{key}_matrix.json').read_text(encoding='utf-8'))
    checks.append(dict(id=key, status='PASS', score=score['total']))
    print(key, 'PASS', score['total'], flush=True)
(ROOT/'results'/'SELECTED_REPLAY.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
