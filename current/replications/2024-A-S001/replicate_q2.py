"""S001 Q2 partial reimplementation on original data; no thrust or RL reproduction."""
from pathlib import Path
import json,hashlib,csv,sys,platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.io import loadmat
R=Path(__file__).resolve().parent
font=FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
plt.rcParams.update({'font.family':font.get_name(),'axes.unicode_minus':False,'font.size':10,'axes.linewidth':0.7,'svg.fonttype':'none'})
raw=R/'附件2-风电机组采集数据.mat'
data=loadmat(raw,simplify_cells=True)['data_TS_WF']
rows=[]
def mape(y,p):
 assert np.all(np.abs(y)>1e-12)
 return float(np.mean(np.abs((p-y)/y))*100)
for field in ['WF_1','WF_2']:
 for i,w in enumerate(data[field]['WT'],1):
  inp=w['inputs'];out=w['outputs'];omega=w['states'][1:,1]
  # Units scaled for a well-conditioned least squares solve; identical model family to p60.
  X=np.column_stack((inp[:-1,0]/1e6,inp[1:,1]**3/1000,np.ones(1999)))
  y=out[1:,2];actual_t=out[1:,0]
  for mode,n in [('all_fit_diagnostic',1999),('chronological_holdout',1399)]:
   coef=np.linalg.lstsq(X[:n],y[:n],rcond=None)[0];pred=X@coef
   sl=slice(None) if n==1999 else slice(n,None)
   baseline=inp[:-1,0]
   rows.append(dict(field=field,turbine=i,mode=mode,power_mape=mape(y[sl],pred[sl]),torque_mape=mape(actual_t[sl],(pred/omega)[sl]),baseline_power_mape=mape(y[sl],baseline[sl]),samples=len(y[sl])))
with (R/'metrics.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
def style(ax):
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',color='#e8a0a0',linestyle=':',linewidth=.5);ax.set_axisbelow(True);ax.set_xlim(0,101);ax.set_xticks([1,11,21,31,41,51,61,71,81,91,100]);ax.set_xlabel('风机编号')
def save(fig,name):
 fig.savefig(R/(name+'.png'),dpi=200);fig.savefig(R/(name+'.svg'));plt.close(fig)
for metric,title,name in [('power_mape','输出功率平均绝对百分比误差（%）','01_power'),('torque_mape','主轴扭矩平均绝对百分比误差（%）','02_torque')]:
 fig,axes=plt.subplots(2,1,figsize=(7,6.6),layout='constrained')
 for ax,field in zip(axes,['WF_1','WF_2']):
  rs=[x for x in rows if x['field']==field and x['mode']=='all_fit_diagnostic'];v=[x[metric] for x in rs]
  ax.vlines(range(1,101),0,v,color='#3979d5',linewidth=.7);style(ax);ax.set_ylim(0,max(v)*1.13);ax.set_ylabel(title);ax.set_title(f'{field}：全样本拟合诊断（非独立测试）',fontsize=11)
 fig.suptitle('原始数据再实现 · 参考S001上下分图构图',fontsize=12);save(fig,name)
fig,axes=plt.subplots(2,1,figsize=(7,6.6),layout='constrained')
for ax,field in zip(axes,['WF_1','WF_2']):
 rs=[x for x in rows if x['field']==field and x['mode']=='chronological_holdout']
 ax.plot(range(1,101),[x['baseline_power_mape'] for x in rs],color='#999999',linewidth=.9,label='上一拍功率指令基线')
 ax.plot(range(1,101),[x['power_mape'] for x in rs],color='#3979d5',linewidth=.9,label='上一拍指令＋风速三次项＋截距')
 style(ax);ax.set_ylim(bottom=0);ax.set_ylabel('功率预测MAPE（%）');ax.set_title(f'{field}：前1399对训练，后600对测试',fontsize=11);ax.legend(frameon=False,fontsize=9)
fig.suptitle('新增验证 · 按时间留出，逐机组比较',fontsize=12);save(fig,'03_holdout')
summary={}
for mode in ['all_fit_diagnostic','chronological_holdout']:
 summary[mode]={f:{k:float(np.mean([x[k] for x in rows if x['mode']==mode and x['field']==f])) for k in ['power_mape','torque_mape','baseline_power_mape']} for f in ['WF_1','WF_2']}
report={'status':'PARTIAL_REIMPLEMENTATION_RUN','input_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'source_paper':'S001 pp20,60–61; plotting reference pp22,24','scope':'Reimplements linear-in-parameters output-power model and appendix torque=Pout/omega. Uses all1999 pairs for fit diagnostic, then1399/600 chronological evaluation. Paper figure uses100 times; figures are not exact numerical reproduction. No efficiency fitted or inserted. Thrust branch, rainflow, RL, robust optimization NOT_RUN.','summary':summary,'outputs':['01_power.png','02_torque.png','03_holdout.png','metrics.csv'],'runtime':{'python':sys.version,'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
(R/'run_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
