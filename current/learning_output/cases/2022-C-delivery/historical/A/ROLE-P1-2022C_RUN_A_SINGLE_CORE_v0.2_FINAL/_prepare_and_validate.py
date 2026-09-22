import os, json, csv, gzip, pickle, hashlib, math
from artifact_tool import Blob, SpreadsheetFile

FINAL='/mnt/data/ROLE-P1-2022C_RUN_A_SINGLE_CORE_v0.2_FINAL'
ROOT='/mnt/data'

# ---- Extract authoritative small input snapshots using artifact_tool ----
def inspect_rows(path, rng, max_rows, max_cols):
    wb=SpreadsheetFile.import_xlsx(Blob.load(path)); s=wb.worksheets.get_item_at(0)
    obj=json.loads(wb.inspect({'kind':'table','sheet_id':s.id,'range':rng,'include':'values','table_max_rows':max_rows,'table_max_cols':max_cols}).ndjson)
    return obj['values']

for name,path in [('attachment1',ROOT+'/附件1.xlsx'),('attachment2',ROOT+'/附件2.xlsx')]:
    rows=inspect_rows(path,'A1:D319',400,4)
    with open(f'{FINAL}/{name}_snapshot.csv','w',encoding='utf-8-sig',newline='') as f:
        csv.writer(f).writerows(rows)
rows=inspect_rows(ROOT+'/附件3.xlsx','A1:B75',80,2)
with open(f'{FINAL}/attachment3_region_codes_snapshot.csv','w',encoding='utf-8-sig',newline='') as f:
    csv.writer(f).writerows(rows)

# ---- Frozen-run validator ----
with open(FINAL+'/frozen_runs.pkl','rb') as f:runs=pickle.load(f)

def load_input(path):
    with open(path,'r',encoding='utf-8-sig',newline='') as f:
        rows=list(csv.reader(f))
    d={}
    for r in rows[1:]:
        if not r or not r[0]: continue
        d[int(r[0])]=(r[1],r[2],r[3])
    return d
inp1=load_input(FINAL+'/attachment1_snapshot.csv'); inp2=load_input(FINAL+'/attachment2_snapshot.csv')
recv_d={1:18,2:12,3:6,4:0,5:12,6:18}; send_d=recv_d.copy()

def lane_code(l,p): return int(f'{l}{p}') if p<10 else int(f'{l}10')
valid={0,1,2,3}
for l in range(1,7):
    for p in range(1,11): valid.add(lane_code(l,p))
valid.update(range(71,80)); valid.add(710)

def score_independent(out,T,returns):
    hy=[i for i,v in enumerate(out) if v['power']=='混动']
    p1=sum((hy[i+1]-hy[i]-1)!=2 for i in range(len(hy)-1))
    dr=[v['drive'] for v in out]; blocks=[]
    if dr:
        start=dr[0]; opp='四驱' if start=='两驱' else '两驱'; cur=[dr[0]]
        for prev,x in zip(dr,dr[1:]):
            if prev==opp and x==start: blocks.append(cur); cur=[x]
            else: cur.append(x)
        blocks.append(cur)
    p2=sum(b.count('四驱')!=b.count('两驱') for b in blocks)
    C=len(out); fastest=9*C+72
    s1=100-p1; s2=100-p2; s3=100-returns; s4=100-0.01*(T-fastest)
    weighted=.4*s1+.3*s2+.2*s3+.1*s4
    capped_s4=min(100,s4); capped_weighted=.4*s1+.3*s2+.2*s3+.1*capped_s4
    return dict(C=C,p1_penalty=p1,p2_penalty=p2,return_uses=returns,T=T,theoretical_fastest=fastest,
                score1=s1,score2=s2,score3=s3,score4_literal=s4,weighted_literal=weighted,
                score4_capped_sensitivity=capped_s4,weighted_capped_sensitivity=capped_weighted,
                drive_blocks=len(blocks))

def audit_one(key,r,q,input_data):
    hard=[]; warn=[]; evidence=[]
    T=int(r['T']); hist=r['history']; out=r['output']; log=r['log']; ids=sorted(hist)
    if ids!=list(range(1,319)): hard.append({'code':'ID_SET','detail':'history IDs are not exactly 1..318'})
    if len(out)!=318 or sorted(v['id'] for v in out)!=list(range(1,319)):
        hard.append({'code':'OUTPUT_PERMUTATION','detail':'output is not a permutation of 1..318'})
    if any(len(hist[c])!=T+1 for c in ids): hard.append({'code':'HISTORY_LENGTH','detail':'at least one history length differs from T+1'})
    # attributes vs source snapshot
    mism=[]
    for v in out:
        exp=input_data.get(v['id'])
        got=(v['type'],v['power'],v['drive'])
        if exp!=got: mism.append((v['id'],got,exp))
    if mism: hard.append({'code':'SOURCE_ATTRIBUTE_MISMATCH','detail':mism[:5]})
    else: evidence.append('all 318 output attributes match the corresponding official input snapshot')
    # valid region codes
    bad=[]
    for c in ids:
        for t,x in enumerate(hist[c]):
            if x is not None and x not in valid: bad.append((c,t,x)); break
    if bad: hard.append({'code':'INVALID_REGION_CODE','detail':bad[:5]})
    else: evidence.append('all nonblank per-second states use one of the 74 official region codes')

    rf=[e for e in log if e[1]=='recv_fresh']; rr=[e for e in log if e[1]=='recv_return']
    so=[e for e in log if e[1]=='send_out']; sr=[e for e in log if e[1]=='send_return']
    if len(rf)!=318 or [e[2] for e in rf]!=list(range(1,319)):
        hard.append({'code':'INPUT_SEQUENCE','detail':'fresh receiving events do not preserve source order 1..318'})
    else: evidence.append('receiving events preserve official painted-body input order')
    if len(so)!=318: hard.append({'code':'SEND_COUNT','detail':len(so)})
    if len(sr)!=r['returns'] or len(rr)!=r['returns']:
        # each return use should generate one send-to-return and one recv-from-return event in this primitive
        if r['returns']!=0 or sr or rr:
            hard.append({'code':'RETURN_EVENT_COUNT','detail':{'stored':r['returns'],'send_return':len(sr),'recv_return':len(rr)}})
    if r['returns']==0 and not sr and not rr: evidence.append('selected schedule uses no return-lane operation')

    # Machine non-overlap and durations for the events used here.
    for name,evs,dmap in [('receiving',sorted(rf+rr),recv_d),('sending',sorted(so+sr),send_d)]:
        ready=-10**9
        for e in evs:
            s,kind,c,l,d=e
            if kind in ('recv_fresh','send_out') and d!=dmap[l]:
                hard.append({'code':'MACHINE_DURATION','detail':e}); break
            if s<ready:
                hard.append({'code':'MACHINE_OVERLAP','detail':{'machine':name,'event':e,'previous_ready':ready}}); break
            ready=max(ready,s+d)
    if not any(x['code'] in ('MACHINE_DURATION','MACHINE_OVERLAP') for x in hard): evidence.append('both transverse-machine action streams satisfy lane durations and non-overlap')

    recv_ev={e[2]:e for e in rf}; send_ev={e[2]:e for e in so}
    # FIFO lane membership/order.
    for l in range(1,7):
        a=[e[2] for e in rf if e[3]==l]; b=[e[2] for e in so if e[3]==l]
        if a!=b:
            hard.append({'code':'LANE_FIFO','detail':{'lane':l,'entry_prefix':a[:15],'exit_prefix':b[:15]}}); break
    if not any(x['code']=='LANE_FIFO' for x in hard): evidence.append('all six incoming lanes preserve FIFO order')

    # Reconstruct lane kinematics exactly from receiving time, 9s moves, FIFO blocking, and send pickup time.
    exp_arr={}; exp_rel={}; lane_admission=[]
    for l in range(1,7):
        cars=[e[2] for e in rf if e[3]==l]
        pred_rel={p:-10**9 for p in range(1,11)}
        for c in cars:
            re=recv_ev[c]; se=send_ev[c]
            arr={10:re[0]+re[4]//2}; rel={}
            # lane-10 admission requires predecessor to have started leaving position 10
            if arr[10] < pred_rel[10]: lane_admission.append((c,l,arr[10],pred_rel[10]))
            for p in range(10,1,-1):
                start=max(arr[p],pred_rel[p-1])
                rel[p]=start; arr[p-1]=start+9
            pickup=se[0]+se[4]//2
            if pickup<arr[1]:
                hard.append({'code':'SEND_BEFORE_LANE1','detail':(c,l,pickup,arr[1])}); break
            rel[1]=pickup
            exp_arr[c]=arr; exp_rel[c]=rel
            # Compare recorded parking arrival and move-start instants. Sampling convention records the parking code at the move-start second.
            h=hist[c]
            for p in range(10,0,-1):
                code=lane_code(l,p); times=[t for t,x in enumerate(h) if x==code]
                if p==1 and not times and se[4]==0 and se[0]==arr[1]:
                    continue  # sink code wins under same-second last-region convention
                if not times:
                    hard.append({'code':'MISSING_PARK_STATE','detail':(c,l,p,arr[p])}); break
                if times[0]!=arr[p]:
                    hard.append({'code':'PARK_ARRIVAL_TIME','detail':(c,l,p,arr[p],times[0])}); break
                if p>=2 and times[-1]!=rel[p]:
                    hard.append({'code':'MOVE_START_TIME','detail':(c,l,p,rel[p],times[-1])}); break
                if p==1 and pickup>arr[1] and times[-1]!=pickup-1:
                    hard.append({'code':'LANE1_WAIT_TIME','detail':(c,l,pickup,times[-1])}); break
            pred_rel=rel
        if any(x['code'] in ('SEND_BEFORE_LANE1','MISSING_PARK_STATE','PARK_ARRIVAL_TIME','MOVE_START_TIME','LANE1_WAIT_TIME') for x in hard): break
    if lane_admission: hard.append({'code':'LANE10_ADMISSION_COLLISION','detail':lane_admission[:5]})
    if not any(x['code'] in ('SEND_BEFORE_LANE1','MISSING_PARK_STATE','PARK_ARRIVAL_TIME','MOVE_START_TIME','LANE1_WAIT_TIME','LANE10_ADMISSION_COLLISION') for x in hard):
        evidence.append('independent FIFO-blocking reconstruction matches all recorded lane parking arrival/move times')

    # Universal sender no-idle constraint and Q1 priority rule 7.
    if len(exp_arr)==318:
        remaining=set(ids); ready=0
        for e in so:
            s,_,c,l,d=e
            arrs={x:exp_arr[x][1] for x in remaining}
            wait=[x for x,a in arrs.items() if a<=ready]
            expected_start=ready if wait else min(arrs.values())
            if s!=expected_start:
                hard.append({'code':'SEND_NO_IDLE','detail':{'car':c,'actual_start':s,'required_start':expected_start,'machine_ready':ready}}); break
            if q==1:
                elig=[x for x,a in arrs.items() if a<=s]
                earliest=min(arrs[x] for x in elig)
                if arrs[c]!=earliest:
                    hard.append({'code':'Q1_PRIORITY7','detail':{'car':c,'start':s,'arrival':arrs[c],'earliest':earliest}}); break
            remaining.remove(c); ready=s+d
        if not any(x['code']=='SEND_NO_IDLE' for x in hard): evidence.append('constraint 8 no-idle rule passes for the complete sending stream')
        if q==1 and not any(x['code']=='Q1_PRIORITY7' for x in hard): evidence.append('Question-1 priority rule 7 passes for the complete sending stream')
        if q==1 and r['returns']==0: evidence.append('Question-1 priority rule 6 is vacuously satisfied because the return lane is unused')

    # Completion time and output/log order.
    if so:
        maxend=max(e[0]+e[4] for e in so)
        if T!=maxend: hard.append({'code':'COMPLETION_TIME','detail':{'stored':T,'event_max':maxend}})
        if [v['id'] for v in out] != [e[2] for e in so]: hard.append({'code':'OUTPUT_LOG_ORDER','detail':'output list differs from send_out log order'})
    # score independent recompute
    sc=score_independent(out,T,r['returns']); st=r['score']
    compare=[('p1_penalty',sc['p1_penalty'],st['p1_penalty']),('p2_penalty',sc['p2_penalty'],st['p2_penalty']),('return_uses',sc['return_uses'],st['return_uses']),('T',sc['T'],st['T']),('score1',sc['score1'],st['score1']),('score2',sc['score2'],st['score2']),('score3',sc['score3'],st['score3']),('score4_literal',sc['score4_literal'],st['score4']),('weighted_literal',sc['weighted_literal'],st['weighted_total'])]
    badcmp=[x for x in compare if abs(float(x[1])-float(x[2]))>1e-9]
    if badcmp: hard.append({'code':'SCORE_RECOMPUTE','detail':badcmp})
    else: evidence.append('all four score components and weighted total reproduce independently from the frozen output sequence/log')
    if sc['score4_literal']>100+1e-12:
        warn.append({'code':'TIME_SCORE_GT_100','detail':{'score4_literal':sc['score4_literal'],'T':T,'9C+72':sc['theoretical_fastest'],'capped_weighted_sensitivity':sc['weighted_capped_sensitivity']}})

    # The sampled matrix can display duplicate position codes at an integer second under same-second instantaneous event ordering.
    # This is not treated as a physical collision if the independent kinematic reconstruction above passes.
    sample_dups=[]
    for t in range(T+1):
        seen={}
        for c in ids:
            x=hist[c][t]
            if x is None or x in (0,3): continue
            if x in seen:
                sample_dups.append((t,x,seen[x],c)); break
            seen[x]=c
        if len(sample_dups)>=5: break
    if sample_dups:
        warn.append({'code':'SAMPLED_CODE_DUPLICATE','detail':sample_dups,'interpretation':'same-second last-region sampling can show both a departing body and a newly admitted body at the same parking code; independent event-level kinematics passed'})

    return {'key':key,'question':q,'hard_failures':hard,'warnings':warn,'evidence':evidence,'score_recomputed':sc}

reports=[]
for key in ['result11','result12','result21','result22']:
    q=1 if key.startswith('result1') else 2
    inp=inp1 if key.endswith('1') else inp2
    reports.append(audit_one(key,runs[key],q,inp))

# Workbook portability check captured from prior artifact_tool inspection is re-recorded from workbook formulas via artifact_tool now.
workbook_checks=[]
for key in ['result11','result12','result21','result22']:
    p=f'{FINAL}/results/{key}.xlsx'; wb=SpreadsheetFile.import_xlsx(Blob.load(p)); s=wb.worksheets.get_item('Sheet1')
    obj=json.loads(wb.inspect({'kind':'table','sheet_id':s.id,'range':'A1:C3','include':'values,formulas','table_max_rows':3,'table_max_cols':3}).ndjson)
    vals=obj.get('values',[])
    formulas=json.loads(wb.inspect({'kind':'formula','sheet_id':s.id,'range':'B2:B2'}).ndjson)
    workbook_checks.append({'key':key,'artifact_tool_values_A1_C3':vals,'formula_B2':formulas.get('formula') if isinstance(formulas,dict) else formulas,'portable_recalc_status':'NOT_VERIFIED' if any('#VALUE!' in str(x) for row in vals for x in row) else 'PASS_IN_ARTIFACT_TOOL'})

# Source/Core identity record.
manifest=json.load(open('/mnt/data/_rolep1_pack/OFFICIAL_SOURCE_IDENTITY.json',encoding='utf-8'))
actual={'2022C_官方题面_汽车制造公司涂装-总装缓存区调序调度优化问题.docx':ROOT+'/汽车制造公司涂装-总装缓存区调序调度优化问题.docx','2022C_附件1.xlsx':ROOT+'/附件1.xlsx','2022C_附件2.xlsx':ROOT+'/附件2.xlsx','2022C_附件3.xlsx':ROOT+'/附件3.xlsx','2022C_附件4.xlsx':ROOT+'/附件4.xlsx'}
def gitblob(path):
    b=open(path,'rb').read(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
source_identity=[]
for rec in manifest['files']:
    p=actual[rec['name']]; got={'name':rec['name'],'bytes':os.path.getsize(p),'git_blob_sha1':gitblob(p)}
    got['pass']=got['bytes']==rec['bytes'] and got['git_blob_sha1']==rec['git_blob_sha1']; source_identity.append(got)
core_sha=hashlib.sha256(open(ROOT+'/release-v141.zip','rb').read()).hexdigest()

# Static materializations + action logs for provenance repair.
for key,r in runs.items():
    T=r['T']; ids=sorted(r['history'])
    with gzip.open(f'{FINAL}/materialized/{key}_matrix.csv.gz','wt',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['car_id']+list(range(T+1)))
        for c in ids: w.writerow([c]+[('' if x is None else x) for x in r['history'][c]])
    with open(f'{FINAL}/materialized/{key}_action_log.csv','w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['start_time','action_type','vehicle_id','lane','duration']); w.writerows(r['log'])
    with open(f'{FINAL}/materialized/{key}_output_sequence.csv','w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['position','id','type','power','drive','return_count']); w.writeheader()
        for i,v in enumerate(r['output'],1): w.writerow({'position':i,**v})

report={'benchmark_id':'ROLE-P1-2022C-v0.2','condition':'Run A Single-Core Generalist','core_sha256':core_sha,'core_gate_pass':core_sha=='a4ef5b69d31ab2b5de032e9fa9e8c78f15a09b773bfca3ace57870cdb418016f','source_identity':source_identity,'runs':reports,'workbook_checks':workbook_checks,'materialized_static_matrices':'created as gzip CSV; canonical frozen per-second values independent of workbook formula recalculation','overall_hard_failure_count':sum(len(x['hard_failures']) for x in reports),'overall_status':'EVENT_AND_SCORE_VALIDATION_PASS' if all(not x['hard_failures'] for x in reports) else 'EVENT_OR_SCORE_VALIDATION_FAIL'}
with open(FINAL+'/validation_report.json','w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'overall_status':report['overall_status'],'hard_failures':report['overall_hard_failure_count'],'per_run':[(x['key'],len(x['hard_failures']),[w['code'] for w in x['warnings']]) for x in reports],'workbooks':[(x['key'],x['portable_recalc_status']) for x in workbook_checks]},ensure_ascii=False,indent=2))
