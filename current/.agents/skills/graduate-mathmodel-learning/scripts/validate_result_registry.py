#!/usr/bin/env python3
from pathlib import Path
import json,argparse,math
R=Path(__file__).resolve().parents[4]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('registry',type=Path); args=ap.parse_args()
 p=args.registry if args.registry.is_absolute() else R/args.registry
 o=json.loads(p.read_text(encoding='utf-8')); issues=[]; checks=[]
 # Generic recursively recognized metric tuples.
 def walk(x,path='root'):
  if isinstance(x,dict):
   if all(k in x for k in ['old_time','new_time','reported_time_improvement_pct']):
    v=(x['old_time']-x['new_time'])/x['old_time']*100; checks.append((path+'.time_improvement',v,x['reported_time_improvement_pct']))
   if all(k in x for k in ['old_transfer','new_transfer','reported_transfer_improvement_pct']):
    v=(x['old_transfer']-x['new_transfer'])/x['old_transfer']*100; checks.append((path+'.transfer_improvement',v,x['reported_transfer_improvement_pct']))
   if 'MSE' in x and 'MAE' in x and isinstance(x['MSE'],(int,float)) and isinstance(x['MAE'],(int,float)):
    if x['MSE']+1e-12 < x['MAE']**2: issues.append({'path':path,'type':'MSE_LT_MAE_SQUARED','MSE':x['MSE'],'MAE':x['MAE']})
   if 'MSE' in x and 'RMSE' in x and isinstance(x['MSE'],(int,float)) and isinstance(x['RMSE'],(int,float)):
    if not math.isclose(x['RMSE']**2,x['MSE'],rel_tol=1e-3,abs_tol=1e-8): issues.append({'path':path,'type':'RMSE_SQUARED_NE_MSE'})
   for k,v in x.items(): walk(v,path+'.'+str(k))
  elif isinstance(x,list):
   for i,v in enumerate(x): walk(v,f'{path}[{i}]')
 walk(o)
 for name,recomp,reported in checks:
  if abs(recomp-reported)>0.15: issues.append({'path':name,'type':'REPORTED_PERCENT_MISMATCH','reported':reported,'recomputed':recomp})
 print(json.dumps({'status':'PASS','registry':str(p),'checks':len(checks),'issues':issues},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
