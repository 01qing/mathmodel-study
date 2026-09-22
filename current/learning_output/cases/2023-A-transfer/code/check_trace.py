"""Read-only independent reconstruction of collisions, retry stages and frozen counters."""
import math

def check_trace(result,params):
    log=result['trace'];n=params.get('n',2);eps=1e-6;errors=[];count=0
    hear=params.get('hear',[[i!=j for j in range(n)] for i in range(n)])
    interfere=params.get('interfere',hear)
    w=params.get('cwmin',16);cap=params.get('cwmax',1024);retry=params.get('retries',32)
    def ck(label,ok,detail):
        nonlocal count
        count+=1
        if not ok:errors.append(dict(check=label,detail=detail))
    prev=[None]*n;successes=[0]*n
    for k,p in enumerate(log):
        i=p['node'];old=prev[i]
        expected_stage=0 if old is None or old['success'] or old['stage']==retry else old['stage']+1
        ck('stage',p['stage']==expected_stage,k)
        ck('contention_window',p['cw']==min(cap,w*2**p['stage']),k)
        ck('uniform_draw_support',0<=p['backoff']<p['cw'],k)
        origin=0 if old is None else old['release']
        # Merge carrier-busy intervals, then count only complete slots after each DIFS.
        def carrier_end(b):return b['end'] if params.get('sense_mode')=='data_only' else b['release'] or float('inf')
        intervals=sorted((max(origin,b['start']),min(p['start'],carrier_end(b))) for b in log
                         if b['node']!=i and hear[i][b['node']] and b['start']<p['start']-eps and carrier_end(b)>origin+eps)
        union=[]
        for a,b in intervals:
            if union and a<=union[-1][1]+eps:union[-1][1]=max(b,union[-1][1])
            else:union.append([a,b])
        cursor=origin;slots=0
        for a,b in union:
            slots+=max(0,math.floor((a-cursor-43)/9+1e-7));cursor=max(cursor,b)
        slots+=max(0,math.floor((p['start']-cursor-43)/9+1e-7))
        ck('frozen_backoff',slots==p['backoff'],[k,slots,p['backoff']])
        ck('difs',p['start']>=cursor+43-eps,k)
        if p['success'] is not None:
            collision=any(b['node']!=i and interfere[i][b['node']] and max(p['start'],b['start'])<min(p['end'],b['end'])-eps for b in log)
            ck('collision_outcome',p['success']==(not collision and not p['noise_bad']),k)
            ck('ack_timeout',abs(p['release']-p['end']-(48 if p['success'] else 65))<eps,k)
            if result['warmup_us']<=p['release']<=result['warmup_us']+result['duration_us'] and p['success']:successes[i]+=1
        prev[i]=p
    ck('payload_accounting',successes==result['successes'],[successes,result['successes']])
    return dict(status='PASS' if not errors else 'FAIL',checks=count,errors=errors[:20],error_count=len(errors),packets=len(log))
