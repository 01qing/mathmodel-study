#!/usr/bin/env python3
from search_cases import search
r=search('2025 A NPU Davinci DAG EarlyFree 贪心 缓存分配 spill GP NSGA-II MOPSO Pareto 传输硬约束',mode='evaluation',top=20)
h=[x for x in r['matches'] if x['case_group']=='2025-A']; ids=[x['paper_id'] for x in h]
assert 'S028' in ids,ids
s=next(x for x in h if x['paper_id']=='S028')
assert s['reading_status'].startswith('CORE_REVIEWED'),s['reading_status']
cs=s.get('mathmodel_core_summary') or {}
assert cs.get('reproduction_level')=='R2',cs
assert 'Q1' in cs.get('baseline_summary',{}) and 'Q3' in cs.get('baseline_summary',{}),cs
assert any('33792' in w for w in cs.get('decision_warning',[])),cs
assert any('lexicographic' in w.lower() for w in cs.get('decision_warning',[])),cs
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S025','S026','S027','S028'],m
assert m.get('status')=='FINAL_TRAIN_GROUP_COMPLETE',m
assert m.get('mini_transfer_status')=='PASS_AFTER_RULE_REVISION',m
print('v1.28 2025-A S028 MathModel-Core retrieval regression PASS')
