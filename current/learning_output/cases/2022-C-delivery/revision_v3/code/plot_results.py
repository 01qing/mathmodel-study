from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'results/RETURN_COMPARISON.json').read_text(encoding='utf-8'))
fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
for i,d in enumerate(data):
 for offset,field,label,color in [(-.2,'return_arm_score','Return-enabled search','#d9903d'),(.2,'no_return_arm_score','No-return route search','#196b87')]:
  gain=d[field]-d['v2_score'];ax.bar(i+offset,gain,width=.36,color=color,label=label if i==0 else None)
  ax.text(i+offset,gain+.007,f'{gain:.3f}',ha='center',va='bottom',fontsize=10)
ax.set_xticks(range(4),[d['id'] for d in data]);ax.set_ylim(0,.62)
ax.set_ylabel('Score gain over common v2 starting solution')
ax.set_title('2022-C: 24 candidate evaluations per search arm')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
ax.legend(loc='upper left');fig.savefig(ROOT/'deliverables/result_analysis.png',dpi=160)
