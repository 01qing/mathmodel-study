#!/usr/bin/env python3
from search_cases import search
r=search('2025 A NPU 核内调度 ABQPSO 量子粒子群 DPEA 双种群 Pareto 禁忌搜索 缓存 SPILL',mode='evaluation',top=20)
h=[x for x in r['matches'] if x['case_group']=='2025-A']; ids=[x['paper_id'] for x in h]
assert 'S026' in ids,ids
s=next(x for x in h if x['paper_id']=='S026')
assert s['reading_status'].startswith('CORE_REVIEWED'),s['reading_status']
cs=s.get('mathmodel_core_summary') or {}
assert cs.get('reproduction_level')=='R2',cs
assert 'Q2' in cs.get('baseline_summary',{}),cs
assert any('Mbest' in w or 'quantum' in w.lower() for w in cs.get('decision_warning',[])),cs
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S025','S026','S027','S028'],m
print('v1.26 2025-A S026 MathModel-Core retrieval regression PASS')
