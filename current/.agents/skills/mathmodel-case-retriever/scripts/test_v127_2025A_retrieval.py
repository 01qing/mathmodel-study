#!/usr/bin/env python3
from search_cases import search
r=search('2025 A NPU 核内调度 MCBGS 多约束平衡贪心 MOACADSA first fit spill DOSA 传输容差 10 15 多序列协同',mode='evaluation',top=20)
h=[x for x in r['matches'] if x['case_group']=='2025-A']; ids=[x['paper_id'] for x in h]
assert 'S027' in ids,ids
s=next(x for x in h if x['paper_id']=='S027')
assert s['reading_status'].startswith('CORE_REVIEWED'),s['reading_status']
cs=s.get('mathmodel_core_summary') or {}
assert cs.get('reproduction_level')=='R2',cs
assert 'Q1' in cs.get('baseline_summary',{}) and 'Q3' in cs.get('baseline_summary',{}),cs
assert any('89.2' in w or 'aggregate' in w.lower() for w in cs.get('decision_warning',[])),cs
assert any('10%' in w or '15%' in w for w in cs.get('decision_warning',[])),cs
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S025','S026','S027','S028'],m
print('v1.27 2025-A S027 MathModel-Core retrieval regression PASS')
