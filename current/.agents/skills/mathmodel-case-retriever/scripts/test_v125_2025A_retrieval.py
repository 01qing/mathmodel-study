#!/usr/bin/env python3
from search_cases import search
r=search('NPU DAG 核内调度 缓存驻留 peak Vstay SPILL 多级缓存 执行时间 搬运量 1.05 硬约束',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2025-A']
ids=[x['paper_id'] for x in hits]
assert 'S025' in ids,ids
s=next(x for x in hits if x['paper_id']=='S025')
assert s['reading_status'].startswith('CORE_REVIEWED'),s
cs=s.get('mathmodel_core_summary') or {}
assert cs.get('reproduction_level')=='R2',cs
assert 'Q1' in cs.get('baseline_summary',{}),cs
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S025','S026','S027','S028'],m
print('v1.25 2025-A S025 MathModel-Core retrieval regression PASS')
