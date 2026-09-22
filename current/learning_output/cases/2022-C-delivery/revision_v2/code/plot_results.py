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
    summary=next(x for x in json.loads((ROOT/'results/MULTISEED_SUMMARY.json').read_text(encoding='utf-8')) if x['id']==d['id'])
    gains=[s-summary['start_score'] for s in summary['scores']]
    axes[1].scatter([i+(j-2)*.05 for j in range(5)],gains,s=35,color='#176b87')
    axes[1].plot([i-.2,i+.2],[summary['median']-summary['start_score']]*2,color='#e8a34b',linewidth=2)
axes[0].set_xticks(range(4),[d['id'] for d in data])
axes[0].set_ylabel('Official weighted score')
axes[0].set_title('Baseline and arrival sensitivity')
axes[1].set_title('Gain over v1: five independent continuations')
axes[1].set_xticks(range(4),[d['id'] for d in data])
axes[1].set_xlabel('Each dot = one seed; orange line = median')
axes[1].set_ylabel('Score gain (60 mutations per seed)')
for ax in axes:
    if ax==axes[0]:ax.legend(fontsize=8)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('2022-C | no-return feasible subset | same warm start for each seed',fontsize=12)
fig.savefig(ROOT/'deliverables/result_analysis.png',dpi=160)
