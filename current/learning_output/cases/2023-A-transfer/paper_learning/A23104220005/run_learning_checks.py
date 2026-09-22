"""Bounded Python probes and continuous-window diagnostics; not MATLAB reproduction.
Run with Python 3 from any cwd. Frozen v1 simulator is imported without modification.
"""
from pathlib import Path
import sys, json, random, statistics, hashlib

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
sys.path.insert(0, str(CASE / 'code'))
from wlan import simulate, scenario
from analytic import bianchi, q2_exact


def deadline_probe(q, seed, tolerant, seconds=10):
    """Isolate deadline equality in author's Q1/Q2 scheduling pattern.
    Deliberate differences: common fixed horizon, Python RNG, joint set captured
    before mutation. This is NOT a literal port of the full appendix.
    """
    rng = random.Random(seed)
    rate = 455.8 if q == 1 else 275.3
    d = 13.6 + 12240 / rate
    deadlines = [int(16*rng.random())*9. for _ in range(2)]
    stage = [0, 0]; retries = [0, 0]; successes = 0
    near = 0; first_near = None; collisions = 0; joint = 0
    limit = seconds * 1e6
    while min(deadlines) <= limit:
        t = min(deadlines)
        gap = abs(deadlines[0]-deadlines[1])
        if 0 < gap < 1e-7:
            near += 1
            if first_near is None: first_near = dict(time_us=t, gap_us=gap)
        senders = [i for i in range(2) if abs(deadlines[i]-t) < 1e-7] if tolerant else [i for i in range(2) if deadlines[i] == t]
        failed = q == 1 and len(senders) == 2
        busy = d + (65 if failed else 48) + 43
        if t + d + (65 if failed else 48) > limit: break
        if failed: collisions += 1
        else: successes += len(senders)
        if len(senders) == 2: joint += 1
        for i in range(2):
            if i in senders:
                if failed:
                    if retries[i] < 32:
                        retries[i] += 1; stage[i] = min(stage[i]+1, 6)
                    else: retries[i] = 0; stage[i] = 0
                else: retries[i] = 0; stage[i] = 0
                deadlines[i] += busy + int((16*2**stage[i])*rng.random())*9
            else:
                deadlines[i] += busy
    return dict(q=q, seed=seed, tolerant=tolerant, total_mbps=successes*12000/limit,
                collisions=collisions, joint_events=joint, near_equal_events=near,
                first_near_equal=first_near)


def window_diagnostics(q, seed, seconds=10):
    warmup = 500000.
    result = simulate(**scenario(q), seed=seed, duration=seconds*1e6, warmup=warmup, trace=True)
    bins = [[0]*len(result['mbps']) for _ in range(seconds)]
    completions = 0; noise = 0; failures = 0
    for packet in result.pop('trace'):
        release = packet['release']
        if release is None or release < warmup or release > warmup+seconds*1e6: continue
        k = min(seconds-1, int((release-warmup)//1e6))
        completions += 1; noise += int(packet['noise_bad']); failures += int(not packet['success'])
        if packet['success']: bins[k][packet['node']] += 1
    assert [sum(row[i] for row in bins) for i in range(len(result['mbps']))] == result['successes']
    assert completions == sum(result['attempts'])
    assert failures == sum(result['failures'])
    mbps = [[v*.012 for v in row] for row in bins]
    totals = [sum(row) for row in mbps]
    fairness = [sum(row)**2/(len(row)*sum(v*v for v in row)) if any(row) else 0 for row in mbps]
    return dict(q=q, seed=seed, whole_run=result, windows_per_node_mbps=mbps,
                total_window_min=min(totals), total_window_max=max(totals),
                total_window_sd=statistics.stdev(totals), minimum_window_jain=min(fairness),
                completed_attempt_failure_fraction=failures/completions,
                noise_marked_completed_attempts=noise, conservation_checks='PASS')


def main():
    seeds = [101, 202, 303, 404, 505]
    probes = [deadline_probe(q,s,t) for q in [1,2] for s in seeds for t in [False,True]]
    windows = []
    for q in range(1,5):
        for seed in seeds:
            windows.append(window_diagnostics(q,seed))
        print(f'Q{q} continuous diagnostics complete', flush=True)
    # Direct substitution in the published Q4 expression (53), not its solver.
    tau1 = tau2 = .1
    ps = 3*tau1*(1-tau1)*(1-tau2)/(1-(1-tau1)**2)
    # Local branch probe: converted pp47/49 increment total by two, leave node
    # counters and stage untouched. This exposes the branch, not reachability.
    stage = [2,0,3]; per_ap = [0,0,0]; total = 0
    total += 2
    branch = dict(total_success_increment=total, per_ap_success_increment=per_ap,
                  stages_after_success_branch=stage, expected_stage_reset=[0,0,0],
                  scope='local branch arithmetic, not complete MATLAB execution')
    sources = {str(p.relative_to(CASE)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [CASE/'code/wlan.py', CASE/'code/analytic.py', Path(__file__)]}
    out = dict(scope='our Python probes and frozen-model diagnostics; no MATLAB or PDF parsing',
               seeds=seeds, seconds_per_run=10, sources=sources,
               analytical=dict(q1=bianchi(),q2=q2_exact()), deadline_probes=probes,
               q4_probability_probe=dict(tau1=tau1,tau2=tau2,Ps=ps,
                   interpretation='expression not a probability on entire unit square; attainable solver domain not proved'),
               q4_local_branch_probe=branch, continuous_windows=windows)
    (HERE/'LEARNING_CHECKS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({f'Q{q}':{str(t):statistics.mean(r['total_mbps'] for r in probes if r['q']==q and r['tolerant']==t) for t in [False,True]} for q in [1,2]},indent=2))


if __name__ == '__main__': main()
