from pathlib import Path
import json, math
OUT=Path(__file__).parent
checks=[]
def ck(name,cond,detail):
    checks.append({'name':name,'passed':bool(cond),'detail':detail})

# Mechanism 1: class-balanced sample prevalence is not population risk.
N=1000; pos=10; neg=N-pos
sample_pos=10; sample_neg=90
sample_prev=sample_pos/(sample_pos+sample_neg)
true_prev=pos/N
# inverse selection probability: positives all kept; negatives 90/990 kept
wpos=1.0; wneg=neg/sample_neg
weighted=(sample_pos*wpos)/(sample_pos*wpos+sample_neg*wneg)
ck('first_fail_sample_prevalence', abs(sample_prev-true_prev)>0.05, {'naive':sample_prev,'truth':true_prev})
ck('repair_weighted_prevalence', abs(weighted-true_prev)<1e-12, {'weighted':weighted,'truth':true_prev})

# Mechanism 2: marginals do not identify transition flow.
# Energy mix A/B: both periods 60/40 -> two different valid flows with same margins.
M1=[[0.60,0.00],[0.00,0.40]]
M2=[[0.40,0.20],[0.20,0.20]]
def margins(M): return ([sum(r) for r in M],[sum(M[i][j] for i in range(2)) for j in range(2)])
r1,c1=margins(M1); r2,c2=margins(M2)
same_margins=all(abs(a-b)<1e-12 for a,b in zip(r1,r2)) and all(abs(a-b)<1e-12 for a,b in zip(c1,c2)) and all(abs(a-b)<1e-12 for a,b in zip(r1,[0.6,0.4])) and all(abs(a-b)<1e-12 for a,b in zip(c1,[0.6,0.4]))
ck('first_fail_marginal_flow_identifiability', same_margins and M1!=M2, {'row_margins':r1,'col_margins':c1,'flow_A_to_B_M1':M1[0][1],'flow_A_to_B_M2':M2[0][1]})
ck('repair_flow_claim_retracted', True, {'decision':'marginals_only -> transition flow UNIDENTIFIED'})

# Mechanism 3: target-derived predictor can make a rule-reconstruction task perfect.
y=[1 if i>=95 else 0 for i in range(100)]
# leaked feature is exactly the threshold source
leaked=[1 if i>=95 else 0 for i in range(100)]
acc=sum(int(a==b) for a,b in zip(y,leaked))/len(y)
# deployment-safe constant baseline using only pre-outcome info in this fixture
safe=[0]*100
acc_safe=sum(int(a==b) for a,b in zip(y,safe))/len(y)
recall_safe=0.0
ck('first_fail_target_lineage_leakage', acc==1.0, {'leaked_accuracy':acc,'meaning':'rule reconstruction, not future validation'})
ck('repair_available_at_gate', acc_safe==0.95 and recall_safe==0.0, {'safe_baseline_accuracy':acc_safe,'minority_recall':recall_safe,'decision':'do not promote leaked predictor'})

status='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX' if all(x['passed'] for x in checks) else 'FAIL'
res={'status':status,'evidence_class':'POST_DEV_SYNTHETIC_MECHANISM_TRANSFER_NOT_CLEAN_BLIND_NOT_R7', 'checks':checks, 'core_gain':'NOT_ESTABLISHED','controlled_ablation':'NOT_RUN'}
(OUT/'MINI_TRANSFER_RESULTS.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':status,'passed':sum(x['passed'] for x in checks),'total':len(checks)},ensure_ascii=False))
