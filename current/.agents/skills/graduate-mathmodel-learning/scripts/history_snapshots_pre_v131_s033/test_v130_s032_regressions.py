from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
A=ROOT/'.agents/skills/mathmodel-case-retriever/assets'
checks=[]
def ck(name,cond):
 if not cond: raise AssertionError(name)
 checks.append(name)
P={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
ck('S032 train',P['S032']['split']=='train'); ck('S032 pages71',P['S032']['pages']==71); ck('S032 reviewed all',P['S032']['reviewed_pages']==list(range(1,72))); ck('S032 R2',P['S032']['reproduction_level']=='R2')
for f in ['knowledge_base/paper_reviews/2025-C-S032-core.json','knowledge_base/candidate_competitions/S032.json','knowledge_base/result_registry/S032.json','knowledge_base/code_cases/2025-C-S032-appendix-code.json','knowledge_base/figure_argumentation/S032.json','knowledge_base/method_modules/2025-C-S032-modules.json','knowledge_base/cross_paper_maps/2025-C-S032-S036.json','knowledge_base/figure_decision_rules/2025-C-provisional.json']:
 ck('asset '+f,(ROOT/f).exists())
reg=json.loads((ROOT/'knowledge_base/result_registry/S032.json').read_text(encoding='utf-8'))
ids={e['id'] for e in reg['entries']}
for x in ['Q1_METRIC_TABLE','Q2_EXTREME_FIT','Q3_JRC_RANGE_CONFLICT','Q3_SCALE_FACTOR_INJECTION','Q4_SCORE_COMPARISON','Q4_ENTROPY_IMPLEMENTATIONS','Q4_GA_CROSSOVER','Q4_DDENSITY_DIRECTION','Q2_AMPLITUDE_SEMANTICS','Q3_CURVATURE_SAMPLING_DIRECTION','Q4_PJRC_FORMULA_CONFLICT','Q4_ADJACENCY_CONTRACT','Q2_Q3_ORACLE_INTERMEDIATE_BYPASS']:
 ck('registry '+x,x in ids)
code=json.loads((ROOT/'knowledge_base/code_cases/2025-C-S032-appendix-code.json').read_text(encoding='utf-8'))
for x in ['Q1_SPLIT_LOADER_MISSING','Q2_ROBUST_FIT_NOT_IMPLEMENTED','Q3_HEADLINE_LOG_ATTENTION_ABSENT','Q3_PER_IMAGE_SCALE_FACTOR','Q4_DENSITY_ENTROPY_BUG','Q4_PPIGA_CODE_ABSENT','Q2_AMPLITUDE_DEFINITION_DRIFT','Q3_CURVATURE_WEIGHT_DIRECTION_REVERSED','Q4_PJRC_FORMULA_PROSE_CONFLICT','Q4_ADJACENCY_PAIR_CONTRACT_DRIFT','Q2_ORACLE_MASK_BYPASS','Q3_ORACLE_MASK_BYPASS']:
 ck('code '+x, any(a['id']==x for a in code['findings']))
# generic gates learned from S032
for fn in ['metric-identity-requires-aggregation-provenance.json','fit-plausibility-and-reject-gate.json','calibration-constant-provenance.json','clipping-saturation-invalidates-association.json','histogram-density-is-not-discrete-probability.json','endogenous-score-not-external-validation.json','duplicate-crossover-offspring.json','pseudo-probability-needs-calibration.json','upstream-uncertainty-must-propagate.json','oracle-intermediate-bypass.json']:
 ck('generic '+fn,(ROOT/'knowledge_base/error_patterns'/fn).exists())
# Dev reserve/Test protection
for pid in ['S030','S031']:
 ck(pid+' dev',P[pid]['split']=='dev'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
for pid in ['S021','S022','S023','S024','S037','S038']:
 ck(pid+' test',P[pid]['split']=='test'); ck(pid+' unread',P[pid].get('reviewed_pages',[])==[])
# Manifest and source hash contract
ck('split sha',hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()=='0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347')
sa=json.loads((ROOT/'learning_output/analyses/S032_source_audit.json').read_text(encoding='utf-8'))
ck('S032 source hash',sa['sha256']=='6f14d27f0371e94857a592c7469eeec37172009384bdba8a847c26019e8d96c8'); ck('visual 71', '71/71' in sa['visual_audit'])
# Capability/persistence prompt is stored
pr=(ROOT/'MathModel-Core_采纳后统一训练提示词_v1.30.txt').read_text(encoding='utf-8')
for term in ['Capability Evidence Gate','Controlled Core Ablation','Persistent Evidence Contract','Lean Core + Retrieval','No-Core / Previous-Core / New-Core']:
 ck('prompt '+term,term in pr)
# Fit identity calculations preserved
q1=reg['entries'][0]['reported']
for name,expected in [('morphology',0.7623762376),('UNet',0.7908101572),('improved_UNet',0.8445984980)]:
 iou=q1[name]['IoU_pct']/100; calc=2*iou/(1+iou); ck('IoU-F1 calc '+name,abs(calc-expected)<1e-8)
# all other Train papers not silently marked reviewed beyond existing state; S033 remains unread
ck('S033 unread',P['S033'].get('reviewed_pages',[])==[])
# exact count for stable specialist suite. First execution revealed the suite contains 63 substantive checks; the hard-coded 62 was a harness bookkeeping error, not a failed semantic check.
assert len(checks)==75, len(checks)
print(f'PASS {len(checks)}/{len(checks)}')
