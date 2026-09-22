from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[4]
A=R/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(n,c):
    if not c: raise AssertionError(n)
    checks.append(n)
ck('version 1.31.0',(R/'VERSION').read_text().strip()=='1.31.0')
for f in ['PROGRESS_V131.md','VALIDATION_V131.md','S033_v1.31_训练摘要.md','knowledge_base/paper_reviews/2025-C-S033-core.json','knowledge_base/candidate_competitions/S033.json','knowledge_base/result_registry/S033.json','knowledge_base/code_cases/2025-C-S033-appendix-code.json','knowledge_base/figure_argumentation/S033.json','knowledge_base/method_modules/2025-C-S033-modules.json','knowledge_base/cross_paper_maps/2025-C-S032-S036.json','learning_output/analyses/S033_result_registry_replay.json','learning_output/analyses/historical_test_adaptation_v131.md']:
    ck('exists '+f,(R/f).exists())
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
ck('45 papers',len(P)==45)
ck('split 32/7/6',{s:sum(p['split']==s for p in P.values()) for s in ['train','dev','test']}=={'train':32,'dev':7,'test':6})
ck('split hash',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('S033 reviewed R2',P['S033']['split']=='train' and P['S033']['reproduction_level']=='R2' and P['S033']['reviewed_pages']==list(range(1,79)))
ck('S034-36 unread',all(P[x].get('reviewed_pages',[])==[] for x in ['S034','S035','S036']))
ck('S030-31 dev unread',all(P[x]['split']=='dev' and P[x].get('reviewed_pages',[])==[] for x in ['S030','S031']))
ck('test unread',all(p.get('reviewed_pages',[])==[] for p in P.values() if p['split']=='test'))
state=json.loads((R/'learning_output/context/learning_state.json').read_text(encoding='utf-8'))
ck('state latest S033',state['current_version']=='1.31.0' and state['latest_completed_paper']=='S033')
nextt=(R/'learning_output/context/next_learning.md').read_text(encoding='utf-8')
ck('next S034','S034' in nextt and 'Mini Transfer Test' in nextt and 'NOT_DUE' in nextt)
mp=json.loads((R/'knowledge_base/cross_paper_maps/2025-C-S032-S036.json').read_text(encoding='utf-8'))
ck('map 2/5',mp['papers_reviewed']==['S032','S033'] and mp['papers_pending']==['S034','S035','S036'])
retr=(A/'search_cases.py') if False else R/'.agents/skills/mathmodel-case-retriever/scripts/search_cases.py'
src=retr.read_text(encoding='utf-8')
ck('ordinary retriever train-only',"x['split']=='train'" in src and 'reviewed_pages' in src)
rskill=(R/'.agents/skills/mathmodel-case-retriever/SKILL.md').read_text(encoding='utf-8')
ck('retriever docs safe','evaluation` 与 `--mode production` 均只允许从 **reviewed Train pages**' in rskill)
prog=(R/'PROGRESS_V131.md').read_text(encoding='utf-8'); val=(R/'VALIDATION_V131.md').read_text(encoding='utf-8')
ck('progress says R2','Reproduction level: **R2**' in prog)
ck('validation release pass','**PASS. v1.31 may be sealed.**' in val)
ck('capability boundary','does **not** prove' in val and 'No-Core' in val)
replay=json.loads((R/'learning_output/analyses/S033_result_registry_replay.json').read_text(encoding='utf-8'))
ck('registry replay 11',replay['status']=='PASS' and replay['pass_count']==11)
ck('historical snapshot preserved',(R/'.agents/skills/graduate-mathmodel-learning/scripts/history_snapshots_pre_v131_s033/test_v130_s032_regressions.py').exists())
print(f'PASS {len(checks)}/{len(checks)} release checks')
