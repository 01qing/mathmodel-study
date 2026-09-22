from pathlib import Path
import json, hashlib, importlib.util
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(name, cond):
    if not cond: raise AssertionError(name)
    checks.append(name)
pre=ROOT/'learning_output/dev_validation/2025-B-S029/pre_solution_baseline.md'
post=ROOT/'learning_output/dev_validation/2025-B-S029/post_solution_gap_analysis.md'
ck('pre exists', pre.exists())
ck('post exists', post.exists())
ck('freeze sha', hashlib.sha256(pre.read_bytes()).hexdigest()=='f0c9a3e4878c8b16272b8e9c1634e08008aa4c712b3cf1fe3fe9090cafc8341e')
papers=json.loads((A/'papers.json').read_text(encoding='utf-8')); P={p['paper_id']:p for p in papers}
ck('S029 dev', P['S029']['split']=='dev')
ck('S029 pages57', P['S029']['pages']==57)
ck('S029 reviewed exact', P['S029']['reviewed_pages']==list(range(1,58)))
ck('S029 R2 ceiling', P['S029']['reproduction_level']=='R2_DEV_EQUIVALENT')
ck('S029 dev boundary', P['S029']['dev_boundary']=='DEV_ONLY_NOT_TRAIN_RETRIEVAL')
ck('S029 review file', P['S029']['review_file'].endswith('post_solution_gap_analysis.md'))
ck('S029 baseline file', P['S029']['dev_baseline_file'].endswith('pre_solution_baseline.md'))
for pid in ['S030','S031']:
    ck(pid+' dev reserve', P[pid]['split']=='dev')
    ck(pid+' unread', P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
    ck(pid+' test', P[pid]['split']=='test')
    ck(pid+' unread', P[pid].get('reviewed_pages',[])==[])
for fn in ['group-independence-not-row-balance.json','unlabeled-target-alignment-not-accuracy.json','target-batch-statistics-transductive-contract.json','planned-significance-not-result.json','appendix-wrapper-not-self-contained.json']:
    ck('generic '+fn, (ROOT/'knowledge_base/error_patterns'/fn).exists())
ref=(ROOT/'.agents/skills/graduate-mathmodel-learning/references/dev-validation-and-retrieval-boundary.md').read_text(encoding='utf-8')
for term in ['split=train','reviewed_pages','freeze Core','independent solution freeze','Dev-specific','Test solution content']:
    ck('boundary '+term, term in ref)
src=(ROOT/'.agents/skills/mathmodel-case-retriever/scripts/search_cases.py').read_text(encoding='utf-8')
for term in ["x['split']=='train'","reviewed_pages","mode not in ['evaluation','production']","candidate_pool_groups"]:
    ck('retriever source '+term, term in src)
ck('split sha', hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
ck('papers45', len(papers)==45)
counts={k:sum(p['split']==k for p in papers) for k in ['train','dev','test']}
ck('train32', counts['train']==32)
ck('dev7', counts['dev']==7)
ck('test6', counts['test']==6)
chunks=json.loads((A/'chunks.json').read_text(encoding='utf-8'))
ck('chunks6752', len(chunks)==6752)
groups={}
for p in papers: groups.setdefault(p['case_group'],set()).add(p['split'])
ck('case group isolation', all(len(v)==1 for v in groups.values()))
for pid in ['S039','S040','S041']:
    ck(pid+' train', P[pid]['split']=='train')
    ck(pid+' reviewed backfill', P[pid].get('reviewed_pages')==list(range(1,P[pid]['pages']+1)))
pt=post.read_text(encoding='utf-8')
for term in ['Random row split','Unlabeled target','transductive','Headline metrics','significance','self-contained']:
    ck('post '+term, term in pt)
pret=pre.read_text(encoding='utf-8')
for term in ['EESM + monotonic rate calibration','SVD-derived TxBF','group/trajectory/location/terminal holdout','6-hour Baseline']:
    ck('pre '+term, term in pret)
# Actual retriever behavior in both ordinary modes.
sp=ROOT/'.agents/skills/mathmodel-case-retriever/scripts/search_cases.py'
spec=importlib.util.spec_from_file_location('search_cases_v129',sp); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
outs=[mod.search('NPU 缓存 调度',mode='evaluation',top=4), mod.search('轴承 迁移学习 故障诊断',mode='production',top=4)]
def safe(out):
    for m in out['matches']:
        p=P[m['paper_id']]
        if p['split']!='train' or m['page'] not in p.get('reviewed_pages',[]): return False
    return True
ck('evaluation reviewed-train only', safe(outs[0]))
ck('production reviewed-train only', safe(outs[1]))
ck('ordinary retrieval excludes dev-test', all(m['paper_id'] not in {'S013','S014','S015','S016','S021','S022','S023','S024','S029','S030','S031','S037','S038'} for o in outs for m in o['matches']))
assert len(checks)==67, len(checks)
print(f'PASS {len(checks)}/{len(checks)}')
