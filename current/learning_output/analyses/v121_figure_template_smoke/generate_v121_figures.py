from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
OUT=Path(__file__).parent

# 1 temporal window split schematic
fig,ax=plt.subplots(figsize=(10,4.8))
ax.set_xlim(0,100); ax.set_ylim(0,4); ax.axis('off')
for y,label,mode in [(2.8,'Unsafe: build overlapping windows, then random split','unsafe'),(1.2,'Preferred: split timeline first, then build windows within each partition','safe')]:
    ax.text(0,y+0.62,label,fontsize=11,weight='bold')
    if mode=='unsafe':
        starts=[5,12,19,26,33,40,47,54,61,68]
        for i,s in enumerate(starts):
            r=Rectangle((s,y),22,0.35,fill=False,linewidth=1.2,linestyle='-' if i%2==0 else '--')
            ax.add_patch(r)
        ax.text(5,y-0.38,'Randomly assigned overlapping windows share timestamps across train/test',fontsize=9)
    else:
        ax.plot([5,90],[y+0.17,y+0.17],linewidth=1.3)
        ax.axvline(62,ymin=0.19,ymax=0.41,linestyle='--',linewidth=1)
        ax.text(30,y-0.38,'Train-only windows',ha='center',fontsize=9)
        ax.text(77,y-0.38,'Test-only windows',ha='center',fontsize=9)
        for s in [7,16,25,34]: ax.add_patch(Rectangle((s,y),18,0.35,fill=False,linewidth=1.2))
        for s in [66,75]: ax.add_patch(Rectangle((s,y),14,0.35,fill=False,linewidth=1.2))
        ax.text(62,y+0.55,'boundary/gap',ha='center',fontsize=9)
fig.tight_layout(); fig.savefig(OUT/'01_temporal_window_split.png',dpi=220,bbox_inches='tight'); plt.close(fig)

# 2 proxy-to-physical calibration sensitivity
proxy=np.linspace(0.1,1.0,180)
fig,ax=plt.subplots(figsize=(8.5,5.2))
for scale in [8,16,24]:
    k=np.clip(scale*proxy,1e-3,None)
    v=120*np.log(25/k)
    v=np.maximum(v,0)
    ax.plot(proxy,v,label=f'proxy→density scale={scale:g}')
ax.axhline(80,linestyle='--',linewidth=1,label='example congestion threshold')
ax.set_xlabel('Relative density proxy')
ax.set_ylabel('Greenberg speed output (nominal unit)')
ax.set_title('Without calibration, the same proxy implies different physical speeds')
ax.legend(fontsize=8)
ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig(OUT/'02_proxy_physical_calibration.png',dpi=220); plt.close(fig)

# 3 evidence ladder for intervention claims
fig,ax=plt.subplots(figsize=(10,5.4)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
steps=[
 (0.6,4.3,2.2,0.9,'Correlation /\nco-movement','association only'),
 (3.3,4.3,2.2,0.9,'Assumed multiplier\nscenario','sensitivity only'),
 (6.0,4.3,2.2,0.9,'Calibrated traffic\nsimulation','model-based counterfactual'),
 (3.3,1.8,2.2,0.9,'Observed intervention\n+ causal design','empirical effect'),
 (6.0,1.8,2.2,0.9,'Policy decision\nwith uncertainty','actionable evidence')]
for x,y,w,h,t,sub in steps:
    ax.add_patch(Rectangle((x,y),w,h,fill=False,linewidth=1.5))
    ax.text(x+w/2,y+h/2+0.08,t,ha='center',va='center',fontsize=10)
    ax.text(x+w/2,y-0.22,sub,ha='center',va='top',fontsize=8)
for a,b in [((2.8,4.75),(3.3,4.75)),((5.5,4.75),(6.0,4.75)),((4.4,4.3),(4.4,2.7)),((5.5,2.25),(6.0,2.25)),((7.1,4.3),(7.1,2.7))]:
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='->',mutation_scale=12,linewidth=1.2))
ax.text(0.6,5.55,'Do not jump from association or a hand-set multiplier directly to “the lane opening caused improvement”.',fontsize=11,weight='bold')
fig.tight_layout(); fig.savefig(OUT/'03_intervention_evidence_ladder.png',dpi=220,bbox_inches='tight'); plt.close(fig)
