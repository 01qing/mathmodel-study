"""Bounded reconstructions from converted paper text, not an author-program run.
Physical PDF page numbers refer to Markdown page markers. No PDF is opened.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def weights(p, w, r):
    widths = [min(w * 2**i, 1024) for i in range(r + 1)]
    b00 = 1 / sum(p**i * (width + 1) / 2 for i, width in enumerate(widths))
    return widths, [b00 * p**i for i in range(r + 1)]


def attempt(p, w, r):
    return sum(weights(p, w, r)[1])


def root(f):
    lo, hi = 0., 1.
    assert f(lo) * f(hi) <= 0
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def q3_original_s(rate, w, r):
    # Appendix pp47-49, capped Wi, k rounded upward as explicitly coded.
    d = 13.6 + 12240 / rate
    k = math.ceil(d / 9)
    def ph(p):
        widths, bs = weights(p, w, r)
        return sum(b * (width-k-1)*(width-k)/(2*width)
                   for width, b in zip(widths, bs) if width-1 >= k)
    p = root(lambda p: .1 + .9*(1-ph(p)) - p)
    tau = attempt(p, w, r)
    ptr = 1-(1-tau)**2
    # Appendix p42 includes (1-tau), unlike body Eq6-25.
    ps = 2*tau*(1-tau)*.9*ph(p)/ptr
    s = ptr*ps*12000/((1-ptr)*9+ptr*ps*(d+91)+ptr*(1-ps)*(d+108))
    assert abs(.1+.9*(1-ph(p))-p) < 1e-12
    return dict(p=p, tau=tau, ph=ph(p), original_s_mbps=s)


def main():
    registry = json.loads((ROOT/'learning_output/cases/2023-A-transfer/PAPER_MARKDOWN_REGISTRY.json').read_text(encoding='utf-8'))
    paper = next(p for p in registry['papers'] if p['paper_id']=='A23102480015')
    identities = {}
    for prefix in ('markdown', 'raw_layout'):
        path = ROOT/paper[prefix+'_repo_path']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == paper[prefix+'_sha256']
        identities[prefix] = dict(path=paper[prefix+'_repo_path'], sha256=digest)

    # Audit printed paired columns, allowing rounding in both five-decimal fields.
    printed = {
      'q3_model_p29':([.14442,.13430,.14368,.19007,.18413,.18961],
                      [44.41043,36.67841,44.51861,30.45981,26.04794,34.67287]),
      'q3_simulation_p30':([.15794,.13057,.15769,.20025,.17053,.22264],
                           [45.29719,37.44748,45.30293,31.71960,27.01195,35.26618]),
      'q4_model_p34':([.35196,.28294,.35197,.51349,.44696,.51351],
                      [96.03677,77.04132,96.03752,77.16336,64.17043,78.16417]),
      'q4_simulation_p34':([.33549,.27023,.33478,.49221,.40941,.49268],
                           [96.21853,77.50196,96.01490,77.96606,64.85054,78.51571])}
    rates = [286.8]*3+[158.4]*3
    rows=[]
    for table,(norms,mbps) in printed.items():
        for i,(u,s,rate) in enumerate(zip(norms,mbps,rates),1):
            gap = s-u*rate
            rows.append(dict(table=table,parameter=i,normalized=u,rate=rate,
                             printed_mbps=s,product_mbps=u*rate,gap_mbps=gap,
                             rounding_consistent=abs(gap)<=rate*.000005+.000005))
    assert sum(not row['rounding_consistent'] for row in rows if '_model_' in row['table']) == 12
    # These failures characterize the printed artifact, not a guessed correction.
    recon=[]
    for i,(rate,w,r) in enumerate(zip(rates,[16,32,16]*2,[6,5,32]*2),1):
        result=q3_original_s(rate,w,r)
        result.update(parameter=i, rate=rate, cwmin=w,retries=r,
                      printed_mbps=printed['q3_model_p29'][1][i-1])
        result['difference_mbps']=result['original_s_mbps']-result['printed_mbps']
        recon.append(result)

    # 1 us timing rounds duration upward, but reward must remain exact bytes.
    quantization=[]
    for rate,payload in itertools.product([455.8,275.3,286.8,158.4],range(100,1501,100)):
        d=13.6+8*(30+payload)/rate
        d_grid=math.ceil(d)
        credited_bits=d_grid*(payload*8/rate)/d*rate
        assert credited_bits >= payload*8-1e-9
        quantization.append(dict(rate=rate,payload_bytes=payload,exact_duration_us=d,
                                 rounded_duration_us=d_grid,credited_bits=credited_bits,
                                 reward_error_percent=100*(credited_bits/(payload*8)-1)))

    # pp56-57: randint(0,CW-1)+1, followed by exactly this BACKOFF ordering.
    backoff=[]
    for draw in range(16):
        counter=draw+1; elapsed=0
        while counter>0:
            elapsed+=9; counter-=1
        assert elapsed==(draw+1)*9
        backoff.append(dict(draw=draw,appendix_backoff_us=elapsed,required_backoff_us=draw*9))
    # p58: reset CW, then an unconditional doubling in the same failure branch.
    retry=[]
    for limit in (5,6,32):
        cw=16; tries=0
        for _ in range(limit):
            tries+=1
            if tries==limit: cw=16; tries=0
            cw=min(cw*2,1024)
        assert cw==32 and tries==0
        retry.append(dict(max_retry=limit,after_reset_cw=cw,expected_new_packet_cw=16))

    # p79: outer nodes are forced to ACK for every multi-transmitter set;
    # center stays UNKNOWN then succeeds because p78 sets drop_rate=0.
    collision_sets=[]
    for count in (1,2,3):
        for subset in itertools.combinations((1,2,3),count):
            expected={i:not(2 in subset and any(j!=2 for j in subset)) for i in subset}
            appendix={i:True for i in subset}
            collision_sets.append(dict(transmitters=subset,body_low_sir_success=expected,
                                       appendix_local_branch_success=appendix,
                                       matches=appendix==expected))
    assert sum(not x['matches'] for x in collision_sets)==3
    # A controlled branch input: two equal-duration simultaneous successes.
    d=13.6+12240/275.3
    duplicate_reward=dict(start_times_us=[100,100],end_times_us=[100+d,100+d],
                          appendix_p69_bits=(d*(12000/275.3)/d+0)*275.3,
                          packet_reward_bits=24000)
    assert abs(duplicate_reward['appendix_p69_bits']-12000)<1e-8
    output=dict(scope='local scalar and branch reconstructions; no full author-program execution',
                source_identities=identities,printed_column_audit=rows,
                q3_original_s_reconstruction=recon,quantized_reward=quantization,
                backoff_cases=backoff,retry_reset_cases=retry,
                q4_collision_sets=collision_sets,simultaneous_success_reward=duplicate_reward)
    (HERE/'CHECKS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(q3_reconstruction=recon,
        inconsistent_printed_rows=[(x['table'],x['parameter']) for x in rows if not x['rounding_consistent']],
        max_quantized_reward_error=max(quantization,key=lambda x:x['reward_error_percent']),
        branch_checks='PASS: 16 backoff, 3 retry, 7 transmitter subsets, 1 double reward'),ensure_ascii=False))


if __name__=='__main__':
    main()
