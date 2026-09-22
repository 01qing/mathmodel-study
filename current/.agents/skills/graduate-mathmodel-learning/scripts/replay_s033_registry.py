from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[4]
out=[]
def check(name, condition, observed=None, expected=None):
    if not condition:
        raise AssertionError(f'{name}: observed={observed!r} expected={expected!r}')
    out.append({'check':name,'status':'PASS','observed':observed,'expected':expected})

# Q2 Table 1 arithmetic replay.
a=[0.3810,0.5924,0.8129,0.7408,0.6472,0.8926,0.0462,0.6926,0.4720]
b=[0.4992,0.6938,0.9177,0.8826,0.8607,0.8915,0.8218,0.8137,0.7918]
ma=sum(a)/len(a); mb=sum(b)/len(b)
check('Q2 table has nine rows',len(a)==len(b)==9,9,9)
check('Q2 GD/Newton mean replay',abs(ma-0.5864111111111111)<1e-12,ma,0.5864111111111111)
check('Q2 NN/Adam mean replay',abs(mb-0.7969777777777778)<1e-12,mb,0.7969777777777778)
check('Q2 reported 0.587 is rounding-compatible',abs(ma-0.587)<0.001,ma,0.587)
check('Q2 reported 0.795 is only approximate',abs(mb-0.795)<0.003,mb,0.795)

# Q4 hard feasibility replay: this is a PASS when the audit correctly detects an author-result violation.
required=500.0; row3=412.3105; code_threshold=300.0
check('Q4 author row3 violates stated 500mm spacing',row3<required,row3,'<500')
check('Q4 printed code threshold differs from body hard constraint',code_threshold!=required,code_threshold,required)

# Bernoulli entropy semantic replay at p=0.5.
p=0.5
paper_term=-p*math.log2(p)
bernoulli=-(p*math.log2(p)+(1-p)*math.log2(1-p))
check('Q4 paper entropy term differs from Bernoulli entropy',abs(paper_term-bernoulli)>1e-12,paper_term,bernoulli)
check('Q4 Bernoulli entropy at p=.5 equals 1 bit',abs(bernoulli-1.0)<1e-12,bernoulli,1.0)

# Body/code depth incompatibility.
body_lower=[2000,3000,4000,6000]
code_max=500
check('Q4 deep body intervals excluded by visible loader',all(x>code_max for x in body_lower),body_lower,f'> {code_max}')

# Fixed-vs-estimated period contract.
Pvals=[94.25]*9
check('Q2 final displayed period constant across rows',len(set(Pvals))==1,Pvals[0],'single fixed value')

payload={
 'paper_id':'S033','case_group':'2025-C','version':'1.31.0',
 'scope':'Audit/replay checks only. PASS means the registered arithmetic/semantic inconsistency was reproducibly checked; it is not author-code reproduction and does not raise S033 above R2.',
 'checks':out,'pass_count':len(out),'status':'PASS'
}
p=ROOT/'learning_output/analyses/S033_result_registry_replay.json'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'PASS {len(out)}/{len(out)} -> {p}')
