from pathlib import Path
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'results/RESULTS.json').read_text(encoding='utf-8'))
fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), layout='constrained')
for i, d in enumerate(data):
    for shift, field, color, label in [(-.24,'baseline','#bdc7d4','FIFO baseline'),(0,'score','#176b87','Selected policy'),(.24,'cadence_9s_same_policy_sensitivity','#e8a34b','Same policy: 9s arrivals')]:
        axes[0].bar(i+shift,d[field]['total'],width=.24,color=color,label=label if i==0 else None)
    saved=json.loads((ROOT/'results'/f"{d['id']}.json").read_text(encoding='utf-8'))
    best=[]; value=-1e9
    for t in saved['search_trace']:
        value=max(value,t['score']['total']);best.append(value)
    axes[1].plot(range(1,len(best)+1),best,label=d['id'])
axes[0].set_xticks(range(4),[d['id'] for d in data])
axes[0].set_ylabel('Official weighted score')
axes[0].set_title('Baseline and arrival sensitivity')
axes[1].set_title('Best score across evaluated candidates')
axes[1].set_xlabel('Candidate evaluation')
axes[1].set_ylabel('Best score so far')
for ax in axes:
    ax.legend(fontsize=8);ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('2022-C | no-return feasible subset | one fixed search seed',fontsize=12)
fig.savefig(ROOT/'deliverables/result_analysis.png',dpi=160)
