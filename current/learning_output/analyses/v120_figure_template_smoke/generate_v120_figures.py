from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent

# 1. Effect-size + corrected significance evidence template
names=['Temperature','Waveform','Material','Waveform×Material']
effect=np.array([0.06,0.31,0.14,0.12])
lo=np.array([0.04,0.28,0.11,0.09])
hi=np.array([0.08,0.34,0.17,0.15])
adj_p=np.array([0.004,0.0001,0.0003,0.001])
y=np.arange(len(names))
fig,ax=plt.subplots(figsize=(7.2,4.4))
ax.errorbar(effect,y,xerr=[effect-lo,hi-effect],fmt='o',capsize=4)
ax.axvline(0,linewidth=1)
ax.set_yticks(y,names)
ax.set_xlabel('Adjusted effect size (template)')
ax.set_title('Effect size + uncertainty; significance is secondary')
for i,(e,p) in enumerate(zip(effect,adj_p)):
    ax.text(hi[i]+0.01,i,f'adj p={p:.3g}',va='center',fontsize=9)
fig.tight_layout(); fig.savefig(OUT/'01_effect_size_corrected_tests.png',dpi=180); plt.close(fig)

# 2. Mixed-variable feasibility replay template
labels=['Paper lower f','Code lower f','Reported f','Replayed f']
vals=[50000,5000,7862.85,7862.85]
fig,ax=plt.subplots(figsize=(7.2,4.2))
ax.bar(labels,vals)
ax.axhline(50000,linestyle='--',linewidth=1,label='paper feasible lower bound')
ax.set_ylabel('Frequency (Hz)')
ax.set_title('Paper–code domain registry / reported-point feasibility')
ax.legend()
ax.tick_params(axis='x',rotation=18)
fig.tight_layout(); fig.savefig(OUT/'02_domain_feasibility_replay.png',dpi=180); plt.close(fig)

# 3. Scalarized objective replay template
lam=np.array([0.01,0.1,1,10,100])
reported=np.array([1.05,-21.15,-2215.32,-5945538.16,-106854.87])
replayed=np.array([1.0481,-21.151,-2215.32,3644533.5,-1786213.46])
fig,ax=plt.subplots(figsize=(7.2,4.2))
idx=np.arange(len(lam)); w=0.38
ax.bar(idx-w/2,reported,w,label='reported L')
ax.bar(idx+w/2,replayed,w,label='replayed L')
ax.set_xticks(idx,[str(x) for x in lam])
ax.set_xlabel('lambda')
ax.set_ylabel('Scalarized objective')
ax.set_title('Result-table objective replay')
ax.legend()
fig.tight_layout(); fig.savefig(OUT/'03_scalarized_objective_replay.png',dpi=180); plt.close(fig)
print('generated',3,'figures in',OUT)
