from pathlib import Path
import json,hashlib
from collections import Counter
R=Path(__file__).resolve().parents[4];A=R/'.agents/skills/mathmodel-case-retriever/assets';V=R/'learning_output/validation/v139';checks=[]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(n,c):assert c,n;checks.append(n)
ck('version',(R/'VERSION').read_text().strip()=='1.39.0')
st=load('learning_output/context/learning_state.json');ck('state version',st['current_version']=='1.39.0')
ck('current Dev and historical Train distinguished',st['latest_completed_dev_paper']=='S013' and st['latest_completed_train_paper']=='S045')
ck('R2 only',st['reproduction_level_latest']=='S013:R2')
ck('no capability gain assertion',st['core_gain']=='NOT_ESTABLISHED')
papers=json.loads((A/'papers.json').read_text(encoding='utf-8'));P={p['paper_id']:p for p in papers}
ck('45 / 32-7-6',len(P)==45 and Counter(p['split'] for p in papers)==dict(train=32,dev=7,test=6))
ck('6752 chunks',len(json.loads((A/'chunks.json').read_text(encoding='utf-8')))==6752)
ck('all Train still reviewed',all(p.get('reviewed_pages') for p in papers if p['split']=='train'))
ck('S013 Dev-only113',P['S013']['split']=='dev' and P['S013']['reviewed_pages']==list(range(1,114)) and P['S013']['dev_boundary']=='DEV_ONLY_NOT_TRAIN_RETRIEVAL')
for pid in ['S014','S015','S016','S030','S031','S021','S022','S023','S024','S037','S038']:
    ck(pid+' still unread',P[pid].get('reviewed_pages',[])==[])
ck('frozen split hash',sha(A/'split_manifest.json')=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
base=load('BASELINE_FILES_V138.json');renames={x['old']:x['new'] for x in load('RELEASE_FILENAME_REPAIRS.json')}
allowed={'VERSION','README.md','.agents/skills/graduate-mathmodel-learning/SKILL.md',
         'learning_output/context/learning_state.json','learning_output/context/next_learning.md','.agents/skills/mathmodel-case-retriever/assets/papers.json'}
changed=[];excluded_cache=[]
for path,h in base.items():
    p=R/renames.get(path,path)
    if '__pycache__' in Path(path).parts and path.endswith('.pyc') and not p.exists():
        excluded_cache.append(path);continue
    if not p.is_file() or sha(p)!=h:changed.append(path)
ck('baseline changes confined to release allowlist',set(changed)<=allowed)
ck('original baseline1470 unchanged',load('BASELINE_PRESERVATION_V139.json')['original_core_unchanged'])
ck('retrieval chunks byte identical to baseline',sha(A/'chunks.json')==base['.agents/skills/mathmodel-case-retriever/assets/chunks.json'])
H=R/'learning_output/analyses/dev_2024D_presolution';mf=json.loads((H/'DEV_2024D_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
ck('independent55 frozen files',len(mf['files'])==55 and all(sha(H/k)==v['sha256'] for k,v in mf['files'].items()))
ck('original freeze manifest',sha(H/'DEV_2024D_FREEZE_MANIFEST.json')=='ee139e2a7063fd6cb3a279ae5acba633f2e6784f8afa62d9e51fbc9a1db42a7e')
D=load('DEV_CASE_V139.json');ck('S013 original source included and hash verified',sha(R/D['source'])==D['source_sha256'])
hd=R/'learning_output/dev_validation/2024-D-S013'
ledger=json.loads((hd/'PAGE_AUDIT_LEDGER.json').read_text(encoding='utf-8'))
ck('visual113 evidence files portable',len(ledger['pages'])==113 and all((hd/p['visual_evidence']).is_file() for p in ledger['pages']))
cards=json.loads((hd/'S013_QUESTION_CARDS.json').read_text(encoding='utf-8'));schema=load('knowledge_base/core_schema/mathmodel_core_question_schema_v1.json')
ck('four complete question cards',set(cards['question_cards'])=={'Q1','Q2','Q3','Q4'} and all(all(k in c for k in schema['question_card_fields']) for c in cards['question_cards'].values()))
reg=load(D['registry']);ck('28 key result records',len(reg['entries'])==28)
ck('contradictions not replaced by success',{'contradicted','author_reported','not_reproducible_from_visible_evidence'} <= {x['status'] for x in reg['entries']})
ck('registry evidence files resolve',all((hd/x['evidence_file']).exists() for x in reg['entries']))
composer=json.loads((hd/'S013_METHOD_MAP_AND_COMPOSER.json').read_text(encoding='utf-8'))
ck('seven gates do not mean all pass',len(composer['seven_gates'])==7 and composer['decision'].startswith('DO_NOT_IMPORT'))
ck('Dev case group not prematurely closed',not composer['group_final'])
ck('original failure history retained',(hd/'COUNTEREXAMPLE_RESULTS.json').exists() and (hd/'RECOVERY_STATE_PRE_CLOSURE.json').exists())
ck('contracts18 executed',load('learning_output/validation/v139/contracts.json')['checks']==18 and load('learning_output/validation/v139/contracts.json')['status']=='PASS')
rows=load('learning_output/validation/v139/historical_effective.json')
ck('historical22 plus S045 effective compatibility',len(rows)==23 and all(x['effective_status'] in ['PASS_UNMODIFIED','PASS_ADAPTED'] for x in rows))
ck('original historical failures preserved',any(x['status']=='FAIL' for x in load('learning_output/validation/v139/historical_original.json')))
ck('adapter first-fail preserved',(V/'historical_effective_first_attempt.json').is_file())
ck('retrieval smoke on release',load('learning_output/validation/v139/retrieval.json')['status']=='PASS')
skill=(R/'.agents/skills/graduate-mathmodel-learning/SKILL.md').read_text(encoding='utf-8')
ck('single Core identity and reference reachable','MathModel-Core' in skill and (R/'.agents/skills/graduate-mathmodel-learning/references/dev-data-contracts-v139.md').is_file())
ck('no newly split role Skill',not any((R/'.agents/skills'/x).exists() for x in ['MathModel-Master','MathModel-Architect','MathModel-Engineer','MathModel-Writer','MathModel-Reviewer']))
scope=load('RELEASE_SCOPE_V139.json');ck('pending experiments explicit','independent downstream utility' in scope['pending_nonrelease_goals'] and scope['integrated_model_improvement']=='NOT_ESTABLISHED')
for n in ['PROGRESS_V139.md','REPRODUCTION_V139.md','RELEASE_FILENAME_REPAIRS.json']:
    ck('release document '+n,(R/n).is_file())
out={'status':'PASS','checks':len(checks),'names':checks,'changed_baseline_files':changed,'excluded_compiled_caches':excluded_cache,
     'scope':'release contract / compatibility / integrity; no blind capability gain','original_historical_failures_not_erased':True}
(V/'release_contract.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
