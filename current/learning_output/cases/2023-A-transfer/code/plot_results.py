from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'results/RESULTS.json').read_text());analytic=json.loads((ROOT/'results/ANALYTIC.json').read_text())
base=[next(x for x in data if x['id']==f'Q{q}_base') for q in range(1,5)]
fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
x=list(range(4));sim=[a['total_mean'] for a in base];ci=[a['ci95_halfwidth'] for a in base]
ax.bar([v-.18 for v in x],sim,.35,color='#196b87',yerr=ci,capsize=4,label='Event simulation (95% MC interval)')
ax.bar([v+.18 for v in x],[analytic[f'q{q}']['total_mbps'] for q in range(1,5)],.35,color='#d9903d',label='Numerical model: exact only for Q2')
ax.set_xticks(x,['Q1','Q2','Q3','Q4']);ax.set_ylabel('Aggregate throughput (Mbps)');ax.legend(fontsize=9)
ax.set_title('Model comparison under declared exchange-sensing assumptions')
ax.spines[['top','right']].set_visible(False);fig.savefig(ROOT/'deliverables/model_comparison.png',dpi=160)
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
q4=base[3];axes[0].bar(['AP1','AP2','AP3'],q4['per_node_mean'],color=['#196b87','#d9903d','#196b87'])
axes[0].set_title('Q4: central-node disadvantage');axes[0].set_ylabel('Throughput (Mbps)')
for i,v in enumerate(q4['per_node_mean']):axes[0].text(i,v+.6,f'{v:.2f}',ha='center')
for rate,color in [(286.8,'#196b87'),(158.4,'#d9903d')]:
 rows=[next(d for d in data if d['id']==f'Q3_{rate}_W{w}_r{r}') for w,r in [(16,6),(32,5),(16,32)]]
 axes[1].errorbar(range(3),[d['total_mean'] for d in rows],yerr=[d['ci95_halfwidth'] for d in rows],marker='o',capsize=4,label=f'{rate} Mbps',color=color)
axes[1].set_xticks(range(3),['W16 / r6','W32 / r5','W16 / r32']);axes[1].set_ylabel('Aggregate throughput (Mbps)');axes[1].set_title('Q3: appendix-6 parameter comparison');axes[1].legend()
for a in axes:a.spines[['top','right']].set_visible(False)
fig.savefig(ROOT/'deliverables/hidden_and_fairness.png',dpi=160)
